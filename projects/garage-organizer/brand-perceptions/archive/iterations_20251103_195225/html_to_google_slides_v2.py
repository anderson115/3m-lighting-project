#!/usr/bin/env python3
"""
Convert HTML slides to Google Slides with ACTUAL DESIGN
Not just text dumps - real layouts, colors, shapes
"""

import os
import json
from bs4 import BeautifulSoup
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/presentations', 'https://www.googleapis.com/auth/drive']

# Google Slides units: 1 point = 1/72 inch
# 1920px @ 72dpi = 1920pts = 26.67 inches
PT_TO_EMU = 12700  # 1 point = 12700 EMU (English Metric Units)

def pt_to_emu(points):
    """Convert points to EMU"""
    return int(points * PT_TO_EMU)

def hex_to_rgb(hex_color):
    """Convert hex color to RGB dict for Google Slides"""
    hex_color = hex_color.lstrip('#')
    return {
        'red': int(hex_color[0:2], 16) / 255,
        'green': int(hex_color[2:4], 16) / 255,
        'blue': int(hex_color[4:6], 16) / 255
    }

def get_credentials():
    """Get Google API credentials"""
    credentials_path = 'credentials.json'

    with open(credentials_path, 'r') as f:
        cred_data = json.load(f)

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

        try:
            creds.refresh(Request())
            cred_data['tokens']['access_token'] = creds.token
            with open(credentials_path, 'w') as f:
                json.dump(cred_data, f, indent=2)
        except:
            pass

    return creds

def create_slide_1(service, presentation_id):
    """Create Slide 1 with actual layout"""
    requests = []
    slide_id = 'slide_1_designed'

    # Create blank slide
    requests.append({
        'createSlide': {
            'objectId': slide_id,
            'slideLayoutReference': {'predefinedLayout': 'BLANK'}
        }
    })

    # Headline
    requests.append({
        'createShape': {
            'objectId': f'{slide_id}_headline',
            'shapeType': 'TEXT_BOX',
            'elementProperties': {
                'pageObjectId': slide_id,
                'size': {
                    'width': {'magnitude': pt_to_emu(1680), 'unit': 'EMU'},
                    'height': {'magnitude': pt_to_emu(100), 'unit': 'EMU'}
                },
                'transform': {
                    'scaleX': 1, 'scaleY': 1,
                    'translateX': pt_to_emu(80),
                    'translateY': pt_to_emu(80),
                    'unit': 'EMU'
                }
            }
        }
    })

    requests.append({
        'insertText': {
            'objectId': f'{slide_id}_headline',
            'text': "Command's Market Presence is Strong, But Creator Discussions Reveal a Tension Worth Exploring"
        }
    })

    # Style headline
    requests.append({
        'updateTextStyle': {
            'objectId': f'{slide_id}_headline',
            'style': {
                'fontSize': {'magnitude': 32, 'unit': 'PT'},
                'foregroundColor': {'opaqueColor': {'rgbColor': hex_to_rgb('#111827')}},
                'bold': True,
                'fontFamily': 'Inter'
            },
            'fields': 'fontSize,foregroundColor,bold,fontFamily'
        }
    })

    # Left column - "The Pattern" section
    pattern_y = 200
    requests.append({
        'createShape': {
            'objectId': f'{slide_id}_pattern_header',
            'shapeType': 'TEXT_BOX',
            'elementProperties': {
                'pageObjectId': slide_id,
                'size': {
                    'width': {'magnitude': pt_to_emu(800), 'unit': 'EMU'},
                    'height': {'magnitude': pt_to_emu(30), 'unit': 'EMU'}
                },
                'transform': {
                    'scaleX': 1, 'scaleY': 1,
                    'translateX': pt_to_emu(80),
                    'translateY': pt_to_emu(pattern_y),
                    'unit': 'EMU'
                }
            }
        }
    })

    requests.append({
        'insertText': {
            'objectId': f'{slide_id}_pattern_header',
            'text': '✱ THE PATTERN'
        }
    })

    requests.append({
        'updateTextStyle': {
            'objectId': f'{slide_id}_pattern_header',
            'style': {
                'fontSize': {'magnitude': 12, 'unit': 'PT'},
                'foregroundColor': {'opaqueColor': {'rgbColor': hex_to_rgb('#374151')}},
                'bold': True,
                'fontFamily': 'Inter'
            },
            'fields': 'fontSize,foregroundColor,bold,fontFamily'
        }
    })

    # Pattern body
    requests.append({
        'createShape': {
            'objectId': f'{slide_id}_pattern_body',
            'shapeType': 'TEXT_BOX',
            'elementProperties': {
                'pageObjectId': slide_id,
                'size': {
                    'width': {'magnitude': pt_to_emu(800), 'unit': 'EMU'},
                    'height': {'magnitude': pt_to_emu(150), 'unit': 'EMU'}
                },
                'transform': {
                    'scaleX': 1, 'scaleY': 1,
                    'translateX': pt_to_emu(80),
                    'translateY': pt_to_emu(pattern_y + 40),
                    'unit': 'EMU'
                }
            }
        }
    })

    requests.append({
        'insertText': {
            'objectId': f'{slide_id}_pattern_body',
            'text': 'Command appears frequently in YouTube content—particularly in instructional videos where creators demonstrate picture hanging and organization techniques. However, surface damage appears as a topic in creator feedback more frequently than damage-free benefits are highlighted as an advantage.'
        }
    })

    requests.append({
        'updateTextStyle': {
            'objectId': f'{slide_id}_pattern_body',
            'style': {
                'fontSize': {'magnitude': 14, 'unit': 'PT'},
                'foregroundColor': {'opaqueColor': {'rgbColor': hex_to_rgb('#1F2937')}},
                'fontFamily': 'Inter'
            },
            'fields': 'fontSize,foregroundColor,fontFamily'
        }
    })

    # Hard Truth Panel (colored box)
    truth_y = 390
    requests.append({
        'createShape': {
            'objectId': f'{slide_id}_truth_box',
            'shapeType': 'RECTANGLE',
            'elementProperties': {
                'pageObjectId': slide_id,
                'size': {
                    'width': {'magnitude': pt_to_emu(800), 'unit': 'EMU'},
                    'height': {'magnitude': pt_to_emu(180), 'unit': 'EMU'}
                },
                'transform': {
                    'scaleX': 1, 'scaleY': 1,
                    'translateX': pt_to_emu(80),
                    'translateY': pt_to_emu(truth_y),
                    'unit': 'EMU'
                }
            }
        }
    })

    # Style the box with gradient-like background
    requests.append({
        'updateShapeProperties': {
            'objectId': f'{slide_id}_truth_box',
            'shapeProperties': {
                'shapeBackgroundFill': {
                    'solidFill': {
                        'color': {'rgbColor': hex_to_rgb('#F3F4F6')}
                    }
                },
                'outline': {
                    'outlineFill': {
                        'solidFill': {
                            'color': {'rgbColor': hex_to_rgb('#1E3A8A')}
                        }
                    },
                    'weight': {'magnitude': pt_to_emu(4), 'unit': 'EMU'},
                    'dashStyle': 'SOLID',
                    'propertyState': 'RENDERED'
                }
            },
            'fields': 'shapeBackgroundFill,outline'
        }
    })

    # Hard Truth header
    requests.append({
        'createShape': {
            'objectId': f'{slide_id}_truth_header',
            'shapeType': 'TEXT_BOX',
            'elementProperties': {
                'pageObjectId': slide_id,
                'size': {
                    'width': {'magnitude': pt_to_emu(750), 'unit': 'EMU'},
                    'height': {'magnitude': pt_to_emu(30), 'unit': 'EMU'}
                },
                'transform': {
                    'scaleX': 1, 'scaleY': 1,
                    'translateX': pt_to_emu(110),
                    'translateY': pt_to_emu(truth_y + 20),
                    'unit': 'EMU'
                }
            }
        }
    })

    requests.append({
        'insertText': {
            'objectId': f'{slide_id}_truth_header',
            'text': 'HARD TRUTH'
        }
    })

    requests.append({
        'updateTextStyle': {
            'objectId': f'{slide_id}_truth_header',
            'style': {
                'fontSize': {'magnitude': 12, 'unit': 'PT'},
                'foregroundColor': {'opaqueColor': {'rgbColor': hex_to_rgb('#1E3A8A')}},
                'bold': True,
                'fontFamily': 'Inter'
            },
            'fields': 'fontSize,foregroundColor,bold,fontFamily'
        }
    })

    # Hard Truth body
    requests.append({
        'createShape': {
            'objectId': f'{slide_id}_truth_body',
            'shapeType': 'TEXT_BOX',
            'elementProperties': {
                'pageObjectId': slide_id,
                'size': {
                    'width': {'magnitude': pt_to_emu(750), 'unit': 'EMU'},
                    'height': {'magnitude': pt_to_emu(120), 'unit': 'EMU'}
                },
                'transform': {
                    'scaleX': 1, 'scaleY': 1,
                    'translateX': pt_to_emu(110),
                    'translateY': pt_to_emu(truth_y + 55),
                    'unit': 'EMU'
                }
            }
        }
    })

    requests.append({
        'insertText': {
            'objectId': f'{slide_id}_truth_body',
            'text': 'In YouTube creator content, surface damage concerns outweigh damage-free benefit emphasis.\n\nThis matters because: When creator feedback contradicts positioning, marketing ROI is compromised.'
        }
    })

    requests.append({
        'updateTextStyle': {
            'objectId': f'{slide_id}_truth_body',
            'style': {
                'fontSize': {'magnitude': 13, 'unit': 'PT'},
                'foregroundColor': {'opaqueColor': {'rgbColor': hex_to_rgb('#111827')}},
                'fontFamily': 'Inter'
            },
            'fields': 'fontSize,foregroundColor,fontFamily'
        }
    })

    # Right column - Balance scale visualization (simplified)
    scale_x = 1000
    scale_y = 200

    # Left weight (heavier - amber)
    requests.append({
        'createShape': {
            'objectId': f'{slide_id}_weight_left',
            'shapeType': 'ELLIPSE',
            'elementProperties': {
                'pageObjectId': slide_id,
                'size': {
                    'width': {'magnitude': pt_to_emu(80), 'unit': 'EMU'},
                    'height': {'magnitude': pt_to_emu(80), 'unit': 'EMU'}
                },
                'transform': {
                    'scaleX': 1, 'scaleY': 1,
                    'translateX': pt_to_emu(scale_x),
                    'translateY': pt_to_emu(scale_y + 120),
                    'unit': 'EMU'
                }
            }
        }
    })

    requests.append({
        'updateShapeProperties': {
            'objectId': f'{slide_id}_weight_left',
            'shapeProperties': {
                'shapeBackgroundFill': {
                    'solidFill': {
                        'color': {'rgbColor': hex_to_rgb('#F59E0B')}
                    }
                }
            },
            'fields': 'shapeBackgroundFill'
        }
    })

    # Right weight (lighter - blue)
    requests.append({
        'createShape': {
            'objectId': f'{slide_id}_weight_right',
            'shapeType': 'ELLIPSE',
            'elementProperties': {
                'pageObjectId': slide_id,
                'size': {
                    'width': {'magnitude': pt_to_emu(50), 'unit': 'EMU'},
                    'height': {'magnitude': pt_to_emu(50), 'unit': 'EMU'}
                },
                'transform': {
                    'scaleX': 1, 'scaleY': 1,
                    'translateX': pt_to_emu(scale_x + 350),
                    'translateY': pt_to_emu(scale_y + 80),
                    'unit': 'EMU'
                }
            }
        }
    })

    requests.append({
        'updateShapeProperties': {
            'objectId': f'{slide_id}_weight_right',
            'shapeProperties': {
                'shapeBackgroundFill': {
                    'solidFill': {
                        'color': {'rgbColor': hex_to_rgb('#1E3A8A')}
                    }
                }
            },
            'fields': 'shapeBackgroundFill'
        }
    })

    # Labels
    requests.append({
        'createShape': {
            'objectId': f'{slide_id}_label_left',
            'shapeType': 'TEXT_BOX',
            'elementProperties': {
                'pageObjectId': slide_id,
                'size': {
                    'width': {'magnitude': pt_to_emu(150), 'unit': 'EMU'},
                    'height': {'magnitude': pt_to_emu(40), 'unit': 'EMU'}
                },
                'transform': {
                    'scaleX': 1, 'scaleY': 1,
                    'translateX': pt_to_emu(scale_x - 30),
                    'translateY': pt_to_emu(scale_y + 220),
                    'unit': 'EMU'
                }
            }
        }
    })

    requests.append({
        'insertText': {
            'objectId': f'{slide_id}_label_left',
            'text': 'Surface Damage\nDiscussions'
        }
    })

    requests.append({
        'updateTextStyle': {
            'objectId': f'{slide_id}_label_left',
            'style': {
                'fontSize': {'magnitude': 11, 'unit': 'PT'},
                'foregroundColor': {'opaqueColor': {'rgbColor': hex_to_rgb('#92400E')}},
                'fontFamily': 'Inter'
            },
            'fields': 'fontSize,foregroundColor,fontFamily'
        }
    })

    requests.append({
        'createShape': {
            'objectId': f'{slide_id}_label_right',
            'shapeType': 'TEXT_BOX',
            'elementProperties': {
                'pageObjectId': slide_id,
                'size': {
                    'width': {'magnitude': pt_to_emu(150), 'unit': 'EMU'},
                    'height': {'magnitude': pt_to_emu(40), 'unit': 'EMU'}
                },
                'transform': {
                    'scaleX': 1, 'scaleY': 1,
                    'translateX': pt_to_emu(scale_x + 290),
                    'translateY': pt_to_emu(scale_y + 180),
                    'unit': 'EMU'
                }
            }
        }
    })

    requests.append({
        'insertText': {
            'objectId': f'{slide_id}_label_right',
            'text': 'Damage-Free\nBenefits'
        }
    })

    requests.append({
        'updateTextStyle': {
            'objectId': f'{slide_id}_label_right',
            'style': {
                'fontSize': {'magnitude': 11, 'unit': 'PT'},
                'foregroundColor': {'opaqueColor': {'rgbColor': hex_to_rgb('#1E3A8A')}},
                'fontFamily': 'Inter'
            },
            'fields': 'fontSize,foregroundColor,fontFamily'
        }
    })

    # Data table below balance scale
    table_y = scale_y + 280

    # Create simple data visualization
    requests.append({
        'createShape': {
            'objectId': f'{slide_id}_data',
            'shapeType': 'TEXT_BOX',
            'elementProperties': {
                'pageObjectId': slide_id,
                'size': {
                    'width': {'magnitude': pt_to_emu(500), 'unit': 'EMU'},
                    'height': {'magnitude': pt_to_emu(100), 'unit': 'EMU'}
                },
                'transform': {
                    'scaleX': 1, 'scaleY': 1,
                    'translateX': pt_to_emu(scale_x),
                    'translateY': pt_to_emu(table_y),
                    'unit': 'EMU'
                }
            }
        }
    })

    requests.append({
        'insertText': {
            'objectId': f'{slide_id}_data',
            'text': 'DISCUSSION TYPE\t\tVIDEOS\n\nSurface Damage\t\t24\nDamage-Free Emphasis\t11'
        }
    })

    requests.append({
        'updateTextStyle': {
            'objectId': f'{slide_id}_data',
            'style': {
                'fontSize': {'magnitude': 13, 'unit': 'PT'},
                'foregroundColor': {'opaqueColor': {'rgbColor': hex_to_rgb('#1F2937')}},
                'fontFamily': 'Inter'
            },
            'fields': 'fontSize,foregroundColor,fontFamily'
        }
    })

    # Execute
    body = {'requests': requests}
    response = service.presentations().batchUpdate(
        presentationId=presentation_id,
        body=body
    ).execute()

    print(f'✅ Created Slide 1 with actual design')
    return response

def main():
    print("🚀 HTML to Google Slides v2 - WITH ACTUAL DESIGN")
    print("=" * 60)

    creds = get_credentials()
    service = build('slides', 'v1', credentials=creds)

    # Create new presentation
    presentation = {
        'title': '3M Garage Organization - DESIGNED'
    }
    presentation = service.presentations().create(body=presentation).execute()
    presentation_id = presentation.get('presentationId')

    print(f'✅ Created presentation: {presentation_id}')
    print(f'   https://docs.google.com/presentation/d/{presentation_id}/edit')

    # Build slide 1 with real design
    create_slide_1(service, presentation_id)

    print(f"\n" + "=" * 60)
    print(f"✅ COMPLETE - WITH COLORS, LAYOUT, SHAPES")
    print(f"📊 View: https://docs.google.com/presentation/d/{presentation_id}/edit")
    print(f"=" * 60)

if __name__ == '__main__':
    main()
