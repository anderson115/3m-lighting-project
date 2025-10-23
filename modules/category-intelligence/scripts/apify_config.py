"""Utility for configuring Apify tasks programmatically (no runs)."""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

import requests


APIFY_ENV_PATH = Path("/Volumes/DATA/config/offbrain/category-intelligence/apify.env")
API_BASE = "https://api.apify.com/v2"


@dataclass
class TaskConfig:
    name: str
    actor_id: str
    input_payload: Dict[str, object]
    options: Optional[Dict[str, object]] = None


DEFAULT_TASKS: List[TaskConfig] = [
    TaskConfig(
        name="garage-hooks-walmart",
        actor_id="apify/walmart-product-search",
        input_payload={
            "query": "garage hooks",
            "maxItems": 400,
            "country": "US",
        },
    ),
    TaskConfig(
        name="garage-hooks-amazon",
        actor_id="apify/amazon-crawler",
        input_payload={
            "search": "garage hook",
            "resultsPerPage": 40,
            "maxResults": 200,
            "domain": "com",
        },
    ),
    TaskConfig(
        name="garage-hooks-home-depot",
        actor_id="epctex/home-depot-scraper",
        input_payload={
            "search": "garage hooks",
            "maxItems": 200,
            "includeReviews": False,
        },
    ),
    TaskConfig(
        name="garage-hooks-lowes",
        actor_id="maxcopell/lowes-product-search",
        input_payload={
            "search": "garage hook",
            "maxItems": 200,
        },
    ),
]


def load_credentials(env_path: Path = APIFY_ENV_PATH) -> Dict[str, str]:
    if not env_path.exists():
        raise FileNotFoundError(f"Apify credentials missing: {env_path}")
    credentials: Dict[str, str] = {}
    for line in env_path.read_text().splitlines():
        if not line or line.strip().startswith("#"):
            continue
        key, _, value = line.partition("=")
        credentials[key.strip()] = value.strip()
    required = {"APIFY_API_TOKEN", "APIFY_USER_ID"}
    if not required.issubset(credentials):
        missing = required - credentials.keys()
        raise RuntimeError(f"Apify credentials incomplete. Missing: {missing}")
    return credentials


def list_tasks(token: str) -> Dict[str, dict]:
    params = {"token": token, "my": "1", "limit": 1000}
    resp = requests.get(f"{API_BASE}/actor-tasks", params=params, timeout=30)
    resp.raise_for_status()
    items = resp.json().get("data", {}).get("items", [])
    return {item["name"]: item for item in items}


def upsert_task(token: str, existing: Optional[dict], task: TaskConfig, dry_run: bool) -> None:
    payload = {
        "name": task.name,
        "actorId": task.actor_id,
        "input": task.input_payload,
    }
    if task.options:
        payload["options"] = task.options

    if existing:
        task_id = existing["id"]
        if dry_run:
            print(f"[dry-run] Would update task {task.name} ({task_id})")
            return
        resp = requests.put(
            f"{API_BASE}/actor-tasks/{task_id}",
            params={"token": token},
            json=payload,
            timeout=30,
        )
        resp.raise_for_status()
        print(f"Updated task {task.name}")
    else:
        if dry_run:
            print(f"[dry-run] Would create task {task.name}")
            return
        resp = requests.post(
            f"{API_BASE}/actor-tasks",
            params={"token": token},
            json=payload,
            timeout=30,
        )
        resp.raise_for_status()
        print(f"Created task {task.name}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Configure Apify tasks (no execution)")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Persist changes instead of dry-run",
    )
    args = parser.parse_args()

    creds = load_credentials()
    token = creds["APIFY_API_TOKEN"]

    existing = list_tasks(token)
    for task in DEFAULT_TASKS:
        upsert_task(token, existing.get(task.name), task, dry_run=not args.apply)

    if not args.apply:
        print("Dry run finished. Re-run with --apply to create/update tasks.")


if __name__ == "__main__":
    main()
