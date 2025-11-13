#!/usr/bin/env python3
"""
Update all deliverable files with corrected pain point percentages.
Uses Reddit-only base (n=1,129) instead of incorrect multi-platform base (n=2,974).
"""

import os
import re

# Corrected pain point data (Reddit n=1,129)
CORRECTED_DATA = {
    'Paint/Surface Damage': {'count': 363, 'pct': 32.2},
    'Removal Issues': {'count': 262, 'pct': 23.2},
    'Installation Difficulty': {'count': 230, 'pct': 20.4},
    'Rental/Lease': {'count': 157, 'pct': 13.9},
    'Weight Capacity': {'count': 131, 'pct': 11.6},
    'Adhesive Failure': {'count': 72, 'pct': 6.4},
    'Texture/Surface': {'count': 67, 'pct': 5.9},
}

BASE_SIZE = 1129

# Fabricated comparisons
FABRICATED = {
    'Installation Difficulty': {'fake': 64, 'inflation': 3.1},
    'Weight Capacity': {'fake': 58, 'inflation': 5.0},
    'Rental/Lease': {'fake': 31, 'inflation': 2.2},
    'Rust/Durability': {'fake': 39, 'note': 'NO EVIDENCE'},
    'Follow-on Purchases': {'fake': 73, 'note': 'NO DATA'},
}

def create_pain_point_table_markdown():
    """Create updated pain point table for markdown files."""
    table = """| Pain Point | Count | Percentage | Base |
|-----------|-------|------------|------|
"""
    for name, data in CORRECTED_DATA.items():
        table += f"| **{name}** | {data['count']} | **{data['pct']}%** | {data['count']}/{BASE_SIZE} |\n"

    return table

def create_comparison_table_markdown():
    """Create fabricated vs actual comparison table."""
    table = """| Pain Point | Fabricated | Actual | Inflation | Evidence |
|-----------|------------|--------|-----------|----------|
| Installation Difficulty | 64% | 20.4% | **3.1X** | 230/1,129 |
| Weight Capacity | 58% | 11.6% | **5.0X** | 131/1,129 |
| Rental Restrictions | 31% | 13.9% | **2.2X** | 157/1,129 |
| Rust/Durability | 39% | <1% | **NO EVIDENCE** | Not applicable |
| Follow-on Purchases | 73% | N/A | **NO DATA** | No purchase data |
"""
    return table

def create_html_table():
    """Create updated pain point table for HTML."""
    table = """            <table class="data-table">
                <thead>
                    <tr>
                        <th>Pain Point</th>
                        <th>Mentions</th>
                        <th>Percentage</th>
                        <th>Context</th>
                    </tr>
                </thead>
                <tbody>
"""

    contexts = {
        'Paint/Surface Damage': 'Dominant concern (32% of posts)',
        'Removal Issues': 'Nearly 1 in 4 posts',
        'Installation Difficulty': '1 in 5 posts mention difficulty',
        'Rental/Lease': 'Significant rental market concern',
        'Weight Capacity': 'Pre and post-purchase discussions',
        'Adhesive Failure': 'Immediate failure cases',
        'Texture/Surface': 'Textured walls incompatibility',
    }

    for name, data in CORRECTED_DATA.items():
        table += f"""                    <tr>
                        <td><strong>{name}</strong></td>
                        <td>{data['count']} / {BASE_SIZE}</td>
                        <td><strong>{data['pct']}%</strong></td>
                        <td>{contexts.get(name, 'Reddit discussions')}</td>
                    </tr>
"""

    table += """                </tbody>
            </table>"""

    return table

print("Pain Point Prevalence Update Script")
print("=" * 60)
print(f"Base Size: {BASE_SIZE} Reddit posts")
print(f"Total Pain Points: {len(CORRECTED_DATA)}")
print()
print("Corrected Percentages:")
for name, data in CORRECTED_DATA.items():
    print(f"  {name:30s}: {data['count']:3d} / {BASE_SIZE} = {data['pct']:5.1f}%")
print()
print("=" * 60)
print("Tables generated successfully")
print()
print("MARKDOWN TABLE:")
print(create_pain_point_table_markdown())
print()
print("COMPARISON TABLE:")
print(create_comparison_table_markdown())
