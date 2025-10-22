# Consumer Video Module - 3M Lighting Project

**Status:** Clean slate - ready for execution  
**Date:** October 21, 2025  
**Location:** `/modules/consumer-video/`

## Folder Structure

```
consumer-video/
├── config.py                  # Processing configuration
├── config/
│   └── model_paths.yaml      # Model location references
├── data/
│   ├── raw-videos/           # Copy source videos here
│   ├── processed/            # Intermediate analysis (generated)
│   ├── outputs/              # Final deliverables (generated)
│   └── logs/                 # Processing logs (generated)
├── scripts/
│   └── archive/              # Previous processing scripts (archived)
└── docs/                     # Documentation (to be created)
```

## Media Source

**All raw consumer videos stored at:**  
`/Volumes/DATA/consulting/3m-lighting-consumer-videos/Intro Videos`

- 82 video files (8.5GB)
- 15 unique consumers
- Activities 1-10 captured

## Configuration

Edit `config.py` to set:
- Processing tier (FREE/PLUS/PRO)
- Confidence thresholds  
- Focus areas
- Model paths

## Current State

- ✅ Folder structure cleaned and reset
- ✅ Old analysis files archived
- ✅ Configuration updated with correct paths
- ✅ Ready for new processing pipeline

## Next Steps

1. Copy relevant videos from media source to `data/raw-videos/`
2. Review configuration in `config.py`
3. Create/execute processing pipeline

---

**Last Updated:** October 21, 2025
