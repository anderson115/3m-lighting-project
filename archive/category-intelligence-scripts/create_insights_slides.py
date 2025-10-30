#!/usr/bin/env python3
"""Create professional product insights slides matching Offbrain design"""

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

# Load insights
with open('product_insights.json') as f:
    insights = json.load(f)

# Offbrain Design System
DARK_BG = {'red': 0.18, 'green': 0.20, 'blue': 0.25}
ORANGE = {'red': 1.0, 'green': 0.42, 'blue': 0.22}
CYAN = {'red': 0.0, 'green': 0.80, 'blue': 0.95}
DARK_GRAY = {'red': 0.3, 'green': 0.3, 'blue': 0.3}
LIGHT_GRAY = {'red': 0.95, 'green': 0.95, 'blue': 0.95}
WHITE = {'red': 1.0, 'green': 1.0, 'blue': 1.0}
DARK_TEXT = {'red': 0.18, 'green': 0.20, 'blue': 0.25}
LIGHT_TEXT = {'red': 0.7, 'green': 0.7, 'blue': 0.7}

print("="*80)
print("CREATING PRODUCT INSIGHTS SLIDES")
print("="*80)

presentation = slides_service.presentations().get(presentationId=PRESENTATION_ID).execute()
current_slide_count = len(presentation['slides'])

print(f"\nCurrent slides: {current_slide_count}")

# ==============================================================================
# SLIDE 2: MARKET OPPORTUNITIES
# ==============================================================================

print("\n" + "="*80)
print("CREATING SLIDE 2: MARKET OPPORTUNITIES")
print("="*80)

slide2_id = f'market_opportunities_{id(insights)}'
requests = []

# Create slide
requests.append({
    'createSlide': {
        'objectId': slide2_id,
        'insertionIndex': current_slide_count,
        'slideLayoutReference': {'predefinedLayout': 'BLANK'}
    }
})

requests.append({
    'updatePageProperties': {
        'objectId': slide2_id,
        'pageProperties': {
            'pageBackgroundFill': {
                'solidFill': {'color': {'rgbColor': DARK_BG}}
            }
        },
        'fields': 'pageBackgroundFill'
    }
})

slides_service.presentations().batchUpdate(
    presentationId=PRESENTATION_ID,
    body={'requests': requests}
).execute()

print(f"✓ Created slide: {slide2_id}")

# Add content
requests = []

# Title
title_id = f'{slide2_id}_title'
requests.append({
    'createShape': {
        'objectId': title_id,
        'shapeType': 'TEXT_BOX',
        'elementProperties': {
            'pageObjectId': slide2_id,
            'size': {'width': {'magnitude': 600, 'unit': 'PT'}, 'height': {'magnitude': 60, 'unit': 'PT'}},
            'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': 50, 'translateY': 35, 'unit': 'PT'}
        }
    }
})

requests.append({'insertText': {'objectId': title_id, 'text': 'MARKET OBSERVATIONS', 'insertionIndex': 0}})
requests.append({
    'updateTextStyle': {
        'objectId': title_id,
        'style': {'bold': True, 'fontSize': {'magnitude': 36, 'unit': 'PT'}, 'foregroundColor': {'opaqueColor': {'rgbColor': WHITE}}},
        'fields': 'bold,fontSize,foregroundColor'
    }
})

# Page number
page_num_id = f'{slide2_id}_pagenum'
requests.append({
    'createShape': {
        'objectId': page_num_id,
        'shapeType': 'ELLIPSE',
        'elementProperties': {
            'pageObjectId': slide2_id,
            'size': {'width': {'magnitude': 45, 'unit': 'PT'}, 'height': {'magnitude': 45, 'unit': 'PT'}},
            'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': 675, 'translateY': 25, 'unit': 'PT'}
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
        'style': {'bold': True, 'fontSize': {'magnitude': 24, 'unit': 'PT'}, 'foregroundColor': {'opaqueColor': {'rgbColor': WHITE}}},
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

# Divider
divider_id = f'{slide2_id}_divider'
requests.append({
    'createLine': {
        'objectId': divider_id,
        'lineCategory': 'STRAIGHT',
        'elementProperties': {
            'pageObjectId': slide2_id,
            'size': {'width': {'magnitude': 670, 'unit': 'PT'}, 'height': {'magnitude': 0, 'unit': 'PT'}},
            'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': 50, 'translateY': 100, 'unit': 'PT'}
        }
    }
})

requests.append({
    'updateLineProperties': {
        'objectId': divider_id,
        'lineProperties': {
            'lineFill': {'solidFill': {'color': {'rgbColor': ORANGE}}},
            'weight': {'magnitude': 3, 'unit': 'PT'}
        },
        'fields': 'lineFill,weight'
    }
})

# 4 Quadrant Boxes (2x2 grid)
boxes = [
    {
        'title': 'Quality Gap',
        'subtitle': 'Cabinets',
        'metrics': '$377\nAVG PRICE\n\n2.8★\nRATING',
        'observation': 'High price, low satisfaction',
        'color': ORANGE,
        'x': 50, 'y': 130, 'w': 320, 'h': 140
    },
    {
        'title': 'Installation Barrier',
        'subtitle': 'Premium',
        'metrics': '734%\nPRICE\nPREMIUM',
        'observation': 'Drill vs. adhesive',
        'color': CYAN,
        'x': 400, 'y': 130, 'w': 320, 'h': 140
    },
    {
        'title': 'Market Saturation',
        'subtitle': 'Shelving',
        'metrics': '6.8\nPRODUCTS\nPER BRAND',
        'observation': 'Highly crowded',
        'color': DARK_GRAY,
        'x': 50, 'y': 295, 'w': 320, 'h': 140
    },
    {
        'title': 'Emerging Category',
        'subtitle': 'Rails & Tracks',
        'metrics': '82\nPRODUCTS\n\n109\nAVG REVIEWS',
        'observation': 'Low saturation, high interest',
        'color': {'red': 0.4, 'green': 0.8, 'blue': 0.4},  # Green
        'x': 400, 'y': 295, 'w': 320, 'h': 140
    }
]

for i, box in enumerate(boxes):
    # Background
    bg_id = f'{slide2_id}_box{i}_bg'
    requests.append({
        'createShape': {
            'objectId': bg_id,
            'shapeType': 'RECTANGLE',
            'elementProperties': {
                'pageObjectId': slide2_id,
                'size': {'width': {'magnitude': box['w'], 'unit': 'PT'}, 'height': {'magnitude': box['h'], 'unit': 'PT'}},
                'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': box['x'], 'translateY': box['y'], 'unit': 'PT'}
            }
        }
    })

    requests.append({
        'updateShapeProperties': {
            'objectId': bg_id,
            'shapeProperties': {
                'shapeBackgroundFill': {'solidFill': {'color': {'rgbColor': LIGHT_GRAY}}},
                'outline': {'propertyState': 'NOT_RENDERED'}
            },
            'fields': 'shapeBackgroundFill,outline'
        }
    })

    # Border
    border_id = f'{slide2_id}_box{i}_border'
    requests.append({
        'createShape': {
            'objectId': border_id,
            'shapeType': 'RECTANGLE',
            'elementProperties': {
                'pageObjectId': slide2_id,
                'size': {'width': {'magnitude': 8, 'unit': 'PT'}, 'height': {'magnitude': box['h'], 'unit': 'PT'}},
                'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': box['x'], 'translateY': box['y'], 'unit': 'PT'}
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

    # Title
    title_box_id = f'{slide2_id}_box{i}_title'
    requests.append({
        'createShape': {
            'objectId': title_box_id,
            'shapeType': 'TEXT_BOX',
            'elementProperties': {
                'pageObjectId': slide2_id,
                'size': {'width': {'magnitude': box['w'] - 25, 'unit': 'PT'}, 'height': {'magnitude': 30, 'unit': 'PT'}},
                'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': box['x'] + 15, 'translateY': box['y'] + 10, 'unit': 'PT'}
            }
        }
    })

    requests.append({'insertText': {'objectId': title_box_id, 'text': box['title'], 'insertionIndex': 0}})
    requests.append({
        'updateTextStyle': {
            'objectId': title_box_id,
            'style': {'bold': True, 'fontSize': {'magnitude': 20, 'unit': 'PT'}, 'foregroundColor': {'opaqueColor': {'rgbColor': box['color']}}},
            'fields': 'bold,fontSize,foregroundColor'
        }
    })

    # Subtitle
    subtitle_box_id = f'{slide2_id}_box{i}_subtitle'
    requests.append({
        'createShape': {
            'objectId': subtitle_box_id,
            'shapeType': 'TEXT_BOX',
            'elementProperties': {
                'pageObjectId': slide2_id,
                'size': {'width': {'magnitude': box['w'] - 25, 'unit': 'PT'}, 'height': {'magnitude': 25, 'unit': 'PT'}},
                'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': box['x'] + 15, 'translateY': box['y'] + 35, 'unit': 'PT'}
            }
        }
    })

    requests.append({'insertText': {'objectId': subtitle_box_id, 'text': box['subtitle'], 'insertionIndex': 0}})
    requests.append({
        'updateTextStyle': {
            'objectId': subtitle_box_id,
            'style': {'fontSize': {'magnitude': 18, 'unit': 'PT'}, 'foregroundColor': {'opaqueColor': {'rgbColor': DARK_TEXT}}},
            'fields': 'fontSize,foregroundColor'
        }
    })

    # Metrics (large center)
    metrics_id = f'{slide2_id}_box{i}_metrics'
    requests.append({
        'createShape': {
            'objectId': metrics_id,
            'shapeType': 'TEXT_BOX',
            'elementProperties': {
                'pageObjectId': slide2_id,
                'size': {'width': {'magnitude': box['w'] - 25, 'unit': 'PT'}, 'height': {'magnitude': 80, 'unit': 'PT'}},
                'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': box['x'] + 15, 'translateY': box['y'] + 45, 'unit': 'PT'}
            }
        }
    })

    requests.append({'insertText': {'objectId': metrics_id, 'text': box['metrics'], 'insertionIndex': 0}})
    requests.append({
        'updateTextStyle': {
            'objectId': metrics_id,
            'style': {'fontSize': {'magnitude': 18, 'unit': 'PT'}, 'foregroundColor': {'opaqueColor': {'rgbColor': DARK_TEXT}}},
            'fields': 'fontSize,foregroundColor',
            'textRange': {'type': 'ALL'}
        }
    })
    requests.append({
        'updateParagraphStyle': {
            'objectId': metrics_id,
            'style': {'alignment': 'CENTER', 'lineSpacing': 100},
            'fields': 'alignment,lineSpacing'
        }
    })

# Citation
citation_id = f'{slide2_id}_citation'
requests.append({
    'createShape': {
        'objectId': citation_id,
        'shapeType': 'TEXT_BOX',
        'elementProperties': {
            'pageObjectId': slide2_id,
            'size': {'width': {'magnitude': 670, 'unit': 'PT'}, 'height': {'magnitude': 30, 'unit': 'PT'}},
            'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': 50, 'translateY': 505, 'unit': 'PT'}
        }
    }
})

requests.append({'insertText': {'objectId': citation_id, 'text': '[1] Weighted analysis | See Appendix for methodology', 'insertionIndex': 0}})
requests.append({
    'updateTextStyle': {
        'objectId': citation_id,
        'style': {'italic': True, 'fontSize': {'magnitude': 10, 'unit': 'PT'}, 'foregroundColor': {'opaqueColor': {'rgbColor': LIGHT_TEXT}}},
        'fields': 'italic,fontSize,foregroundColor'
    }
})

slides_service.presentations().batchUpdate(
    presentationId=PRESENTATION_ID,
    body={'requests': requests}
).execute()

print("✓ Slide 2 complete - Market Opportunities")

# ==============================================================================
# SLIDE 3: COMPETITIVE DYNAMICS
# ==============================================================================

print("\n" + "="*80)
print("CREATING SLIDE 3: COMPETITIVE DYNAMICS")
print("="*80)

slide3_id = f'competitive_dynamics_{id(insights)}'
requests = []

# Create slide
requests.append({
    'createSlide': {
        'objectId': slide3_id,
        'insertionIndex': current_slide_count + 1,
        'slideLayoutReference': {'predefinedLayout': 'BLANK'}
    }
})

requests.append({
    'updatePageProperties': {
        'objectId': slide3_id,
        'pageProperties': {
            'pageBackgroundFill': {
                'solidFill': {'color': {'rgbColor': DARK_BG}}
            }
        },
        'fields': 'pageBackgroundFill'
    }
})

slides_service.presentations().batchUpdate(
    presentationId=PRESENTATION_ID,
    body={'requests': requests}
).execute()

print(f"✓ Created slide: {slide3_id}")

# Add content
requests = []

# Title
title_id = f'{slide3_id}_title'
requests.append({
    'createShape': {
        'objectId': title_id,
        'shapeType': 'TEXT_BOX',
        'elementProperties': {
            'pageObjectId': slide3_id,
            'size': {'width': {'magnitude': 600, 'unit': 'PT'}, 'height': {'magnitude': 60, 'unit': 'PT'}},
            'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': 50, 'translateY': 35, 'unit': 'PT'}
        }
    }
})

requests.append({'insertText': {'objectId': title_id, 'text': 'COMPETITIVE LANDSCAPE', 'insertionIndex': 0}})
requests.append({
    'updateTextStyle': {
        'objectId': title_id,
        'style': {'bold': True, 'fontSize': {'magnitude': 36, 'unit': 'PT'}, 'foregroundColor': {'opaqueColor': {'rgbColor': WHITE}}},
        'fields': 'bold,fontSize,foregroundColor'
    }
})

# Page number
page_num_id = f'{slide3_id}_pagenum'
requests.append({
    'createShape': {
        'objectId': page_num_id,
        'shapeType': 'ELLIPSE',
        'elementProperties': {
            'pageObjectId': slide3_id,
            'size': {'width': {'magnitude': 45, 'unit': 'PT'}, 'height': {'magnitude': 45, 'unit': 'PT'}},
            'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': 675, 'translateY': 25, 'unit': 'PT'}
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

requests.append({'insertText': {'objectId': page_num_id, 'text': str(current_slide_count + 2), 'insertionIndex': 0}})
requests.append({
    'updateTextStyle': {
        'objectId': page_num_id,
        'style': {'bold': True, 'fontSize': {'magnitude': 24, 'unit': 'PT'}, 'foregroundColor': {'opaqueColor': {'rgbColor': WHITE}}},
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

# Divider
divider_id = f'{slide3_id}_divider'
requests.append({
    'createLine': {
        'objectId': divider_id,
        'lineCategory': 'STRAIGHT',
        'elementProperties': {
            'pageObjectId': slide3_id,
            'size': {'width': {'magnitude': 670, 'unit': 'PT'}, 'height': {'magnitude': 0, 'unit': 'PT'}},
            'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': 50, 'translateY': 100, 'unit': 'PT'}
        }
    }
})

requests.append({
    'updateLineProperties': {
        'objectId': divider_id,
        'lineProperties': {
            'lineFill': {'solidFill': {'color': {'rgbColor': ORANGE}}},
            'weight': {'magnitude': 3, 'unit': 'PT'}
        },
        'fields': 'lineFill,weight'
    }
})

# 3 vertical boxes for retailer dominance
retailer_boxes = [
    {'title': 'Lowes Dominance', 'categories': 'Shelving 86%\nCabinets 85%', 'color': {'red': 0.0, 'green': 0.4, 'blue': 0.8}, 'x': 50},
    {'title': 'Target Position', 'categories': 'Garage Org 71%', 'color': CYAN, 'x': 275},
    {'title': 'Amazon Spread', 'categories': 'Storage 56%\nHooks 33%', 'color': ORANGE, 'x': 500}
]

for i, box in enumerate(retailer_boxes):
    box_y = 130
    box_w = 210
    box_h = 180

    # Background
    bg_id = f'{slide3_id}_retail{i}_bg'
    requests.append({
        'createShape': {
            'objectId': bg_id,
            'shapeType': 'RECTANGLE',
            'elementProperties': {
                'pageObjectId': slide3_id,
                'size': {'width': {'magnitude': box_w, 'unit': 'PT'}, 'height': {'magnitude': box_h, 'unit': 'PT'}},
                'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': box['x'], 'translateY': box_y, 'unit': 'PT'}
            }
        }
    })

    requests.append({
        'updateShapeProperties': {
            'objectId': bg_id,
            'shapeProperties': {
                'shapeBackgroundFill': {'solidFill': {'color': {'rgbColor': LIGHT_GRAY}}},
                'outline': {'propertyState': 'NOT_RENDERED'}
            },
            'fields': 'shapeBackgroundFill,outline'
        }
    })

    # Border
    border_id = f'{slide3_id}_retail{i}_border'
    requests.append({
        'createShape': {
            'objectId': border_id,
            'shapeType': 'RECTANGLE',
            'elementProperties': {
                'pageObjectId': slide3_id,
                'size': {'width': {'magnitude': 8, 'unit': 'PT'}, 'height': {'magnitude': box_h, 'unit': 'PT'}},
                'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': box['x'], 'translateY': box_y, 'unit': 'PT'}
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

    # Title
    title_box_id = f'{slide3_id}_retail{i}_title'
    requests.append({
        'createShape': {
            'objectId': title_box_id,
            'shapeType': 'TEXT_BOX',
            'elementProperties': {
                'pageObjectId': slide3_id,
                'size': {'width': {'magnitude': box_w - 25, 'unit': 'PT'}, 'height': {'magnitude': 40, 'unit': 'PT'}},
                'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': box['x'] + 15, 'translateY': box_y + 15, 'unit': 'PT'}
            }
        }
    })

    requests.append({'insertText': {'objectId': title_box_id, 'text': box['title'], 'insertionIndex': 0}})
    requests.append({
        'updateTextStyle': {
            'objectId': title_box_id,
            'style': {'bold': True, 'fontSize': {'magnitude': 20, 'unit': 'PT'}, 'foregroundColor': {'opaqueColor': {'rgbColor': box['color']}}},
            'fields': 'bold,fontSize,foregroundColor'
        }
    })

    # Categories
    cat_box_id = f'{slide3_id}_retail{i}_cats'
    requests.append({
        'createShape': {
            'objectId': cat_box_id,
            'shapeType': 'TEXT_BOX',
            'elementProperties': {
                'pageObjectId': slide3_id,
                'size': {'width': {'magnitude': box_w - 25, 'unit': 'PT'}, 'height': {'magnitude': 120, 'unit': 'PT'}},
                'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': box['x'] + 15, 'translateY': box_y + 50, 'unit': 'PT'}
            }
        }
    })

    requests.append({'insertText': {'objectId': cat_box_id, 'text': box['categories'], 'insertionIndex': 0}})
    requests.append({
        'updateTextStyle': {
            'objectId': cat_box_id,
            'style': {'fontSize': {'magnitude': 18, 'unit': 'PT'}, 'foregroundColor': {'opaqueColor': {'rgbColor': DARK_TEXT}}},
            'fields': 'fontSize,foregroundColor'
        }
    })
    requests.append({
        'updateParagraphStyle': {
            'objectId': cat_box_id,
            'style': {'alignment': 'CENTER', 'lineSpacing': 120},
            'fields': 'alignment,lineSpacing'
        }
    })

# Bottom insight box
insight_bg_id = f'{slide3_id}_insight_bg'
requests.append({
    'createShape': {
        'objectId': insight_bg_id,
        'shapeType': 'RECTANGLE',
        'elementProperties': {
            'pageObjectId': slide3_id,
            'size': {'width': {'magnitude': 670, 'unit': 'PT'}, 'height': {'magnitude': 140, 'unit': 'PT'}},
            'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': 50, 'translateY': 330, 'unit': 'PT'}
        }
    }
})

requests.append({
    'updateShapeProperties': {
        'objectId': insight_bg_id,
        'shapeProperties': {
            'shapeBackgroundFill': {'solidFill': {'color': {'rgbColor': LIGHT_GRAY}}},
            'outline': {'propertyState': 'NOT_RENDERED'}
        },
        'fields': 'shapeBackgroundFill,outline'
    }
})

# Border
insight_border_id = f'{slide3_id}_insight_border'
requests.append({
    'createShape': {
        'objectId': insight_border_id,
        'shapeType': 'RECTANGLE',
        'elementProperties': {
            'pageObjectId': slide3_id,
            'size': {'width': {'magnitude': 8, 'unit': 'PT'}, 'height': {'magnitude': 140, 'unit': 'PT'}},
            'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': 50, 'translateY': 330, 'unit': 'PT'}
        }
    }
})

requests.append({
    'updateShapeProperties': {
        'objectId': insight_border_id,
        'shapeProperties': {
            'shapeBackgroundFill': {'solidFill': {'color': {'rgbColor': DARK_GRAY}}},
            'outline': {'propertyState': 'NOT_RENDERED'}
        },
        'fields': 'shapeBackgroundFill,outline'
    }
})

# Insight text
insight_title_id = f'{slide3_id}_insight_title'
requests.append({
    'createShape': {
        'objectId': insight_title_id,
        'shapeType': 'TEXT_BOX',
        'elementProperties': {
            'pageObjectId': slide3_id,
            'size': {'width': {'magnitude': 640, 'unit': 'PT'}, 'height': {'magnitude': 30, 'unit': 'PT'}},
            'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': 65, 'translateY': 345, 'unit': 'PT'}
        }
    }
})

requests.append({'insertText': {'objectId': insight_title_id, 'text': 'Key Observation', 'insertionIndex': 0}})
requests.append({
    'updateTextStyle': {
        'objectId': insight_title_id,
        'style': {'bold': True, 'fontSize': {'magnitude': 20, 'unit': 'PT'}, 'foregroundColor': {'opaqueColor': {'rgbColor': DARK_GRAY}}},
        'fields': 'bold,fontSize,foregroundColor'
    }
})

insight_text_id = f'{slide3_id}_insight_text'
requests.append({
    'createShape': {
        'objectId': insight_text_id,
        'shapeType': 'TEXT_BOX',
        'elementProperties': {
            'pageObjectId': slide3_id,
            'size': {'width': {'magnitude': 640, 'unit': 'PT'}, 'height': {'magnitude': 80, 'unit': 'PT'}},
            'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': 65, 'translateY': 375, 'unit': 'PT'}
        }
    }
})

requests.append({'insertText': {'objectId': insight_text_id, 'text': 'Clear retailer specialization patterns emerge. Some categories show single-retailer dominance (>85%), while others remain fragmented. Market entry strategy should consider channel-specific dynamics.', 'insertionIndex': 0}})
requests.append({
    'updateTextStyle': {
        'objectId': insight_text_id,
        'style': {'fontSize': {'magnitude': 18, 'unit': 'PT'}, 'foregroundColor': {'opaqueColor': {'rgbColor': DARK_TEXT}}},
        'fields': 'fontSize,foregroundColor'
    }
})

# Citation
citation_id = f'{slide3_id}_citation'
requests.append({
    'createShape': {
        'objectId': citation_id,
        'shapeType': 'TEXT_BOX',
        'elementProperties': {
            'pageObjectId': slide3_id,
            'size': {'width': {'magnitude': 670, 'unit': 'PT'}, 'height': {'magnitude': 30, 'unit': 'PT'}},
            'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': 50, 'translateY': 505, 'unit': 'PT'}
        }
    }
})

requests.append({'insertText': {'objectId': citation_id, 'text': '[1] Retailer market share calculated from weighted product distribution | See Appendix', 'insertionIndex': 0}})
requests.append({
    'updateTextStyle': {
        'objectId': citation_id,
        'style': {'italic': True, 'fontSize': {'magnitude': 10, 'unit': 'PT'}, 'foregroundColor': {'opaqueColor': {'rgbColor': LIGHT_TEXT}}},
        'fields': 'italic,fontSize,foregroundColor'
    }
})

slides_service.presentations().batchUpdate(
    presentationId=PRESENTATION_ID,
    body={'requests': requests}
).execute()

print("✓ Slide 3 complete - Competitive Dynamics")

print(f"\n{'='*80}")
print("✓ ALL SLIDES CREATED SUCCESSFULLY")
print(f"{'='*80}")
print(f"\nView at: https://docs.google.com/presentation/d/{PRESENTATION_ID}")
