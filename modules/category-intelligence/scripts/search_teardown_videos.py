#!/usr/bin/env python3
"""
Comprehensive YouTube Search for Product Teardown/Review Videos
Uses multiple search strategies per product for exhaustive coverage
"""
import json
import subprocess
from pathlib import Path
from urllib.parse import quote_plus
import time

def search_youtube_videos(query, max_results=10):
    """Search YouTube using yt-dlp."""
    search_url = f"ytsearch{max_results}:{query}"

    try:
        result = subprocess.run([
            'yt-dlp',
            '--dump-json',
            '--no-warnings',
            '--no-playlist',
            '--skip-download',
            search_url
        ], capture_output=True, text=True, timeout=30)

        videos = []
        for line in result.stdout.strip().split('\n'):
            if line:
                try:
                    video_data = json.loads(line)
                    videos.append({
                        'video_id': video_data.get('id'),
                        'title': video_data.get('title'),
                        'duration': video_data.get('duration'),
                        'view_count': video_data.get('view_count', 0),
                        'upload_date': video_data.get('upload_date'),
                        'url': f"https://www.youtube.com/watch?v={video_data.get('id')}"
                    })
                except json.JSONDecodeError:
                    continue

        return videos
    except Exception as e:
        print(f"  Error searching '{query}': {e}")
        return []


def generate_search_queries(product):
    """Generate comprehensive search queries for a product."""
    brand = product['brand']
    title = product['title'][:60]  # Truncate long titles
    asin = product['asin']

    # Extract product type from title
    title_lower = title.lower()
    if 'magnetic' in title_lower and 'hook' in title_lower:
        product_type = "magnetic hooks"
    elif 'adhesive' in title_lower and 'hook' in title_lower:
        product_type = "adhesive hooks"
    elif 'broom' in title_lower or 'mop' in title_lower:
        product_type = "broom mop holder"
    elif 'bike' in title_lower:
        product_type = "bike mount"
    elif 'cord' in title_lower or 'cable' in title_lower:
        product_type = "cord organizer"
    elif 'pegboard' in title_lower:
        product_type = "pegboard system"
    elif 'hose' in title_lower:
        product_type = "hose holder"
    else:
        product_type = "garage hooks"

    queries = [
        # Direct product searches
        f"{brand} {product_type} review",
        f"{brand} {product_type} unboxing",
        f"{brand} {product_type} test",
        f"{brand} {product_type} installation",
        f"{brand} {product_type} how to install",

        # ASIN-based (some reviewers use this)
        f"{asin} review",
        f"{asin} unboxing",

        # Generic product type (to find comparison videos)
        f"{product_type} review comparison",
        f"best {product_type} 2024",
        f"{product_type} installation guide",

        # Failure/problem videos (critical for teardown insights)
        f"{brand} {product_type} problems",
        f"{brand} {product_type} not working",
        f"{product_type} fail"
    ]

    return queries


def main():
    # Load top 20 products
    products_path = Path("outputs/top20_bestsellers_for_teardown.json")
    products = json.loads(products_path.read_text())

    all_results = {}

    print("="*70)
    print("COMPREHENSIVE YOUTUBE TEARDOWN VIDEO SEARCH")
    print("="*70)
    print(f"Products: {len(products)}")
    print(f"Search queries per product: ~12")
    print(f"Estimated total searches: {len(products) * 12}")
    print("="*70)
    print()

    for i, product in enumerate(products, 1):
        print(f"\n[{i}/{len(products)}] {product['brand']} - {product['title'][:50]}...")
        print(f"    ASIN: {product['asin']} | BSR: {product['bsr']:,}")

        queries = generate_search_queries(product)
        product_videos = {}
        video_ids_seen = set()

        for query_idx, query in enumerate(queries, 1):
            print(f"    Query {query_idx}/{len(queries)}: \"{query}\"", end="")

            videos = search_youtube_videos(query, max_results=5)

            new_videos = 0
            for video in videos:
                if video['video_id'] not in video_ids_seen:
                    video_ids_seen.add(video['video_id'])
                    product_videos[video['video_id']] = video
                    new_videos += 1

            print(f" → {new_videos} new videos")
            time.sleep(0.5)  # Rate limiting

        print(f"    TOTAL UNIQUE VIDEOS FOUND: {len(product_videos)}")

        all_results[product['asin']] = {
            'product': product,
            'videos': list(product_videos.values()),
            'total_videos': len(product_videos)
        }

    # Save results
    output_path = Path("outputs/teardown_videos_search_results.json")
    with open(output_path, 'w') as f:
        json.dump(all_results, f, indent=2)

    # Summary
    print(f"\n\n{'='*70}")
    print("SEARCH COMPLETE")
    print(f"{'='*70}")

    total_videos = sum(r['total_videos'] for r in all_results.values())
    print(f"\nTotal videos found: {total_videos}")
    print(f"Average per product: {total_videos / len(products):.1f}")

    print(f"\nProducts with most video coverage:")
    sorted_products = sorted(all_results.items(),
                            key=lambda x: x[1]['total_videos'],
                            reverse=True)

    for asin, data in sorted_products[:10]:
        print(f"  • {data['product']['brand']} ({asin}): {data['total_videos']} videos")

    print(f"\n{'='*70}")
    print(f"Results saved to: {output_path}")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()
