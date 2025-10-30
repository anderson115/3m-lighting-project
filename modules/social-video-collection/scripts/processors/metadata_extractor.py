#!/usr/bin/env python3
"""
Metadata Extractor
Extracts comments, description, and engagement data from search results
"""

import json
from pathlib import Path
from typing import Dict, List

from .base_processor import BaseProcessor


class MetadataExtractor(BaseProcessor):
    """Extract comments and metadata from search results"""

    @property
    def output_filename(self) -> str:
        return "metadata.json"

    @property
    def processor_name(self) -> str:
        return "Metadata Extraction"

    def process(self, video_path: Path, metadata: Dict) -> Dict:
        """
        Extract metadata, description, and comments

        Returns:
            {
                'description': '...',
                'hashtags': [...],
                'comments': [...],
                'engagement': {...},
                'creator': {...}
            }
        """
        # Description and hashtags
        description = metadata.get('text', '') or metadata.get('desc', '')
        hashtags = [
            {
                'tag': tag.get('name', ''),
                'id': tag.get('id', '')
            }
            for tag in metadata.get('hashtags', [])
        ]

        # Engagement metrics
        engagement = {
            'views': metadata.get('playCount', 0),
            'likes': metadata.get('diggCount', 0),
            'comments_count': metadata.get('commentCount', 0),
            'shares': metadata.get('shareCount', 0),
            'saved': metadata.get('collectCount', 0)
        }

        # Creator info
        author_meta = metadata.get('authorMeta', {})
        creator = {
            'username': author_meta.get('name', ''),
            'nickname': author_meta.get('nickName', ''),
            'bio': author_meta.get('signature', ''),
            'verified': author_meta.get('verified', False),
            'followers': author_meta.get('fans', 0),
            'following': author_meta.get('following', 0),
            'total_videos': author_meta.get('video', 0),
            'total_likes': author_meta.get('heart', 0)
        }

        # Video metadata
        video_meta = metadata.get('videoMeta', {})
        video_info = {
            'duration': video_meta.get('duration', 0),
            'width': video_meta.get('width', 0),
            'height': video_meta.get('height', 0),
            'ratio': video_meta.get('ratio', ''),
            'cover_url': video_meta.get('coverUrl', ''),
            'dynamic_cover_url': video_meta.get('dynamicCover', '')
        }

        # Music/audio info
        music_meta = metadata.get('musicMeta', {})
        audio = {
            'music_name': music_meta.get('musicName', ''),
            'music_author': music_meta.get('musicAuthor', ''),
            'music_id': music_meta.get('musicId', ''),
            'original': music_meta.get('musicOriginal', False)
        }

        # Comments - extract if available in metadata
        # Note: Apify may not include comments in free tier
        comments = []
        if 'comments' in metadata:
            for comment in metadata.get('comments', [])[:50]:  # Limit to 50
                comments.append({
                    'text': comment.get('text', ''),
                    'likes': comment.get('digg_count', 0),
                    'create_time': comment.get('create_time', 0),
                    'user': comment.get('user', {}).get('nickname', '')
                })

        # Platform metadata
        platform_data = {
            'video_id': metadata.get('id', ''),
            'create_time': metadata.get('createTime', ''),
            'url': metadata.get('webVideoUrl', ''),
            'is_ad': metadata.get('isAd', False),
            'location': metadata.get('locationCreated', '')
        }

        return {
            'description': description,
            'hashtags': hashtags,
            'engagement': engagement,
            'creator': creator,
            'video_info': video_info,
            'audio': audio,
            'comments': comments,
            'platform': platform_data
        }
