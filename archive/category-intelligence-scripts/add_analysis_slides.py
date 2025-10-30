#!/usr/bin/env python3
"""Add placeholder slides for social video analysis sections"""

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

print("Adding analysis section slides...\n")

# Define new slides to add after Methods (position 4)
new_slides = [
    "CONSUMER PAIN POINTS",
    "EMOTIONAL LANDSCAPE",
    "VISUAL THEMES & PATTERNS",
    "CONTENT STRATEGIES",
    "BUYING TRIGGERS"
]

# Create slides
requests = []
for i, title in enumerate(new_slides):
    requests.append({
        'createSlide': {
            'insertionIndex': 3 + i + 1,  # After Methods slide (position 3)
            'slideLayoutReference': {
                'predefinedLayout': 'TITLE_ONLY'
            }
        }
    })

result = slides_service.presentations().batchUpdate(
    presentationId=PRESENTATION_ID,
    body={'requests': requests}
).execute()

print(f"✓ Created {len(new_slides)} new analysis slides")

# Add titles to each slide
title_requests = []
for i, reply in enumerate(result['replies']):
    slide_id = reply['createSlide']['objectId']
    title = new_slides[i]

    # Find title placeholder
    presentation = slides_service.presentations().get(
        presentationId=PRESENTATION_ID
    ).execute()

    for slide in presentation['slides']:
        if slide['objectId'] == slide_id:
            # Find title element
            for element in slide.get('pageElements', []):
                if 'shape' in element:
                    shape = element['shape']
                    if shape.get('placeholder', {}).get('type') == 'TITLE':
                        title_requests.append({
                            'insertText': {
                                'objectId': element['objectId'],
                                'text': title
                            }
                        })
                        title_requests.append({
                            'updateTextStyle': {
                                'objectId': element['objectId'],
                                'style': {
                                    'bold': True,
                                    'fontSize': {'magnitude': 40, 'unit': 'PT'}
                                },
                                'fields': 'bold,fontSize'
                            }
                        })
                        break
            break

if title_requests:
    slides_service.presentations().batchUpdate(
        presentationId=PRESENTATION_ID,
        body={'requests': title_requests}
    ).execute()
    print(f"✓ Added titles to analysis slides")

print(f"\n✓ Presentation now has {len(presentation['slides']) + len(new_slides)} slides")
print(f"✓ Reserved slides 4-8 for social video analysis")
print(f"\nLink: https://docs.google.com/presentation/d/{PRESENTATION_ID}/edit")
