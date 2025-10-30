#!/usr/bin/env python3
"""
Base Processor Class
All video processors inherit from this for consistent interface
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from abc import ABC, abstractmethod


class BaseProcessor(ABC):
    """Base class for all video processors"""

    def __init__(self, config: Dict, video_dir: Path):
        """
        Args:
            config: Processing configuration
            video_dir: Path to video directory
        """
        self.config = config
        self.video_dir = Path(video_dir)
        self.output_file = self.video_dir / self.output_filename

    @property
    @abstractmethod
    def output_filename(self) -> str:
        """Filename for processor output (e.g., 'transcript.json')"""
        pass

    @property
    @abstractmethod
    def processor_name(self) -> str:
        """Human-readable processor name"""
        pass

    @abstractmethod
    def process(self, video_path: Path, metadata: Dict) -> Dict:
        """
        Process video and return extracted data

        Args:
            video_path: Path to video file
            metadata: Video metadata from search results

        Returns:
            Extracted data dictionary
        """
        pass

    def is_processed(self) -> bool:
        """Check if video already processed"""
        return self.output_file.exists()

    def save_output(self, data: Dict) -> None:
        """Save processor output to JSON"""
        with open(self.output_file, 'w') as f:
            json.dump(data, f, indent=2)

    def load_output(self) -> Optional[Dict]:
        """Load existing output if available"""
        if self.is_processed():
            with open(self.output_file) as f:
                return json.load(f)
        return None

    def run(self, video_path: Path, metadata: Dict, force: bool = False) -> Dict:
        """
        Execute processor with resume capability

        Args:
            video_path: Path to video file
            metadata: Video metadata
            force: Force reprocessing even if output exists

        Returns:
            Extracted data
        """
        if not force and self.is_processed():
            print(f"  ↻ {self.processor_name}: Already processed (skipping)")
            return self.load_output()

        print(f"  ▸ {self.processor_name}: Processing...")

        try:
            data = self.process(video_path, metadata)
            self.save_output(data)
            print(f"  ✓ {self.processor_name}: Complete")
            return data

        except Exception as e:
            print(f"  ✗ {self.processor_name}: Failed - {str(e)[:100]}")
            raise
