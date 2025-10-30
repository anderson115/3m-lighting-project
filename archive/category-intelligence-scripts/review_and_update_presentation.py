#!/usr/bin/env python3
"""Review and update presentation structure"""

import json
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

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

PRESENTATION_ID = '1opG3t90RNV-QvNl57mSThaXTa_7rarAy6thUsJ2h8eM'

print("Reading presentation structure...\n")

presentation = slides_service.presentations().get(
    presentationId=PRESENTATION_ID
).execute()

print(f"Title: {presentation['title']}")
print(f"Total slides: {len(presentation['slides'])}\n")
print("="*80)

# List all slides with their content
for i, slide in enumerate(presentation['slides'], 1):
    print(f"\nSlide {i}: ID={slide['objectId']}")

    # Extract text content
    text_content = []
    if 'pageElements' in slide:
        for element in slide['pageElements']:
            if 'shape' in element and 'text' in element['shape']:
                for text_run in element['shape']['text'].get('textElements', []):
                    if 'textRun' in text_run:
                        text = text_run['textRun']['content'].strip()
                        if text:
                            text_content.append(text)

    if text_content:
        print("Content:")
        for text in text_content[:5]:  # First 5 text elements
            print(f"  • {text[:100]}{'...' if len(text) > 100 else ''}")
    else:
        print("  (No text content)")

print("\n" + "="*80)
print("\nSLIDE STRUCTURE ANALYSIS")
print("="*80)

# Identify which slides need updating
print("\nSlides to update for current approach:")
print("1. Update sample size references (189 → 153)")
print("2. Update methodology references to include emotion analysis")
print("3. Reserve slides for upcoming analysis sections")

print("\n✓ Review complete")
