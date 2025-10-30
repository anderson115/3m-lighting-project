#!/usr/bin/env python3
"""
Upload PowerPoint to Google Drive and convert to Google Slides
"""

import json
import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Load credentials
CREDENTIALS_PATH = '/Users/anderson115/.config/google-drive-credentials.json'
PPTX_PATH = '/Users/anderson115/00-interlink/12-work/3m-lighting-project/Garage_Organizers_Category_Intelligence_FINAL.pptx'
TARGET_FOLDER_NAME = '3M-garage-organizer'

def load_credentials():
    """Load OAuth credentials from file"""
    with open(CREDENTIALS_PATH, 'r') as f:
        creds_data = json.load(f)

    # Extract credentials from nested structure
    installed = creds_data.get('installed', {})
    tokens = creds_data.get('tokens', {})

    # Create credentials object
    creds = Credentials(
        token=tokens.get('access_token'),
        refresh_token=tokens.get('refresh_token'),
        token_uri=installed.get('token_uri', 'https://oauth2.googleapis.com/token'),
        client_id=installed.get('client_id'),
        client_secret=installed.get('client_secret'),
        scopes=['https://www.googleapis.com/auth/drive']
    )

    return creds

def find_folder(service, folder_name):
    """Find folder by name in Google Drive"""
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    results = service.files().list(
        q=query,
        spaces='drive',
        fields='files(id, name)'
    ).execute()

    folders = results.get('files', [])
    return folders[0]['id'] if folders else None

def create_folder(service, folder_name):
    """Create a new folder in Google Drive"""
    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    folder = service.files().create(
        body=file_metadata,
        fields='id'
    ).execute()
    return folder.get('id')

def upload_and_convert_to_slides(service, file_path, folder_id):
    """Upload PowerPoint and convert to Google Slides"""
    file_name = os.path.basename(file_path)

    file_metadata = {
        'name': file_name.replace('.pptx', ''),  # Remove extension for cleaner name
        'mimeType': 'application/vnd.google-apps.presentation',  # Convert to Google Slides
        'parents': [folder_id]
    }

    media = MediaFileUpload(
        file_path,
        mimetype='application/vnd.openxmlformats-officedocument.presentationml.presentation',
        resumable=True
    )

    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id, webViewLink'
    ).execute()

    return file

def main():
    print("Loading credentials...")
    creds = load_credentials()

    print("Building Google Drive service...")
    service = build('drive', 'v3', credentials=creds)

    print(f"Searching for folder '{TARGET_FOLDER_NAME}'...")
    folder_id = find_folder(service, TARGET_FOLDER_NAME)

    if not folder_id:
        print(f"Folder not found. Creating '{TARGET_FOLDER_NAME}'...")
        folder_id = create_folder(service, TARGET_FOLDER_NAME)
        print(f"Created folder with ID: {folder_id}")
    else:
        print(f"Found folder with ID: {folder_id}")

    print(f"\nUploading '{os.path.basename(PPTX_PATH)}' and converting to Google Slides...")
    file = upload_and_convert_to_slides(service, PPTX_PATH, folder_id)

    print("\n" + "="*70)
    print("SUCCESS! File uploaded and converted to Google Slides")
    print("="*70)
    print(f"File ID: {file['id']}")
    print(f"View Link: {file['webViewLink']}")
    print("="*70)

    return file['webViewLink']

if __name__ == '__main__':
    main()
