#!/usr/bin/env python3
"""Download mobile app reviews from Apple + Google stores and build a consolidated sample."""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import random
import time
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator

import requests
from google_play_scraper import Sort, reviews as gp_reviews

APPS = {
    'instagram': {
        'app_store_id': 389801252,
        'play_store_id': 'com.instagram.android',
    },
    'tiktok': {
        'app_store_id': 835599320,
        'play_store_id': 'com.zhiliaoapp.musically',
    },
    'youtube': {
        'app_store_id': 544007664,
        'play_store_id': 'com.google.android.youtube',
    },
    'facebook': {
        'app_store_id': 284882215,
        'play_store_id': 'com.facebook.katana',
    },
}

APPLE_BASE_URL = (
    'https://itunes.apple.com/{country}/rss/customerreviews/'
    'page={page}/sortBy={sort}/id={app_id}/json'
)
APPLE_SORTS = ('mostRecent', 'mostHelpful')
APPLE_PAGE_LIMIT = 10


@dataclass
class ReviewRecord:
    """Normalized review payload for either store."""

    store: str
    app: str
    review_id: str
    timestamp: dt.datetime
    rating: int | None
    version: str | None
    author: str | None
    title: str | None
    content: str | None
    votes: int | None

    def as_row(self) -> list[str]:
        return [
            self.store,
            self.app,
            self.review_id,
            self.timestamp.isoformat(),
            '' if self.rating is None else str(self.rating),
            self.version or '',
            self.author or '',
            self.title or '',
            (self.content or '').replace('\r', ' ').replace('\n', ' ').strip(),
            '' if self.votes is None else str(self.votes),
        ]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path('outputs/research/mobile_app_reviews_12mo.csv'))
    parser.add_argument('--country', default='us', help='App Store country storefront')
    parser.add_argument('--sample-size', type=int, default=500, help='Target sample per app/store')
    parser.add_argument(
        '--cutoff-date',
        default='2024-11-13',
        help='Earliest UTC date (YYYY-MM-DD) to include reviews from',
    )
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--sleep', type=float, default=0.4, help='Delay between paginated requests')
    return parser.parse_args()


def _iter_app_store_pages(app_id: int, country: str, sleep: float) -> Iterator[tuple[str, dict]]:
    for sort in APPLE_SORTS:
        for page in range(1, APPLE_PAGE_LIMIT + 1):
            url = APPLE_BASE_URL.format(country=country, page=page, sort=sort, app_id=app_id)
            resp = requests.get(url, timeout=30)
            if resp.status_code == 400:
                break
            resp.raise_for_status()
            payload = resp.json()
            entries = payload.get('feed', {}).get('entry', [])
            if len(entries) <= 1:
                break
            yield sort, payload
            time.sleep(sleep)


def fetch_app_store_reviews(app: str, app_id: int, country: str, cutoff: dt.datetime, sleep: float) -> list[ReviewRecord]:
    seen: dict[str, ReviewRecord] = {}
    for sort, payload in _iter_app_store_pages(app_id, country, sleep):
        entries = payload.get('feed', {}).get('entry', [])
        for entry in entries[1:]:
            review_id = entry.get('id', {}).get('label')
            if not review_id:
                continue
            updated_raw = entry.get('updated', {}).get('label')
            if not updated_raw:
                continue
            updated = dt.datetime.fromisoformat(updated_raw.replace('Z', '+00:00'))
            if updated < cutoff:
                continue
            rating_str = entry.get('im:rating', {}).get('label')
            votes_str = entry.get('im:voteCount', {}).get('label')
            seen[review_id] = ReviewRecord(
                store='app_store',
                app=app,
                review_id=review_id,
                timestamp=updated,
                rating=int(rating_str) if rating_str else None,
                version=entry.get('im:version', {}).get('label'),
                author=entry.get('author', {}).get('name', {}).get('label'),
                title=entry.get('title', {}).get('label'),
                content=entry.get('content', {}).get('label'),
                votes=int(votes_str) if votes_str else None,
            )
    return sorted(seen.values(), key=lambda r: r.timestamp, reverse=True)


def fetch_play_store_reviews(app: str, package: str, cutoff: dt.datetime, sleep: float) -> list[ReviewRecord]:
    collected: list[ReviewRecord] = []
    token = None
    while True:
        batch, token = gp_reviews(
            package,
            lang='en',
            country='us',
            sort=Sort.NEWEST,
            count=200,
            continuation_token=token,
        )
        if not batch:
            break
        stop = False
        for item in batch:
            stamped = item.get('at')
            if stamped is None:
                continue
            if stamped.tzinfo is None:
                stamped = stamped.replace(tzinfo=dt.timezone.utc)
            stamped = stamped.astimezone(dt.timezone.utc)
            if stamped < cutoff:
                stop = True
                break
            collected.append(
                ReviewRecord(
                    store='play_store',
                    app=app,
                    review_id=item.get('reviewId', ''),
                    timestamp=stamped,
                    rating=item.get('score'),
                    version=item.get('appVersion'),
                    author=item.get('userName'),
                    title=item.get('title'),
                    content=item.get('content'),
                    votes=item.get('thumbsUpCount'),
                )
            )
        if stop or token is None:
            break
        time.sleep(sleep)
    return collected


def stratified_sample(reviews: list[ReviewRecord], sample_size: int, seed: int) -> list[ReviewRecord]:
    if len(reviews) <= sample_size:
        return reviews
    buckets: dict[tuple[int, int], list[ReviewRecord]] = defaultdict(list)
    for review in reviews:
        buckets[(review.timestamp.year, review.timestamp.month)].append(review)
    random.seed(seed)
    for bucket in buckets.values():
        random.shuffle(bucket)
    months = sorted(buckets.keys())
    base_quota = max(1, sample_size // max(1, len(months)))
    sampled: list[ReviewRecord] = []
    for key in months:
        bucket = buckets[key]
        take = min(base_quota, len(bucket))
        sampled.extend(bucket[:take])
        buckets[key] = bucket[take:]
    remaining = sample_size - len(sampled)
    if remaining > 0:
        leftovers = [review for bucket in buckets.values() for review in bucket]
        random.shuffle(leftovers)
        sampled.extend(leftovers[:remaining])
    return sampled[:sample_size]


def write_consolidated(reviews: list[ReviewRecord], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('w', newline='', encoding='utf-8') as handle:
        writer = csv.writer(handle)
        writer.writerow(['store', 'app', 'review_id', 'timestamp', 'rating', 'version', 'author', 'title', 'content', 'votes'])
        for record in reviews:
            writer.writerow(record.as_row())


def main() -> None:
    args = parse_args()
    cutoff = dt.datetime.fromisoformat(args.cutoff_date).replace(tzinfo=dt.timezone.utc)
    all_samples: list[ReviewRecord] = []
    for app, ids in APPS.items():
        app_store_reviews = fetch_app_store_reviews(app, ids['app_store_id'], args.country, cutoff, args.sleep)
        sample_app_store = stratified_sample(app_store_reviews, args.sample_size, args.seed)
        all_samples.extend(sample_app_store)

        play_store_reviews = fetch_play_store_reviews(app, ids['play_store_id'], cutoff, args.sleep)
        sample_play_store = stratified_sample(play_store_reviews, args.sample_size, args.seed)
        all_samples.extend(sample_play_store)

        print(
            f"{app}: apple={len(app_store_reviews)} -> sample {len(sample_app_store)} | "
            f"google={len(play_store_reviews)} -> sample {len(sample_play_store)}"
        )

    write_consolidated(all_samples, args.output)
    print(f"Wrote consolidated sample -> {args.output}")


if __name__ == '__main__':
    main()
