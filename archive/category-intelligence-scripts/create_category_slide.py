#!/usr/bin/env python3
"""Create category summary slide matching Offbrain design system"""

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

# Load analysis data
with open('weighted_category_summary.json') as f:
    data = json.load(f)

print("="*80)
print("CREATING CATEGORY OVERVIEW SLIDE")
print("="*80)

# Get presentation to find where to insert
presentation = slides_service.presentations().get(
    presentationId=PRESENTATION_ID
).execute()

print(f"\nPresentation: {presentation['title']}")
print(f"Total slides: {len(presentation['slides'])}")

# Offbrain Design System Colors
DARK_BG = {'red': 0.18, 'green': 0.20, 'blue': 0.25}  # #2E3340
ORANGE = {'red': 1.0, 'green': 0.42, 'blue': 0.22}  # #FF6B38
CYAN = {'red': 0.0, 'green': 0.80, 'blue': 0.95}  # #00CCF2
LIGHT_GRAY = {'red': 0.95, 'green': 0.95, 'blue': 0.95}  # #F2F2F2
WHITE = {'red': 1.0, 'green': 1.0, 'blue': 1.0}
DARK_TEXT = {'red': 0.18, 'green': 0.20, 'blue': 0.25}

# Create slide
slide_id = f'category_overview_{id(data)}'
requests = []

# 1. Create slide
requests.append({
    'createSlide': {
        'objectId': slide_id,
        'insertionIndex': len(presentation['slides']),
        'slideLayoutReference': {
            'predefinedLayout': 'BLANK'
        }
    }
})

# 2. Set dark background
requests.append({
    'updatePageProperties': {
        'objectId': slide_id,
        'pageProperties': {
            'pageBackgroundFill': {
                'solidFill': {
                    'color': {
                        'rgbColor': DARK_BG
                    }
                }
            }
        },
        'fields': 'pageBackgroundFill'
    }
})

# Execute initial creation
slides_service.presentations().batchUpdate(
    presentationId=PRESENTATION_ID,
    body={'requests': requests}
).execute()

print(f"\n✓ Created slide: {slide_id}")

# Now add content
requests = []

# 3. Title (top left, white text)
title_id = f'{slide_id}_title'
requests.append({
    'createShape': {
        'objectId': title_id,
        'shapeType': 'TEXT_BOX',
        'elementProperties': {
            'pageObjectId': slide_id,
            'size': {
                'width': {'magnitude': 600, 'unit': 'PT'},
                'height': {'magnitude': 60, 'unit': 'PT'}
            },
            'transform': {
                'scaleX': 1,
                'scaleY': 1,
                'translateX': 50,
                'translateY': 35,
                'unit': 'PT'
            }
        }
    }
})

requests.append({
    'insertText': {
        'objectId': title_id,
        'text': 'CATEGORY OVERVIEW',
        'insertionIndex': 0
    }
})

requests.append({
    'updateTextStyle': {
        'objectId': title_id,
        'style': {
            'bold': True,
            'fontSize': {'magnitude': 36, 'unit': 'PT'},
            'foregroundColor': {'opaqueColor': {'rgbColor': WHITE}}
        },
        'fields': 'bold,fontSize,foregroundColor'
    }
})

# 4. Page number (top right, orange circle)
page_num_id = f'{slide_id}_page_num'
requests.append({
    'createShape': {
        'objectId': page_num_id,
        'shapeType': 'ELLIPSE',
        'elementProperties': {
            'pageObjectId': slide_id,
            'size': {
                'width': {'magnitude': 45, 'unit': 'PT'},
                'height': {'magnitude': 45, 'unit': 'PT'}
            },
            'transform': {
                'scaleX': 1,
                'scaleY': 1,
                'translateX': 675,
                'translateY': 25,
                'unit': 'PT'
            }
        }
    }
})

requests.append({
    'updateShapeProperties': {
        'objectId': page_num_id,
        'shapeProperties': {
            'shapeBackgroundFill': {
                'solidFill': {
                    'color': {'rgbColor': ORANGE}
                }
            }
        },
        'fields': 'shapeBackgroundFill'
    }
})

requests.append({
    'insertText': {
        'objectId': page_num_id,
        'text': str(len(presentation['slides']) + 1),
        'insertionIndex': 0
    }
})

requests.append({
    'updateTextStyle': {
        'objectId': page_num_id,
        'style': {
            'bold': True,
            'fontSize': {'magnitude': 24, 'unit': 'PT'},
            'foregroundColor': {'opaqueColor': {'rgbColor': WHITE}}
        },
        'fields': 'bold,fontSize,foregroundColor',
        'textRange': {'type': 'ALL'}
    }
})

requests.append({
    'updateParagraphStyle': {
        'objectId': page_num_id,
        'style': {
            'alignment': 'CENTER'
        },
        'fields': 'alignment'
    }
})

# 5. Orange divider line under title
divider_id = f'{slide_id}_divider'
requests.append({
    'createLine': {
        'objectId': divider_id,
        'lineCategory': 'STRAIGHT',
        'elementProperties': {
            'pageObjectId': slide_id,
            'size': {
                'width': {'magnitude': 670, 'unit': 'PT'},
                'height': {'magnitude': 0, 'unit': 'PT'}
            },
            'transform': {
                'scaleX': 1,
                'scaleY': 1,
                'translateX': 50,
                'translateY': 100,
                'unit': 'PT'
            }
        }
    }
})

requests.append({
    'updateLineProperties': {
        'objectId': divider_id,
        'lineProperties': {
            'lineFill': {
                'solidFill': {
                    'color': {'rgbColor': ORANGE}
                }
            },
            'weight': {'magnitude': 3, 'unit': 'PT'}
        },
        'fields': 'lineFill,weight'
    }
})

# Get top categories for content boxes
categories = sorted(data['categories'], key=lambda x: x['weighted_count'], reverse=True)[:3]

# Define content box layout (3 boxes in a row)
box_colors = [ORANGE, CYAN, {'red': 0.5, 'green': 0.5, 'blue': 0.5}]  # Orange, Cyan, Gray
box_y = 130
box_width = 210
box_height = 280
box_spacing = 15

for i, (category, color) in enumerate(zip(categories, box_colors)):
    box_x = 50 + (i * (box_width + box_spacing))

    # Background box
    bg_box_id = f'{slide_id}_box_{i}_bg'
    requests.append({
        'createShape': {
            'objectId': bg_box_id,
            'shapeType': 'RECTANGLE',
            'elementProperties': {
                'pageObjectId': slide_id,
                'size': {
                    'width': {'magnitude': box_width, 'unit': 'PT'},
                    'height': {'magnitude': box_height, 'unit': 'PT'}
                },
                'transform': {
                    'scaleX': 1,
                    'scaleY': 1,
                    'translateX': box_x,
                    'translateY': box_y,
                    'unit': 'PT'
                }
            }
        }
    })

    requests.append({
        'updateShapeProperties': {
            'objectId': bg_box_id,
            'shapeProperties': {
                'shapeBackgroundFill': {
                    'solidFill': {
                        'color': {'rgbColor': LIGHT_GRAY}
                    }
                },
                'outline': {
                    'propertyState': 'NOT_RENDERED'
                }
            },
            'fields': 'shapeBackgroundFill,outline'
        }
    })

    # Thick colored left border
    border_id = f'{slide_id}_box_{i}_border'
    requests.append({
        'createShape': {
            'objectId': border_id,
            'shapeType': 'RECTANGLE',
            'elementProperties': {
                'pageObjectId': slide_id,
                'size': {
                    'width': {'magnitude': 8, 'unit': 'PT'},
                    'height': {'magnitude': box_height, 'unit': 'PT'}
                },
                'transform': {
                    'scaleX': 1,
                    'scaleY': 1,
                    'translateX': box_x,
                    'translateY': box_y,
                    'unit': 'PT'
                }
            }
        }
    })

    requests.append({
        'updateShapeProperties': {
            'objectId': border_id,
            'shapeProperties': {
                'shapeBackgroundFill': {
                    'solidFill': {
                        'color': {'rgbColor': color}
                    }
                },
                'outline': {'propertyState': 'NOT_RENDERED'}
            },
            'fields': 'shapeBackgroundFill,outline'
        }
    })

    # Category name (header)
    header_id = f'{slide_id}_box_{i}_header'
    requests.append({
        'createShape': {
            'objectId': header_id,
            'shapeType': 'TEXT_BOX',
            'elementProperties': {
                'pageObjectId': slide_id,
                'size': {
                    'width': {'magnitude': box_width - 25, 'unit': 'PT'},
                    'height': {'magnitude': 50, 'unit': 'PT'}
                },
                'transform': {
                    'scaleX': 1,
                    'scaleY': 1,
                    'translateX': box_x + 15,
                    'translateY': box_y + 15,
                    'unit': 'PT'
                }
            }
        }
    })

    cat_name = category['category'].replace(' & ', '\n& ')
    requests.append({
        'insertText': {
            'objectId': header_id,
            'text': cat_name,
            'insertionIndex': 0
        }
    })

    requests.append({
        'updateTextStyle': {
            'objectId': header_id,
            'style': {
                'bold': True,
                'fontSize': {'magnitude': 20, 'unit': 'PT'},
                'foregroundColor': {'opaqueColor': {'rgbColor': color}}
            },
            'fields': 'bold,fontSize,foregroundColor',
            'textRange': {'type': 'ALL'}
        }
    })

    # Metrics content
    metrics_text = f"""

{int(category['weighted_count']):,}
PRODUCTS

${category['avg_price']:.0f}
AVG PRICE

{category['avg_rating']:.1f}★
RATING

{category['brand_count']}
BRANDS"""

    metrics_id = f'{slide_id}_box_{i}_metrics'
    requests.append({
        'createShape': {
            'objectId': metrics_id,
            'shapeType': 'TEXT_BOX',
            'elementProperties': {
                'pageObjectId': slide_id,
                'size': {
                    'width': {'magnitude': box_width - 25, 'unit': 'PT'},
                    'height': {'magnitude': 210, 'unit': 'PT'}
                },
                'transform': {
                    'scaleX': 1,
                    'scaleY': 1,
                    'translateX': box_x + 15,
                    'translateY': box_y + 65,
                    'unit': 'PT'
                }
            }
        }
    })

    requests.append({
        'insertText': {
            'objectId': metrics_id,
            'text': metrics_text,
            'insertionIndex': 0
        }
    })

    requests.append({
        'updateTextStyle': {
            'objectId': metrics_id,
            'style': {
                'fontSize': {'magnitude': 18, 'unit': 'PT'},
                'foregroundColor': {'opaqueColor': {'rgbColor': DARK_TEXT}}
            },
            'fields': 'fontSize,foregroundColor',
            'textRange': {'type': 'ALL'}
        }
    })

    requests.append({
        'updateParagraphStyle': {
            'objectId': metrics_id,
            'style': {
                'alignment': 'CENTER',
                'lineSpacing': 110
            },
            'fields': 'alignment,lineSpacing'
        }
    })

# 6. Citation at bottom
citation_id = f'{slide_id}_citation'
requests.append({
    'createShape': {
        'objectId': citation_id,
        'shapeType': 'TEXT_BOX',
        'elementProperties': {
            'pageObjectId': slide_id,
            'size': {
                'width': {'magnitude': 670, 'unit': 'PT'},
                'height': {'magnitude': 30, 'unit': 'PT'}
            },
            'transform': {
                'scaleX': 1,
                'scaleY': 1,
                'translateX': 50,
                'translateY': 505,
                'unit': 'PT'
            }
        }
    }
})

requests.append({
    'insertText': {
        'objectId': citation_id,
        'text': f'[1] Based on weighted analysis of {len(data["categories"])} product categories | Bias-corrected for retailer distribution',
        'insertionIndex': 0
    }
})

requests.append({
    'updateTextStyle': {
        'objectId': citation_id,
        'style': {
            'italic': True,
            'fontSize': {'magnitude': 10, 'unit': 'PT'},
            'foregroundColor': {'opaqueColor': {'rgbColor': {'red': 0.7, 'green': 0.7, 'blue': 0.7}}}
        },
        'fields': 'italic,fontSize,foregroundColor'
    }
})

# Execute all content requests
slides_service.presentations().batchUpdate(
    presentationId=PRESENTATION_ID,
    body={'requests': requests}
).execute()

print(f"\n✓ Added content to slide")
print(f"  - Title: CATEGORY OVERVIEW")
print(f"  - Page number: {len(presentation['slides']) + 1}")
print(f"  - Content boxes: 3 (top categories)")
print(f"  - Design: Dark background, thick colored borders, orange accents")

print(f"\n{'='*80}")
print(f"✓ SLIDE CREATED SUCCESSFULLY")
print(f"{'='*80}")
print(f"\nView at: https://docs.google.com/presentation/d/{PRESENTATION_ID}")
