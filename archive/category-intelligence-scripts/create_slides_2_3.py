#!/usr/bin/env python3
"""Create slides 2 & 3 matching EXACT design from slide 2 (3 THINGS TO KNOW format)"""

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
CYAN = {'red': 0.0, 'green': 0.8, 'blue': 0.95}  # #00CCF2
BLACK = {'red': 0.0, 'green': 0.0, 'blue': 0.0}
WHITE = {'red': 1.0, 'green': 1.0, 'blue': 1.0}
LIGHT_GRAY = {'red': 0.95, 'green': 0.95, 'blue': 0.96}  # #F2F2F5
GRAY_TEXT = {'red': 0.4, 'green': 0.4, 'blue': 0.4}

print("="*80)
print("CREATING SLIDES 2 & 3 - EXACT MATCH TO SLIDE 2 FORMAT")
print("="*80)

presentation = slides_service.presentations().get(presentationId=PRESENTATION_ID).execute()
current_slide_count = len(presentation['slides'])

# ==============================================================================
# SLIDE 2: QUALITY & MARKET DYNAMICS
# ==============================================================================

slide_id = 'quality_market_dynamics'
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

requests.append({'insertText': {'objectId': title_id, 'text': 'QUALITY & MARKET DYNAMICS', 'insertionIndex': 0}})
requests.append({
    'updateTextStyle': {
        'objectId': title_id,
        'style': {'bold': True, 'fontSize': {'magnitude': 32, 'unit': 'PT'}, 'foregroundColor': {'opaqueColor': {'rgbColor': WHITE}}},
        'fields': 'bold,fontSize,foregroundColor'
    }
})

# Page number circle
page_num_id = f'{slide_id}_pagenum'
requests.append({
    'createShape': {
        'objectId': page_num_id,
        'shapeType': 'ELLIPSE',
        'elementProperties': {
            'pageObjectId': slide_id,
            'size': {'width': {'magnitude': 50, 'unit': 'PT'}, 'height': {'magnitude': 50, 'unit': 'PT'}},
            'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': 670, 'translateY': 40, 'unit': 'PT'}
        }
    }
})

requests.append({
    'updateShapeProperties': {
        'objectId': page_num_id,
        'shapeProperties': {'shapeBackgroundFill': {'solidFill': {'color': {'rgbColor': ORANGE}}}},
        'fields': 'shapeBackgroundFill'
    }
})

requests.append({'insertText': {'objectId': page_num_id, 'text': str(current_slide_count + 1), 'insertionIndex': 0}})
requests.append({
    'updateTextStyle': {
        'objectId': page_num_id,
        'style': {'bold': True, 'fontSize': {'magnitude': 28, 'unit': 'PT'}, 'foregroundColor': {'opaqueColor': {'rgbColor': WHITE}}},
        'fields': 'bold,fontSize,foregroundColor',
        'textRange': {'type': 'ALL'}
    }
})

requests.append({
    'updateParagraphStyle': {
        'objectId': page_num_id,
        'style': {'alignment': 'CENTER'},
        'fields': 'alignment'
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

# 3 Content Boxes
boxes = [
    {
        'title': '$377 Cabinets Rated 2.8★',
        'what': 'Highest-priced category shows lowest customer satisfaction scores',
        'so_what': 'Quality gap suggests unmet expectations in premium storage segment',
        'color': ORANGE,
        'y': 140
    },
    {
        'title': 'Shelving: 5.1 Products Per Brand',
        'what': '225 brands competing in shelving with high product density',
        'so_what': 'Crowded market may indicate commoditization or low differentiation',
        'color': CYAN,
        'y': 282
    },
    {
        'title': '736% Installation Barrier Premium',
        'what': 'Drill-required products ($142) vs adhesive ($17) show dramatic price gap',
        'so_what': 'Installation convenience commands significant price premium in market',
        'color': BLACK,
        'y': 424
    }
]

for i, box in enumerate(boxes):
    box_height = 130

    # Background box with shadow
    bg_id = f'{slide_id}_box{i}_bg'
    requests.append({
        'createShape': {
            'objectId': bg_id,
            'shapeType': 'RECTANGLE',
            'elementProperties': {
                'pageObjectId': slide_id,
                'size': {'width': {'magnitude': 670, 'unit': 'PT'}, 'height': {'magnitude': box_height, 'unit': 'PT'}},
                'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': 50, 'translateY': box['y'], 'unit': 'PT'}
            }
        }
    })

    requests.append({
        'updateShapeProperties': {
            'objectId': bg_id,
            'shapeProperties': {
                'shapeBackgroundFill': {'solidFill': {'color': {'rgbColor': LIGHT_GRAY}}},
                'outline': {'propertyState': 'NOT_RENDERED'},
                'shadow': {
                    'type': 'OUTER',
                    'blurRadius': {'magnitude': 4, 'unit': 'PT'},
                    'color': {'rgbColor': {'red': 0, 'green': 0, 'blue': 0}},
                    'alpha': 0.15,
                    'transform': {
                        'translateX': 0,
                        'translateY': 2,
                        'unit': 'PT'
                    }
                }
            },
            'fields': 'shapeBackgroundFill,outline,shadow'
        }
    })

    # Thick colored left border
    border_id = f'{slide_id}_box{i}_border'
    requests.append({
        'createShape': {
            'objectId': border_id,
            'shapeType': 'RECTANGLE',
            'elementProperties': {
                'pageObjectId': slide_id,
                'size': {'width': {'magnitude': 10, 'unit': 'PT'}, 'height': {'magnitude': box_height, 'unit': 'PT'}},
                'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': 50, 'translateY': box['y'], 'unit': 'PT'}
            }
        }
    })

    requests.append({
        'updateShapeProperties': {
            'objectId': border_id,
            'shapeProperties': {
                'shapeBackgroundFill': {'solidFill': {'color': {'rgbColor': box['color']}}},
                'outline': {'propertyState': 'NOT_RENDERED'}
            },
            'fields': 'shapeBackgroundFill,outline'
        }
    })

    # Title (colored, bold)
    title_box_id = f'{slide_id}_box{i}_title'
    requests.append({
        'createShape': {
            'objectId': title_box_id,
            'shapeType': 'TEXT_BOX',
            'elementProperties': {
                'pageObjectId': slide_id,
                'size': {'width': {'magnitude': 630, 'unit': 'PT'}, 'height': {'magnitude': 35, 'unit': 'PT'}},
                'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': 70, 'translateY': box['y'] + 15, 'unit': 'PT'}
            }
        }
    })

    requests.append({'insertText': {'objectId': title_box_id, 'text': box['title'], 'insertionIndex': 0}})
    requests.append({
        'updateTextStyle': {
            'objectId': title_box_id,
            'style': {'bold': True, 'fontSize': {'magnitude': 22, 'unit': 'PT'}, 'foregroundColor': {'opaqueColor': {'rgbColor': box['color']}}},
            'fields': 'bold,fontSize,foregroundColor'
        }
    })

    # WHAT text
    what_id = f'{slide_id}_box{i}_what'
    requests.append({
        'createShape': {
            'objectId': what_id,
            'shapeType': 'TEXT_BOX',
            'elementProperties': {
                'pageObjectId': slide_id,
                'size': {'width': {'magnitude': 630, 'unit': 'PT'}, 'height': {'magnitude': 30, 'unit': 'PT'}},
                'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': 70, 'translateY': box['y'] + 50, 'unit': 'PT'}
            }
        }
    })

    what_text = f"WHAT: {box['what']}"
    requests.append({'insertText': {'objectId': what_id, 'text': what_text, 'insertionIndex': 0}})
    requests.append({
        'updateTextStyle': {
            'objectId': what_id,
            'style': {'fontSize': {'magnitude': 18, 'unit': 'PT'}, 'foregroundColor': {'opaqueColor': {'rgbColor': {'red': 0.2, 'green': 0.2, 'blue': 0.2}}}},
            'fields': 'fontSize,foregroundColor'
        }
    })

    # Bold the "WHAT:" part
    requests.append({
        'updateTextStyle': {
            'objectId': what_id,
            'style': {'bold': True},
            'fields': 'bold',
            'textRange': {'type': 'FIXED_RANGE', 'startIndex': 0, 'endIndex': 5}
        }
    })

    # SO WHAT text
    so_what_id = f'{slide_id}_box{i}_sowhat'
    requests.append({
        'createShape': {
            'objectId': so_what_id,
            'shapeType': 'TEXT_BOX',
            'elementProperties': {
                'pageObjectId': slide_id,
                'size': {'width': {'magnitude': 630, 'unit': 'PT'}, 'height': {'magnitude': 40, 'unit': 'PT'}},
                'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': 70, 'translateY': box['y'] + 80, 'unit': 'PT'}
            }
        }
    })

    so_what_text = f"SO WHAT: {box['so_what']}"
    requests.append({'insertText': {'objectId': so_what_id, 'text': so_what_text, 'insertionIndex': 0}})
    requests.append({
        'updateTextStyle': {
            'objectId': so_what_id,
            'style': {'fontSize': {'magnitude': 18, 'unit': 'PT'}, 'foregroundColor': {'opaqueColor': {'rgbColor': {'red': 0.2, 'green': 0.2, 'blue': 0.2}}}},
            'fields': 'fontSize,foregroundColor'
        }
    })

    # Bold the "SO WHAT:" part
    requests.append({
        'updateTextStyle': {
            'objectId': so_what_id,
            'style': {'bold': True},
            'fields': 'bold',
            'textRange': {'type': 'FIXED_RANGE', 'startIndex': 0, 'endIndex': 8}
        }
    })

# Citation
citation_id = f'{slide_id}_citation'
requests.append({
    'createShape': {
        'objectId': citation_id,
        'shapeType': 'TEXT_BOX',
        'elementProperties': {
            'pageObjectId': slide_id,
            'size': {'width': {'magnitude': 670, 'unit': 'PT'}, 'height': {'magnitude': 20, 'unit': 'PT'}},
            'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': 50, 'translateY': 510, 'unit': 'PT'}
        }
    }
})

requests.append({'insertText': {'objectId': citation_id, 'text': '[2] Quality gap analysis & market saturation metrics | See Appendix for methodology', 'insertionIndex': 0}})
requests.append({
    'updateTextStyle': {
        'objectId': citation_id,
        'style': {'italic': True, 'fontSize': {'magnitude': 9, 'unit': 'PT'}, 'foregroundColor': {'opaqueColor': {'rgbColor': GRAY_TEXT}}},
        'fields': 'italic,fontSize,foregroundColor'
    }
})

slides_service.presentations().batchUpdate(
    presentationId=PRESENTATION_ID,
    body={'requests': requests}
).execute()

print("✓ Slide 2 complete - Quality & Market Dynamics")

# ==============================================================================
# SLIDE 3: RETAILER CHANNEL PATTERNS
# ==============================================================================

current_slide_count = len(slides_service.presentations().get(presentationId=PRESENTATION_ID).execute()['slides'])

slide_id = 'retailer_channel_patterns'
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

requests.append({'insertText': {'objectId': title_id, 'text': 'RETAILER CHANNEL PATTERNS', 'insertionIndex': 0}})
requests.append({
    'updateTextStyle': {
        'objectId': title_id,
        'style': {'bold': True, 'fontSize': {'magnitude': 32, 'unit': 'PT'}, 'foregroundColor': {'opaqueColor': {'rgbColor': WHITE}}},
        'fields': 'bold,fontSize,foregroundColor'
    }
})

# Page number circle
page_num_id = f'{slide_id}_pagenum'
requests.append({
    'createShape': {
        'objectId': page_num_id,
        'shapeType': 'ELLIPSE',
        'elementProperties': {
            'pageObjectId': slide_id,
            'size': {'width': {'magnitude': 50, 'unit': 'PT'}, 'height': {'magnitude': 50, 'unit': 'PT'}},
            'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': 670, 'translateY': 40, 'unit': 'PT'}
        }
    }
})

requests.append({
    'updateShapeProperties': {
        'objectId': page_num_id,
        'shapeProperties': {'shapeBackgroundFill': {'solidFill': {'color': {'rgbColor': ORANGE}}}},
        'fields': 'shapeBackgroundFill'
    }
})

requests.append({'insertText': {'objectId': page_num_id, 'text': str(current_slide_count + 1), 'insertionIndex': 0}})
requests.append({
    'updateTextStyle': {
        'objectId': page_num_id,
        'style': {'bold': True, 'fontSize': {'magnitude': 28, 'unit': 'PT'}, 'foregroundColor': {'opaqueColor': {'rgbColor': WHITE}}},
        'fields': 'bold,fontSize,foregroundColor',
        'textRange': {'type': 'ALL'}
    }
})

requests.append({
    'updateParagraphStyle': {
        'objectId': page_num_id,
        'style': {'alignment': 'CENTER'},
        'fields': 'alignment'
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

# 3 Content Boxes
boxes = [
    {
        'title': "Lowe's: 85% of Cabinets, 55% of Shelving",
        'what': 'Single retailer dominates two largest product categories by dollar value',
        'so_what': 'Channel concentration risk in high-ticket storage categories',
        'color': ORANGE,
        'y': 140
    },
    {
        'title': 'Amazon Leads Hooks & Hangers (32%)',
        'what': 'Online channel captures plurality of highest-volume accessory category',
        'so_what': 'E-commerce strength in low-ticket, high-frequency purchase segment',
        'color': CYAN,
        'y': 282
    },
    {
        'title': 'Target: 38% of Bins & Baskets',
        'what': 'Mid-market retailer shows outsized share in portable storage despite smaller overall footprint',
        'so_what': 'Category merchandising strategies vary significantly by retailer positioning',
        'color': BLACK,
        'y': 424
    }
]

for i, box in enumerate(boxes):
    box_height = 130

    # Background box with shadow
    bg_id = f'{slide_id}_box{i}_bg'
    requests.append({
        'createShape': {
            'objectId': bg_id,
            'shapeType': 'RECTANGLE',
            'elementProperties': {
                'pageObjectId': slide_id,
                'size': {'width': {'magnitude': 670, 'unit': 'PT'}, 'height': {'magnitude': box_height, 'unit': 'PT'}},
                'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': 50, 'translateY': box['y'], 'unit': 'PT'}
            }
        }
    })

    requests.append({
        'updateShapeProperties': {
            'objectId': bg_id,
            'shapeProperties': {
                'shapeBackgroundFill': {'solidFill': {'color': {'rgbColor': LIGHT_GRAY}}},
                'outline': {'propertyState': 'NOT_RENDERED'},
                'shadow': {
                    'type': 'OUTER',
                    'blurRadius': {'magnitude': 4, 'unit': 'PT'},
                    'color': {'rgbColor': {'red': 0, 'green': 0, 'blue': 0}},
                    'alpha': 0.15,
                    'transform': {
                        'translateX': 0,
                        'translateY': 2,
                        'unit': 'PT'
                    }
                }
            },
            'fields': 'shapeBackgroundFill,outline,shadow'
        }
    })

    # Thick colored left border
    border_id = f'{slide_id}_box{i}_border'
    requests.append({
        'createShape': {
            'objectId': border_id,
            'shapeType': 'RECTANGLE',
            'elementProperties': {
                'pageObjectId': slide_id,
                'size': {'width': {'magnitude': 10, 'unit': 'PT'}, 'height': {'magnitude': box_height, 'unit': 'PT'}},
                'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': 50, 'translateY': box['y'], 'unit': 'PT'}
            }
        }
    })

    requests.append({
        'updateShapeProperties': {
            'objectId': border_id,
            'shapeProperties': {
                'shapeBackgroundFill': {'solidFill': {'color': {'rgbColor': box['color']}}},
                'outline': {'propertyState': 'NOT_RENDERED'}
            },
            'fields': 'shapeBackgroundFill,outline'
        }
    })

    # Title (colored, bold)
    title_box_id = f'{slide_id}_box{i}_title'
    requests.append({
        'createShape': {
            'objectId': title_box_id,
            'shapeType': 'TEXT_BOX',
            'elementProperties': {
                'pageObjectId': slide_id,
                'size': {'width': {'magnitude': 630, 'unit': 'PT'}, 'height': {'magnitude': 35, 'unit': 'PT'}},
                'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': 70, 'translateY': box['y'] + 15, 'unit': 'PT'}
            }
        }
    })

    requests.append({'insertText': {'objectId': title_box_id, 'text': box['title'], 'insertionIndex': 0}})
    requests.append({
        'updateTextStyle': {
            'objectId': title_box_id,
            'style': {'bold': True, 'fontSize': {'magnitude': 22, 'unit': 'PT'}, 'foregroundColor': {'opaqueColor': {'rgbColor': box['color']}}},
            'fields': 'bold,fontSize,foregroundColor'
        }
    })

    # WHAT text
    what_id = f'{slide_id}_box{i}_what'
    requests.append({
        'createShape': {
            'objectId': what_id,
            'shapeType': 'TEXT_BOX',
            'elementProperties': {
                'pageObjectId': slide_id,
                'size': {'width': {'magnitude': 630, 'unit': 'PT'}, 'height': {'magnitude': 30, 'unit': 'PT'}},
                'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': 70, 'translateY': box['y'] + 50, 'unit': 'PT'}
            }
        }
    })

    what_text = f"WHAT: {box['what']}"
    requests.append({'insertText': {'objectId': what_id, 'text': what_text, 'insertionIndex': 0}})
    requests.append({
        'updateTextStyle': {
            'objectId': what_id,
            'style': {'fontSize': {'magnitude': 18, 'unit': 'PT'}, 'foregroundColor': {'opaqueColor': {'rgbColor': {'red': 0.2, 'green': 0.2, 'blue': 0.2}}}},
            'fields': 'fontSize,foregroundColor'
        }
    })

    # Bold the "WHAT:" part
    requests.append({
        'updateTextStyle': {
            'objectId': what_id,
            'style': {'bold': True},
            'fields': 'bold',
            'textRange': {'type': 'FIXED_RANGE', 'startIndex': 0, 'endIndex': 5}
        }
    })

    # SO WHAT text
    so_what_id = f'{slide_id}_box{i}_sowhat'
    requests.append({
        'createShape': {
            'objectId': so_what_id,
            'shapeType': 'TEXT_BOX',
            'elementProperties': {
                'pageObjectId': slide_id,
                'size': {'width': {'magnitude': 630, 'unit': 'PT'}, 'height': {'magnitude': 40, 'unit': 'PT'}},
                'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': 70, 'translateY': box['y'] + 80, 'unit': 'PT'}
            }
        }
    })

    so_what_text = f"SO WHAT: {box['so_what']}"
    requests.append({'insertText': {'objectId': so_what_id, 'text': so_what_text, 'insertionIndex': 0}})
    requests.append({
        'updateTextStyle': {
            'objectId': so_what_id,
            'style': {'fontSize': {'magnitude': 18, 'unit': 'PT'}, 'foregroundColor': {'opaqueColor': {'rgbColor': {'red': 0.2, 'green': 0.2, 'blue': 0.2}}}},
            'fields': 'fontSize,foregroundColor'
        }
    })

    # Bold the "SO WHAT:" part
    requests.append({
        'updateTextStyle': {
            'objectId': so_what_id,
            'style': {'bold': True},
            'fields': 'bold',
            'textRange': {'type': 'FIXED_RANGE', 'startIndex': 0, 'endIndex': 8}
        }
    })

# Citation
citation_id = f'{slide_id}_citation'
requests.append({
    'createShape': {
        'objectId': citation_id,
        'shapeType': 'TEXT_BOX',
        'elementProperties': {
            'pageObjectId': slide_id,
            'size': {'width': {'magnitude': 670, 'unit': 'PT'}, 'height': {'magnitude': 20, 'unit': 'PT'}},
            'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': 50, 'translateY': 510, 'unit': 'PT'}
        }
    }
})

requests.append({'insertText': {'objectId': citation_id, 'text': '[3] Retailer category share analysis | See Appendix for methodology', 'insertionIndex': 0}})
requests.append({
    'updateTextStyle': {
        'objectId': citation_id,
        'style': {'italic': True, 'fontSize': {'magnitude': 9, 'unit': 'PT'}, 'foregroundColor': {'opaqueColor': {'rgbColor': GRAY_TEXT}}},
        'fields': 'italic,fontSize,foregroundColor'
    }
})

slides_service.presentations().batchUpdate(
    presentationId=PRESENTATION_ID,
    body={'requests': requests}
).execute()

print("✓ Slide 3 complete - Retailer Channel Patterns")

print(f"\n{'='*80}")
print("✓ SLIDES 2 & 3 CREATED - EXACT MATCH TO EXISTING FORMAT")
print(f"{'='*80}")
print(f"\nView at: https://docs.google.com/presentation/d/{PRESENTATION_ID}")
