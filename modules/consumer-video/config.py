"""Shared configuration for the consumer video / JTBD module.

This file provides sensible defaults while allowing deployments to
override paths through environment variables. See modules/consumer-video
/docs/ for integration guidance.
"""

from __future__ import annotations

import os
from pathlib import Path

# Base directories can be overridden to support different clients/projects
MODULE_ROOT = Path(__file__).resolve().parent
DEFAULT_DATA_ROOT = MODULE_ROOT / "data"
DATA_ROOT = Path(os.environ.get("CONSUMER_VIDEO_DATA_ROOT", DEFAULT_DATA_ROOT))

DEFAULT_MEDIA_SOURCE = "/Volumes/DATA/media/<client>/<project>/raw/consumer-video"
MEDIA_SOURCE = os.environ.get("CONSUMER_VIDEO_MEDIA_SOURCE", DEFAULT_MEDIA_SOURCE)

# Directory layout (relative to DATA_ROOT by default)
PATHS = {
    "raw_videos": str(DATA_ROOT / "raw-videos"),
    "processed": str(DATA_ROOT / "processed"),
    "outputs": str(DATA_ROOT / "outputs"),
    "logs": str(DATA_ROOT / "logs"),
    "consumer_texts": str(DATA_ROOT / "consumer_texts"),
    "insights": str(DATA_ROOT / "insights"),
}

# Processing parameters
PROCESSING_CONFIG = {
    "tier": os.environ.get("CONSUMER_VIDEO_TIER", "PRO"),
    "confidence_threshold": float(os.environ.get("CONSUMER_VIDEO_CONFIDENCE", 0.65)),
    "priority_questions": [int(q) for q in os.environ.get("CONSUMER_VIDEO_PRIORITY_QS", "3,7,8").split(",")],
    "focus_areas": [
        "pain_points",
        "3m_adjacency",
        "golden_moments",
        "workarounds",
    ],
    "emotion_sensitivity": os.environ.get("CONSUMER_VIDEO_EMOTION", "high"),
    "quote_preference": os.environ.get("CONSUMER_VIDEO_QUOTE_PREFERENCE", "impactful"),
    "frame_sample_interval": int(os.environ.get("CONSUMER_VIDEO_FRAME_INTERVAL", 5)),
    "emotion_window": int(os.environ.get("CONSUMER_VIDEO_EMOTION_WINDOW", 5)),
    "max_quotes_per_category": int(os.environ.get("CONSUMER_VIDEO_MAX_QUOTES", 20)),
    "max_pain_points": int(os.environ.get("CONSUMER_VIDEO_MAX_PAIN_POINTS", 7)),
    "generate_html_visualization": os.environ.get("CONSUMER_VIDEO_HTML", "true").lower() == "true",
}

# Model references (override via env if needed)
MODEL_PATHS = {
    "qwen": os.environ.get("CONSUMER_VIDEO_MODEL_QWEN", "/Volumes/TARS/llm-models/qwen2.5-vl-7b-instruct"),
    "whisper": os.environ.get("CONSUMER_VIDEO_MODEL_WHISPER", "large-v3-turbo"),
    "hubert": os.environ.get("CONSUMER_VIDEO_MODEL_HUBERT", "/Volumes/TARS/llm-models/hubert-large"),
}

__all__ = ["MEDIA_SOURCE", "PATHS", "PROCESSING_CONFIG", "MODEL_PATHS", "DATA_ROOT"]
