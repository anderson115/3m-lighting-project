# Slide Recreation Guide - offbrain Template System

**Purpose:** Recreate slides across new client projects using locked design system

---

## 🎨 Design System (Locked)

### Colors
```css
:root {
    --primary: #2D3748;    /* Charcoal */
    --accent: #14B8A6;     /* Teal */
    --text: #1A202C;       /* Dark Gray */
    --text-light: #4A5568; /* Light Gray */
}
```

### Typography
- **Font:** Inter (400, 500, 600, 700, 800, 900)
- **Headline:** 33pt / 900 weight / -0.04em letter-spacing
- **Section Header:** 12pt / 800 weight / uppercase / 0.12em spacing
- **Body Text:** 12pt / 400 weight / 19pt line-height

### Canvas
- **Dimensions:** 1920×1080px (16:9)
- **Margins:** 80px all sides
- **Content Area:** 1760×920px

---

## 🔧 Template Workflow

### Step 1: Select Template Type
**Default (Two-Column Classic)** → Traditional consulting format
**Keynote (Asymmetric Dynamic)** → Modern, high-impact format

### Step 2: Swap Content
Replace data while keeping structure unchanged

---

## 📋 Slide 1: Insight Card with Balance Scale

**Use Case:** Highlight imbalance/disparity between two metrics

**Data Points Needed:**
- Headline (strategic tension)
- Pattern narrative
- Insight narrative
- Hard Truth statement + explanation
- Provocation question + 3 considerations
- 3 Conversation starters
- 2 primary metrics (balance scale comparison)
- 2-row data table
- 3-segment sentiment distribution (percentages)

**Key Components:**

1. **Balance Scale** (right column)
   - Left platform = metric A (teal gradient)
   - Right platform = metric B (charcoal gradient)
   - Larger value = heavier side tilts

2. **Data Table** (right column)
   - 2 rows × 2 columns
   - Left label, right number (large, accent color)

3. **Sentiment Bar** (right column)
   - 3 segments: Neutral%, Positive%, Negative%
   - Colors: gray, teal, charcoal

**Recreation Steps (Default):**
1. Copy `SLIDE1_DEFAULT.html` structure
2. Update headline (line 312)
3. Replace Pattern section (line 318)
4. Replace Insight section (line 325)
5. Update Hard Truth panel (line 327-330)
6. Update Provocation question + list (line 334-340)
7. Update Conversation starters (line 346-349)
8. Adjust balance scale platform widths (line 357-358)
9. Update data table rows (line 366-367)
10. Modify sentiment percentages (line 375-376)
11. Update footer source text (line 388)

**Critical Metrics to Adjust:**
- `.platform.left::before` width = larger metric value (%)
- `.platform.right::before` width = smaller metric value (%)
- Platform label text = metric names
- Data table values = your numbers
- Sentiment segments = your percentages

---

## 🎯 Slide 2: Performance Spectrum with Sentiment

**Use Case:** Show performance variance across contexts + sentiment analysis

**Data Points Needed:**
- Headline (performance perception framing)
- Pattern narrative
- Insight narrative
- Hard Truth statement + explanation
- Provocation question + 3 options
- 3 Conversation starters
- 3 performance contexts + confidence scores (%)
- Positive vs. Negative sentiment labels
- 1 frequency metric (e.g., "1 in 6")

**Key Components:**

1. **Performance Bars** (right column)
   - 3 horizontal bars showing % confidence
   - Top bar = teal gradient (strongest)
   - Middle bar = teal gradient (strong)
   - Bottom bar = gray gradient (weaker)

2. **Sentiment Cards** (right column)
   - 2 cards: "High" (positive), "Low" (negative)
   - Teal border for positive, charcoal for negative

3. **Temperature/Frequency Box** (right column)
   - Yellow gradient background
   - Large stat (1 in 6, 17%, etc.)
   - Supporting description

**Recreation Steps (Default):**
1. Copy `SLIDE2_DEFAULT.html` structure
2. Update headline + brand name
3. Replace Pattern/Insight/Hard Truth sections
4. Update Provocation + Conversation starters
5. Adjust performance bars:
   - Line 176-183: Bar 1 label + width
   - Line 185-192: Bar 2 label + width
   - Line 194-201: Bar 3 label + width
6. Update sentiment card values (line 218-219)
7. Modify temperature box stat (line 234)
8. Update footer (line 412)

**Critical Metrics to Adjust:**
- `.spectrum-bar` width = your % values
- `.spectrum-bar.medium` width = lower confidence bar
- `.sentiment-value` text = "High"/"Low" labels
- `.temp-stat` = your frequency metric
- `.temp-description` = supporting detail

---

## 🗺️ Slide 3: Territory Grid with Opportunity Zones

**Use Case:** Brand segmentation, competitive landscape, market gaps

**Data Points Needed:**
- Headline (specialization + white space)
- Pattern narrative (brand territories)
- Insight narrative (optimization gaps)
- Hard Truth statement (market opportunity)
- Provocation question (segmentation options)
- 3 Conversation starters
- 3 brand territories + descriptions
- 3 use case statistics (%, frequency, etc.)
- 4 opportunity zone bullet points

**Key Components:**

1. **Territory Grid** (right column)
   - 3 rows × 2 columns
   - Left: Dark gradient labels (brand names)
   - Right: Light background descriptions
   - Rounded corners on all 4 outer corners

2. **Use Case Stats** (right column)
   - 3 rows with label + large accent number
   - Row separators

3. **White Space Opportunities Box** (right column)
   - Green gradient background
   - Teal border
   - 4 bullet points with teal circles

**Recreation Steps (Default):**
1. Copy `SLIDE3_DEFAULT.html` structure
2. Update headline
3. Replace Pattern/Insight/Hard Truth sections
4. Update Provocation + Conversation starters
5. Modify territory grid:
   - Line 371-388: Update 3 brand names + descriptions
6. Update use case stats:
   - Line 400-406: Update label + number (3 rows)
7. Modify opportunity zones:
   - Line 413: Update 4 bullet points
8. Update footer (line 421)

**Critical Metrics to Adjust:**
- Territory label text = brand/category names
- Territory description = application focus
- Use case labels + numbers = your metrics
- Opportunity bullet points = market gaps

---

## 🎲 Slide 4: Competitive Positioning Matrix

**Use Case:** Brand positioning, competitive landscape, market gaps

**Data Points Needed:**
- Headline (market positioning opportunity)
- Pattern narrative
- Insight narrative
- Hard Truth statement + explanation
- Provocation question + 3 options
- 3 Conversation starters
- 4 quadrant labels (e.g., "Budget Niche", "Premium Mainstream", etc.)
- 4 brand names for quadrants
- 2 axis labels (e.g., "Budget ← Price Positioning → Premium")
- 3 legend category items
- 4 brand bubble colors (teal, orange, red, gray gradients)

**Key Components:**

1. **Competitive Matrix** (right column)
   - 2×2 grid with 4 equal quadrants
   - Each quadrant = intersection of 2 positioning dimensions
   - Brand bubble centered in quadrant (circle with initials)

2. **Quadrant Labels** (inside each quadrant)
   - Top-left: Budget/Niche position
   - Top-right: Premium/Mainstream position
   - Bottom-left: Budget/Mainstream position
   - Bottom-right: Premium/Niche position

3. **Brand Bubbles**
   - Color-coded (teal = creator advocacy, orange = mainstream, red = specialist)
   - Hover animation on desktop
   - Initials or short brand name centered

4. **Legend** (below matrix)
   - 3 items explaining color coding
   - Left-aligned list format

**Recreation Steps (Default):**
1. Copy `SLIDE4_DEFAULT.html` structure
2. Update headline (line 247)
3. Replace Pattern section (line 252)
4. Replace Insight section (line 259)
5. Update Hard Truth panel (line 265-269)
6. Update Provocation question + list (line 273-282)
7. Update Conversation starters (line 352-357)
8. Modify quadrant labels (line 423-451, 4 labels inside matrix)
9. Update brand names + colors (line 423-451, 4 bubbles)
10. Update legend items (line 456-468, 3 items)
11. Update axis labels (line 412-415, X and Y positioning text)
12. Update footer source text (line 467)

**Critical Metrics to Adjust:**
- `.quadrant-label` text = your positioning descriptors
- `.brand-bubble` text = brand initials or names
- `.brand-label` text = full brand name
- `.axis-label-h`, `.axis-label-v` = your axis dimensions
- `.legend-item` descriptions = 3 category explanations
- Bubble colors = `linear-gradient` values for each brand

---

## 🔄 Template Switching: Default ↔ Keynote

**Differences:**

| Element | Default | Keynote |
|---------|---------|---------|
| Column Split | 50/50 (800/900px) | 2/3 + 1/3 (1100/612px) |
| Narrative Cards | Text sections | Dark gradient cards |
| Data Presentation | Right column layout | Sidebar stat blocks |
| Headlines | Standard | Left border accent |
| Visual Balance | Horizontal | Editorial asymmetric |

**To Convert Default → Keynote:**
1. Open Default template
2. Remove left-column from content-container
3. Create dark insight cards for Pattern/Insight/Hard Truth
4. Create light cards for Provocation/Conversation
5. Move data to right sidebar as stat blocks
6. Add headline left border
7. Adjust widths: main (1100px) + sidebar (612px)
8. Add card shadows + gradients

**Files:**
- Default: `SLIDE1_DEFAULT.html`, `SLIDE2_DEFAULT.html`, `SLIDE3_DEFAULT.html`, `SLIDE4_DEFAULT.html`
- Keynote: `SLIDE1_KEYNOTE.html`, `SLIDE2_KEYNOTE.html`, `SLIDE3_KEYNOTE.html`, `SLIDE4_KEYNOTE.html`

---

## 📂 File Naming Convention

**For New Client Projects:**

```
/3m-lighting-project/modules/[CLIENT-NAME]/

SLIDE1_DEFAULT.html      → Balance scale insight
SLIDE1_KEYNOTE.html      → Balance scale (keynote)
SLIDE2_DEFAULT.html      → Performance spectrum
SLIDE2_KEYNOTE.html      → Performance spectrum (keynote)
SLIDE3_DEFAULT.html      → Territory/opportunity
SLIDE3_KEYNOTE.html      → Territory/opportunity (keynote)
SLIDE4_DEFAULT.html      → Competitive positioning
SLIDE4_KEYNOTE.html      → Competitive positioning (keynote)

TEMPLATE_COLORS.md       → Color palette + hex codes
TEMPLATE_METRICS.md      → Data sources + calculations
SLIDE_SPEC_[CLIENT].md   → Client-specific measurements
```

---

## 🚀 Quick Start for New Client

**1. Data Gathering** (45 min)
- [ ] Identify 4 key insights (one per slide type)
- [ ] Collect data for balance scale (2 metrics + sentiment %)
- [ ] Gather performance/sentiment data (3 contexts + %)
- [ ] Document opportunity zones (4 gaps)
- [ ] Define brand territories (3 segments)
- [ ] Map competitive positioning (4 brands × 2 axes)

**2. Template Selection** (5 min)
- [ ] Choose Default or Keynote template
- [ ] Note layout preference

**3. Content Swap** (80 min)
- [ ] Copy 4 appropriate template files
- [ ] Replace all narrative sections (Slides 1-4)
- [ ] Update all numeric/quadrant values
- [ ] Verify percentages add to 100%
- [ ] Update all axis/positioning labels
- [ ] Update footer source text

**4. Visual QA** (30 min)
- [ ] Open in Safari browser
- [ ] Verify all content visible (scroll test)
- [ ] Check alignment + spacing
- [ ] Confirm colors render correctly
- [ ] Screenshot each slide

**5. Handoff** (5 min)
- [ ] Export all 4 HTML files
- [ ] Provide data source documentation
- [ ] Share color/font specs
- [ ] Document any custom adjustments

---

## 🔐 Design Principles (Don't Change)

✅ **Locked (Never Change):**
- Charcoal/Teal color palette
- Inter font family
- BOLD aesthetic (shadows, heavy weights, gradients)
- 1920×1080 canvas
- 80px margins
- Typography scale

❌ **Never Modify:**
- `--primary`, `--accent`, `--text` color values
- Font family declarations
- Margin/padding system (break alignment)
- Component shadows/gradients
- Conversation starters 3-column grid

✏️ **Always Customize:**
- Headline text
- Narrative sections
- Numeric data values
- Brand/category names
- Metric labels
- Footer source text

---

## 📖 Content Mapping Template

Use this for each new client project:

```markdown
# [CLIENT NAME] - Slide Specifications

## Slide 1: [Insight Type]
- Metric A: [NUMBER] ([CONTEXT])
- Metric B: [NUMBER] ([CONTEXT])
- Hard Truth: [1-2 SENTENCE STATEMENT]
- Opportunity: [STRATEGIC IMPLICATION]

## Slide 2: [Performance Type]
- Performance Context 1: [%]
- Performance Context 2: [%]
- Performance Context 3: [%]
- Sentiment Positive: [LABEL]
- Sentiment Negative: [LABEL]
- Frequency Metric: [1 IN X or X%]

## Slide 3: [Opportunity Type]
- Territory 1: [BRAND/CATEGORY] - [DESCRIPTION]
- Territory 2: [BRAND/CATEGORY] - [DESCRIPTION]
- Territory 3: [BRAND/CATEGORY] - [DESCRIPTION]
- Stat 1: [LABEL] = [NUMBER]
- Stat 2: [LABEL] = [NUMBER]
- Stat 3: [LABEL] = [NUMBER]
- Opportunity 1: [GAP]
- Opportunity 2: [GAP]
- Opportunity 3: [GAP]
- Opportunity 4: [GAP]

## Slide 4: [Competitive Positioning Type]
- X-Axis Label: [POSITIONING DIMENSION] (left side) → [OPPOSITE] (right side)
- Y-Axis Label: [POSITIONING DIMENSION] (bottom) → [OPPOSITE] (top)
- Quadrant 1 Label: [POSITION DESCRIPTOR]
- Quadrant 1 Brand: [BRAND NAME]
- Quadrant 2 Label: [POSITION DESCRIPTOR]
- Quadrant 2 Brand: [BRAND NAME]
- Quadrant 3 Label: [POSITION DESCRIPTOR]
- Quadrant 3 Brand: [BRAND NAME]
- Quadrant 4 Label: [POSITION DESCRIPTOR]
- Quadrant 4 Brand: [BRAND NAME]
- Legend Item 1: [CATEGORY] - [DESCRIPTION]
- Legend Item 2: [CATEGORY] - [DESCRIPTION]
- Legend Item 3: [CATEGORY] - [DESCRIPTION]
```

---

**Version:** 1.0
**Last Updated:** 2025-11-03
**Template Coverage:** 3 core slide types × 2 layout options = 6 reusable templates
