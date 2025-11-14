"""Collect X/Twitter search results via snscrape."""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import List

import yaml
import urllib3

try:
    import snscrape.modules.twitter as sntwitter
except ImportError as exc:  # pragma: no cover - dependency guard
    raise SystemExit("snscrape is required. Install with `pip install snscrape`." ) from exc


@dataclass
class QueryConfig:
    label: str
    search: str
    max_results: int


@dataclass
class Config:
    queries: List[QueryConfig]


def load_config(path: Path) -> Config:
    raw = yaml.safe_load(path.read_text())
    queries: List[QueryConfig] = []
    for entry in raw.get("queries", []):
        queries.append(
            QueryConfig(
                label=entry["label"],
                search=entry["search"],
                max_results=int(entry.get("max_results", 50)),
            )
        )
    if not queries:
        raise ValueError("No X queries defined")
    return Config(queries=queries)


def scrape_query(cfg: QueryConfig, insecure: bool = False) -> List[dict]:
    scraper = sntwitter.TwitterSearchScraper(cfg.search)
    if insecure:
        scraper._session.verify = False  # type: ignore[attr-defined]
    results: List[dict] = []
    for item in scraper.get_items():
        results.append(
            {
                "platform": "x",
                "label": cfg.label,
                "search": cfg.search,
                "tweet_id": item.id,
                "date": item.date.isoformat(),
                "content": item.rawContent,
                "username": item.user.username,
                "displayname": item.user.displayname,
                "like_count": item.likeCount,
                "reply_count": item.replyCount,
                "retweet_count": item.retweetCount,
                "quote_count": getattr(item, "quoteCount", None),
                "url": item.url,
                "lang": item.lang,
            }
        )
        if len(results) >= cfg.max_results:
            break
    return results


def write_records(path: Path, records: List[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            json.dump(record, handle)
            handle.write("\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("clients/3m/projects/251106-3m-accent-lighting/configs/social/x_queries.yaml"),
        help="Path to the x_queries.yaml config",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("/Volumes/DATA/Consulting/251106-3M-accent-lighting/raw/social/x/x_snscrape_sample.jsonl"),
        help="Where to store the JSONL output",
    )
    parser.add_argument(
        "--insecure",
        action="store_true",
        help="Skip SSL verification (only if a proxy intercepts certificates)",
    )
    args = parser.parse_args()

    config = load_config(args.config)
    if args.insecure:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    all_records: List[dict] = []
    for query in config.queries:
        all_records.extend(scrape_query(query, insecure=args.insecure))

    if not all_records:
        raise SystemExit("snscrape returned zero X posts")

    write_records(args.output, all_records)
    print(f"Wrote {len(all_records)} X posts to {args.output}")


if __name__ == "__main__":
    main()
