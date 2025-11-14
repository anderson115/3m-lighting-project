#!/usr/bin/env python3
"""
Authenticate with YouTube Data API v3 using Google OAuth.
Run this first to get YouTube access token.
"""

import json
import pickle
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials

SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']

def authenticate():
    """Authenticate and save YouTube token."""
    creds_file = Path(__file__).parent / 'google_credentials.json'
    token_file = Path(__file__).parent / 'youtube_token.pickle'

    # Load credentials
    with open(creds_file, 'r') as f:
        cred_data = json.load(f)

    # Create OAuth client config
    client_config = {
        "installed": cred_data["installed"]
    }

    # Run OAuth flow
    flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
    creds = flow.run_local_server(port=0)

    # Save token
    with open(token_file, 'wb') as token:
        pickle.dump(creds, token)

    print(f"\n✓ Authentication successful!")
    print(f"✓ Token saved to: {token_file}")
    print(f"\nYou can now run: python3 collect_3m_claw_youtube_google.py")

if __name__ == "__main__":
    authenticate()
