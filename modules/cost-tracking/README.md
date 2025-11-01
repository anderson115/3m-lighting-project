# Cost Tracking - REAL DATA from Chat Logs

## What This Does

Analyzes your Claude Code conversation logs to extract:
- **Session time** - when you worked and for how long
- **Token usage** - actual API costs
- **Module attribution** - which project based on files touched
- **CSV export** - ready for database

## Usage

```bash
# View all costs
python3 modules/cost-tracking/scripts/analyze_costs.py

# Export to CSV
python3 modules/cost-tracking/scripts/analyze_costs.py --csv costs.csv

# Filter by module
python3 modules/cost-tracking/scripts/analyze_costs.py --module category-intelligence
```

## Example Output

```
CLAUDE CODE COST ANALYSIS
==================================================

category-intelligence:
  Sessions:     10
  Duration:     189.3 hours
  API Cost:     $19.88

social-video-collection:
  Sessions:     3
  Duration:     47.5 hours
  API Cost:     $5.06

TOTAL:
  Sessions:     60
  Duration:     627.1 hours
  API Cost:     $59.40
```

## CSV Format

```csv
date,module,summary,duration_min,tokens_in,tokens_out,cost
2025-10-24,category-intelligence,Report Generation,4584.7,267186,442139,7.4336
```

## How It Works

1. **Reads** `~/.claude/projects/.../` JSONL files
2. **Extracts** timestamps, tokens, files touched
3. **Attributes** to modules based on file paths
4. **Calculates** API costs using pricing.yaml rates

## No Manual Tracking Required

All data comes from your actual Claude Code sessions.
