#!/usr/bin/env python3
"""Add Methods infographic slide to presentation"""

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
    scopes=['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/presentations']
)

slides_service = build('slides', 'v1', credentials=creds)

PRESENTATION_ID = '1opG3t90RNV-QvNl57mSThaXTa_7rarAy6thUsJ2h8eM'

print("Reading current presentation structure...")

# Get presentation
presentation = slides_service.presentations().get(
    presentationId=PRESENTATION_ID
).execute()

print(f"Title: {presentation['title']}")
print(f"Current slides: {len(presentation['slides'])}")

# Create new slide at position 3 (index 2)
requests = [
    {
        'createSlide': {
            'insertionIndex': 2,
            'slideLayoutReference': {
                'predefinedLayout': 'BLANK'
            }
        }
    }
]

result = slides_service.presentations().batchUpdate(
    presentationId=PRESENTATION_ID,
    body={'requests': requests}
).execute()

new_slide_id = result['replies'][0]['createSlide']['objectId']
print(f"\n✓ Created new slide at position 3")
print(f"  Slide ID: {new_slide_id}")

# Now add content - create visual infographic
# Page dimensions (standard Google Slides)
PAGE_WIDTH = 9144000  # 10 inches in EMU
PAGE_HEIGHT = 5143500  # 5.625 inches in EMU

def pt_to_emu(pt):
    """Convert points to EMU (English Metric Units)"""
    return int(pt * 12700)

# Define colors
BLUE = {'red': 0.26, 'green': 0.52, 'blue': 0.96}  # #4285F4
GREEN = {'red': 0.13, 'green': 0.73, 'blue': 0.33}  # #22BB55
ORANGE = {'red': 0.96, 'green': 0.56, 'blue': 0.26}  # #F58F42
PURPLE = {'red': 0.61, 'green': 0.35, 'blue': 0.71}  # #9B59B5
GRAY = {'red': 0.4, 'green': 0.4, 'blue': 0.4}
WHITE = {'red': 1.0, 'green': 1.0, 'blue': 1.0}
DARK = {'red': 0.2, 'green': 0.2, 'blue': 0.2}

content_requests = []

# Title
content_requests.append({
    'createShape': {
        'objectId': f'{new_slide_id}_title',
        'shapeType': 'TEXT_BOX',
        'elementProperties': {
            'pageObjectId': new_slide_id,
            'size': {
                'width': {'magnitude': PAGE_WIDTH - pt_to_emu(100), 'unit': 'EMU'},
                'height': {'magnitude': pt_to_emu(80), 'unit': 'EMU'}
            },
            'transform': {
                'scaleX': 1,
                'scaleY': 1,
                'translateX': pt_to_emu(50),
                'translateY': pt_to_emu(30),
                'unit': 'EMU'
            }
        }
    }
})

content_requests.append({
    'insertText': {
        'objectId': f'{new_slide_id}_title',
        'text': 'Methodology'
    }
})

content_requests.append({
    'updateTextStyle': {
        'objectId': f'{new_slide_id}_title',
        'style': {
            'bold': True,
            'fontSize': {'magnitude': 44, 'unit': 'PT'},
            'foregroundColor': {'opaqueColor': {'rgbColor': DARK}}
        },
        'fields': 'bold,fontSize,foregroundColor'
    }
})

# Data Source Box (Left)
y_start = 120
box_width = 220
box_height = 100
spacing = 20

content_requests.append({
    'createShape': {
        'objectId': f'{new_slide_id}_source_box',
        'shapeType': 'ROUND_RECTANGLE',
        'elementProperties': {
            'pageObjectId': new_slide_id,
            'size': {
                'width': {'magnitude': pt_to_emu(box_width), 'unit': 'EMU'},
                'height': {'magnitude': pt_to_emu(box_height), 'unit': 'EMU'}
            },
            'transform': {
                'scaleX': 1,
                'scaleY': 1,
                'translateX': pt_to_emu(50),
                'translateY': pt_to_emu(y_start),
                'unit': 'EMU'
            }
        }
    }
})

content_requests.append({
    'updateShapeProperties': {
        'objectId': f'{new_slide_id}_source_box',
        'shapeProperties': {
            'shapeBackgroundFill': {
                'solidFill': {'color': {'rgbColor': BLUE}}
            }
        },
        'fields': 'shapeBackgroundFill'
    }
})

content_requests.append({
    'createShape': {
        'objectId': f'{new_slide_id}_source_text',
        'shapeType': 'TEXT_BOX',
        'elementProperties': {
            'pageObjectId': new_slide_id,
            'size': {
                'width': {'magnitude': pt_to_emu(box_width - 20), 'unit': 'EMU'},
                'height': {'magnitude': pt_to_emu(box_height - 20), 'unit': 'EMU'}
            },
            'transform': {
                'scaleX': 1,
                'scaleY': 1,
                'translateX': pt_to_emu(60),
                'translateY': pt_to_emu(y_start + 10),
                'unit': 'EMU'
            }
        }
    }
})

content_requests.append({
    'insertText': {
        'objectId': f'{new_slide_id}_source_text',
        'text': 'DATA SOURCE\n\nTikTok Videos\n(Apify API)\n\n189 videos'
    }
})

content_requests.append({
    'updateTextStyle': {
        'objectId': f'{new_slide_id}_source_text',
        'style': {
            'bold': True,
            'fontSize': {'magnitude': 18, 'unit': 'PT'},
            'foregroundColor': {'opaqueColor': {'rgbColor': WHITE}}
        },
        'fields': 'bold,fontSize,foregroundColor'
    }
})

content_requests.append({
    'updateParagraphStyle': {
        'objectId': f'{new_slide_id}_source_text',
        'style': {
            'alignment': 'CENTER'
        },
        'fields': 'alignment'
    }
})

# Arrow 1
arrow_x = 50 + box_width + spacing
content_requests.append({
    'createShape': {
        'objectId': f'{new_slide_id}_arrow1',
        'shapeType': 'RIGHT_ARROW',
        'elementProperties': {
            'pageObjectId': new_slide_id,
            'size': {
                'width': {'magnitude': pt_to_emu(60), 'unit': 'EMU'},
                'height': {'magnitude': pt_to_emu(30), 'unit': 'EMU'}
            },
            'transform': {
                'scaleX': 1,
                'scaleY': 1,
                'translateX': pt_to_emu(arrow_x),
                'translateY': pt_to_emu(y_start + 35),
                'unit': 'EMU'
            }
        }
    }
})

content_requests.append({
    'updateShapeProperties': {
        'objectId': f'{new_slide_id}_arrow1',
        'shapeProperties': {
            'shapeBackgroundFill': {
                'solidFill': {'color': {'rgbColor': GRAY}}
            }
        },
        'fields': 'shapeBackgroundFill'
    }
})

# Processing Pipeline Box (Center)
pipeline_x = arrow_x + 60 + spacing
content_requests.append({
    'createShape': {
        'objectId': f'{new_slide_id}_pipeline_box',
        'shapeType': 'ROUND_RECTANGLE',
        'elementProperties': {
            'pageObjectId': new_slide_id,
            'size': {
                'width': {'magnitude': pt_to_emu(260), 'unit': 'EMU'},
                'height': {'magnitude': pt_to_emu(box_height), 'unit': 'EMU'}
            },
            'transform': {
                'scaleX': 1,
                'scaleY': 1,
                'translateX': pt_to_emu(pipeline_x),
                'translateY': pt_to_emu(y_start),
                'unit': 'EMU'
            }
        }
    }
})

content_requests.append({
    'updateShapeProperties': {
        'objectId': f'{new_slide_id}_pipeline_box',
        'shapeProperties': {
            'shapeBackgroundFill': {
                'solidFill': {'color': {'rgbColor': GREEN}}
            }
        },
        'fields': 'shapeBackgroundFill'
    }
})

content_requests.append({
    'createShape': {
        'objectId': f'{new_slide_id}_pipeline_text',
        'shapeType': 'TEXT_BOX',
        'elementProperties': {
            'pageObjectId': new_slide_id,
            'size': {
                'width': {'magnitude': pt_to_emu(240), 'unit': 'EMU'},
                'height': {'magnitude': pt_to_emu(box_height - 20), 'unit': 'EMU'}
            },
            'transform': {
                'scaleX': 1,
                'scaleY': 1,
                'translateX': pt_to_emu(pipeline_x + 10),
                'translateY': pt_to_emu(y_start + 10),
                'unit': 'EMU'
            }
        }
    }
})

content_requests.append({
    'insertText': {
        'objectId': f'{new_slide_id}_pipeline_text',
        'text': 'AI PROCESSING\n\n→ Transcription (Whisper)\n→ Visual Analysis (GPT-4)\n→ Audio Features (Librosa)\n→ Emotion (Claude)'
    }
})

content_requests.append({
    'updateTextStyle': {
        'objectId': f'{new_slide_id}_pipeline_text',
        'style': {
            'bold': True,
            'fontSize': {'magnitude': 18, 'unit': 'PT'},
            'foregroundColor': {'opaqueColor': {'rgbColor': WHITE}}
        },
        'fields': 'bold,fontSize,foregroundColor'
    }
})

content_requests.append({
    'updateParagraphStyle': {
        'objectId': f'{new_slide_id}_pipeline_text',
        'style': {
            'alignment': 'CENTER'
        },
        'fields': 'alignment'
    }
})

# Arrow 2
arrow2_x = pipeline_x + 260 + spacing
content_requests.append({
    'createShape': {
        'objectId': f'{new_slide_id}_arrow2',
        'shapeType': 'RIGHT_ARROW',
        'elementProperties': {
            'pageObjectId': new_slide_id,
            'size': {
                'width': {'magnitude': pt_to_emu(60), 'unit': 'EMU'},
                'height': {'magnitude': pt_to_emu(30), 'unit': 'EMU'}
            },
            'transform': {
                'scaleX': 1,
                'scaleY': 1,
                'translateX': pt_to_emu(arrow2_x),
                'translateY': pt_to_emu(y_start + 35),
                'unit': 'EMU'
            }
        }
    }
})

content_requests.append({
    'updateShapeProperties': {
        'objectId': f'{new_slide_id}_arrow2',
        'shapeProperties': {
            'shapeBackgroundFill': {
                'solidFill': {'color': {'rgbColor': GRAY}}
            }
        },
        'fields': 'shapeBackgroundFill'
    }
})

# Output Box (Right)
output_x = arrow2_x + 60 + spacing
content_requests.append({
    'createShape': {
        'objectId': f'{new_slide_id}_output_box',
        'shapeType': 'ROUND_RECTANGLE',
        'elementProperties': {
            'pageObjectId': new_slide_id,
            'size': {
                'width': {'magnitude': pt_to_emu(box_width), 'unit': 'EMU'},
                'height': {'magnitude': pt_to_emu(box_height), 'unit': 'EMU'}
            },
            'transform': {
                'scaleX': 1,
                'scaleY': 1,
                'translateX': pt_to_emu(output_x),
                'translateY': pt_to_emu(y_start),
                'unit': 'EMU'
            }
        }
    }
})

content_requests.append({
    'updateShapeProperties': {
        'objectId': f'{new_slide_id}_output_box',
        'shapeProperties': {
            'shapeBackgroundFill': {
                'solidFill': {'color': {'rgbColor': ORANGE}}
            }
        },
        'fields': 'shapeBackgroundFill'
    }
})

content_requests.append({
    'createShape': {
        'objectId': f'{new_slide_id}_output_text',
        'shapeType': 'TEXT_BOX',
        'elementProperties': {
            'pageObjectId': new_slide_id,
            'size': {
                'width': {'magnitude': pt_to_emu(box_width - 20), 'unit': 'EMU'},
                'height': {'magnitude': pt_to_emu(box_height - 20), 'unit': 'EMU'}
            },
            'transform': {
                'scaleX': 1,
                'scaleY': 1,
                'translateX': pt_to_emu(output_x + 10),
                'translateY': pt_to_emu(y_start + 10),
                'unit': 'EMU'
            }
        }
    }
})

content_requests.append({
    'insertText': {
        'objectId': f'{new_slide_id}_output_text',
        'text': 'INSIGHTS\n\n• Pain Points\n• Emotions\n• Buying Triggers\n• Content Themes'
    }
})

content_requests.append({
    'updateTextStyle': {
        'objectId': f'{new_slide_id}_output_text',
        'style': {
            'bold': True,
            'fontSize': {'magnitude': 18, 'unit': 'PT'},
            'foregroundColor': {'opaqueColor': {'rgbColor': WHITE}}
        },
        'fields': 'bold,fontSize,foregroundColor'
    }
})

content_requests.append({
    'updateParagraphStyle': {
        'objectId': f'{new_slide_id}_output_text',
        'style': {
            'alignment': 'CENTER'
        },
        'fields': 'alignment'
    }
})

# Sample Size note at bottom
content_requests.append({
    'createShape': {
        'objectId': f'{new_slide_id}_note',
        'shapeType': 'TEXT_BOX',
        'elementProperties': {
            'pageObjectId': new_slide_id,
            'size': {
                'width': {'magnitude': PAGE_WIDTH - pt_to_emu(100), 'unit': 'EMU'},
                'height': {'magnitude': pt_to_emu(50), 'unit': 'EMU'}
            },
            'transform': {
                'scaleX': 1,
                'scaleY': 1,
                'translateX': pt_to_emu(50),
                'translateY': pt_to_emu(y_start + box_height + 30),
                'unit': 'EMU'
            }
        }
    }
})

content_requests.append({
    'insertText': {
        'objectId': f'{new_slide_id}_note',
        'text': 'n=153 videos | Garage Organizers category | TikTok platform | October 2025'
    }
})

content_requests.append({
    'updateTextStyle': {
        'objectId': f'{new_slide_id}_note',
        'style': {
            'fontSize': {'magnitude': 18, 'unit': 'PT'},
            'foregroundColor': {'opaqueColor': {'rgbColor': GRAY}},
            'italic': True
        },
        'fields': 'fontSize,foregroundColor,italic'
    }
})

content_requests.append({
    'updateParagraphStyle': {
        'objectId': f'{new_slide_id}_note',
        'style': {
            'alignment': 'CENTER'
        },
        'fields': 'alignment'
    }
})

# Execute all content requests
print(f"\nAdding infographic content...")
slides_service.presentations().batchUpdate(
    presentationId=PRESENTATION_ID,
    body={'requests': content_requests}
).execute()

print("✓ Methods infographic slide created successfully!")
print(f"\n✓ Link: https://docs.google.com/presentation/d/{PRESENTATION_ID}/edit")
print(f"\n✓ CONFIRMATION: Successfully edited presentation and added visual Methods slide at position 3")
