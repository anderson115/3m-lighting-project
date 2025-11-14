#!/usr/bin/env python3
"""
Consolidate all collected product and social data into master dataset
"""

import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = DATA_DIR / "consolidated"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def load_json(file_path):
    """Load JSON file"""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"  ⚠ Error loading {file_path.name}: {e}")
        return None

def consolidate_products():
    """Merge all product datasets"""
    print("\n📦 Consolidating Product Data...")

    all_products = []

    # Load baseline products (2,000)
    baseline_file = DATA_DIR / "retailers" / "all_products_final_with_lowes.json"
    if baseline_file.exists():
        baseline_data = load_json(baseline_file)
        if baseline_data:
            print(f"  ✓ Loaded {len(baseline_data)} baseline products")
            all_products.extend(baseline_data)

    # Load expanded coverage (812 new Amazon products)
    expanded_dir = DATA_DIR / "expanded_coverage"
    if expanded_dir.exists():
        for file in expanded_dir.glob("amazon_products_*.json"):
            data = load_json(file)
            if data:
                if isinstance(data, list):
                    print(f"  ✓ Loaded {len(data)} products from {file.name}")
                    all_products.extend(data)
                elif isinstance(data, dict) and 'products' in data:
                    print(f"  ✓ Loaded {len(data['products'])} products from {file.name}")
                    all_products.extend(data['products'])

    # Deduplicate by ASIN (Amazon) or product URL
    unique_products = {}
    for product in all_products:
        # Try ASIN first, then URL, then title as fallback
        key = product.get('asin') or product.get('url') or product.get('title')
        if key and key not in unique_products:
            unique_products[key] = product
        elif key and key in unique_products:
            # If duplicate has more data (reviews), keep it
            existing = unique_products[key]
            if product.get('reviews') and not existing.get('reviews'):
                unique_products[key] = product

    final_products = list(unique_products.values())

    print(f"\n  📊 Product Stats:")
    print(f"  Total products: {len(final_products)}")
    print(f"  Products with ratings: {sum(1 for p in final_products if p.get('rating'))}")
    print(f"  Products with reviews: {sum(1 for p in final_products if isinstance(p.get('reviews'), list) and p.get('reviews'))}")

    # Brand analysis
    brand_counts = defaultdict(int)
    brand_ratings = defaultdict(list)
    for p in final_products:
        brand = p.get('brand') or p.get('manufacturer') or 'Unknown'
        brand_counts[brand] += 1
        if p.get('rating'):
            try:
                rating = float(p['rating'])
                brand_ratings[brand].append(rating)
            except (ValueError, TypeError):
                pass

    print(f"  Unique brands: {len(brand_counts)}")

    # Top brands
    top_brands = sorted(brand_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    print(f"\n  🏆 Top 10 Brands by Product Count:")
    for i, (brand, count) in enumerate(top_brands, 1):
        avg_rating = sum(brand_ratings[brand]) / len(brand_ratings[brand]) if brand_ratings[brand] else 0
        print(f"  {i:2d}. {brand:20s} - {count:3d} products ({avg_rating:.2f}★)")

    return final_products

def consolidate_social_videos():
    """Merge all YouTube and social video data"""
    print("\n🎥 Consolidating Social Video Data...")

    all_videos = []

    # Load baseline YouTube data
    baseline_file = DATA_DIR / "youtube_garage_consumer_insights.json"
    if baseline_file.exists():
        baseline_data = load_json(baseline_file)
        if baseline_data and isinstance(baseline_data, dict):
            videos = baseline_data.get('videos', [])
            print(f"  ✓ Loaded {len(videos)} baseline YouTube videos")
            all_videos.extend(videos)

    # Load 3M Claw specific videos
    social_dir = DATA_DIR / "social_videos"
    if social_dir.exists():
        for file in social_dir.glob("youtube_*.json"):
            data = load_json(file)
            if data:
                if isinstance(data, dict) and 'videos' in data:
                    videos = data['videos']
                    print(f"  ✓ Loaded {len(videos)} videos from {file.name}")
                    all_videos.extend(videos)
                elif isinstance(data, list):
                    print(f"  ✓ Loaded {len(data)} videos from {file.name}")
                    all_videos.extend(data)

    # Deduplicate by video_id
    unique_videos = {}
    for video in all_videos:
        vid_id = video.get('video_id')
        if vid_id and vid_id not in unique_videos:
            unique_videos[vid_id] = video

    final_videos = list(unique_videos.values())

    print(f"\n  📊 Video Stats:")
    print(f"  Total unique videos: {len(final_videos)}")

    total_views = sum(v.get('views', 0) for v in final_videos if v.get('views'))
    print(f"  Total views: {total_views:,}")

    # 3M Claw specific
    claw_videos = [v for v in final_videos if '3m claw' in (v.get('title', '') + v.get('search_query', '')).lower()]
    print(f"  3M Claw videos: {len(claw_videos)}")
    claw_views = sum(v.get('views', 0) for v in claw_videos if v.get('views'))
    print(f"  3M Claw total views: {claw_views:,}")

    return final_videos

def consolidate_reddit():
    """Merge all Reddit data"""
    print("\n💬 Consolidating Reddit Data...")

    all_posts = []

    social_dir = DATA_DIR / "social_videos"
    if social_dir.exists():
        for file in social_dir.glob("reddit_*.json"):
            data = load_json(file)
            if data:
                if isinstance(data, dict) and 'posts' in data:
                    posts = data['posts']
                    print(f"  ✓ Loaded {len(posts)} posts from {file.name}")
                    all_posts.extend(posts)
                elif isinstance(data, list):
                    print(f"  ✓ Loaded {len(data)} posts from {file.name}")
                    all_posts.extend(data)

    print(f"\n  📊 Reddit Stats:")
    print(f"  Total posts: {len(all_posts)}")

    return all_posts

def main():
    print("=" * 80)
    print("DATA CONSOLIDATION - Category Intelligence")
    print("=" * 80)

    # Consolidate all data
    products = consolidate_products()
    videos = consolidate_social_videos()
    reddit_posts = consolidate_reddit()

    # Create master dataset
    master_data = {
        'consolidated_at': datetime.now().isoformat(),
        'data_sources': {
            'baseline_products': 'retailers/all_products_final_with_lowes.json',
            'expanded_amazon': 'expanded_coverage/amazon_products_*.json',
            'baseline_youtube': 'youtube_garage_consumer_insights.json',
            '3m_claw_social': 'social_videos/*'
        },
        'summary': {
            'total_products': len(products),
            'total_videos': len(videos),
            'total_reddit_posts': len(reddit_posts),
            'products_with_ratings': sum(1 for p in products if p.get('rating')),
            'products_with_reviews': sum(1 for p in products if isinstance(p.get('reviews'), list) and p.get('reviews')),
            'total_review_count': sum(len(p['reviews']) for p in products if isinstance(p.get('reviews'), list)),
            'video_total_views': sum(v.get('views', 0) for v in videos if v.get('views'))
        },
        'products': products,
        'videos': videos,
        'reddit_posts': reddit_posts
    }

    # Save consolidated dataset
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = OUTPUT_DIR / f"master_dataset_{timestamp}.json"

    with open(output_file, 'w') as f:
        json.dump(master_data, f, indent=2)

    print("\n" + "=" * 80)
    print("CONSOLIDATION COMPLETE")
    print("=" * 80)
    print(f"\n📊 Master Dataset Summary:")
    print(f"  Products: {len(products):,}")
    print(f"  - With ratings: {master_data['summary']['products_with_ratings']:,}")
    print(f"  - With reviews: {master_data['summary']['products_with_reviews']:,}")
    print(f"  - Total reviews: {master_data['summary']['total_review_count']:,}")
    print(f"\n  Videos: {len(videos):,}")
    print(f"  - Total views: {master_data['summary']['video_total_views']:,}")
    print(f"\n  Reddit posts: {len(reddit_posts)}")
    print(f"\n💾 Saved to: {output_file}")
    print(f"   File size: {output_file.stat().st_size / 1024 / 1024:.1f} MB")

    # Also save a lightweight summary
    summary_file = OUTPUT_DIR / f"data_summary_{timestamp}.json"
    summary_only = {
        'consolidated_at': master_data['consolidated_at'],
        'summary': master_data['summary'],
        'brand_breakdown': {},
        'top_rated_products': sorted(
            [p for p in products if p.get('rating')],
            key=lambda x: (float(x.get('rating', 0) or 0), int(x.get('reviewCount', 0) or 0)),
            reverse=True
        )[:20]
    }

    # Brand breakdown
    brand_counts = defaultdict(int)
    brand_ratings = defaultdict(list)
    for p in products:
        brand = p.get('brand') or p.get('manufacturer') or 'Unknown'
        brand_counts[brand] += 1
        if p.get('rating'):
            try:
                rating = float(p['rating'])
                brand_ratings[brand].append(rating)
            except (ValueError, TypeError):
                pass

    summary_only['brand_breakdown'] = {
        brand: {
            'product_count': count,
            'avg_rating': sum(brand_ratings[brand]) / len(brand_ratings[brand]) if brand_ratings[brand] else None,
            'rating_count': len(brand_ratings[brand])
        }
        for brand, count in sorted(brand_counts.items(), key=lambda x: x[1], reverse=True)
    }

    with open(summary_file, 'w') as f:
        json.dump(summary_only, f, indent=2)

    print(f"\n💾 Summary saved to: {summary_file}")

    return master_data

if __name__ == "__main__":
    main()
