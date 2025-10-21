# 3M Consumer Video Analysis - README

## Project Status
✅ Clean slate - ready for execution
📁 Directory structure created
📋 Master plan and configuration files in place
📹 82 consumer videos cataloged and ready for processing

## Video File Manifest
**All raw consumer videos are located at:**
`/Volumes/Data/consulting/3m-lighting-consumer-videos/`

See the **VIDEO FILE MANIFEST** section in `MASTER_PLAN_Consumer_Video_Analysis.md` for:
- Complete file listing (82 videos, 8.5GB)
- Participant breakdown (15 consumers)
- Activity categories (Activities 1-10)
- File naming conventions
- Processing priorities

## Quick Start

1. **Copy relevant video files** from `/Volumes/Data/consulting/3m-lighting-consumer-videos/` to `/raw_videos/`
2. **Review configuration** in `config.py`
3. **Execute with Claude Code:**
   ```bash
   claude code: "Execute 3M consumer video analysis pipeline per MASTER_PLAN"
   ```

## Directory Structure
```
3m-lighting-processed/
├── MASTER_PLAN_Consumer_Video_Analysis.md  # Complete execution plan
├── config.py                                # Processing configuration
├── README.md                                # This file
├── raw_videos/                              # Place source videos here
├── processed/                               # Intermediate analysis outputs
├── outputs/                                 # Final deliverables
└── logs/                                    # Processing logs
```

## Configuration Options

Edit `config.py` to customize:
- **Processing tier:** FREE, PLUS, PRO
- **Confidence threshold:** 0.70 - 0.90
- **Priority questions:** Which discussion guide questions matter most
- **Focus areas:** Pain points, 3M adjacency, golden moments, workarounds
- **Emotion sensitivity:** How much weight to give audio emotion analysis

## Expected Outputs

After processing completes, check `/outputs/` for:
- `final_synthesis_report.md` - Main deliverable
- `pain_points_ranked.json` - Severity-ranked pain points
- `quotes_library.json` - Curated verbatims
- `3m_adjacency_map.json` - Product touchpoints
- `golden_moments.json` - Success language
- `workarounds_inventory.json` - Compensating behaviors

## Processing Timeline

- **FREE tier:** ~2.5 hours for 15 videos
- **PLUS tier:** ~1.5 hours for 15 videos  
- **PRO tier:** ~1 hour for 15 videos

## Next Steps

1. Copy consumer video files to `/raw_videos/`
2. Verify config settings in `config.py`
3. Run Claude Code execution command
4. Review outputs in `/outputs/` folder

---
**Last Updated:** October 21, 2025  
**Status:** Ready for video processing
