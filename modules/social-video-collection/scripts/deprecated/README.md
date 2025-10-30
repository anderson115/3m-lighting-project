# Deprecated Scripts

These scripts are kept for reference but are no longer used in the current workflow.

## Deprecated Files

- **03_process_videos.py** - Replaced by `batch_processor.py`
- **03_transcribe.py** - Now part of `processors/transcription.py`
- **04_extract_visuals.py** - Now part of `processors/visual_analysis.py`
- **05_audio_features.py** - Now part of `processors/audio_features.py`

## Current Workflow

Use these scripts instead:

1. `01_search_videos.py` - Search for videos
2. `02_download_videos.py` - Download videos
3. `batch_processor.py` - Process all videos (replaces 03, 04, 05)
4. `04_consolidate_data.py` - Consolidate results

See `docs/FOLDER_STRUCTURE.md` for full documentation.
