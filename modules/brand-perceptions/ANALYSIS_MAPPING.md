# Analysis Mapping & Requirements
**Project:** Brand Perceptions - 3M Garage Organizers
**Client:** 3M
**Date:** 2025-11-02

---

## Dataset Overview

**Total Records:** 2,878
- **Product Reviews:** 1,049 (Amazon)
- **Social Media:** 1,829 (Reddit + YouTube)

**Quality Metrics:**
- 97.3% verified purchases
- 100% field completeness
- 72.9% Command brand focus

---

## Analysis Categories & Deliverables

### 1. SENTIMENT ANALYSIS

**Objective:** Understand overall brand sentiment and perception across platforms

**Input Data:**
```python
# Product Reviews (1,049 records)
{
  "review_text": "Full review content...",
  "rating": "5.0 out of 5 stars",
  "verified_purchase": true
}

# Social Media (1,829 records)
{
  "post_text": "Post/comment content...",
  "source": "reddit|youtube_video|youtube_comment"
}
```

**Analysis Methods:**
- Rating distribution (Amazon 1-5 stars)
- Sentiment classification (positive/neutral/negative)
- Sentiment by brand (Command vs 3M vs competitors)
- Sentiment by platform comparison
- Verified vs unverified sentiment delta

**Expected Outputs:**

1. **Sentiment Scores Dataset**
   - Add `sentiment_score` field (-1 to +1)
   - Add `sentiment_label` field (positive/neutral/negative)
   - Export: `data/analysis/sentiment_enhanced.json`

2. **Sentiment Summary Report**
   - Overall sentiment: X% positive, Y% neutral, Z% negative
   - By brand breakdown
   - By platform breakdown
   - By product breakdown (top 11 products)
   - Format: `SENTIMENT_ANALYSIS_REPORT.md`

3. **Visualizations**
   - Sentiment distribution histogram
   - Sentiment by brand bar chart
   - Sentiment by platform comparison
   - Rating distribution (Amazon only)
   - Export: `data/analysis/visualizations/sentiment_*.png`

**Key Questions to Answer:**
- What is the overall sentiment toward Command products?
- How does sentiment differ between platforms?
- Do verified purchases have different sentiment than unverified?
- Which products have the most positive/negative sentiment?

---

### 2. BRAND PERCEPTION & POSITIONING

**Objective:** Map competitive landscape and brand associations

**Input Data:**
```python
{
  "brand_mentions": ["Command", "3M", "VHB"],
  "post_text": "Full content for co-occurrence analysis",
  "product_title": "Product names for brand extraction"
}
```

**Analysis Methods:**
- Brand mention frequency across all sources
- Co-occurrence analysis (which brands mentioned together)
- Brand association mapping (adjectives/attributes per brand)
- Competitive mentions (Navona, generic hooks, alternatives)
- Context analysis (positive vs negative brand mentions)

**Expected Outputs:**

1. **Brand Frequency Table**
   | Brand | Total Mentions | Amazon | Reddit | YouTube | Sentiment |
   |-------|---------------|--------|--------|---------|-----------|
   | Command | 765 | 765 | X | Y | +0.XX |
   | 3M | 368 | 368 | X | Y | +0.XX |

   - Export: `data/analysis/brand_mentions.csv`

2. **Brand Co-occurrence Matrix**
   - Which brands appear together in same text
   - Competitive comparison frequency
   - Export: `data/analysis/brand_cooccurrence.json`

3. **Brand Association Report**
   - Top adjectives/attributes per brand
   - Positive associations: "strong", "reliable", "easy"
   - Negative associations: "falls", "weak", "damage"
   - Format: `BRAND_PERCEPTION_REPORT.md`

4. **Competitive Positioning Map**
   - 2D plot: Sentiment vs Mention Frequency
   - Brand clustering visualization
   - Export: `data/analysis/visualizations/brand_positioning.png`

**Key Questions to Answer:**
- How is Command perceived vs 3M parent brand?
- What are the key brand attributes?
- Who are the main competitors mentioned?
- How does Command compare to alternatives?

---

### 3. TOPIC MODELING

**Objective:** Discover key themes and conversation topics

**Input Data:**
```python
# All text combined (2,878 documents)
corpus = reviews['review_text'] + social['post_text']
```

**Analysis Methods:**
- Topic modeling (LDA or BERTopic)
- 10-15 topics extraction
- Topic labeling (manual or GPT-assisted)
- Topic distribution per document
- Topic evolution over time (if dates parsed)

**Expected Outputs:**

1. **Topic Dictionary**
   ```json
   {
     "topic_1": {
       "label": "Adhesion Strength",
       "keywords": ["stick", "hold", "strong", "weight", "fall"],
       "prevalence": 0.23
     }
   }
   ```
   - Export: `data/analysis/topics.json`

2. **Topic Distribution Dataset**
   - Add `primary_topic`, `topic_scores` to each record
   - Export: `data/analysis/topic_enhanced.json`

3. **Topic Analysis Report**
   - Top 10-15 topics with descriptions
   - Topic prevalence ranking
   - Topic distribution by source
   - Topic-sentiment correlation
   - Format: `TOPIC_MODELING_REPORT.md`

4. **Visualizations**
   - Topic word clouds (1 per topic)
   - Topic prevalence bar chart
   - Topic-sentiment heatmap
   - Export: `data/analysis/visualizations/topics/`

**Expected Topics (Hypotheses):**
- Adhesion strength/failure
- Surface compatibility (walls, wood, metal)
- Removal/damage concerns
- Garage organization use cases
- Weight capacity
- Weather resistance (outdoor use)
- Price/value
- Installation ease
- Alternative comparisons
- Product durability

**Key Questions to Answer:**
- What are the main conversation themes?
- Which topics drive positive vs negative sentiment?
- How do topics differ across platforms?
- What use cases are most discussed?

---

### 4. PAIN POINTS & FEATURE ANALYSIS

**Objective:** Identify product issues and customer needs

**Input Data:**
```python
# Low-rated reviews (1-3 stars)
low_rated = [r for r in reviews if "1.0" in r['rating'] or "2.0" in r['rating'] or "3.0" in r['rating']]

# Negative sentiment social posts
negative_social = [s for s in social if sentiment_score < -0.2]
```

**Analysis Methods:**
- Negative review text analysis
- Common complaint extraction
- Feature request identification
- Problem frequency ranking
- Use case failure analysis

**Expected Outputs:**

1. **Pain Points Ranking**
   | Issue | Frequency | % of Negative | Example Quote |
   |-------|-----------|---------------|---------------|
   | Adhesion failure | 234 | 45% | "fell off wall after 2 days" |
   | Surface damage | 123 | 24% | "removed paint when removing" |

   - Export: `data/analysis/pain_points.csv`

2. **Feature Requests**
   - Extracted wishes/requests from text
   - "I wish it had...", "Would be better if..."
   - Frequency ranking
   - Export: `data/analysis/feature_requests.json`

3. **Pain Points Report**
   - Top 10 issues detailed
   - Root cause analysis (when possible)
   - Mitigation recommendations
   - Format: `PAIN_POINTS_REPORT.md`

4. **Use Case Failure Analysis**
   - Which use cases have highest failure rates
   - Surface type correlations
   - Weight/load issues
   - Export: `data/analysis/use_case_failures.json`

**Key Questions to Answer:**
- What are the top 5 customer pain points?
- Which features are most requested?
- What causes product failures?
- Which use cases are problematic?

---

### 5. PRODUCT PERFORMANCE BENCHMARKING

**Objective:** Compare products and identify winners/losers

**Input Data:**
```python
# 11 unique products from reviews
products = reviews.groupby('product_id')

# Cross-platform product mentions
product_mentions = social[social['post_text'].contains(product_name)]
```

**Analysis Methods:**
- Average rating per product
- Rating distribution analysis
- Verified vs unverified comparison
- Sentiment score per product
- Cross-platform performance

**Expected Outputs:**

1. **Product Scorecard**
   | Product | Reviews | Avg Rating | Verified % | Sentiment | Reddit | YouTube |
   |---------|---------|------------|------------|-----------|--------|---------|
   | Command Picture Strips | 100 | 4.2 | 98% | +0.45 | 23 | 12 |

   - All 11 products ranked
   - Export: `data/analysis/product_scorecard.csv`

2. **Performance Distribution**
   - Rating distribution per product (histograms)
   - Sentiment range per product (box plots)
   - Export: `data/analysis/visualizations/product_performance_*.png`

3. **Product Benchmarking Report**
   - Top 3 performers (highest rated/sentiment)
   - Bottom 3 performers
   - Product-specific insights
   - Recommendations for product improvements
   - Format: `PRODUCT_BENCHMARKING_REPORT.md`

4. **Verification Impact Analysis**
   - Do verified purchases rate differently?
   - Sentiment delta: verified vs unverified
   - Statistical significance testing
   - Export: `data/analysis/verification_impact.json`

**Key Questions to Answer:**
- Which products perform best/worst?
- How do ratings vary by product?
- Does verified purchase status affect sentiment?
- Which products need improvement?

---

### 6. ENGAGEMENT & VIRALITY ANALYSIS

**Objective:** Understand what drives engagement and sharing

**Input Data:**
```python
# YouTube videos with high views
viral_videos = [v for v in social if v['source'] == 'youtube_video' and v['score'] > 100000]

# Reddit posts with high engagement
popular_posts = [p for p in social if p['source'] == 'reddit' and p['num_comments'] > 10]
```

**Analysis Methods:**
- View count analysis (YouTube)
- Comment count correlation
- Engagement patterns
- Content type analysis
- Viral content characteristics

**Expected Outputs:**

1. **Engagement Metrics**
   | Platform | Avg Views/Score | Avg Comments | Top Post | Engagement Rate |
   |----------|----------------|--------------|----------|----------------|
   | YouTube | 853K | 4.5 | "Garage Org Makeover" | 0.5% |
   | Reddit | 12 | 3.2 | "Command Hook Review" | 26% |

   - Export: `data/analysis/engagement_metrics.csv`

2. **Viral Content Analysis**
   - Characteristics of top 10% most-viewed content
   - Common themes in viral videos
   - Engagement drivers
   - Format: `VIRAL_CONTENT_REPORT.md`

3. **Engagement Visualizations**
   - View count distribution
   - Comment count correlation scatter plot
   - Engagement by content type
   - Export: `data/analysis/visualizations/engagement_*.png`

4. **Content Performance Prediction**
   - Features that predict high engagement
   - Regression analysis (views ~ topic + sentiment + length)
   - Export: `data/analysis/engagement_model.json`

**Key Questions to Answer:**
- What makes content go viral?
- Which topics drive most engagement?
- How does engagement differ by platform?
- What content characteristics predict success?

---

## Analysis Workflow

### Phase 1: Data Preparation (Week 1)
1. Load consolidated datasets
2. Text preprocessing (lowercase, remove special chars, tokenization)
3. Feature extraction (sentiment, entities, topics)
4. Enhanced dataset creation

### Phase 2: Core Analysis (Week 2)
1. Sentiment analysis → Report
2. Brand perception → Report
3. Topic modeling → Report
4. Pain points → Report
5. Product performance → Scorecard
6. Engagement analysis → Report

### Phase 3: Synthesis (Week 3)
1. Cross-analysis insights
2. Executive summary
3. Recommendations
4. Presentation deck

---

## Output File Structure

```
data/analysis/
├── enhanced_datasets/
│   ├── sentiment_enhanced.json          (2,878 records + sentiment scores)
│   ├── topic_enhanced.json              (2,878 records + topic assignments)
│   └── full_analysis.json               (2,878 records + all analysis fields)
├── reports/
│   ├── SENTIMENT_ANALYSIS_REPORT.md
│   ├── BRAND_PERCEPTION_REPORT.md
│   ├── TOPIC_MODELING_REPORT.md
│   ├── PAIN_POINTS_REPORT.md
│   ├── PRODUCT_BENCHMARKING_REPORT.md
│   ├── VIRAL_CONTENT_REPORT.md
│   └── EXECUTIVE_SUMMARY.md
├── visualizations/
│   ├── sentiment/
│   │   ├── distribution.png
│   │   ├── by_brand.png
│   │   └── by_platform.png
│   ├── topics/
│   │   ├── topic_*.png (word clouds)
│   │   └── prevalence.png
│   ├── products/
│   │   ├── scorecard.png
│   │   └── performance_*.png
│   └── engagement/
│       ├── views_distribution.png
│       └── engagement_correlation.png
└── data_exports/
    ├── brand_mentions.csv
    ├── pain_points.csv
    ├── product_scorecard.csv
    ├── engagement_metrics.csv
    └── topics.json
```

---

## Analysis Tools Recommendations

### Python Stack
- **pandas**: Data manipulation
- **numpy**: Numerical operations
- **scikit-learn**: Machine learning, topic modeling (LDA)
- **transformers** (Hugging Face): Sentiment analysis (RoBERTa, BERT)
- **spaCy**: NLP preprocessing, entity extraction
- **matplotlib/seaborn**: Visualizations
- **plotly**: Interactive dashboards
- **wordcloud**: Topic word clouds

### Alternative: GPT-4 Based Analysis
- Use GPT-4 for sentiment, topic extraction, pain point identification
- Batch processing via API
- More accurate but slower and more expensive
- Recommended for smaller samples or validation

### Database Queries
- Use PostgreSQL for aggregations
- Complex queries for cross-analysis
- Fast filtering and grouping

---

## Success Criteria

### Data Quality
- ✅ 100% records processed
- ✅ <5% errors in sentiment classification
- ✅ Topic coherence score > 0.5
- ✅ Statistical significance validated

### Deliverable Completeness
- ✅ All 6 reports generated
- ✅ All visualizations created
- ✅ Enhanced datasets exported
- ✅ Executive summary finalized

### Insight Quality
- ✅ Actionable recommendations provided
- ✅ Clear competitive insights
- ✅ Product improvement suggestions
- ✅ Brand positioning clarity

---

## Timeline Estimate

**Week 1: Setup & Sentiment** (8-12 hours)
- Environment setup
- Sentiment analysis
- Initial visualizations

**Week 2: Deep Analysis** (12-16 hours)
- Brand perception
- Topic modeling
- Pain points
- Product benchmarking

**Week 3: Synthesis** (8-10 hours)
- Engagement analysis
- Cross-analysis
- Report writing
- Presentation creation

**Total: 28-38 hours** (3-4 weeks part-time)

---

**Status:** ✅ MAPPED AND READY
**Next Step:** Begin Phase 1 - Data Preparation
**Owner:** Analytics Team
**Expected Completion:** 3-4 weeks from start

---

**Last Updated:** 2025-11-02 01:00:00
