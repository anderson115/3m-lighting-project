#!/usr/bin/env python3
"""
Convert HTML slides to Google Slides using Google Slides API
"""

import os
import json
from bs4 import BeautifulSoup
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Scopes for Google Slides API
SCOPES = ['https://www.googleapis.com/auth/presentations', 'https://www.googleapis.com/auth/drive']

def get_credentials():
    """Get Google API credentials"""
    credentials_path = 'credentials.json'

    if not os.path.exists(credentials_path):
        print(f"❌ ERROR: {credentials_path} not found")
        return None

    # Load credentials file
    with open(credentials_path, 'r') as f:
        cred_data = json.load(f)

    # Check if it has tokens already
    if 'tokens' in cred_data:
        token_info = cred_data['tokens']
        creds = Credentials(
            token=token_info.get('access_token'),
            refresh_token=token_info.get('refresh_token'),
            token_uri=token_info.get('token_uri'),
            client_id=token_info.get('client_id'),
            client_secret=token_info.get('client_secret'),
            scopes=token_info.get('scopes', SCOPES)
        )

        # Try to refresh token
        try:
            print("🔄 Refreshing expired token...")
            creds.refresh(Request())
            print("✅ Token refreshed")

            # Update credentials file with new token
            cred_data['tokens']['access_token'] = creds.token
            with open(credentials_path, 'w') as f:
                json.dump(cred_data, f, indent=2)

        except Exception as e:
            print(f"❌ Token refresh failed: {e}")
            print("🔄 Requesting new authorization...")

            # Fall back to re-authorization
            if 'installed' in cred_data:
                flow = InstalledAppFlow.from_client_config(
                    cred_data,
                    SCOPES
                )
                creds = flow.run_local_server(port=0)

                # Save new tokens
                cred_data['tokens'] = {
                    'access_token': creds.token,
                    'refresh_token': creds.refresh_token,
                    'token_uri': creds.token_uri,
                    'client_id': creds.client_id,
                    'client_secret': creds.client_secret,
                    'scopes': creds.scopes
                }
                with open(credentials_path, 'w') as f:
                    json.dump(cred_data, f, indent=2)
                print("✅ New token saved")
            else:
                return None

    else:
        print("❌ No tokens found in credentials file")
        return None

    return creds

def parse_html_slide(html_path):
    """Extract content from HTML slide"""
    with open(html_path, 'r') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')

    # Extract key elements
    headline = soup.find(class_='headline')
    sections = soup.find_all(class_='section')

    data = {
        'headline': headline.get_text(strip=True) if headline else '',
        'sections': [],
        'raw_text': soup.get_text(separator='\n', strip=True)
    }

    for section in sections:
        header = section.find(class_='section-header')
        body = section.find(class_='body-text')

        if header or body:
            section_data = {
                'header': header.get_text(strip=True) if header else '',
                'body': body.get_text(strip=True) if body else ''
            }
            data['sections'].append(section_data)

    return data

def create_presentation(service, title="3M Garage Organization Slides"):
    """Create new Google Slides presentation"""
    presentation = {
        'title': title
    }
    presentation = service.presentations().create(body=presentation).execute()
    print(f'✅ Created presentation: {presentation.get("presentationId")}')
    print(f'   View: https://docs.google.com/presentation/d/{presentation.get("presentationId")}/edit')
    return presentation.get('presentationId')

def add_text_slide(service, presentation_id, slide_data, slide_index):
    """Add slide with text content"""
    requests = []

    # Create blank slide
    slide_id = f'slide_{slide_index}'
    requests.append({
        'createSlide': {
            'objectId': slide_id,
            'slideLayoutReference': {
                'predefinedLayout': 'BLANK'
            }
        }
    })

    # Add title
    if slide_data.get('headline'):
        title_id = f'title_{slide_index}'
        requests.append({
            'createShape': {
                'objectId': title_id,
                'shapeType': 'TEXT_BOX',
                'elementProperties': {
                    'pageObjectId': slide_id,
                    'size': {
                        'height': {'magnitude': 80, 'unit': 'PT'},
                        'width': {'magnitude': 650, 'unit': 'PT'}
                    },
                    'transform': {
                        'scaleX': 1,
                        'scaleY': 1,
                        'translateX': 40,
                        'translateY': 40,
                        'unit': 'PT'
                    }
                }
            }
        })
        requests.append({
            'insertText': {
                'objectId': title_id,
                'text': slide_data['headline']
            }
        })

    # Add body content
    y_position = 140
    for i, section in enumerate(slide_data.get('sections', [])[:3]):  # Max 3 sections
        if section.get('header') or section.get('body'):
            body_id = f'body_{slide_index}_{i}'
            text_content = f"{section.get('header', '')}\n{section.get('body', '')}"

            requests.append({
                'createShape': {
                    'objectId': body_id,
                    'shapeType': 'TEXT_BOX',
                    'elementProperties': {
                        'pageObjectId': slide_id,
                        'size': {
                            'height': {'magnitude': 100, 'unit': 'PT'},
                            'width': {'magnitude': 650, 'unit': 'PT'}
                        },
                        'transform': {
                            'scaleX': 1,
                            'scaleY': 1,
                            'translateX': 40,
                            'translateY': y_position,
                            'unit': 'PT'
                        }
                    }
                }
            })
            requests.append({
                'insertText': {
                    'objectId': body_id,
                    'text': text_content.strip()
                }
            })
            y_position += 120

    # Execute batch update
    if requests:
        body = {'requests': requests}
        response = service.presentations().batchUpdate(
            presentationId=presentation_id,
            body=body
        ).execute()
        print(f'✅ Added slide {slide_index}')
        return response

def main():
    """Main conversion function"""
    print("🚀 HTML to Google Slides Converter")
    print("=" * 60)

    # Get credentials
    creds = get_credentials()
    if not creds:
        return

    # Build service
    try:
        service = build('slides', 'v1', credentials=creds)
        print("✅ Connected to Google Slides API")
    except HttpError as error:
        print(f'❌ API error: {error}')
        return

    # Find HTML slides
    html_files = [
        'slide1_FINAL.html',
        'SLIDE2_DEFAULT.html',
        'SLIDE3_DEFAULT.html',
        'SLIDE4_DEFAULT.html',
        'SLIDE5_DEFAULT.html',
        'SLIDE6_DEFAULT.html'
    ]

    # Create presentation
    presentation_id = create_presentation(service, "3M Garage Organization - Brand Perceptions")

    # Convert each slide
    for i, html_file in enumerate(html_files):
        if os.path.exists(html_file):
            print(f"\n📄 Processing: {html_file}")
            slide_data = parse_html_slide(html_file)
            add_text_slide(service, presentation_id, slide_data, i)
        else:
            print(f"⚠️  Not found: {html_file}")

    print(f"\n" + "=" * 60)
    print(f"✅ CONVERSION COMPLETE")
    print(f"📊 View presentation:")
    print(f"   https://docs.google.com/presentation/d/{presentation_id}/edit")
    print(f"\n💡 Next steps:")
    print(f"   1. Open presentation in Google Slides")
    print(f"   2. File → Download → Microsoft PowerPoint (.pptx)")
    print(f"=" * 60)

if __name__ == '__main__':
    main()
