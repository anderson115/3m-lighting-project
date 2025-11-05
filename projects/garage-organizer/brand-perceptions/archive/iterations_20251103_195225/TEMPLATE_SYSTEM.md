# offbrain Design System - Template Architecture

**Status:** Two template styles established with full content implementation

---

## 🎨 Design System Foundation

### Locked Design Decisions
- ✅ **Colors:** Charcoal (#2D3748) primary, Teal (#14B8A6) accent
- ✅ **Typography:** Inter font family (400/500/600/700/800/900 weights)
- ✅ **Aesthetic:** BOLD (dramatic shadows, heavy weights, strong gradients)
- ✅ **Canvas:** 1920×1080px (16:9), 80px margins, 1760×920px content area

---

## 📋 Template System

### Template 1: **Default** (Two-Column Classic)
**Positioning:** Standard consulting format for versatile use

**Structure:**
- 50/50 column split (800px + 900px)
- Left column: Narrative content
- Right column: Data visualizations
- Horizontal eye movement

**Visual Language:**
- Traditional section headers with uppercase + letter-spacing
- Hard Truth panel: Dark gradient background with border-left accent
- Data presented in tables, grids, and structured layouts
- Clean separation between narrative and data zones

**Best For:**
- Multi-client template system
- Conservative corporate audiences
- Standard consulting engagements
- High data density requirements
- 15-20 slide decks with balanced narrative/data

---

### Template 2: **Keynote** (Asymmetric Dynamic)
**Positioning:** High-impact format for executive presentations

**Structure:**
- 2/3 + 1/3 asymmetric split (1100px main + 612px sidebar)
- Main column: Large dark insight cards
- Right sidebar: Vertical stat blocks
- Magazine editorial layout

**Visual Language:**
- Dark gradient cards for all narrative sections
- Light cards for Provocation and Conversation sections
- Compact data presentation in sidebar stat blocks
- Headline with border-left accent for editorial feel
- Dramatic contrast between dark insights and light sections

**Best For:**
- High-impact executive presentations
- C-suite/board audiences
- When standing out from competitors matters
- Narrative-driven strategic insights
- Modern consulting positioning

---

## 📊 Implemented Slides

### Slide 1: Command Brand Perception

**Content Type:** Narrative-heavy with single data comparison

**Components:**
- Balance scale visualization (weighted circles, gradient beam)
- 2-row data table
- Sentiment distribution bar chart
- Pattern, Hard Truth, Provocation, Conversation Starters sections

**Files:**
- `FULL_SLIDE_V1.html` (Default template)
- `FULL_SLIDE_V2.html` (Keynote template)

**Layout Complexity:** Medium
- Single primary visualization (balance scale)
- Straightforward data presentation
- Focus on narrative storytelling

---

### Slide 3: Market Application Landscape

**Content Type:** Complex data comparison with multiple brands

**Components:**
- Brand territory grid/mapping (3 brands)
- Use case distribution statistics (percentages)
- Opportunity zones callout box
- Pattern, Insight, Hard Truth, Provocation, Conversation Starters sections

**Files:**
- `SLIDE3_DEFAULT.html` (Default template)
- `SLIDE3_KEYNOTE.html` (Keynote template)

**Layout Complexity:** High
- Multiple data comparisons
- Territory/segmentation visualization
- Structured brand comparison
- More complex information architecture

---

## 🔧 Component Library

### Narrative Components

**1. Pattern Section** (✱ icon)
- Purpose: Factual observation without judgment
- Style: Neutral gray icon, regular weight body text
- Both templates: Similar treatment

**2. Insight Section** (✱ icon)
- Purpose: Key pattern highlighting
- Style: Same as Pattern section
- Both templates: Similar treatment

**3. Hard Truth Panel**
- Purpose: Uncomfortable but data-supported insight
- **Default:** Dark panel with diamond icon (rotated square)
- **Keynote:** Dark gradient card with teal header
- Both include explanation text with highlighted keywords

**4. Provocation Question** (? icon)
- Purpose: Strategic question worth exploring
- Both templates: Circular teal badge with question mark
- Include "Consider:" subheader and bullet points

**5. Conversation Starters** (→ arrows)
- Purpose: Entry points for strategic discussion
- Both templates: Arrow-prefixed list items
- Strategic questions framed for client discussion

---

### Data Visualization Components

**Balance Scale** (Slide 1)
- Fulcrum (triangle), beam (gradient), platforms (gradient bars)
- Weighted circles showing imbalance (radial gradients)
- Labels positioned below platforms
- **Default:** Full-size implementation
- **Keynote:** Compact version in sidebar stat block

**Data Table/Grid**
- **Default:** Full table with rows and borders
- **Keynote:** Data pills or compact list format

**Sentiment Bar Chart**
- Horizontal segmented bar with percentages
- 3 segments: Neutral (gray), Positive (teal), Negative (charcoal)
- Labels below or inline depending on space
- Rounded corners with border and shadow

**Brand Territory Grid** (Slide 3)
- **Default:** Horizontal grid layout with labeled rows
- **Keynote:** Vertical compact list in stat block

**Use Case Statistics**
- **Default:** Table-style rows with large accent numbers
- **Keynote:** Pill-style cards with numbers on right

**Opportunity Zones**
- Green gradient background with teal border
- Bullet list with circle markers
- **Default:** Larger standalone box
- **Keynote:** Nested within stat block

---

## 📐 Layout Adaptation Rules

### How Default Template Handles Different Content

**Narrative-Heavy (Slide 1):**
- Left: 4 narrative sections stacked
- Right: Visualizations stacked vertically
- Balanced information density

**Data-Heavy (Slide 3):**
- Left: Condensed narrative sections
- Right: Multiple data components stacked
- Grid/table structures for comparisons
- Still maintains 800/900px split

### How Keynote Template Handles Different Content

**Narrative-Heavy (Slide 1):**
- Main: Large dark insight cards (Pattern, Hard Truth)
- Main: Light cards (Provocation, Conversation Starters)
- Sidebar: Data visualizations in stat blocks
- Dramatic visual hierarchy

**Data-Heavy (Slide 3):**
- Main: Still uses dark/light card alternation
- Sidebar: Multiple stat blocks stacked
- Compact data presentation in pills/lists
- Maintains editorial feel despite data complexity

---

## 🎯 Design System Principles

### Visual Hierarchy
1. Headline (36pt, 900 weight) - sets strategic context
2. Section headers (11-12pt, 800 weight, uppercase, teal accent)
3. Body text (13-14pt, 400-500 weight, readable line height)
4. Data callouts (22-28pt, 900 weight, teal accent)

### Color Usage
- **Primary (Charcoal #2D3748):** Headers, dark panels, professional grounding
- **Accent (Teal #14B8A6):** Attention, data emphasis, borders, icons
- **Text (#1A202C):** Body copy, readable
- **Light (#4A5568):** Supporting text, de-emphasized content

### Spacing System
- Section margins: 32-36pt between major sections
- Internal padding: 22-36px within cards/panels
- Gap between columns: 48-60px
- Consistent 80px canvas margins

### Shadow Strategy (BOLD aesthetic)
- Heavy shadows: `0 12px 32px rgba(45, 55, 72, 0.4)` for dark cards
- Medium shadows: `0 8px 24px` for panels and elevated elements
- Light shadows: `0 4px 12px` for subtle elevation
- Icon glows: `0 6px 16px` with color-matched rgba

### Typography Scale
- **Headline:** 36pt / 900 weight / -0.04em letter-spacing
- **Section Header:** 11-12pt / 800 weight / 0.12em letter-spacing / uppercase
- **Body Text:** 13-14pt / 400-500 weight / 21-23pt line-height
- **Card Text:** 14-16pt / 500-700 weight / 23-24pt line-height
- **Data Value:** 22-28pt / 900 weight (Default), 24-42pt (Keynote sidebar)
- **Data Label:** 10-12pt / 600-700 weight

---

## 📂 File Structure

### Slide 1 Files
- `FULL_SLIDE_V1.html` - Default template
- `FULL_SLIDE_V2.html` - Keynote template
- `FULL_SLIDE_V3.html` - Centered Minimal (alternate, not in template system)
- `FULL_SLIDES_COMPARISON.html` - Side-by-side viewer

### Slide 3 Files
- `SLIDE3_DEFAULT.html` - Default template
- `SLIDE3_KEYNOTE.html` - Keynote template
- `SLIDE3_COMPARISON.html` - Side-by-side viewer

### Design Documentation
- `TEMPLATE_SYSTEM.md` - This file (architecture overview)
- `FULL_SLIDES_NOTES.md` - Slide 1 layout comparison notes
- `LAYOUT_NOTES.md` - Original 4-layout comparison notes
- `FONT_NOTES.md` - Font selection rationale
- `COLOR_SCHEMES.md` - Color palette development

### Design Iterations (Archive)
- `slide1_test.html` - First iteration (62/100 score)
- `slide1_v2.html` - Second iteration (87/100 score)
- `slide1_FINAL.html` - Final iteration (94/100 score)
- `color_*.html` - 5 color scheme options
- `typo_*.html` - 3 typography variations
- `LAYOUT_COMPARISON.html` - 4 layout structure options
- `FONT_COMPARISON.html` - 4 font family options

---

## 🚀 Next Steps

### Immediate
1. **Build Slide 2** (Scotch brand perception) in both templates
   - Content available in `SLIDE_TESTS_v3.md`
   - Different layout requirements than Slides 1 or 3
   - Test template system with another content type

2. **Refine based on feedback**
   - User will provide direction on iterations needed
   - Adjust components, spacing, or visual treatments

### Design System Export
Once all 3 slides approved:
1. Extract component specifications
2. Document spacing system
3. Create typography scale reference
4. Export color variables
5. Provide layout grid measurements
6. Hand off to Figma designer for component library

### Production Implementation
After Figma components built:
1. Create PowerPoint master slides
2. Build component library in PPT
3. Document slide creation workflow
4. Train team on template usage

---

## 💡 Template Selection Guidance

### Use Default Template When:
- Building multi-client decks
- Presenting to conservative audiences
- Need high data density (15-20+ slides)
- Want safe, proven consulting format
- Bain/BCG standard aesthetic desired

### Use Keynote Template When:
- Presenting to C-suite/board
- Want to stand out from competitors
- Content is narrative-driven with data support
- Modern, confident positioning matters
- Bloomberg Businessweek editorial feel desired

### Mix Both Templates When:
- Opening/closing slides: Keynote for impact
- Detailed analysis: Default for data density
- Creates visual variety while maintaining cohesion

---

**Design System Version:** 1.0
**Last Updated:** 2025-11-03
**Templates Established:** 2 (Default, Keynote)
**Slides Implemented:** 2 (Slide 1, Slide 3)
**Remaining:** Slide 2 (Scotch brand)
