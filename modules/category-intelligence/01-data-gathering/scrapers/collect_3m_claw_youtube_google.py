#!/usr/bin/env python3
"""
Collect 3M Claw YouTube videos using Google YouTube Data API v3.
Uses existing Google Workspace OAuth credentials.
Target: 100+ videos about 3M Claw products.
"""

import os
import json
import pickle
from datetime import datetime
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Search queries for 3M Claw
SEARCH_QUERIES = [
    "3M Claw hooks",
    "3M Claw review",
    "3M Claw drywall hangers",
    "3M Claw installation",
    "3M Claw picture hanger",
    "3M Claw garage organization",
    "3M Claw vs Command hooks",
    "3M Claw how to use",
    "3M Claw product review",
    "3M Claw unboxing",
]

SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']

def get_youtube_service():
    """Get authenticated YouTube API service."""
    creds = None
    token_file = Path(__file__).parent / 'youtube_token.pickle'
    creds_file = Path(__file__).parent / 'google_credentials.json'

    # Load existing token
    if token_file.exists():
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)

    # If no valid creds, authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing expired token...")
            creds.refresh(Request())
        else:
            # Load from credentials file and use refresh token
            print("Loading credentials from google_credentials.json...")
            with open(creds_file, 'r') as f:
                cred_data = json.load(f)

            # Use tokens section if it exists
            if 'tokens' in cred_data:
                token_data = cred_data['tokens']
                creds = Credentials(
                    token=token_data.get('access_token'),
                    refresh_token=token_data.get('refresh_token'),
                    token_uri=token_data.get('token_uri'),
                    client_id=token_data.get('client_id'),
                    client_secret=token_data.get('client_secret'),
                    scopes=SCOPES
                )
                # Refresh to get YouTube scope
                creds.refresh(Request())
            else:
                print("ERROR: No tokens found in credentials file")
                return None

        # Save token for future use
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)

    return build('youtube', 'v3', credentials=creds)

def search_youtube(youtube, query, max_results=15):
    """Search YouTube and get video metadata."""
    print(f"\n🎥 Searching: '{query}' (target: {max_results} videos)")

    try:
        # Search for videos
        search_response = youtube.search().list(
            q=query,
            type='video',
            part='id,snippet',
            maxResults=max_results,
            order='relevance'
        ).execute()

        video_ids = [item['id']['videoId'] for item in search_response.get('items', [])]

        if not video_ids:
            print(f"   ✗ No results found")
            return []

        # Get detailed video statistics
        videos_response = youtube.videos().list(
            id=','.join(video_ids),
            part='snippet,statistics,contentDetails'
        ).execute()

        videos = []
        for item in videos_response.get('items', []):
            videos.append({
                "video_id": item['id'],
                "title": item['snippet']['title'],
                "description": item['snippet']['description'],
                "channel": item['snippet']['channelTitle'],
                "channel_id": item['snippet']['channelId'],
                "views": int(item['statistics'].get('viewCount', 0)),
                "likes": int(item['statistics'].get('likeCount', 0)),
                "comments": int(item['statistics'].get('commentCount', 0)),
                "upload_date": item['snippet']['publishedAt'],
                "duration": item['contentDetails']['duration'],
                "url": f"https://youtube.com/watch?v={item['id']}",
                "thumbnail": item['snippet']['thumbnails']['high']['url'],
                "search_query": query
            })

        print(f"   ✓ Collected {len(videos)} videos")
        return videos

    except Exception as e:
        print(f"   ✗ Error: {str(e)}")
        return []

def main():
    """Collect 3M Claw YouTube videos."""

    print("="*70)
    print("3M CLAW YOUTUBE VIDEO COLLECTION (GOOGLE API)")
    print("="*70)
    print(f"Queries: {len(SEARCH_QUERIES)}")
    print(f"Target: ~{len(SEARCH_QUERIES) * 15} videos")
    print()

    # Get YouTube service
    youtube = get_youtube_service()
    if not youtube:
        print("ERROR: Failed to authenticate with YouTube API")
        return

    all_videos = []

    for i, query in enumerate(SEARCH_QUERIES, 1):
        print(f"[{i}/{len(SEARCH_QUERIES)}]", end="")
        videos = search_youtube(youtube, query, max_results=15)
        all_videos.extend(videos)

    # Remove duplicates by video_id
    unique_videos = {}
    for video in all_videos:
        vid_id = video.get('video_id')
        if vid_id and vid_id not in unique_videos:
            unique_videos[vid_id] = video

    final_videos = list(unique_videos.values())

    print(f"\n{'='*70}")
    print(f"COLLECTION COMPLETE")
    print(f"{'='*70}")
    print(f"Total collected: {len(all_videos)} videos")
    print(f"After deduplication: {len(final_videos)} unique videos")
    print(f"Target met: {'✓ YES' if len(final_videos) >= 100 else f'✗ NO ({len(final_videos)}/100)'}")
    print(f"{'='*70}\n")

    # Save results
    if final_videos:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"outputs/3m_claw_youtube_videos_{timestamp}.json"

        os.makedirs("outputs", exist_ok=True)
        with open(output_file, 'w') as f:
            json.dump(final_videos, f, indent=2)

        print(f"✓ Saved to: {output_file}")
        print(f"  Total videos: {len(final_videos)}")
        print(f"  Total views: {sum(v.get('views', 0) for v in final_videos):,}")

        # Show top channels
        channels = {}
        for v in final_videos:
            ch = v.get('channel', 'Unknown')
            channels[ch] = channels.get(ch, 0) + 1

        print(f"\n  Top channels:")
        for ch, count in sorted(channels.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"    {ch}: {count} videos")
    else:
        print("\n✗ No videos collected")

if __name__ == "__main__":
    main()
