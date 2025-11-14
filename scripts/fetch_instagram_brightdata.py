"""Trigger Bright Data Instagram dataset pulls for the configured post URLs."""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List

import requests
import yaml

BRIGHT_ENDPOINT = "https://api.brightdata.com/datasets/v3/scrape"
DEFAULT_BATCH_SIZE = 5
POLL_DELAY_SECONDS = 5


@dataclass
class Config:
    dataset_id: str
    batch_size: int
    urls: List[str]


def load_config(path: Path) -> Config:
    raw = yaml.safe_load(path.read_text())
    dataset_id = raw.get("dataset_id")
    if not dataset_id:
        raise ValueError("dataset_id is required in the config file")
    batch_size = int(raw.get("batch_size") or DEFAULT_BATCH_SIZE)
    urls: List[str] = []
    for group in raw.get("post_groups", []):
        urls.extend(group.get("urls", []))
    if not urls:
        raise ValueError("No Instagram URLs provided in config")
    return Config(dataset_id=dataset_id, batch_size=batch_size, urls=urls)


def chunked(values: List[str], size: int) -> Iterable[List[str]]:
    for i in range(0, len(values), size):
        yield values[i : i + size]


def scrape_batch(dataset_id: str, urls: List[str], token: str, timeout: int = 120) -> List[dict]:
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    payload = {"input": [{"url": url} for url in urls]}
    params = {
        "dataset_id": dataset_id,
        "notify": "false",
        "include_errors": "true",
    }
    response = requests.post(
        BRIGHT_ENDPOINT,
        headers=headers,
        params=params,
        json=payload,
        timeout=timeout,
    )
    response.raise_for_status()
    records: List[dict] = []
    for line in response.iter_lines():
        if not line:
            continue
        record = json.loads(line.decode("utf-8"))
        records.append(record)
    return records


def write_records(path: Path, records: List[dict]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            json.dump(record, handle)
            handle.write("\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("clients/3m/projects/251106-3m-accent-lighting/configs/social/instagram_posts.yaml"),
        help="Path to the instagram_posts.yaml file",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("/Volumes/DATA/Consulting/251106-3M-accent-lighting/raw/social/instagram/brightdata_instagram_batch1.jsonl"),
        help="Where to write the combined JSONL output",
    )
    parser.add_argument(
        "--max-batches",
        type=int,
        default=None,
        help="Optional: limit the number of batches processed",
    )
    parser.add_argument(
        "--sleep",
        type=int,
        default=POLL_DELAY_SECONDS,
        help="Delay between batch calls (seconds)",
    )
    args = parser.parse_args()

    token = os.getenv("BRIGHT_TOKEN")
    if not token:
        raise SystemExit("BRIGHT_TOKEN env var is required")

    config = load_config(args.config)
    output_path = args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)

    all_records: List[dict] = []
    for batch_index, urls in enumerate(chunked(config.urls, config.batch_size), start=1):
        if args.max_batches and batch_index > args.max_batches:
            break
        try:
            batch_records = scrape_batch(config.dataset_id, urls, token)
        except requests.RequestException as exc:  # type: ignore[name-defined]
            raise SystemExit(f"Bright Data request failed for batch {batch_index}: {exc}") from exc
        all_records.extend(batch_records)
        time.sleep(max(args.sleep, 0))

    if not all_records:
        raise SystemExit("Bright Data did not return any Instagram records")

    write_records(output_path, all_records)
    print(f"Wrote {len(all_records)} Instagram comments to {output_path}")


if __name__ == "__main__":
    main()
