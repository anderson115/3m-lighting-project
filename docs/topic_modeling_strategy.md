# Topic Modeling & Tagging Strategy

## Objectives
1. **High-fidelity atomic coding** of social verbatims across Connection, Discovery, Expression, Entertainment, Creativity, plus organic drivers surfaced in Snippets_50.
2. **Creator-status detection** at both snippet and post level for >10K follower profiles or self-identified creators.
3. **Self-learning workflow** that folds manual QA decisions into the model feature store for continuous improvement.

## Pipeline Overview
1. **Ingestion & Normalization**  
   - Pull raw records from Bright Data/Reddit/X collectors into `manual_sample_posts.json`.  
   - Normalize text (emoji handling, newline stripping) and retain metadata (platform, URLs, timestamps).
2. **Atomic Idea Extraction**  
   - Manual reasoning (current phase) + future hybrid model (LLM + rule-based) to split each post into granular snippets.
3. **Feature Augmentation** (implemented in `process_01_generate_master_sheet.py`):  
   - Verbatim excerpt selection (sentence-level lexical overlap).  
   - Agent interpretation + rationale to anchor future model explanations.  
   - Heuristic signals for Connection/Discovery/Expression/Entertainment/Creativity using seeded keyword banks.  
   - Creator flag detection via follower-count regex + creator keyword list (Possible/Confirmed).  
   - Post-level rollups (dominant driver, sentiment stack rank, creator flag).
4. **Annotation Surfaces**  
   - `Snippets_50` sheet with dropdowns for all controlled vocabularies.  
   - `Examples10` replicates 10 posts with every derived snippet for audit ease.
5. **Feedback Capture**  
   - Reviewers adjust dropdowns + notes → stored as truth labels for retraining.
6. **Model Training Plan**  
   - Vectorize snippets using sentence-transformers (e.g., `all-mpnet-base-v2`).  
   - Train multi-label classifiers for drivers & equity measures (One-vs-Rest Logistic Regression + class-weighting).  
   - Train sentiment classifier aligned to Negative/Mixed/Neutral/Positive priority order.  
   - Creator flag model: gradient boosted trees ingest regex outputs, lexical cues, platform metadata.
7. **Active Learning Loop**  
   - Uncertainty sampling (entropy across labels) to prioritize manual reviews.  
   - Human decisions appended to versioned dataset (`annotations_v*.parquet`).  
   - Retrain weekly or after ≥200 new confirmed annotations; track F1 by label.

## Tooling & Extensibility
- **Scripted rebuild**: `python3 scripts/process_01_generate_master_sheet.py` regenerates the workbook deterministically.  
- **Keyword banks**: maintain in YAML to enable quick expansion as new ways of expressing Connection/Creativity emerge.  
- **Model repo**: plan to house training notebooks + inference service under `modules/topic-modeling/`.  
- **Automation hooks**: once accuracy targets met, integrate inference into `core/pipeline` so new social pulls auto-tag before analyst review.

## Accuracy Targets (Initial)
| Label Family | Metric | Target |
|--------------|--------|--------|
| Driver Topics | Macro F1 | ≥0.80 |
| Equity Signals | Recall (Strong) | ≥0.85 |
| Creator Flag | Precision (Confirmed) | ≥0.90 |
| Sentiment | Weighted F1 | ≥0.82 |

## Next Steps
1. Collect ≥200 manually verified snippets with the new equity/creator flags to seed supervised training.  
2. Stand up prototype notebooks (sentence-transformers + scikit-learn) using the annotated CSV export.  
3. Evaluate disagreement heatmaps to refine keyword banks + aggregation heuristics.  
4. Wire active-learning loop into reviewer UI (Google Sheet or Streamlit) to surface high-uncertainty cases first.
