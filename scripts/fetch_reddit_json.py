"""Pull Reddit posts + top comments from public JSON endpoints."""
from __future__ import annotations

import argparse
import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

import requests
import yaml

LISTING_URL = "https://www.reddit.com/r/{name}/{sort}.json"
COMMENT_URL = "https://www.reddit.com{permalink}.json"
DEFAULT_USER_AGENT = "AccentLightingResearchBot/0.1"


@dataclass
class SubredditConfig:
    name: str
    sort: str
    limit: int
    comment_limit: int


@dataclass
class Config:
    user_agent: str
    subreddits: List[SubredditConfig]


def load_config(path: Path) -> Config:
    raw = yaml.safe_load(path.read_text())
    subreddits: List[SubredditConfig] = []
    for entry in raw.get("subreddits", []):
        subreddits.append(
            SubredditConfig(
                name=entry["name"],
                sort=entry.get("sort", "hot"),
                limit=int(entry.get("limit", 25)),
                comment_limit=int(entry.get("comments", 10)),
            )
        )
    if not subreddits:
        raise ValueError("No subreddits defined in config")
    user_agent = raw.get("user_agent", DEFAULT_USER_AGENT)
    return Config(user_agent=user_agent, subreddits=subreddits)


def reddit_get(url: str, headers: Dict[str, str], params: Dict[str, int] | None = None) -> dict:
    response = requests.get(url, headers=headers, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def fetch_comments(permalink: str, comment_limit: int, headers: Dict[str, str]) -> List[dict]:
    payload = reddit_get(COMMENT_URL.format(permalink=permalink.rstrip("/")), headers, params={"limit": comment_limit})
    if len(payload) < 2:
        return []
    comments_block = payload[1]
    children = comments_block.get("data", {}).get("children", [])
    comments: List[dict] = []
    for child in children:
        if child.get("kind") != "t1":
            continue
        data = child.get("data", {})
        comments.append(
            {
                "comment_id": data.get("id"),
                "author": data.get("author"),
                "body": data.get("body"),
                "score": data.get("score"),
                "created_utc": data.get("created_utc"),
                "is_submitter": data.get("is_submitter"),
                "permalink": f"https://www.reddit.com{data.get('permalink', '')}",
            }
        )
        if len(comments) >= comment_limit:
            break
    return comments


def fetch_subreddit(cfg: SubredditConfig, headers: Dict[str, str]) -> List[dict]:
    listing = reddit_get(
        LISTING_URL.format(name=cfg.name, sort=cfg.sort),
        headers,
        params={"limit": cfg.limit},
    )
    posts = listing.get("data", {}).get("children", [])
    records: List[dict] = []
    for post in posts:
        if post.get("kind") != "t3":
            continue
        data = post.get("data", {})
        comments = fetch_comments(data.get("permalink", ""), cfg.comment_limit, headers)
        records.append(
            {
                "platform": "reddit",
                "subreddit": cfg.name,
                "sort": cfg.sort,
                "post_id": data.get("id"),
                "title": data.get("title"),
                "author": data.get("author"),
                "score": data.get("score"),
                "num_comments": data.get("num_comments"),
                "created_utc": data.get("created_utc"),
                "url": data.get("url"),
                "permalink": f"https://www.reddit.com{data.get('permalink', '')}",
                "selftext": data.get("selftext"),
                "comments": comments,
            }
        )
        time.sleep(1)
    return records


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
        default=Path("clients/3m/projects/251106-3m-accent-lighting/configs/social/reddit_sources.yaml"),
        help="Path to the reddit_sources.yaml config",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("/Volumes/DATA/Consulting/251106-3M-accent-lighting/raw/social/reddit/reddit_sample.jsonl"),
        help="Where to store the JSONL output",
    )
    args = parser.parse_args()

    config = load_config(args.config)
    headers = {"User-Agent": config.user_agent}

    all_records: List[dict] = []
    for subreddit in config.subreddits:
        all_records.extend(fetch_subreddit(subreddit, headers))
        time.sleep(2)

    if not all_records:
        raise SystemExit("No Reddit data collected")

    write_records(args.output, all_records)
    print(f"Wrote {len(all_records)} Reddit posts to {args.output}")


if __name__ == "__main__":
    main()
