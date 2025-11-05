#!/usr/bin/env python3
"""
Organize and consolidate all category intelligence data
Remove test files, create clean structure, generate data inventory
"""
import json
import shutil
from pathlib import Path
from collections import defaultdict

def main():
    print("=" * 70)
    print("DATA ORGANIZATION & CONSOLIDATION")
    print("=" * 70)
    print()

    # Define clean structure
    data_dir = Path("data")
    outputs_dir = Path("outputs")

    # 1. Remove test directories
    print("[1/6] Removing test directories...")
    test_dirs = [
        data_dir / "tiktok_audio_test",
        data_dir / "tiktok_transcripts_test",
        data_dir / "tiktok_videos_test",
        data_dir / "youtube_audio_test",
        data_dir / "youtube_transcripts_test"
    ]

    for test_dir in test_dirs:
        if test_dir.exists():
            shutil.rmtree(test_dir)
            print(f"  ✓ Removed {test_dir.name}")

    # 2. Organize video data by source
    print("\n[2/6] Organizing video data by source...")

    video_sources = {
        'youtube': {
            'videos': data_dir / 'youtube_videos',
            'audio': data_dir / 'youtube_audio',
            'transcripts': data_dir / 'youtube_transcripts',
            'metadata': data_dir / 'youtube_garage_consumer_insights.json'
        },
        'tiktok': {
            'videos': data_dir / 'tiktok_videos',
            'audio': data_dir / 'tiktok_audio',
            'transcripts': data_dir / 'tiktok_transcripts',
            'metadata': data_dir / 'tiktok_garage_consumer_insights.json'
        },
        'teardown': {
            'videos': data_dir / 'teardown_videos',
            'audio': data_dir / 'teardown_audio',
            'transcripts': data_dir / 'teardown_transcripts'
        }
    }

    for source, paths in video_sources.items():
        print(f"\n  {source.upper()}:")
        for data_type, path in paths.items():
            if path.exists():
                if path.is_dir():
                    count = len(list(path.iterdir()))
                    print(f"    ✓ {data_type}: {count} files")
                else:
                    size = path.stat().st_size / 1024
                    print(f"    ✓ {data_type}: {size:.1f} KB")

    # 3. Consolidate retailer data
    print("\n[3/6] Consolidating retailer product data...")

    retailer_files = {
        'amazon': data_dir / 'amazon_garage_organizers_mined.json',
        'walmart': data_dir / 'walmart_garage_organizers_mined.json',
        'homedepot': data_dir / 'homedepot_garage_organizers_mined.json',
        'target': data_dir / 'target_products.json',
        'etsy': data_dir / 'etsy_listings.json'
    }

    # Create consolidated retailer directory
    retailer_dir = data_dir / 'retailers'
    retailer_dir.mkdir(exist_ok=True)

    for retailer, source_file in retailer_files.items():
        if source_file.exists():
            dest = retailer_dir / f"{retailer}_products.json"
            if not dest.exists():
                shutil.copy(source_file, dest)
            size = source_file.stat().st_size / 1024
            print(f"  ✓ {retailer}: {size:.1f} KB")

    # 4. Consolidate analysis outputs
    print("\n[4/6] Organizing analysis outputs...")

    analysis_categories = {
        'teardown': [],
        'keyword': [],
        'bsr': [],
        'trends': [],
        'reviews': []
    }

    for output_file in outputs_dir.glob('*.json'):
        name = output_file.stem.lower()
        if 'teardown' in name:
            analysis_categories['teardown'].append(output_file.name)
        elif 'keyword' in name or 'language' in name:
            analysis_categories['keyword'].append(output_file.name)
        elif 'bsr' in name or 'bestseller' in name:
            analysis_categories['bsr'].append(output_file.name)
        elif 'trend' in name or 'emerging' in name:
            analysis_categories['trends'].append(output_file.name)
        elif 'benefit' in name or 'taxonomy' in name:
            analysis_categories['reviews'].append(output_file.name)

    for category, files in analysis_categories.items():
        if files:
            print(f"  {category.upper()}: {len(files)} files")

    # 5. Create data inventory
    print("\n[5/6] Creating data inventory...")

    inventory = {
        'last_updated': '2025-10-26',
        'data_sources': {},
        'analysis_outputs': {},
        'statistics': {}
    }

    # Count transcripts
    teardown_transcripts = list((data_dir / 'teardown_transcripts').glob('*.txt')) if (data_dir / 'teardown_transcripts').exists() else []
    youtube_transcripts = list((data_dir / 'youtube_transcripts').glob('*.txt')) if (data_dir / 'youtube_transcripts').exists() else []
    tiktok_transcripts = list((data_dir / 'tiktok_transcripts').glob('*.txt')) if (data_dir / 'tiktok_transcripts').exists() else []

    inventory['statistics'] = {
        'total_transcripts': len(teardown_transcripts) + len(youtube_transcripts) + len(tiktok_transcripts),
        'teardown_videos': len(teardown_transcripts),
        'youtube_consumer_videos': len(youtube_transcripts),
        'tiktok_consumer_videos': len(tiktok_transcripts)
    }

    # Retailer data
    inventory['data_sources']['retailers'] = {}
    for retailer, source_file in retailer_files.items():
        if source_file.exists():
            try:
                data = json.loads(source_file.read_text())
                count = len(data) if isinstance(data, list) else len(data.get('products', []))
                inventory['data_sources']['retailers'][retailer] = {
                    'products': count,
                    'file': str(source_file.relative_to(data_dir))
                }
            except:
                pass

    # Video metadata
    inventory['data_sources']['video_content'] = {
        'teardown_videos': {
            'count': len(teardown_transcripts),
            'location': 'data/teardown_transcripts/'
        },
        'youtube_consumer': {
            'count': len(youtube_transcripts),
            'location': 'data/youtube_transcripts/'
        },
        'tiktok_consumer': {
            'count': len(tiktok_transcripts),
            'location': 'data/tiktok_transcripts/'
        }
    }

    # Analysis outputs
    inventory['analysis_outputs'] = analysis_categories

    # Save inventory
    inventory_path = Path('data/DATA_INVENTORY.json')
    with open(inventory_path, 'w') as f:
        json.dump(inventory, f, indent=2)

    print(f"  ✓ Saved to {inventory_path}")

    # 6. Summary
    print("\n[6/6] Organization Summary:")
    print(f"{'=' * 70}")
    print(f"  Total transcripts: {inventory['statistics']['total_transcripts']}")
    print(f"    - Teardown videos: {inventory['statistics']['teardown_videos']}")
    print(f"    - YouTube consumer: {inventory['statistics']['youtube_consumer_videos']}")
    print(f"    - TikTok consumer: {inventory['statistics']['tiktok_consumer_videos']}")
    print()
    print(f"  Retailer data sources: {len(inventory['data_sources']['retailers'])}")
    for retailer, info in inventory['data_sources']['retailers'].items():
        print(f"    - {retailer}: {info['products']} products")
    print()
    print(f"  Analysis outputs: {sum(len(files) for files in analysis_categories.values())}")
    for category, files in analysis_categories.items():
        if files:
            print(f"    - {category}: {len(files)} files")

    print(f"\n{'=' * 70}")
    print("DATA ORGANIZATION COMPLETE")
    print(f"{'=' * 70}")
    print("\nData structure:")
    print("  data/")
    print("    ├── retailers/          # Consolidated retailer product data")
    print("    ├── youtube_*/          # YouTube consumer content")
    print("    ├── tiktok_*/           # TikTok consumer content")
    print("    ├── teardown_*/         # Product teardown videos")
    print("    └── DATA_INVENTORY.json # Complete data catalog")
    print()
    print("  outputs/")
    print("    ├── *teardown*          # Teardown analysis")
    print("    ├── *keyword*           # Keyword/language analysis")
    print("    ├── *bsr*               # Bestseller tracking")
    print("    └── *trend*             # Trend analysis")
    print(f"\n{'=' * 70}")

if __name__ == "__main__":
    main()
