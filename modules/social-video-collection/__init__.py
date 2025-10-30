"""
Social Video Collection Module

A reusable, platform-agnostic video data collection pipeline for social media
platforms (TikTok, Instagram Reels, YouTube Shorts). Collects raw structured
data for downstream agentic analysis.

Version: 1.0.0
Author: 3M Lighting Project
"""

__version__ = "1.0.0"
__author__ = "3M Lighting Project"

# Module metadata
MODULE_NAME = "social-video-collection"
MODULE_STATUS = "production-ready"
SUPPORTED_PLATFORMS = ["tiktok", "instagram", "youtube_shorts"]

# Local model paths
LOCAL_MODELS = {
    "whisper": "/Volumes/TARS/llm-models/whisper/large-v3.pt",
    "llava": "/Volumes/TARS/llm-models/llava/",
    "ollama_base": "/Volumes/TARS/llm-models/ollama/"
}
