# 3M Lighting Project - Media Archive

**Created**: November 11, 2025

This folder consolidates all media datasets and video analysis modules for the 3M lighting project.

## Contents

### youtube-datasource/
- **Purpose**: YouTube video collection and analysis module
- **Size**: 369 MB
- **Contents**:
  - Pre-collected YouTube videos used for category intelligence training
  - Video analysis outputs and metadata
  - Organized by category (beginner, intermediate, advanced)
  - Archive data from preflight testing (2025-10-05)

**Active Use**: This module is in active development and maintained locally for quick iteration.

### Related Archives (on R2D2 NAS)
For large processed datasets, see: `/System/Volumes/Data/R2D2/archives/3m-lighting-2025/`
- lighting-2025/ - Complete project archive with all processed outputs
- Contains: raw videos, processed videos, audio extracts, analysis results

## Usage

```bash
# Access youtube videos
cd youtube-datasource/
ls data/3m_lighting/archives/preflight_2025-10-05/videos/

# Run analysis on youtube data
python -m youtube_datasource.analyze

# Pull data from R2D2 archive if needed
cp -r /System/Volumes/Data/R2D2/archives/3m-lighting-2025/lighting-2025 ../
```

## Storage Strategy

- **Local (SSD)**: Active development modules + frequently accessed data (369 MB)
- **NAS (R2D2)**: Archive of completed runs + historical data (7.2 GB)
- **Rationale**: Fast iteration on active work, archived data accessible for reference/restoration

## Migration Notes

See `../DATA-MIGRATION-2025-11-11.md` for details on Nov 11 data reorganization.
