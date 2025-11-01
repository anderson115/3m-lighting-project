#!/usr/bin/env python3
"""
Analyze Claude Code chat logs for real-time cost tracking

Usage:
    python3 modules/cost-tracking/scripts/analyze_costs.py
    python3 modules/cost-tracking/scripts/analyze_costs.py --csv costs.csv
    python3 modules/cost-tracking/scripts/analyze_costs.py --module category-intelligence
"""

import json
import yaml
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import sys


CLAUDE_LOGS = Path.home() / ".claude" / "projects" / "-Users-anderson115-00-interlink-12-work-3m-lighting-project"
CONFIG_PATH = Path(__file__).parent.parent / "config" / "pricing.yaml"


def load_pricing():
    """Load API pricing config"""
    with open(CONFIG_PATH) as f:
        return yaml.safe_load(f)


def parse_conversation(jsonl_path):
    """Parse single conversation file"""
    messages = []
    summary = None

    with open(jsonl_path) as f:
        for line in f:
            if not line.strip():
                continue
            try:
                data = json.loads(line)
                if data.get('type') == 'summary':
                    summary = data.get('summary')
                if 'timestamp' in data and 'message' in data:
                    messages.append(data)
            except:
                continue

    if not messages:
        return None

    # Extract data
    start = datetime.fromisoformat(messages[0]['timestamp'].replace('Z', '+00:00'))
    end = datetime.fromisoformat(messages[-1]['timestamp'].replace('Z', '+00:00'))
    duration = (end - start).total_seconds() / 60

    tokens_in = 0
    tokens_out = 0
    files = set()

    for msg in messages:
        usage = msg.get('message', {}).get('usage', {})
        tokens_in += usage.get('input_tokens', 0)
        tokens_out += usage.get('output_tokens', 0)

        # Extract files touched
        content = msg.get('message', {}).get('content', [])
        if isinstance(content, list):
            for item in content:
                if isinstance(item, dict) and item.get('type') == 'tool_use':
                    fp = item.get('input', {}).get('file_path')
                    if fp:
                        files.add(fp)

    return {
        'id': jsonl_path.stem,
        'summary': summary or 'Untitled',
        'start': start,
        'end': end,
        'duration_min': duration,
        'tokens_in': tokens_in,
        'tokens_out': tokens_out,
        'files': list(files)
    }


def attribute_to_module(files):
    """Determine which module based on files touched"""
    modules = set()
    for f in files:
        if 'modules/' in f:
            parts = f.split('modules/')[1].split('/')
            if parts:
                modules.add(parts[0])
    return list(modules) if modules else ['general']


def calculate_cost(conv, pricing):
    """Calculate API cost for conversation"""
    rate = pricing['api_pricing']['anthropic']['claude_sonnet']
    input_cost = (conv['tokens_in'] / 1_000_000) * rate['input_cost_per_1M_tokens']
    output_cost = (conv['tokens_out'] / 1_000_000) * rate['output_cost_per_1M_tokens']
    return input_cost + output_cost


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--csv', help='Export to CSV')
    parser.add_argument('--module', help='Filter by module')
    args = parser.parse_args()

    # Load pricing
    pricing = load_pricing()

    # Parse all conversations
    print(f"Reading logs from: {CLAUDE_LOGS}")
    convs = []
    for jsonl in CLAUDE_LOGS.glob("*.jsonl"):
        conv = parse_conversation(jsonl)
        if conv:
            convs.append(conv)

    print(f"Found {len(convs)} conversations\n")

    # Group by module
    by_module = defaultdict(list)
    for conv in convs:
        modules = attribute_to_module(conv['files'])
        for mod in modules:
            by_module[mod].append(conv)

    # Filter if requested
    if args.module:
        by_module = {args.module: by_module.get(args.module, [])}

    # Calculate costs
    print("=" * 80)
    print("CLAUDE CODE COST ANALYSIS")
    print("=" * 80)

    total_cost = 0
    total_hours = 0
    total_sessions = 0

    for module in sorted(by_module.keys()):
        module_convs = by_module[module]
        module_cost = sum(calculate_cost(c, pricing) for c in module_convs)
        module_hours = sum(c['duration_min'] for c in module_convs) / 60
        module_sessions = len(module_convs)

        print(f"\n{module}:")
        print(f"  Sessions:     {module_sessions}")
        print(f"  Duration:     {module_hours:.1f} hours")
        print(f"  API Cost:     ${module_cost:.2f}")

        total_cost += module_cost
        total_hours += module_hours
        total_sessions += module_sessions

    print("\n" + "=" * 80)
    print("TOTAL:")
    print(f"  Sessions:     {total_sessions}")
    print(f"  Duration:     {total_hours:.1f} hours")
    print(f"  API Cost:     ${total_cost:.2f}")
    print("=" * 80)

    # CSV export
    if args.csv:
        import csv
        with open(args.csv, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['date', 'module', 'summary', 'duration_min', 'tokens_in', 'tokens_out', 'cost'])

            for module, module_convs in by_module.items():
                for conv in module_convs:
                    cost = calculate_cost(conv, pricing)
                    writer.writerow([
                        conv['start'].date(),
                        module,
                        conv['summary'][:50],
                        round(conv['duration_min'], 1),
                        conv['tokens_in'],
                        conv['tokens_out'],
                        round(cost, 4)
                    ])

        print(f"\nExported to: {args.csv}")


if __name__ == '__main__':
    main()
