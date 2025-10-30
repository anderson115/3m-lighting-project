"""
Video Processing Modules
Modular, scalable processors for multimodal data extraction
"""

from .base_processor import BaseProcessor
from .transcription import TranscriptionProcessor
from .visual_analysis import VisualAnalysisProcessor
from .audio_features import AudioFeaturesProcessor
from .metadata_extractor import MetadataExtractor

__all__ = [
    'BaseProcessor',
    'TranscriptionProcessor',
    'VisualAnalysisProcessor',
    'AudioFeaturesProcessor',
    'MetadataExtractor',
]
