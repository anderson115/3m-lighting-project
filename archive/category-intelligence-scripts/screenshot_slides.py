#!/usr/bin/env python3
"""Take screenshots of slides to see design"""

import json
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import requests

# Load credentials
creds_path = Path.home() / ".config/google-drive-credentials.json"
with open(creds_path) as f:
    creds_data = json.load(f)

creds = Credentials(
    token=creds_data['tokens']['access_token'],
    refresh_token=creds_data['tokens']['refresh_token'],
    token_uri=creds_data['tokens']['token_uri'],
    client_id=creds_data['tokens']['client_id'],
    client_secret=creds_data['tokens']['client_secret'],
    scopes=creds_data['tokens']['scopes']
)

slides_service = build('slides', 'v1', credentials=creds)
drive_service = build('drive', 'v3', credentials=creds)

PRESENTATION_ID = '1opG3t90RNV-QvNl57mSThaXTa_7rarAy6thUsJ2h8eM'

presentation = slides_service.presentations().get(
    presentationId=PRESENTATION_ID
).execute()

print("Getting slide thumbnails...\n")

# Get thumbnails for slides 2 and 3
for i, slide in enumerate(presentation['slides'][:3], 1):
    slide_id = slide['objectId']

    # Get thumbnail
    thumbnail = slides_service.presentations().pages().getThumbnail(
        presentationId=PRESENTATION_ID,
        pageObjectId=slide_id
    ).execute()

    thumbnail_url = thumbnail.get('contentUrl')

    if thumbnail_url:
        # Download thumbnail
        response = requests.get(thumbnail_url)
        output_path = f'/tmp/slide_{i}_{slide_id}.png'
        with open(output_path, 'wb') as f:
            f.write(response.content)
        print(f"Slide {i}: Saved to {output_path}")

print("\nSlide 2 = existing design (good)")
print("Slide 3 = my design (garbage)")
