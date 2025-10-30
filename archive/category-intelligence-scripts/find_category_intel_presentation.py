#!/usr/bin/env python3
"""Find the latest category intelligence presentation"""

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
    token_uri=creds_data['installed']['token_uri'],
    client_id=creds_data['installed']['client_id'],
    client_secret=creds_data['installed']['client_secret'],
    scopes=['https://www.googleapis.com/auth/drive']
)

drive_service = build('drive', 'v3', credentials=creds)

# Search for presentations with various keywords
search_terms = [
    "category intelligence",
    "category intel",
    "3M Lighting",
    "JTBD",
    "Category Growth"
]

print("Searching for category intelligence presentations...\n")

all_presentations = {}

for term in search_terms:
    results = drive_service.files().list(
        q=f"name contains '{term}' and mimeType='application/vnd.google-apps.presentation'",
        pageSize=20,
        fields="files(id, name, modifiedTime, webViewLink, owners)",
        orderBy="modifiedTime desc"
    ).execute()

    files = results.get('files', [])
    for f in files:
        all_presentations[f['id']] = f

# Sort by modified time
sorted_presentations = sorted(
    all_presentations.values(),
    key=lambda x: x['modifiedTime'],
    reverse=True
)

print(f"Found {len(sorted_presentations)} unique presentation(s):\n")
print("="*80)

for i, pres in enumerate(sorted_presentations, 1):
    print(f"\n{i}. {pres['name']}")
    print(f"   Modified: {pres['modifiedTime']}")
    print(f"   Owner: {pres.get('owners', [{}])[0].get('emailAddress', 'Unknown')}")
    print(f"   Link: {pres['webViewLink']}")
    print(f"   ID: {pres['id']}")

print("\n" + "="*80)
print(f"\nMOST RECENT: {sorted_presentations[0]['name']}")
print(f"Link: {sorted_presentations[0]['webViewLink']}")
