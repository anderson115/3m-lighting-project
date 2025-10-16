#!/usr/bin/env python3
"""
Simple script to extract and count all unique source URLs from collector code.
"""

import re

# Manual extraction from grep results
urls = set()

# Resource Curator URLs
urls.update([
    "https://www.homedepot.com/c/ai/garage-storage-buying-guide/9ba683603be9fa5395fab901dcc1afc5",
    "https://www.lowes.com/n/ideas-inspiration/garage-storage-organization-ideas",
    "https://www.homedepot.com",
    "https://www.lowes.com",
    "https://www.familyhandyman.com/list/brilliant-ways-to-organize-your-garage/",
    "https://www.hgtv.com/lifestyle/clean-and-organize/15-garage-storage-and-organization-ideas-pictures",
    "https://www.hgtv.com",
    "https://www.pods.com/blog/diy-garage-organization-ideas",
    "https://www.familyhandyman.com",
    "https://www.pods.com",
    "https://www.extraspace.com/blog/home-organization/organize-garage-tips-decluttering-storage/",
    "https://www.extraspace.com",
    "https://www.thisoldhouse.com/garages/21018117/read-this-before-you-organize-your-garage",
    "https://www.thisoldhouse.com",
])

# Pricing Analyzer URLs
urls.update([
    "https://www.fixr.com/costs/garage-organizer-system",
    "https://www.angi.com/articles/how-much-do-garage-storage-systems-cost.htm",
    "https://www.homeadvisor.com/cost/garages/organize-a-garage/",
    "https://www.amazon.com/s?k=garage+storage",
])

# Brand Discovery URLs
urls.update([
    "https://www.thedrive.com/guides-and-gear/best-garage-storage-systems",
    "https://www.essentialhomeandgarden.com/garage-storage-systems/",
])

# Market Researcher URLs
urls.update([
    "https://www.globenewswire.com/news-release/2024/07/30/2921076/0/en/U-S-Garage-Organization-Product-Market-Report-2024",
    "https://www.transparencymarketresearch.com/north-america-garage-storage-market.html",
    "https://www.grandviewresearch.com/horizon/outlook/garage-organization-and-storage-market/united-states",
    "https://www.marketresearchfuture.com/reports/garage-organization-storage-market-26398",
])

print(f"\n{'='*60}")
print(f"SOURCE URL COUNT")
print(f"{'='*60}\n")

print(f"Resource Curator: 14 URLs")
print(f"Pricing Analyzer: 4 URLs")
print(f"Brand Discovery: 2 base URLs + Amazon scraping")
print(f"Market Researcher: 4 URLs")

print(f"\n{'='*60}")
print(f"TOTAL UNIQUE BASE URLS: {len(urls)}")
print(f"{'='*60}\n")

print("📋 All unique URLs:")
for i, url in enumerate(sorted(urls), 1):
    print(f"  {i:2d}. {url}")

print(f"\n{'='*60}")
print(f"Additional Sources from Scraping:")
print(f"{'='*60}")
print(f"- Amazon scraping: Up to 50 product URLs")
print(f"- Google Trends: pytrends data (no direct URL)")
print(f"- SEC EDGAR: Public company filings (up to 10 URLs)")
print(f"- Each brand has source_urls attached (15 brands × 2 URLs = 30)")

print(f"\n{'='*60}")
estimated_total = len(urls) + 50 + 10 + 30  # Base + Amazon + SEC + brands
print(f"ESTIMATED TOTAL WITH SCRAPING: ~{estimated_total} sources")
print(f"{'='*60}")

if estimated_total >= 100:
    print("✅ SHOULD PASS preflight validation (100+ sources)")
else:
    print(f"⚠️  Need {100 - estimated_total} more sources")
