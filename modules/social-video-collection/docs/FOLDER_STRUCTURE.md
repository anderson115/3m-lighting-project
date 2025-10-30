# Social Video Collection - Folder Structure

This document describes the organization of the social video collection module.

## Directory Structure

```
social-video-collection/
├── config/                      # Configuration files
│   ├── collection_config.yaml   # Base configuration template
│   └── examples/               # Example configurations
│       └── garage_organizers_tiktok.yaml
│
├── data/                        # Data storage (gitignored except structure)
│   ├── processed/              # Processed collections
│   │   └── {collection-name}/
│   │       ├── search_results.json
│   │       ├── status.json
│   │       └── videos/
│   │           └── {video-id}/
│   │               ├── video.mp4
│   │               ├── metadata.json
│   │               ├── transcript.json
│   │               ├── visual_analysis.json
│   │               ├── audio_features.json
│   │               └── frames/
│   ├── raw/                    # Raw scraped data
│   └── outputs/                # Final deliverables
│
├── docs/                        # Documentation
│   ├── QUICK_START.md          # Quick start guide
│   ├── FOLDER_STRUCTURE.md     # This file
│   ├── test-runs/              # Test run archives
│   └── deployment/             # Deployment documentation
│
├── scripts/                     # Core scripts
│   ├── processors/             # Video processing modules
│   │   ├── __init__.py
│   │   ├── base_processor.py
│   │   ├── metadata_extractor.py
│   │   ├── transcription.py
│   │   ├── visual_analysis.py
│   │   └── audio_features.py
│   ├── 01_search_videos.py     # Step 1: Search & collect
│   ├── 02_download_videos.py   # Step 2: Download videos
│   ├── 03_process_videos.py    # Step 3: Process videos (deprecated - use batch_processor)
│   ├── 04_consolidate_data.py  # Step 4: Consolidate results
│   ├── batch_processor.py      # Batch processing orchestrator
│   ├── reprocess_visual.py     # Utility: Reprocess failed visual analysis
│   └── run_collection.py       # End-to-end collection runner
│
├── tests/                       # Unit and integration tests
│
├── web/                         # Web interfaces
│   └── dashboard.html          # Processing status dashboard
│
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore rules
├── __init__.py                  # Python package init
├── README.md                    # Main documentation
├── requirements.txt             # Python dependencies
└── WE-ARE-HERE.md              # Current session state tracker

```

## Key Files

### Configuration
- **config/collection_config.yaml**: Template for new collections
- **config/examples/*.yaml**: Working examples for different categories

### Scripts (Execution Order)
1. **01_search_videos.py**: Search TikTok for videos matching criteria
2. **02_download_videos.py**: Download videos from search results
3. **batch_processor.py**: Process all videos (transcription, visual, audio)
4. **04_consolidate_data.py**: Merge all data into final deliverable

### Processors (Internal Modules)
- **base_processor.py**: Base class with resume capability
- **metadata_extractor.py**: Extract metadata, comments, engagement
- **transcription.py**: Audio transcription via OpenAI Whisper API
- **visual_analysis.py**: Frame analysis via GPT-4 Vision
- **audio_features.py**: Audio feature extraction via Librosa

### Documentation
- **README.md**: Main documentation and usage
- **docs/QUICK_START.md**: Quick start guide
- **WE-ARE-HERE.md**: Current session state (updated during work)
- **docs/test-runs/**: Archived test run summaries

### Web Interfaces
- **web/dashboard.html**: Real-time processing dashboard (reads status.json)

## Data Flow

```
1. Search → data/processed/{collection}/search_results.json
2. Download → data/processed/{collection}/videos/{id}/video.mp4
3. Process → data/processed/{collection}/videos/{id}/*.json
4. Consolidate → data/outputs/{collection}_final.json
```

## Best Practices

1. **Never commit data**: All data directories are gitignored
2. **Use configs**: Create new YAML configs for each collection
3. **Resume capability**: All processors check for existing output before reprocessing
4. **Modular design**: Each processor is independent and can be run separately
5. **Status tracking**: status.json is updated in real-time for monitoring

## Adding New Collections

1. Create new config: `config/examples/{new-collection}.yaml`
2. Run search: `python scripts/01_search_videos.py --config config/examples/{new-collection}.yaml`
3. Download: `python scripts/02_download_videos.py --search-results ...`
4. Process: `python scripts/batch_processor.py --config config/examples/{new-collection}.yaml`
5. Consolidate: `python scripts/04_consolidate_data.py --input ... --output ...`

## Environment Variables

Required environment variables (stored in 1Password, referenced in .env):
- `APIFY_TOKEN`: For TikTok scraping
- `OPENAI_API_KEY`: For Whisper transcription + GPT-4 Vision
- `HF_TOKEN`: (Optional) For Pyannote emotion detection
