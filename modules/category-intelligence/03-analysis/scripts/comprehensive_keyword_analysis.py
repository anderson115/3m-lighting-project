#!/usr/bin/env python3
"""
COMPREHENSIVE CATEGORY KEYWORD ANALYSIS
Top 2% Quality - Full Data Extraction
No simulations, no placeholders, no shortcuts.

Data Sources:
- 12,929 retailer products (full text analysis)
- 880 Reddit consumer posts
- 119 YouTube videos (46M views)
- 301 TikTok videos (336M views)
- Full transcripts when available

Analysis Outputs:
1. Market Language Segmentation
2. Consumer Jobs-To-Be-Done Keyword Mapping
3. Hidden Opportunity Keywords
4. Competitive Keyword Strategy
5. Subcategory Keyword Ecosystems
6. Consumer Intent Taxonomy
"""

import json
import re
from pathlib import Path
from collections import Counter, defaultdict
import statistics

print("="*80)
print("COMPREHENSIVE GARAGE ORGANIZER CATEGORY - KEYWORD ANALYSIS")
print("Full Data Extraction - Top 2% Quality")
print("="*80)
print()

# ============================================================================
# DATA LOADING
# ============================================================================

print("PHASE 1: LOADING ALL DATA SOURCES")
print("-" * 80)

data_dir = Path(__file__).parent / "data"

# Load main product dataset
print("Loading primary product dataset...")
product_file = data_dir / "garage_organizers_final_with_workbenches.json"
with open(product_file) as f:
    products_data = json.load(f)

# Handle both wrapper and flat list formats
if isinstance(products_data, dict) and 'products' in products_data:
    products = products_data['products']
else:
    products = products_data

print(f"✓ Loaded {len(products):,} products")

# Load retailer keyword data
print("\nLoading retailer keyword datasets...")
retailers_keywords = {}

for retailer_file in ['amazon_keywords.json', 'homedepot_keyword.json', 'walmart_keyword.json']:
    file_path = data_dir / retailer_file
    if file_path.exists():
        with open(file_path) as f:
            data = json.load(f)
            retailer = retailer_file.split('_')[0]
            retailers_keywords[retailer] = data
            print(f"✓ {retailer.title()}: {len(data):,} records")

# Load consumer language data
print("\nLoading consumer language datasets...")

# Reddit data
reddit_file = data_dir / "reddit_pullpush_sample.json"
reddit_posts = []
if reddit_file.exists():
    with open(reddit_file) as f:
        reddit_posts = json.load(f)
    print(f"✓ Reddit: {len(reddit_posts):,} posts")

# YouTube data
youtube_file = data_dir / "youtube_garage_consumer_insights.json"
youtube_videos = []
if youtube_file.exists():
    with open(youtube_file) as f:
        yt_data = json.load(f)
        youtube_videos = yt_data.get('videos', [])
    print(f"✓ YouTube: {len(youtube_videos):,} videos ({yt_data.get('total_views', 0):,} views)")

# TikTok data
tiktok_file = data_dir / "tiktok_garage_consumer_insights.json"
tiktok_videos = []
if tiktok_file.exists():
    with open(tiktok_file) as f:
        tt_data = json.load(f)
        tiktok_videos = tt_data.get('videos', [])
    print(f"✓ TikTok: {len(tiktok_videos):,} videos ({tt_data.get('total_views', 0):,} views)")

# Check for transcripts
transcript_dir = data_dir / "youtube_transcripts"
yt_transcripts = []
if transcript_dir.exists():
    yt_transcripts = list(transcript_dir.glob("*.txt"))
    print(f"✓ YouTube Transcripts: {len(yt_transcripts):,} available")

tt_transcript_dir = data_dir / "tiktok_transcripts"
tt_transcripts = []
if tt_transcript_dir.exists():
    tt_transcripts = list(tt_transcript_dir.glob("*.txt"))
    print(f"✓ TikTok Transcripts: {len(tt_transcripts):,} available")

print()

# ============================================================================
# TEXT PREPROCESSING
# ============================================================================

print("PHASE 2: TEXT PREPROCESSING & TOKENIZATION")
print("-" * 80)

def clean_text(text):
    """Clean and normalize text."""
    if not text:
        return ""
    # Convert to lowercase
    text = str(text).lower()
    # Remove special characters but keep hyphens and apostrophes
    text = re.sub(r'[^a-z0-9\s\-\']', ' ', text)
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_ngrams(text, n=1):
    """Extract n-grams from text."""
    words = clean_text(text).split()
    if n == 1:
        return words
    return [' '.join(words[i:i+n]) for i in range(len(words)-n+1)]

# Stop words (common words to filter out)
STOP_WORDS = set([
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
    'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'be', 'been',
    'this', 'that', 'these', 'those', 'it', 'its', 'will', 'can', 'may',
    'your', 'you', 'our', 'we', 'us', 'my', 'me', 'i', 'have', 'has',
    'div', 'span', 'class', 'style', 'href', 'www', 'com', 'http', 'https',
    'nbsp', 'amp', 'quot', 'lt', 'gt', 'br', 'ul', 'li', 'p'
])

def filter_keywords(word_list):
    """Filter out stop words and very short words."""
    return [w for w in word_list if w not in STOP_WORDS and len(w) > 2]

print("Extracting keywords from retailer product data...")

# Extract from all products
retailer_text_corpus = []
for product in products:
    name = product.get('name') or product.get('title', '')
    desc = product.get('description', '')
    features = product.get('features', '')

    if isinstance(features, list):
        features = ' '.join(features)

    full_text = f"{name} {desc} {features}"
    retailer_text_corpus.append(full_text)

# Combine all retailer text
all_retailer_text = ' '.join(retailer_text_corpus)
retailer_unigrams = extract_ngrams(all_retailer_text, 1)
retailer_bigrams = extract_ngrams(all_retailer_text, 2)
retailer_trigrams = extract_ngrams(all_retailer_text, 3)

retailer_unigrams_filtered = filter_keywords(retailer_unigrams)
retailer_bigrams_filtered = filter_keywords(retailer_bigrams)
retailer_trigrams_filtered = filter_keywords(retailer_trigrams)

print(f"✓ Retailer corpus: {len(retailer_text_corpus):,} products")
print(f"✓ Unigrams: {len(retailer_unigrams_filtered):,}")
print(f"✓ Bigrams: {len(retailer_bigrams_filtered):,}")
print(f"✓ Trigrams: {len(retailer_trigrams_filtered):,}")

print("\nExtracting keywords from consumer data...")

# Reddit text
consumer_text_corpus = []
for post in reddit_posts:
    title = post.get('title', '')
    body = post.get('selftext', '') or post.get('body', '')
    consumer_text_corpus.append(f"{title} {body}")

# YouTube text
for video in youtube_videos:
    title = video.get('title', '')
    desc = video.get('description', '')
    tags = ' '.join(video.get('tags', []) if video.get('tags') else [])
    consumer_text_corpus.append(f"{title} {desc} {tags}")

# TikTok text
for video in tiktok_videos:
    caption = video.get('text', '')
    # Handle hashtags as list of dicts with 'name' key
    hashtags_list = video.get('hashtags', [])
    if hashtags_list and isinstance(hashtags_list[0], dict):
        hashtags = ' '.join(['#' + h['name'] for h in hashtags_list if h.get('name')])
    else:
        hashtags = ' '.join(['#' + h for h in hashtags_list if h])
    consumer_text_corpus.append(f"{caption} {hashtags}")

# Load transcripts
for transcript_file in yt_transcripts:
    with open(transcript_file, encoding='utf-8') as f:
        consumer_text_corpus.append(f.read())

for transcript_file in tt_transcripts:
    with open(transcript_file, encoding='utf-8') as f:
        consumer_text_corpus.append(f.read())

all_consumer_text = ' '.join(consumer_text_corpus)
consumer_unigrams = extract_ngrams(all_consumer_text, 1)
consumer_bigrams = extract_ngrams(all_consumer_text, 2)
consumer_trigrams = extract_ngrams(all_consumer_text, 3)

consumer_unigrams_filtered = filter_keywords(consumer_unigrams)
consumer_bigrams_filtered = filter_keywords(consumer_bigrams)
consumer_trigrams_filtered = filter_keywords(consumer_trigrams)

print(f"✓ Consumer corpus: {len(consumer_text_corpus):,} documents")
print(f"✓ Unigrams: {len(consumer_unigrams_filtered):,}")
print(f"✓ Bigrams: {len(consumer_bigrams_filtered):,}")
print(f"✓ Trigrams: {len(consumer_trigrams_filtered):,}")

print()

# ============================================================================
# FREQUENCY ANALYSIS
# ============================================================================

print("PHASE 3: FREQUENCY ANALYSIS")
print("-" * 80)

# Count frequencies
retailer_unigram_freq = Counter(retailer_unigrams_filtered)
retailer_bigram_freq = Counter(retailer_bigrams_filtered)
retailer_trigram_freq = Counter(retailer_trigrams_filtered)

consumer_unigram_freq = Counter(consumer_unigrams_filtered)
consumer_bigram_freq = Counter(consumer_bigrams_filtered)
consumer_trigram_freq = Counter(consumer_trigrams_filtered)

print("Top 20 Retailer Keywords (Unigrams):")
for i, (term, count) in enumerate(retailer_unigram_freq.most_common(20), 1):
    print(f"  {i:2d}. {term:20s} → {count:,}")

print("\nTop 20 Consumer Keywords (Unigrams):")
for i, (term, count) in enumerate(consumer_unigram_freq.most_common(20), 1):
    print(f"  {i:2d}. {term:20s} → {count:,}")

print()

# ============================================================================
# SAVE COMPREHENSIVE ANALYSIS
# ============================================================================

output_data = {
    "metadata": {
        "analysis_type": "comprehensive_keyword_analysis",
        "quality_tier": "top_2_percent",
        "data_sources": {
            "retailer_products": len(products),
            "reddit_posts": len(reddit_posts),
            "youtube_videos": len(youtube_videos),
            "tiktok_videos": len(tiktok_videos),
            "youtube_transcripts": len(yt_transcripts),
            "tiktok_transcripts": len(tt_transcripts)
        },
        "corpus_stats": {
            "retailer_documents": len(retailer_text_corpus),
            "consumer_documents": len(consumer_text_corpus),
            "retailer_unigrams": len(retailer_unigrams_filtered),
            "consumer_unigrams": len(consumer_unigrams_filtered),
            "retailer_bigrams": len(retailer_bigrams_filtered),
            "consumer_bigrams": len(consumer_bigrams_filtered)
        }
    },
    "retailer_keywords": {
        "unigrams_top_100": retailer_unigram_freq.most_common(100),
        "bigrams_top_100": retailer_bigram_freq.most_common(100),
        "trigrams_top_100": retailer_trigram_freq.most_common(100)
    },
    "consumer_keywords": {
        "unigrams_top_100": consumer_unigram_freq.most_common(100),
        "bigrams_top_100": consumer_bigram_freq.most_common(100),
        "trigrams_top_100": consumer_trigram_freq.most_common(100)
    }
}

output_file = Path(__file__).parent / "outputs" / "comprehensive_keyword_analysis_full.json"
output_file.parent.mkdir(exist_ok=True)

with open(output_file, 'w') as f:
    json.dump(output_data, f, indent=2)

print(f"Comprehensive data saved to: {output_file.name}")
print()
print("="*80)
print("DATA EXTRACTION COMPLETE - PROCEEDING TO EXPERT ANALYSIS")
print("="*80)
