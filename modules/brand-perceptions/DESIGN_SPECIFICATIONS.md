# Phase 2 Analysis: Visual Design Specifications
## Design System and Slide Execution Guide

**Purpose:** Complete visual design specifications for 3 test slides. This document provides pixel-perfect specs that a designer can execute in PowerPoint/Keynote with zero ambiguity.

**Deck Format:** Standard 16:9 presentation (1920×1080px or 10×5.625" at 192 DPI)

---

# 1. DESIGN SYSTEM FOUNDATION

## 1.1 Typography System

### Primary Font Stack
**Recommended:** Inter or Helvetica Neue (clean, professional, corporate-friendly)
**Fallback:** Arial, system-ui

### Type Scale and Hierarchy

| Element | Font | Size | Weight | Line Height | Color | Usage |
|---------|------|------|--------|-------------|-------|-------|
| **Slide Title** | Inter | 32pt | Bold (700) | 38pt | #111827 | Main headline |
| **Section Header** | Inter | 20pt | Semibold (600) | 26pt | #374151 | Major sections with icons |
| **Subsection** | Inter | 16pt | Semibold (600) | 22pt | #4B5563 | Minor divisions |
| **Body Text** | Inter | 14pt | Regular (400) | 20pt | #1F2937 | Primary narrative content |
| **Supporting Data** | Inter | 12pt | Regular (400) | 18pt | #6B7280 | Data callouts, explanations |
| **Data Labels** | Inter | 11pt | Medium (500) | 14pt | #374151 | Chart labels, annotations |
| **Footnotes** | Inter | 10pt | Regular (400) | 14pt | #9CA3AF | Source citations |

### Text Treatment Rules
- **Maximum line length:** 80 characters for body text (readability)
- **Paragraph spacing:** 16pt between paragraphs
- **List spacing:** 8pt between list items
- **Emphasis:** Use semibold weight, NOT italics or underline
- **Quotes:** Use typographic quotes "" not straight quotes ""

---

## 1.2 Color Palette

### Primary Colors

| Color Name | Hex Code | RGB | Usage | Sample |
|------------|----------|-----|-------|--------|
| **Deep Gray** | #111827 | 17, 24, 39 | Headlines, primary text | ████ |
| **Slate Gray** | #374151 | 55, 65, 81 | Section headers, icons | ████ |
| **Medium Gray** | #6B7280 | 107, 114, 128 | Supporting text, data | ████ |
| **Light Gray** | #9CA3AF | 156, 163, 175 | Footnotes, subtle elements | ████ |
| **Blue Primary** | #1E3A8A | 30, 58, 138 | Hard Truth icon, emphasis | ████ |
| **Amber Accent** | #F59E0B | 245, 158, 11 | Provocation icon, highlights | ████ |
| **Teal Support** | #0891B2 | 8, 145, 178 | Data visualization accent | ████ |
| **Background** | #FFFFFF | 255, 255, 255 | Slide background | ████ |
| **Panel BG** | #F9FAFB | 249, 250, 251 | Content boxes, panels | ████ |

### Usage Rules
- **Never use pure black (#000000)** - too harsh, use Deep Gray (#111827)
- **Never use pure red** - too alarmist, use amber for warnings
- **Data visualization:** Use Blue Primary, Teal Support, and Medium Gray
- **Backgrounds:** White default, Light Panel BG for boxes/callouts
- **Text on colored backgrounds:** Ensure 4.5:1 contrast ratio minimum (WCAG AA)

---

## 1.3 Icon System

### Icon Specifications

**🔷 HARD TRUTH (Blue Diamond)**
```
Shape: Diamond (rotated 45° square)
Size: 24pt × 24pt
Fill: #1E3A8A (Blue Primary)
Border: None
Position: Upper-left of callout box, 16pt margin
Style: Solid fill, sharp corners
```

**❓ PROVOCATION (Question Mark in Circle)**
```
Shape: Circle with centered question mark
Size: 24pt diameter
Fill: #FEF3C7 (Light Amber background)
Border: 2pt solid #F59E0B (Amber Accent)
Question Mark: #92400E (Dark Amber), 16pt, bold
Position: Inline with section header, left-aligned
Style: Soft, inviting appearance
```

**→ CONVERSATION STARTER (Arrow)**
```
Shape: Right-pointing arrow
Size: 18pt × 12pt
Fill: #6B7280 (Medium Gray)
Border: None
Position: Bullet list leader, 8pt before text
Style: Simple, clean arrow (not decorative)
```

**✱ INSIGHT (Asterisk)**
```
Shape: Six-pointed asterisk
Size: 18pt × 18pt
Fill: #374151 (Slate Gray)
Position: Section header prefix, 8pt before text
Style: Neutral, factual marker
```

### Icon Usage Rules
- Icons are **semantic signals**, not decoration
- Use sparingly (1-2 per slide maximum)
- Always pair with accompanying text label
- Maintain consistent sizing across all slides
- Never stack icons (one icon per section)

---

## 1.4 Layout Grid System

### Slide Canvas
- **Dimensions:** 1920px × 1080px (16:9)
- **Safe margins:** 80px from all edges
- **Content area:** 1760px × 920px (usable space)

### Grid Structure
```
┌─────────────────────────────────────────────────────────────┐
│ 80px margin                                        80px      │
│   ┌─────────────────────────────────────────────┐           │
│   │                                             │           │
│ 8 │  HEADLINE ZONE (200px height)               │ 80px      │
│ 0 │                                             │           │
│ p ├─────────────────────────────────────────────┤ margin    │
│ x │                                             │           │
│   │  CONTENT ZONE (640px height)                │           │
│ m │  - Left column: 800px wide                  │           │
│ a │  - Gutter: 60px                             │           │
│ r │  - Right column: 900px wide                 │           │
│ g │                                             │           │
│ i │                                             │           │
│ n ├─────────────────────────────────────────────┤           │
│   │  FOOTER ZONE (80px height)                  │           │
│   │  - Source citations, page numbers           │           │
│   └─────────────────────────────────────────────┘           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Column System
- **Two-column layout:** 800px + 60px gutter + 900px = 1760px
- **Left column (800px):** Narrative content, story
- **Right column (900px):** Data visualization, supporting evidence
- **Single column:** Full 1760px width for unified content

### Spacing Standards
- **Section spacing:** 32pt between major sections
- **Paragraph spacing:** 16pt between paragraphs
- **List item spacing:** 8pt between items
- **Icon-to-text spacing:** 8pt horizontal gap
- **Chart-to-caption:** 12pt vertical gap

---

## 1.5 Data Visualization Standards

### Chart Color Palette
- **Primary series:** #1E3A8A (Blue Primary)
- **Secondary series:** #0891B2 (Teal Support)
- **Tertiary series:** #6B7280 (Medium Gray)
- **Comparison/negative:** #F59E0B (Amber Accent) - NOT red

### Chart Guidelines
- **No 3D effects** - flat, clean design only
- **No gradients** - solid colors only
- **Grid lines:** Light Gray (#E5E7EB), 0.5pt weight
- **Axis labels:** 11pt, Medium Gray
- **Data labels:** 12pt, positioned above bars/points
- **Legend:** Bottom-right, 12pt, horizontal orientation

### Chart Types for This Deck
1. **Horizontal bar charts** - Comparing metrics across brands
2. **Grouped column charts** - Multiple series side-by-side
3. **Simple comparison tables** - Text-based data with visual weight
4. **Proportional shapes** - Circles or rectangles sized by value
5. **Venn diagrams** - Overlapping territories (simplified, 3 circles max)

---

# 2. SLIDE 1 DESIGN SPECIFICATIONS
## Command Brand Perception - Promise-Reality Tension

### Slide Layout Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                                                                  │
│  HEADLINE (32pt Bold, Deep Gray)                                 │
│  Command's Market Presence is Strong, But Creator               │
│  Discussions Reveal a Tension Worth Exploring                    │
│                                                                  │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  LEFT COLUMN (800px)           │  RIGHT COLUMN (900px)           │
│                                │                                 │
│  ✱ THE PATTERN                 │  [VISUAL: Balance Scale]        │
│  [Narrative text, 14pt]        │   Left side: "Surface Damage    │
│  [3-4 lines describing         │   Discussions"                  │
│  observation]                  │   Right side: "Damage-Free      │
│                                │   Benefits"                     │
│  ────────────────────          │   [Tilted left showing          │
│                                │   imbalance]                    │
│  🔷 HARD TRUTH                 │                                 │
│  [Bold callout in panel]       │  [DATA TABLE below scale]       │
│  [2-3 lines, high impact]      │  ┌────────────────────────┐    │
│                                │  │ Discussion Type │Videos│    │
│  [Why it matters, 12pt]        │  ├────────────────────────┤    │
│                                │  │Surface Damage   │  24  │    │
│  ────────────────────          │  │Damage-Free Emphasis 11 │    │
│                                │  └────────────────────────┘    │
│  ❓ PROVOCATION                │                                 │
│  "Are claims setting           │  [SENTIMENT DISTRIBUTION]       │
│  expectations too high?"       │  Neutral: ███████████ 84%      │
│                                │  Positive: ██ 6.5%              │
│  Consider:                     │  Negative: ██ 6.5%              │
│  • Option A [one line]         │                                 │
│  • Option B [one line]         │                                 │
│  • Option C [one line]         │                                 │
│                                │                                 │
│  ────────────────────          │                                 │
│                                │                                 │
│  → CONVERSATION STARTERS       │                                 │
│  → [Question 1]                │                                 │
│  → [Question 2]                │                                 │
│  → [Question 3]                │                                 │
│                                │                                 │
├──────────────────────────────────────────────────────────────────┤
│  Source: Phase 2 Analysis, 62 Command videos  │  Slide 1 of 3  │
└──────────────────────────────────────────────────────────────────┘
```

### Element-by-Element Specifications

#### HEADLINE
- **Text:** "Command's Market Presence is Strong, But Creator Discussions Reveal a Tension Worth Exploring"
- **Font:** Inter Bold, 32pt
- **Color:** #111827 (Deep Gray)
- **Position:** 80px from top, 80px from left, full width
- **Alignment:** Left-aligned
- **Line height:** 38pt (allows for two lines if needed)

#### LEFT COLUMN CONTENT

**✱ THE PATTERN Section**
- **Header:** "THE PATTERN" with ✱ icon (18pt, #374151)
- **Icon position:** 8pt before text
- **Body text:** 14pt regular, #1F2937, line height 20pt
- **Content width:** 800px
- **Paragraph:** 3-4 sentences describing observation
- **Spacing below:** 32pt

**🔷 HARD TRUTH Panel**
- **Background:** #F9FAFB (light panel)
- **Padding:** 20px all sides
- **Border:** 3pt left border, #1E3A8A (Blue Primary)
- **Icon:** 🔷 24pt, positioned top-left with 16px internal margin
- **Header:** "HARD TRUTH" 16pt semibold, #374151, 8pt after icon
- **Main text:** 14pt semibold, #111827, 2 lines maximum
- **Supporting text:** "This matters because:" 12pt regular, #6B7280
- **Width:** 760px (800px - 20px padding each side)
- **Spacing below:** 32pt

**❓ PROVOCATION Section**
- **Icon:** ❓ 24pt diameter circle, positioned inline with header
- **Question:** 16pt semibold, #111827
- **"Consider:" subheader:** 14pt regular, #4B5563
- **Option list:** 14pt regular, #1F2937
  - Bullet style: Small disc, #6B7280
  - 8pt spacing between items
  - Indented 16pt from margin
- **Spacing below:** 32pt

**→ CONVERSATION STARTERS Section**
- **Header:** "CONVERSATION STARTERS" 16pt semibold, #374151
- **Arrow icons:** → 18pt × 12pt, #6B7280, 8pt before each item
- **Questions:** 14pt regular, #1F2937
- **Format:** Each question on separate line, 8pt spacing
- **Styling:** Questions phrased to invite discussion

#### RIGHT COLUMN CONTENT

**Balance Scale Visual**
- **Position:** Top of right column, centered horizontally
- **Dimensions:** 400px wide × 300px tall
- **Style:** Simple, clean illustration (not photorealistic)
- **Components:**
  - Fulcrum: Centered triangle, #374151
  - Beam: Horizontal line, 2pt weight, #6B7280
  - Left platform: "Surface Damage Discussions" label below
  - Right platform: "Damage-Free Benefits" label below
  - Tilt: 15° angle, left side lower (showing imbalance)
- **Colors:**
  - Left side: #F59E0B (Amber) - higher weight
  - Right side: #1E3A8A (Blue) - lighter weight
- **Labels:** 12pt medium, centered under platforms

**Data Table**
- **Position:** Below balance scale, 24pt vertical gap
- **Dimensions:** 400px wide
- **Style:** Clean, minimal borders
- **Structure:**
  ```
  ┌─────────────────────────┬────────┐
  │ Discussion Type         │ Videos │
  ├─────────────────────────┼────────┤
  │ Surface Damage          │   24   │
  │ Damage-Free Emphasis    │   11   │
  └─────────────────────────┴────────┘
  ```
- **Header row:**
  - Background: #F9FAFB
  - Text: 12pt semibold, #374151
  - Padding: 12pt vertical, 16pt horizontal
- **Data rows:**
  - Text: 14pt regular, #1F2937
  - Numbers: 14pt medium, #111827, right-aligned
  - Padding: 10pt vertical, 16pt horizontal
  - Border: 1pt bottom border, #E5E7EB
- **Border:** 2pt top border #1E3A8A, 1pt other borders #E5E7EB

**Sentiment Distribution Bar**
- **Position:** Below data table, 24pt vertical gap
- **Dimensions:** 400px wide × 120px tall
- **Title:** "Sentiment Distribution" 12pt medium, #374151
- **Bar style:** Horizontal stacked bar
  - Total width: 100%
  - Height: 40pt
  - Rounded corners: 4pt
- **Segments:**
  - Neutral: 84%, #6B7280 (Medium Gray)
  - Positive: 6.5%, #1E3A8A (Blue Primary)
  - Negative: 6.5%, #F59E0B (Amber Accent)
- **Labels:**
  - Inside bars if >10% width: white text, 12pt medium
  - Outside bars if <10%: colored text matching segment, 11pt
  - Format: "Neutral 84%" "Positive 6.5%" "Negative 6.5%"

#### FOOTER
- **Position:** 80px from bottom, full width
- **Left side:** "Source: Phase 2 Analysis, 62 Command videos" 10pt regular, #9CA3AF
- **Right side:** "Slide 1 of 3" 10pt regular, #9CA3AF
- **Divider line:** 1pt horizontal line above footer, #E5E7EB, 16pt gap above text

---

## 2.1 Slide 1 Execution Notes for Designer

### PowerPoint/Keynote Build Instructions

1. **Set up master slide:**
   - Slide size: 16:9 (1920×1080 or equivalent)
   - Background: White (#FFFFFF)
   - Margins: 80px all sides

2. **Create headline:**
   - Text box spanning full width
   - Apply headline typography specs
   - Ensure text wraps cleanly to 2 lines if needed

3. **Create two-column layout:**
   - Left column: 800px starting at 80px from left
   - Right column: 900px starting at 940px from left (800 + 60 + 80)
   - Both columns start 280px from top (after headline zone)

4. **Left column content:**
   - Insert ✱ icon (can use text asterisk or custom SVG)
   - Create "THE PATTERN" section with body text
   - Create Hard Truth panel:
     - Insert rectangle shape (760px wide)
     - Apply background color #F9FAFB
     - Add 3pt left border #1E3A8A
     - Add 🔷 icon using custom shape (diamond, rotated square)
     - Add text with proper hierarchy
   - Create Provocation section with ❓ icon
   - Create Conversation Starters with → bullets

5. **Right column content:**
   - Create balance scale visual:
     - Use PowerPoint shapes (triangles, rectangles, lines)
     - Group elements together
     - Ensure 15° tilt is applied to beam
   - Create data table:
     - Use PowerPoint table (2 columns × 3 rows including header)
     - Apply cell formatting and borders
   - Create sentiment bar chart:
     - Use stacked bar chart type
     - Adjust colors to match spec
     - Position labels appropriately

6. **Footer:**
   - Add divider line across full width
   - Add source citation (left-aligned)
   - Add page number (right-aligned)

### Quality Checklist
- [ ] All text uses Inter font (or specified fallback)
- [ ] All colors match hex codes exactly
- [ ] Icon sizes are consistent (24pt for major icons, 18pt for arrows)
- [ ] Spacing between sections is 32pt
- [ ] Balance scale shows clear visual imbalance
- [ ] Data table is easy to read and scan
- [ ] Sentiment bar proportions are accurate
- [ ] Footer is subtle but readable
- [ ] No elements touch slide edges (80px margins enforced)
- [ ] Text is legible when projected (minimum 12pt)

---

# 3. SLIDE 2 DESIGN SPECIFICATIONS
## Scotch Performance Perception - Advocacy with Boundaries

### Slide Layout Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                                                                  │
│  HEADLINE (32pt Bold, Deep Gray)                                 │
│  Scotch Demonstrates Strong Creator Advocacy—Understanding       │
│  Where It Shines and Where It's Challenged                       │
│                                                                  │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  FULL WIDTH CONTENT                                              │
│                                                                  │
│  ✱ THE PATTERN                                                   │
│  [Narrative paragraph, 14pt, ~600px wide, left-aligned]          │
│  [3-4 sentences about advocacy pattern]                          │
│                                                                  │
│  ──────────────────────────────────────────────────────          │
│                                                                  │
│  THREE-COLUMN SENTIMENT COMPARISON                               │
│                                                                  │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐                   │
│  │ COMMAND   │  │ SCOTCH    │  │ 3M CLAW   │                   │
│  │           │  │           │  │           │                   │
│  │ Positive  │  │ Positive  │  │ Positive  │                   │
│  │  6.5%     │  │  20.6% ✓  │  │  17.5%    │                   │
│  │           │  │           │  │           │                   │
│  │ Negative  │  │ Negative  │  │ Negative  │                   │
│  │  6.5%     │  │  1.5% ✓   │  │  4.8%     │                   │
│  │           │  │           │  │           │                   │
│  │ Pattern:  │  │ Pattern:  │  │ Pattern:  │                   │
│  │ Polarized │  │ Strong    │  │ Favorable │                   │
│  │           │  │ Advocacy  │  │           │                   │
│  └───────────┘  └───────────┘  └───────────┘                   │
│                                                                  │
│  ──────────────────────────────────────────────────────          │
│                                                                  │
│  LEFT COLUMN (800px)           │  RIGHT COLUMN (900px)           │
│                                │                                 │
│  ❓ PROVOCATION                │  [TEMPERATURE CONSIDERATION]    │
│  "Is temperature sensitivity   │   Visual showing:              │
│  fixable or should we          │   - Indoor: High confidence    │
│  transparently communicate?"   │   - Outdoor: Temperature       │
│                                │     consideration              │
│  Consider:                     │                                 │
│  • Option A: Product innovation│  Stats:                        │
│  • Option B: Transparent label │  Temperature mentioned in      │
│  • Option C: Accept boundary   │  ~1 in 6 Scotch videos         │
│                                │                                 │
│  ────────────────────          │  [APPLICATION CONTEXT VISUAL]  │
│                                │  Indoor: ████████████ High     │
│  → CONVERSATION STARTERS       │  Outdoor: ████░░░░░░ Consider  │
│  → [Marketing question]        │                                 │
│  → [Product dev question]      │                                 │
│  → [Strategy question]         │                                 │
│                                │                                 │
├──────────────────────────────────────────────────────────────────┤
│  Source: Phase 2 Analysis, 68 Scotch videos   │  Slide 2 of 3  │
└──────────────────────────────────────────────────────────────────┘
```

### Element-by-Element Specifications

#### HEADLINE
- **Text:** "Scotch Demonstrates Strong Creator Advocacy—Understanding Where It Shines and Where It's Challenged"
- **Font:** Inter Bold, 32pt
- **Color:** #111827 (Deep Gray)
- **Position:** 80px from top, 80px from left, full width
- **Line height:** 38pt

#### THREE-COLUMN SENTIMENT COMPARISON

**Overall Container**
- **Position:** Below headline, 260px from top
- **Dimensions:** 1760px wide × 320px tall
- **Spacing:** Three equal columns with 40px gutters

**Individual Column Specs**
- **Width:** 560px each (1760 - 80 gutters = 1680 / 3 = 560)
- **Background:** #F9FAFB (light panel)
- **Border:** 2pt top border
  - Command: #6B7280 (Medium Gray)
  - Scotch: #1E3A8A (Blue Primary) - highlight as winner
  - 3M Claw: #6B7280 (Medium Gray)
- **Padding:** 24pt all sides
- **Border radius:** 8pt corners

**Column Content Structure**
- **Brand name:** 18pt semibold, #374151, centered
- **Spacing:** 16pt below brand name

**Metric Display (Positive & Negative)**
- **Label:** 12pt medium, #6B7280
- **Value:** 28pt bold, color-coded:
  - Positive values: #1E3A8A (Blue Primary)
  - Negative values: #6B7280 (Medium Gray)
- **Spacing:** 8pt between label and value, 20pt between metrics

**Winner Indicator**
- **Symbol:** ✓ checkmark, 18pt
- **Color:** #1E3A8A (Blue Primary)
- **Position:** Right-aligned next to Scotch values

**Pattern Summary**
- **Label:** "Pattern:" 12pt medium, #6B7280
- **Description:** 14pt semibold, #111827
- **Spacing:** 16pt above from last metric

**Scotch Column Emphasis**
- **Slightly elevated:** 4pt shadow, rgba(0,0,0,0.05)
- **Border:** 2pt instead of 1pt on other columns
- **Background:** Pure white (#FFFFFF) instead of light panel

#### LEFT COLUMN CONTENT (below comparison)

**❓ PROVOCATION Section**
- **Position:** 620px from top (after 320px comparison + 80px spacing)
- **Width:** 800px
- **Icon:** ❓ 24pt, positioned inline
- **Question:** 16pt semibold, #111827, wrapped to 2-3 lines
- **"Consider:" subheader:** 14pt regular, #4B5563, 12pt spacing above
- **Options list:**
  - 13pt regular, #1F2937
  - Bullet style: Small disc
  - 8pt spacing between items
  - Each option 1-2 lines maximum

**→ CONVERSATION STARTERS Section**
- **Position:** Below Provocation, 32pt spacing
- **Header:** "CONVERSATION STARTERS" 16pt semibold, #374151
- **Questions:**
  - Arrow prefix: → 18pt, #6B7280
  - Text: 13pt regular, #1F2937
  - Categorized by audience:
    - "For Marketing:" in italics before marketing question
    - "For Product Dev:" in italics before product question
    - "For Strategy:" in italics before strategy question
  - 12pt spacing between questions

#### RIGHT COLUMN CONTENT

**Temperature Consideration Panel**
- **Position:** Aligned with Provocation section (620px from top)
- **Dimensions:** 900px wide × 280px tall
- **Background:** #F9FAFB with 8pt radius
- **Padding:** 24pt

**Title**
- **Text:** "Application Context: Temperature Consideration"
- **Font:** 16pt semibold, #374151
- **Spacing below:** 16pt

**Visual: Indoor vs Outdoor Confidence**
- **Style:** Horizontal bars showing confidence levels
- **Dimensions:** Full panel width minus padding

**Indoor Application Bar:**
```
Label: "Indoor Applications"    [12pt medium, #374151]
Bar: ████████████████ (85% fill) [#1E3A8A]
Text on bar: "High confidence"   [12pt medium, white]
```

**Outdoor Application Bar:**
```
Label: "Outdoor Applications"   [12pt medium, #374151]
Bar: ████████░░░░░░░ (55% fill) [#F59E0B]
Text on bar: "Temperature consideration" [11pt medium, #92400E]
```

**Bar Specifications:**
- **Height:** 48pt each
- **Spacing between:** 16pt
- **Border radius:** 6pt
- **Background (unfilled portion):** #E5E7EB

**Supporting Stat Callout**
- **Position:** Below bars, 16pt spacing
- **Text:** "Temperature mentioned in ~1 in 6 Scotch videos"
- **Font:** 12pt regular, #6B7280
- **Style:** Italicized
- **Icon:** Small thermometer icon (16pt) before text

#### FOOTER
- Same specifications as Slide 1
- **Source text:** "Source: Phase 2 Analysis, 68 Scotch videos"
- **Page number:** "Slide 2 of 3"

---

## 3.1 Slide 2 Execution Notes for Designer

### PowerPoint/Keynote Build Instructions

1. **Create three-column comparison:**
   - Use three rectangle shapes with rounded corners
   - Position with 40px gutters
   - Apply background colors and borders per spec
   - Scotch column gets subtle shadow effect
   - Add text boxes for each metric with proper formatting
   - Insert ✓ checkmark symbols next to Scotch's winning metrics

2. **Create horizontal confidence bars:**
   - Use PowerPoint bar chart (horizontal orientation)
   - Two series: Indoor and Outdoor
   - Customize colors to match spec
   - Adjust bar widths to show 85% and 55% values
   - Add text labels on bars (white text on filled portion)

3. **Provocation and Conversation sections:**
   - Similar to Slide 1 layout
   - Ensure proper icon placement
   - Format list items with appropriate bullets/arrows

### Quality Checklist
- [ ] Scotch column visually emphasized (shadow, border weight)
- [ ] Checkmarks aligned properly next to Scotch values
- [ ] Confidence bars show accurate proportions (85% and 55%)
- [ ] Text on bars is readable (sufficient contrast)
- [ ] Temperature icon is subtle and professional
- [ ] Three columns are equal width with consistent gutters
- [ ] All spacing matches specifications

---

# 4. SLIDE 3 DESIGN SPECIFICATIONS
## Market Application Landscape - Territories and White Space

### Slide Layout Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                                                                  │
│  HEADLINE (32pt Bold, Deep Gray)                                 │
│  Natural Specialization is Emerging, But Significant             │
│  White Space Remains Unaddressed                                 │
│                                                                  │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ✱ THE PATTERN [Full width, 600px, narrative]                   │
│                                                                  │
│  ──────────────────────────────────────────────────────────      │
│                                                                  │
│  [LARGE VENN DIAGRAM: CENTER OF SLIDE]                           │
│                                                                  │
│       ┌─────────────┐                                            │
│       │  COMMAND    │                                            │
│       │  Territory  │       ┌─────────────┐                     │
│       │             │       │   SCOTCH    │                     │
│       │ • Rental    │       │  Territory  │                     │
│       │ • Temporary │   ┌───┼─────────────┤                     │
│       │ • Damage-   │   │   │ • DIY       │                     │
│       │   Free      │   │   │ • Permanent │                     │
│       └──────┬──────┘   │   │ • Strong    │                     │
│              │          │   │   Hold      │                     │
│              └──────────┴───┴──────┬──────┘                     │
│                   │                │                             │
│              PICTURE HANGING       │                             │
│              (Overlap Zone)        │                             │
│                   │                │                             │
│                   └────────┬───────┘                             │
│                            │                                     │
│                  ┌─────────┴──────────┐                          │
│                  │     3M CLAW        │                          │
│                  │     Territory      │                          │
│                  │                    │                          │
│                  │  • Heavy Items     │                          │
│                  │  • Weight Focus    │                          │
│                  │  • Mirrors         │                          │
│                  └────────────────────┘                          │
│                                                                  │
│  ──────────────────────────────────────────────────────          │
│                                                                  │
│  WHITE SPACE OPPORTUNITIES (Four boxes below diagram)            │
│                                                                  │
│  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐                │
│  │Kitchen │  │Bathroom│  │ Outdoor│  │ Budget │                │
│  │  Org   │  │Storage │  │Extreme │  │Segment │                │
│  │        │  │        │  │Weather │  │        │                │
│  │6% of   │  │Minimal │  │Temp    │  │Price   │                │
│  │content │  │coverage│  │limited │  │resist. │                │
│  └────────┘  └────────┘  └────────┘  └────────┘                │
│                                                                  │
│  🔷 HARD TRUTH: Rental households = 36% of US,                   │
│     but rental content coverage is modest                        │
│                                                                  │
│  → Conversation Starters: [3 strategic questions below]          │
│                                                                  │
├──────────────────────────────────────────────────────────────────┤
│  Source: Phase 2 Analysis, 193 videos all brands │ Slide 3 of 3│
└──────────────────────────────────────────────────────────────────┘
```

### Element-by-Element Specifications

#### HEADLINE
- **Text:** "Natural Specialization is Emerging, But Significant White Space Remains Unaddressed"
- **Font:** Inter Bold, 32pt
- **Color:** #111827 (Deep Gray)
- **Position:** 80px from top, 80px from left
- **Line height:** 38pt

#### ✱ THE PATTERN Section
- **Position:** 200px from top
- **Width:** 1200px (centered)
- **Icon:** ✱ 18pt, #374151
- **Header:** "THE PATTERN" 20pt semibold, #374151
- **Body text:** 14pt regular, #1F2937, line height 20pt
- **Content:** 3-4 sentences introducing territorial pattern
- **Spacing below:** 32pt

#### VENN DIAGRAM - Brand Territories

**Overall Diagram Specifications**
- **Position:** Centered horizontally, 280px from top
- **Dimensions:** 1000px wide × 500px tall
- **Style:** Simplified, clean circles with subtle overlaps

**Circle Specifications:**

**Command Circle (Top Left)**
- **Position:** Upper left of diagram area
- **Diameter:** 320px
- **Fill:** rgba(30, 58, 138, 0.15) - Blue Primary at 15% opacity
- **Border:** 3pt solid #1E3A8A (Blue Primary)
- **Label position:** Inside circle, top portion
  - "COMMAND Territory" 16pt semibold, #1E3A8A
  - Bullet list below (12pt regular, #374151):
    - "• Rental (16 mentions)"
    - "• Temporary"
    - "• Damage-Free (9)"

**Scotch Circle (Top Right)**
- **Position:** Upper right of diagram area
- **Diameter:** 320px
- **Fill:** rgba(8, 145, 178, 0.15) - Teal at 15% opacity
- **Border:** 3pt solid #0891B2 (Teal Support)
- **Label position:** Inside circle, top portion
  - "SCOTCH Territory" 16pt semibold, #0891B2
  - Bullet list below (12pt regular, #374151):
    - "• DIY Projects (34)"
    - "• Permanent"
    - "• Strong Hold (27)"

**3M Claw Circle (Bottom Center)**
- **Position:** Lower center of diagram area
- **Diameter:** 320px
- **Fill:** rgba(107, 114, 128, 0.15) - Medium Gray at 15% opacity
- **Border:** 3pt solid #6B7280 (Medium Gray)
- **Label position:** Inside circle, center portion
  - "3M CLAW Territory" 16pt semibold, #6B7280
  - Bullet list below (12pt regular, #374151):
    - "• Heavy Items (63)"
    - "• Weight Focus"
    - "• Mirrors (18)"

**Overlap Zone (Center)**
- **Position:** Where all three circles intersect
- **Shape:** Irregular polygon (intersection of three circles)
- **Fill:** rgba(245, 158, 11, 0.20) - Amber at 20% opacity
- **Border:** None (defined by circle borders)
- **Label:** Large text in center of overlap
  - "PICTURE HANGING" 18pt bold, #92400E (Dark Amber)
  - "177 mentions" 14pt regular, #92400E
  - "76% of content" 12pt regular, #B45309

**Spacing and Positioning:**
- Command and Scotch circles: Top edges at 280px, separated by 240px centers
- 3M Claw circle: Bottom edge at 720px, centered horizontally
- Circles overlap by approximately 80px to create visible intersection

#### WHITE SPACE OPPORTUNITY BOXES

**Container**
- **Position:** 800px from top (below diagram, 80px spacing)
- **Layout:** Four equal boxes in horizontal row
- **Dimensions:** Each box 400px wide × 140px tall
- **Spacing:** 40px gutters between boxes

**Individual Box Specifications**
- **Background:** #FFFFFF
- **Border:** 2pt solid #E5E7EB
- **Border radius:** 8pt
- **Padding:** 20pt all sides
- **Hover state:** Optional subtle shadow on hover

**Box Content Structure (all four boxes):**

1. **Title line:**
   - Font: 16pt semibold, #374151
   - Position: Top of box

2. **Category:**
   - Font: 14pt regular, #6B7280
   - Position: Below title, 8pt spacing

3. **Key stat:**
   - Font: 13pt medium, #1F2937
   - Position: Below category, 8pt spacing

**Specific Box Content:**

**Box 1: Kitchen Organization**
- Title: "Kitchen Organization"
- Category: "Underserved Application"
- Stat: "6% of current content"
- Note: "High rental pain point"

**Box 2: Bathroom Storage**
- Title: "Bathroom Storage"
- Category: "White Space Opportunity"
- Stat: "Minimal coverage"
- Note: "No-drill + moisture needs"

**Box 3: Outdoor/Extreme Weather**
- Title: "Outdoor Applications"
- Category: "Temperature Limited"
- Stat: "Geographic weak spots"
- Note: "All-temp formulation gap"

**Box 4: Budget Segment**
- Title: "Value Segment"
- Category: "Price Sensitivity Evident"
- Stat: "No brand addresses"
- Note: "Generic competition risk"

#### 🔷 HARD TRUTH Section

**Position:** Below white space boxes, 960px from top
**Layout:** Full width panel

**Panel Specifications:**
- **Background:** #F9FAFB
- **Border:** 3pt left border, #1E3A8A (Blue Primary)
- **Padding:** 20pt all sides
- **Width:** 1760px (full content width)
- **Border radius:** 4pt

**Content:**
- **Icon:** 🔷 24pt, positioned left with 16pt internal margin
- **Text:** 16pt semibold, #111827
  - "Rental households represent approximately 36% of US households, but rental-specific content coverage is modest across all brands."
- **Implication:** 12pt regular, #6B7280, 12pt spacing above
  - "This suggests market opportunity exceeds current content marketing investment."

#### → CONVERSATION STARTERS Section

**Position:** Below Hard Truth, 16pt spacing
**Width:** Full width

**Format:**
- No header (integrate into footer area)
- Three questions in horizontal row
- Each question in its own column (~587px wide with gutters)

**Question Format:**
- **Arrow prefix:** → 18pt, #6B7280
- **Text:** 12pt regular, #1F2937
- **Audience label:** 10pt medium, #F59E0B (Amber), italic
  - "For Portfolio Strategy:" / "For Growth:" / "For Content:"

**Sample Questions:**
1. "Should three brands be viewed as complementary portfolio or competing products?"
2. "Kitchen and bathroom represent daily pain points—who should own this?"
3. "Current coverage: 193 videos. Could ecosystem be 500+ with partnerships?"

#### FOOTER
- **Source:** "Source: Phase 2 Analysis, 193 videos all brands"
- **Page:** "Slide 3 of 3"
- Same specifications as previous slides

---

## 4.1 Slide 3 Execution Notes for Designer

### PowerPoint/Keynote Build Instructions

1. **Create Venn diagram:**
   - Use circle shapes (three circles, 320px diameter)
   - Apply semi-transparent fills (15-20% opacity)
   - Position with strategic overlaps
   - Group overlapping sections can be tricky—may need to:
     - Layer circles in correct order
     - Use "Merge Shapes → Intersect" for overlap zone
     - Manually create overlap polygon and apply amber fill
   - Add text boxes inside each territory
   - Add central "PICTURE HANGING" label in overlap zone

2. **Create white space opportunity boxes:**
   - Four rectangle shapes, equal size
   - Apply borders and rounded corners
   - Distribute evenly with consistent gutters (use PowerPoint's align/distribute tools)
   - Add text content to each box with proper hierarchy

3. **Create Hard Truth panel:**
   - Full-width rectangle with light background
   - Add left border accent
   - Insert diamond icon and text

4. **Conversation starters:**
   - Three-column text layout
   - Arrow bullets
   - Italicized audience labels

### Quality Checklist
- [ ] Venn diagram circles are equal size (320px diameter)
- [ ] Circle overlaps create visible intersection zones
- [ ] Overlap zone (amber) is clearly defined
- [ ] Territory labels are readable inside circles
- [ ] White space boxes are equal width and aligned
- [ ] Box content is consistently formatted across all four
- [ ] Hard Truth panel spans full width
- [ ] Conversation starters are evenly distributed
- [ ] All colors match specified hex codes
- [ ] Text hierarchy is consistent with other slides

---

# 5. EXPORT AND DELIVERY SPECIFICATIONS

## File Format Requirements

### PowerPoint (.PPTX)
- **Version:** PowerPoint 2016 or later
- **Slide size:** 16:9 (1920×1080px)
- **Fonts:** Embed Inter font in presentation file
- **File naming:** `3M_BrandPerceptions_TestSlides_v1.pptx`

### Keynote (.KEY)
- **Version:** Keynote 10.0 or later
- **Slide size:** 1920×1080 at 72 DPI
- **Fonts:** Include Inter font in Keynote package
- **File naming:** `3M_BrandPerceptions_TestSlides_v1.key`

### PDF Export
- **Format:** PDF 1.7 or higher
- **Quality:** High quality (300 DPI for images)
- **Fonts:** Embed all fonts
- **File naming:** `3M_BrandPerceptions_TestSlides_v1.pdf`

## Font Embedding
- **Primary font:** Inter (include Regular, Medium, Semibold, Bold weights)
- **Download:** https://fonts.google.com/specimen/Inter
- **Fallback:** If Inter unavailable, use Helvetica Neue or Arial
- **Licensing:** Inter is open source (OFL), safe for commercial use

## Image Assets
- **Icons:** Create as vector shapes in PowerPoint/Keynote (scalable)
- **Charts:** Native PowerPoint/Keynote charts (editable)
- **Venn diagram:** Vector shapes (not image)
- **Resolution:** Minimum 150 DPI for any raster elements

## Accessibility Considerations
- **Color contrast:** All text meets WCAG AA standard (4.5:1 ratio minimum)
- **Alt text:** Add descriptive alt text to all visual elements
- **Reading order:** Logical tab order for screen readers
- **Color not sole indicator:** Use icons and patterns, not just color

## Version Control
- **File naming convention:**
  - `3M_BrandPerceptions_TestSlides_v1.pptx` (initial version)
  - `3M_BrandPerceptions_TestSlides_v2.pptx` (after revisions)
  - `3M_BrandPerceptions_TestSlides_FINAL.pptx` (approved version)
- **Metadata:** Include author, creation date, revision notes in file properties

---

# 6. DESIGN REVIEW CHECKLIST

## Before Submitting to Client

### Visual Consistency
- [ ] All slides use consistent typography (Inter font family)
- [ ] All colors match specified hex codes exactly
- [ ] All icons are consistent size (24pt for major, 18pt for arrows)
- [ ] Spacing between sections is uniform (32pt standard)
- [ ] Margins are consistent (80px all sides)

### Content Accuracy
- [ ] All data points match source document (PHASE2_COMPREHENSIVE_ANALYSIS.md)
- [ ] No false precision (avoid unnecessary decimals)
- [ ] Natural language used where appropriate (not just numbers)
- [ ] Source citations are accurate and complete

### Strategic Framing
- [ ] Tone is consultative, not prescriptive
- [ ] Hard truths are supported with "why it matters" explanations
- [ ] Provocations offer multiple options to consider
- [ ] Conversation starters invite discussion without forcing conclusions
- [ ] No alarmist or blame language used

### Technical Quality
- [ ] All text is legible when projected (minimum 12pt)
- [ ] Charts and visualizations are accurate
- [ ] Icons and shapes are properly aligned
- [ ] No elements touch slide edges (margins enforced)
- [ ] Fonts are embedded in file

### Accessibility
- [ ] Color contrast meets WCAG AA standard
- [ ] Alt text added to visual elements
- [ ] Text is real text, not images of text
- [ ] Logical reading order for screen readers

### File Preparation
- [ ] Correct file naming convention used
- [ ] Fonts embedded in presentation file
- [ ] Metadata includes author and date
- [ ] PDF export is high quality (300 DPI)
- [ ] Master slides/layouts are properly configured

---

# 7. DESIGN ITERATION GUIDANCE

## Common Revisions to Expect

1. **Headline refinement** - May need to adjust wording for clarity
2. **Data visualization tweaks** - Chart types or layouts may need adjustment
3. **Color adjustments** - Client may have brand color preferences
4. **Icon style** - May need to match existing 3M design system
5. **Spacing modifications** - Some elements may need more/less breathing room

## Flexibility Points
- **Typography:** If Inter is problematic, can substitute with Helvetica Neue
- **Icons:** Can adjust style (outlined vs filled) if needed
- **Chart types:** Can swap (e.g., horizontal to vertical bars) if more effective
- **Colors:** Can adjust saturation/lightness while maintaining intent

## Non-Negotiable Elements
- **80px margins** - Must maintain for projection safety
- **Icon semantics** - 🔷 Hard Truth and ❓ Provocation must remain distinct
- **Data accuracy** - All numbers must trace to source document
- **Tone** - Must remain consultative and respectful
- **Source citations** - Must be present and accurate

---

**Design Specifications Document Complete**

This document provides complete specifications for executing three test slides. All measurements, colors, typography, and layout details are specified for pixel-perfect implementation in PowerPoint or Keynote.

**Next Steps:**
1. Designer implements three slides per these specifications
2. Review slides against checklist (Section 6)
3. Iterate based on feedback
4. Once approved, use as template for full deck development (additional 15-20 slides)
