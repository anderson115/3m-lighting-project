#!/usr/bin/env python3
"""Create Appendix slide with data sources and methodology"""

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

# Design System
DARK_BG = {'red': 0.109, 'green': 0.125, 'blue': 0.153}  # #1C2027
ORANGE = {'red': 1.0, 'green': 0.42, 'blue': 0.21}  # #FF6B35
WHITE = {'red': 1.0, 'green': 1.0, 'blue': 1.0}
LIGHT_GRAY = {'red': 0.95, 'green': 0.95, 'blue': 0.96}  # #F2F2F5
GRAY_TEXT = {'red': 0.4, 'green': 0.4, 'blue': 0.4}

print("="*80)
print("CREATING APPENDIX SLIDE - DATA SOURCES & METHODOLOGY")
print("="*80)

presentation = slides_service.presentations().get(presentationId=PRESENTATION_ID).execute()
current_slide_count = len(presentation['slides'])

# ==============================================================================
# APPENDIX SLIDE
# ==============================================================================

slide_id = 'appendix_methodology'
requests = []

requests.append({
    'createSlide': {
        'objectId': slide_id,
        'insertionIndex': current_slide_count,
        'slideLayoutReference': {'predefinedLayout': 'BLANK'}
    }
})

requests.append({
    'updatePageProperties': {
        'objectId': slide_id,
        'pageProperties': {
            'pageBackgroundFill': {'solidFill': {'color': {'rgbColor': DARK_BG}}}
        },
        'fields': 'pageBackgroundFill'
    }
})

slides_service.presentations().batchUpdate(
    presentationId=PRESENTATION_ID,
    body={'requests': requests}
).execute()

print(f"\n✓ Created slide: {slide_id}")

# Add content
requests = []

# Title
title_id = f'{slide_id}_title'
requests.append({
    'createShape': {
        'objectId': title_id,
        'shapeType': 'TEXT_BOX',
        'elementProperties': {
            'pageObjectId': slide_id,
            'size': {'width': {'magnitude': 550, 'unit': 'PT'}, 'height': {'magnitude': 70, 'unit': 'PT'}},
            'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': 50, 'translateY': 40, 'unit': 'PT'}
        }
    }
})

requests.append({'insertText': {'objectId': title_id, 'text': 'APPENDIX: METHODOLOGY', 'insertionIndex': 0}})
requests.append({
    'updateTextStyle': {
        'objectId': title_id,
        'style': {'bold': True, 'fontSize': {'magnitude': 32, 'unit': 'PT'}, 'foregroundColor': {'opaqueColor': {'rgbColor': WHITE}}},
        'fields': 'bold,fontSize,foregroundColor'
    }
})

# Orange divider
divider_id = f'{slide_id}_divider'
requests.append({
    'createLine': {
        'objectId': divider_id,
        'lineCategory': 'STRAIGHT',
        'elementProperties': {
            'pageObjectId': slide_id,
            'size': {'width': {'magnitude': 670, 'unit': 'PT'}, 'height': {'magnitude': 0, 'unit': 'PT'}},
            'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': 50, 'translateY': 115, 'unit': 'PT'}
        }
    }
})

requests.append({
    'updateLineProperties': {
        'objectId': divider_id,
        'lineProperties': {
            'lineFill': {'solidFill': {'color': {'rgbColor': ORANGE}}},
            'weight': {'magnitude': 2, 'unit': 'PT'}
        },
        'fields': 'lineFill,weight'
    }
})

# Content sections
sections = [
    {
        'title': 'DATA SOURCES',
        'content': '• 3,991 products across 7 retailers (Walmart, Home Depot, Amazon, Target, Lowes, Menards, Ace Hardware)\n• Price, ratings, reviews, brand, and product attributes collected via web scraping\n• Data collected: Q4 2024',
        'y': 145
    },
    {
        'title': 'WEIGHTING METHODOLOGY',
        'content': '• Retailer weights applied to achieve equal 14.3% representation per channel\n• Category weights: Hooks & Hangers reduced from 59% to 27% (0.69x multiplier)\n• Combined weight = retailer_weight × category_weight for each product',
        'y': 235
    },
    {
        'title': 'CATEGORY TAXONOMY',
        'content': '• MECE framework: Hooks & Hangers, Shelving, Rails & Tracks, Bins & Baskets, Specialty Holders, Cabinets\n• 676 products reclassified from generic categories using rule-based logic\n• Subcategories inferred from product names/descriptions (85% confidence)',
        'y': 325
    },
    {
        'title': 'ANALYSIS TECHNIQUES',
        'content': '• Quality gap score = avg_price / (avg_rating²) to identify price-satisfaction mismatches\n• Market saturation = weighted_products / brand_count to measure competition\n• Retailer dominance = share % by weighted product count within each category',
        'y': 415
    }
]

for i, section in enumerate(sections):
    # Section title
    section_title_id = f'{slide_id}_section{i}_title'
    requests.append({
        'createShape': {
            'objectId': section_title_id,
            'shapeType': 'TEXT_BOX',
            'elementProperties': {
                'pageObjectId': slide_id,
                'size': {'width': {'magnitude': 670, 'unit': 'PT'}, 'height': {'magnitude': 25, 'unit': 'PT'}},
                'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': 50, 'translateY': section['y'], 'unit': 'PT'}
            }
        }
    })

    requests.append({'insertText': {'objectId': section_title_id, 'text': section['title'], 'insertionIndex': 0}})
    requests.append({
        'updateTextStyle': {
            'objectId': section_title_id,
            'style': {'bold': True, 'fontSize': {'magnitude': 18, 'unit': 'PT'}, 'foregroundColor': {'opaqueColor': {'rgbColor': ORANGE}}},
            'fields': 'bold,fontSize,foregroundColor'
        }
    })

    # Section content
    section_content_id = f'{slide_id}_section{i}_content'
    requests.append({
        'createShape': {
            'objectId': section_content_id,
            'shapeType': 'TEXT_BOX',
            'elementProperties': {
                'pageObjectId': slide_id,
                'size': {'width': {'magnitude': 670, 'unit': 'PT'}, 'height': {'magnitude': 75, 'unit': 'PT'}},
                'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': 50, 'translateY': section['y'] + 25, 'unit': 'PT'}
            }
        }
    })

    requests.append({'insertText': {'objectId': section_content_id, 'text': section['content'], 'insertionIndex': 0}})
    requests.append({
        'updateTextStyle': {
            'objectId': section_content_id,
            'style': {'fontSize': {'magnitude': 14, 'unit': 'PT'}, 'foregroundColor': {'opaqueColor': {'rgbColor': WHITE}}},
            'fields': 'fontSize,foregroundColor'
        }
    })

    requests.append({
        'updateParagraphStyle': {
            'objectId': section_content_id,
            'style': {'lineSpacing': 120},
            'fields': 'lineSpacing'
        }
    })

slides_service.presentations().batchUpdate(
    presentationId=PRESENTATION_ID,
    body={'requests': requests}
).execute()

print("✓ Appendix slide complete")

print(f"\n{'='*80}")
print("✓ APPENDIX SLIDE CREATED")
print(f"{'='*80}")
print(f"\nView at: https://docs.google.com/presentation/d/{PRESENTATION_ID}")
