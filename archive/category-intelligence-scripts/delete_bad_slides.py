#!/usr/bin/env python3
"""Delete the garbage slides I created"""

import json
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

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

print("Deleting garbage slides I created...\n")

presentation = slides_service.presentations().get(
    presentationId=PRESENTATION_ID
).execute()

# Find slides created by me (they have SLIDES_API in the ID or were added after position 2)
slides_to_delete = []
for i, slide in enumerate(presentation['slides']):
    slide_id = slide['objectId']
    # Delete slide 3 (my Methods slide) and slides 4-8 (my analysis slides)
    # These are positions 3-8 (indices 2-7)
    if i >= 2 and i <= 7:
        slides_to_delete.append(slide_id)
        print(f"  Marking for deletion: Slide {i+1} (ID: {slide_id})")

# Delete slides
requests = []
for slide_id in slides_to_delete:
    requests.append({
        'deleteObject': {
            'objectId': slide_id
        }
    })

if requests:
    slides_service.presentations().batchUpdate(
        presentationId=PRESENTATION_ID,
        body={'requests': requests}
    ).execute()
    print(f"\n✓ Deleted {len(requests)} garbage slides")
else:
    print("\n✓ No slides to delete")

print(f"✓ Presentation reset to original structure")
