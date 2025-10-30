#!/usr/bin/env python3
"""Create professional product insight slides using Gamma API"""

import requests
import json
import time
from pathlib import Path

GAMMA_API_KEY = "sk-gamma-6YVonHx98DG3pRq7o6jPIdtoeAzfk4YWmLrnuuew"
API_BASE = "https://public-api.gamma.app/v0.2/generations"

def create_gamma_presentation(input_text, theme="Barcelona", num_cards=4):
    """Create a Gamma presentation"""

    headers = {
        "X-API-KEY": GAMMA_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "inputText": input_text,
        "format": "presentation",
        "themeName": theme,
        "numCards": num_cards,
        "textMode": "preserve",
        "cardSplit": "inputTextBreaks",
        "textOptions": {
            "amount": "brief",
            "tone": "Professional, analytical, exploratory - using WHAT (observation) and SO WHAT (implication) structure. Avoid affirmative recommendations.",
            "audience": "Senior executives and management consultants evaluating garage organizer market opportunities",
            "language": "en"
        },
        "imageOptions": {
            "source": "noImages"  # Keep it clean and data-focused
        },
        "cardOptions": {
            "dimensions": "16x9"
        },
        "sharingOptions": {
            "workspaceAccess": "edit",
            "externalAccess": "view"
        }
    }

    print(f"Creating Gamma presentation...")
    response = requests.post(API_BASE, headers=headers, json=payload)

    if response.status_code != 200:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return None

    result = response.json()
    generation_id = result.get("generationId")
    print(f"✓ Generation started: {generation_id}")

    # Poll for completion
    max_attempts = 60
    for attempt in range(max_attempts):
        time.sleep(5)

        status_response = requests.get(
            f"{API_BASE}/{generation_id}",
            headers={"X-API-KEY": GAMMA_API_KEY, "Accept": "application/json"}
        )

        if status_response.status_code == 200:
            status_data = status_response.json()
            status = status_data.get("status")

            if status == "completed":
                print(f"✓ Presentation complete!")
                print(f"URL: {status_data.get('gammaUrl')}")
                return status_data
            elif status == "failed":
                print(f"❌ Generation failed: {status_data.get('message', 'Unknown error')}")
                return None
            else:
                print(f"⏳ Status: {status} (attempt {attempt+1}/{max_attempts})")
        else:
            print(f"⚠️  Status check failed: {status_response.status_code}")

    print(f"❌ Timed out after {max_attempts} attempts")
    return None

print("="*80)
print("CREATING PROFESSIONAL PRODUCT SLIDES WITH GAMMA")
print("="*80)

# Load insights data
with open('product_insights.json') as f:
    insights = json.load(f)

# Craft professional slide content with proper structure
slide_content = """# Garage Organizer Category Intelligence: Product Analysis

---

# Category Market Patterns

**90% Hooks & Hangers Before Weighting**

WHAT: Raw product data shows extreme concentration in hanging accessories category (2,343 of 3,991 products)

SO WHAT: Retailer sampling bias detected - Walmart's budget-focused assortment overrepresents low-ticket accessories. True market may be more balanced than product counts suggest.

**Weighted Distribution: 27% Each**

WHAT: After bias correction for retailer representation, Hooks & Hangers and Shelving emerge as co-equal categories at ~27% each

SO WHAT: Market appears more balanced than raw data implies. Category strategy should account for both hanging accessories and horizontal storage platforms equally.

**$377 Cabinets Rated 2.8★**

WHAT: Highest-priced category (Cabinets) shows lowest customer satisfaction scores (2.79★ vs 3.8★ category average)

SO WHAT: Quality gap pattern worth exploring - premium segment shows unmet customer expectations, suggesting innovation opportunity.

---

# Quality & Market Dynamics

**Premium Quality Gap**

WHAT: Cabinets command $377 average price but deliver 2.8★ satisfaction vs Bins & Baskets at $28 with 4.2★ rating

SO WHAT: Value proposition breakdown in high-ticket segment. Are customers paying for features they don't value, or is execution falling short?

**Shelving Market Saturation**

WHAT: 225 brands competing in shelving with 5.1 products per brand - highest density observed

SO WHAT: Crowded market suggests commoditization risk. Differentiation appears challenging. Low barriers to entry may compress margins.

**736% Installation Barrier Premium**

WHAT: Drill-required products average $142 vs adhesive-mount products at $17 - an 8.4x price differential

SO WHAT: Installation convenience commands extraordinary premium. Tool-free solutions may unlock price-sensitive segments or represent value engineering opportunity.

---

# Retailer Channel Patterns

**Lowe's Category Dominance**

WHAT: Single retailer captures 85% of Cabinet category and 55% of Shelving by weighted product count

SO WHAT: Channel concentration risk in high-ticket categories. Lowe's merchandising strategy creates effective category ownership. Other retailers show limited commitment to these segments.

**Amazon's Accessory Strength**

WHAT: Online channel captures 32% plurality in Hooks & Hangers despite 7-retailer competitive set

SO WHAT: E-commerce advantage in low-ticket, high-frequency accessory segment. Suggests convenience/search beats in-store browsing for commodity items.

**Target's Niche Focus**

WHAT: Mid-market retailer commands 38% of Bins & Baskets category despite smaller overall garage storage footprint (14% total)

SO WHAT: Category merchandising strategies vary significantly by retailer positioning. Target over-indexes on portable/aesthetic storage vs structural solutions. Retailer category roles are not uniform.
"""

# Create the presentation
result = create_gamma_presentation(
    input_text=slide_content,
    theme="Barcelona",  # Professional consulting theme
    num_cards=4  # Title + 3 content slides
)

if result:
    print(f"\n{'='*80}")
    print("✓ PROFESSIONAL SLIDES CREATED")
    print(f"{'='*80}")
    print(f"\nView at: {result.get('gammaUrl')}")
    print(f"Credits used: {result.get('creditsUsed', 'N/A')}")

    # Save result for reference
    with open('gamma_presentation.json', 'w') as f:
        json.dump(result, f, indent=2)
    print(f"\n✓ Presentation details saved to: gamma_presentation.json")
else:
    print("\n❌ Failed to create presentation")
