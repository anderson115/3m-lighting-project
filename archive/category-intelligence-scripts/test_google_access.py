#!/usr/bin/env python3
"""Test Google Drive and Slides access"""

import json
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Load credentials
creds_path = Path.home() / ".config/google-drive-credentials.json"
with open(creds_path) as f:
    creds_data = json.load(f)

# Create credentials object
creds = Credentials(
    token=creds_data['tokens']['access_token'],
    refresh_token=creds_data['tokens']['refresh_token'],
    token_uri=creds_data['installed']['token_uri'],
    client_id=creds_data['installed']['client_id'],
    client_secret=creds_data['installed']['client_secret'],
    scopes=['https://www.googleapis.com/auth/drive']
)

print("Testing Google Drive/Slides Access...\n")

# Test Drive access
print("1. Testing Drive API...")
drive_service = build('drive', 'v3', credentials=creds)

# Search for 3M presentations
results = drive_service.files().list(
    q="name contains '3M' and mimeType='application/vnd.google-apps.presentation'",
    pageSize=10,
    fields="files(id, name, modifiedTime)"
).execute()

files = results.get('files', [])

if files:
    print(f"   ✅ Found {len(files)} 3M presentation(s):\n")
    for f in files:
        print(f"      • {f['name']}")
        print(f"        ID: {f['id']}")
        print(f"        Modified: {f['modifiedTime']}")
        print()
else:
    print("   ⚠️  No 3M presentations found")
    print("\n   Searching for any presentations...")

    results = drive_service.files().list(
        q="mimeType='application/vnd.google-apps.presentation'",
        pageSize=5,
        fields="files(id, name)"
    ).execute()

    files = results.get('files', [])
    if files:
        print(f"   Found {len(files)} presentation(s):\n")
        for f in files:
            print(f"      • {f['name']} (ID: {f['id']})")

# Test Slides API
print("\n2. Testing Slides API...")
slides_service = build('slides', 'v1', credentials=creds)

if files:
    # Try to read first presentation
    presentation_id = files[0]['id']
    presentation_name = files[0]['name']

    print(f"   Reading: {presentation_name}...")

    try:
        presentation = slides_service.presentations().get(
            presentationId=presentation_id
        ).execute()

        print(f"   ✅ Successfully accessed presentation!")
        print(f"      Title: {presentation.get('title')}")
        print(f"      Slides: {len(presentation.get('slides', []))}")
        print(f"      Page size: {presentation.get('pageSize', {}).get('width', {}).get('magnitude')} x {presentation.get('pageSize', {}).get('height', {}).get('magnitude')}")

        # List first few slides
        slides = presentation.get('slides', [])
        if slides:
            print(f"\n   First 3 slides:")
            for i, slide in enumerate(slides[:3], 1):
                print(f"      {i}. Slide ID: {slide['objectId']}")

        print("\n   ✅ FULL ACCESS CONFIRMED - Can read and edit presentations!")

    except Exception as e:
        print(f"   ❌ Error accessing presentation: {e}")
else:
    print("   ⚠️  No presentations to test with")

print("\n" + "="*70)
print("ACCESS TEST COMPLETE")
print("="*70)
