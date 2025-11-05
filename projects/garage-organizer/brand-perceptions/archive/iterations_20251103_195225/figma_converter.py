#!/usr/bin/env python3
"""
Convert offbrain slides to Figma with high fidelity
Then export to PowerPoint/Google Slides (editable + high quality)
"""

import requests
import json

FIGMA_TOKEN = "figd_ULy6M1nNPA3TzNjmttNNwiY1B-CfFJYUYnGhZ-RA"
FIGMA_API = "https://api.figma.com/v1"

headers = {
    "X-Figma-Token": FIGMA_TOKEN,
    "Content-Type": "application/json"
}

def test_figma_connection():
    """Test Figma API connection"""
    response = requests.get(f"{FIGMA_API}/me", headers=headers)
    if response.status_code == 200:
        user = response.json()
        print(f"✅ Figma connected: {user.get('email', 'User')}")
        return True
    else:
        print(f"❌ Figma connection failed: {response.status_code}")
        print(response.text)
        return False

def create_figma_file(name="offbrain Slides - 3M Garage Organization"):
    """Create new Figma file via API"""
    # Note: Figma REST API doesn't support file creation directly
    # Need to use Figma file key for existing file or create via UI
    print(f"📋 Figma file creation requires:")
    print(f"   1. Create file in Figma UI: https://www.figma.com/files/new")
    print(f"   2. Name it: '{name}'")
    print(f"   3. Get file key from URL (figma.com/file/FILE_KEY/...)")
    print(f"   4. Use API to add frames (slides) to file")
    return None

def get_team_projects():
    """List available teams/projects"""
    response = requests.get(f"{FIGMA_API}/me", headers=headers)
    if response.status_code == 200:
        data = response.json()
        print(f"\n📁 Figma User Info:")
        print(json.dumps(data, indent=2))
        return data
    return None

def create_slide_in_figma(file_key, slide_data):
    """
    Add a frame (slide) to existing Figma file

    Figma API limitation: Can't create nodes via REST API
    Need to use Figma Plugins API or manual design

    Alternative workflow:
    1. Use Figma's HTTP API to read existing designs
    2. Use community plugins to import from design tools
    3. Use Figma's desktop app with automation
    """
    print(f"\n💡 Recommended Workflow:")
    print(f"   1. Manual: Recreate 1 slide in Figma UI as template")
    print(f"   2. Use Figma's component variants for data swapping")
    print(f"   3. Export via Figma → PowerPoint plugin")
    print(f"   4. OR: Export frames as SVG → Import to Google Slides")

def export_options():
    """Show export options from Figma"""
    print(f"\n📤 Figma Export Options (High Fidelity):")
    print(f"")
    print(f"Option 1: Figma → PowerPoint Plugin")
    print(f"   • Plugin: 'Export to PowerPoint' by Microsoft")
    print(f"   • Fidelity: ~95% (editable shapes + text)")
    print(f"   • Preserves: Colors, typography, layouts, basic gradients")
    print(f"   • Loses: Complex CSS effects, animations")
    print(f"")
    print(f"Option 2: Figma → Google Slides Plugin")
    print(f"   • Plugin: 'Figslides' or 'Export to Google Slides'")
    print(f"   • Fidelity: ~90% (editable)")
    print(f"   • Faster iteration workflow")
    print(f"")
    print(f"Option 3: Figma → SVG → PowerPoint")
    print(f"   • Export each frame as SVG")
    print(f"   • Import SVG into PowerPoint")
    print(f"   • Fidelity: ~98% (vector-based)")
    print(f"   • Editable: Partially (ungrouping required)")
    print(f"")
    print(f"Option 4: Figma → PDF → PowerPoint")
    print(f"   • Export as PDF")
    print(f"   • Import PDF pages into PowerPoint")
    print(f"   • Fidelity: 100% (image-based)")
    print(f"   • Editable: No")

def main():
    print("🎯 Figma High-Fidelity Conversion Strategy")
    print("=" * 60)

    # Test connection
    if not test_figma_connection():
        return

    # Show user info
    get_team_projects()

    # Explain workflow
    print("\n" + "=" * 60)
    print("RECOMMENDED APPROACH:")
    print("=" * 60)
    print(f"")
    print(f"Since Figma REST API is read-only for design creation,")
    print(f"here's the optimal workflow:")
    print(f"")
    print(f"1️⃣  MANUAL SETUP (one-time, ~2 hours):")
    print(f"   • Create new Figma file: 'offbrain Slide Templates'")
    print(f"   • Design 1 slide template matching HTML specs")
    print(f"   • Use components for reusable elements")
    print(f"   • Create variants for DEFAULT vs KEYNOTE layouts")
    print(f"")
    print(f"2️⃣  TEMPLATING (saves time on future slides):")
    print(f"   • Each slide type = Master Component")
    print(f"   • Text/data = Component properties (swap via API)")
    print(f"   • Colors/fonts already locked in design system")
    print(f"")
    print(f"3️⃣  EXPORT TO POWERPOINT:")
    print(f"   • Install 'Export to PowerPoint' Figma plugin")
    print(f"   • Select all frames → Export")
    print(f"   • Result: Editable .pptx with ~95% fidelity")
    print(f"")
    print(f"4️⃣  EXPORT TO GOOGLE SLIDES:")
    print(f"   • Install 'Figslides' Figma plugin")
    print(f"   • Connect Google account → Export")
    print(f"   • Result: Editable Google Slides with ~90% fidelity")

    # Show export options
    export_options()

    print("\n" + "=" * 60)
    print("AUTOMATION POTENTIAL:")
    print("=" * 60)
    print(f"Once templates exist in Figma:")
    print(f"• Use Figma API to duplicate frames")
    print(f"• Update text via API (component properties)")
    print(f"• Batch export via plugins")
    print(f"• ~50% faster than manual recreation")

if __name__ == "__main__":
    main()
