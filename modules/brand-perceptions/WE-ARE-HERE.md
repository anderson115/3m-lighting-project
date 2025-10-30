# Brand Perceptions Module - AI-First Architecture

## Strategic Approach: Intelligence Over Automation

**Philosophy:** Use AI reasoning at every step beyond initial data discovery. Filters for finding sources, intelligence for understanding them.

---

## Phase 1: AI-Driven Brand Portfolio Scoping

**NOT:** Hardcoded brand list with manual scoring
**YES:** Claude researches 3M portfolio and reasons about garage organization fit

**Process:**
1. WebSearch: "3M consumer brands portfolio 2024"
2. Claude analyzes brand portfolio and reasons:
   - Which brands have organization/storage heritage?
   - What consumer perceptions exist? (search and read)
   - Which could credibly stretch into garage innovation?
3. Claude generates prioritized list with strategic rationale
4. Output: `config/brands.yaml` with AI-generated reasoning

**Cost:** $0 (WebSearch + local Sonnet)

---

## Phase 2: Intelligent Perception Discovery

**NOT:** Scrape 200+ posts and count keywords
**YES:** AI-guided recursive research with reasoning

### 2.1 Source Discovery (Filters OK here)
- WebSearch for initial sources per brand
- Filter by: recency, relevance, credibility
- Identify high-signal sources (Reddit threads, YouTube reviews, detailed Amazon reviews)

### 2.2 Deep Perception Analysis (AI Reasoning)
**Per brand, Claude:**
1. **Reads** top sources via WebFetch
2. **Identifies** perception patterns through reasoning:
   - What do consumers genuinely love? (not keyword "love")
   - What frustrates them? (understand context, not just "bad")
   - What adjacent uses appear organically?
3. **Requests more data** when gaps detected:
   - "Users mention weight limits - need more on this"
   - Claude searches: "Command hooks weight limit garage" (targeted)
4. **Synthesizes** into perception map via multi-turn reasoning

**Example Flow:**
```
Initial search → "Command hooks garage organization"
Claude reads top 5 results → Identifies: "Damage-free is loved, but weight limits frustrate"
Claude requests → "Command hooks heavy duty garage complaints"
Claude reads → Reasons: "Users want damage-free BUT for heavier items (tools, bikes)"
Synthesis → Brand perception: "Convenience brand, not durability brand (yet)"
```

**Tools:**
- WebSearch (free, broad discovery)
- WebFetch (free, deep reading)
- Claude reasoning (local Sonnet, $0)
- Opus only when: Multi-document synthesis of 10+ sources required

---

## Phase 3: AI Perception Synthesis

**NOT:** Keyword counting and formulaic scoring
**YES:** Multi-dimensional AI reasoning

### 3.1 Core Perception Extraction
Claude analyzes collected sources and reasons:
- "What 5-10 words truly capture how consumers see this brand?"
- "What functional benefits do they cite? Why do those matter?"
- "What emotional associations emerge from context, not keywords?"

### 3.2 Love/Hate Clustering
Claude identifies patterns through understanding:
- **NOT**: Count instances of "love" or "hate"
- **YES**: Understand what delights vs frustrates through context
- Support with verbatim quotes (source traceable)

### 3.3 Brand Elasticity Mapping
Claude reasons about stretch potential:
- "What adjacent categories do consumers naturally discuss?"
- "What 'hacks' suggest unmet needs the brand could address?"
- "Where do consumers wish this brand would go?"

### 3.4 Garage Category Fit Scoring
Claude scores 6 dimensions through reasoning, not rules:

**Dimensions:**
1. **Utility strength**: Does brand deliver functional performance in storage/organization?
2. **Aesthetic credibility**: Would consumers trust brand for visible garage solutions?
3. **DIY authenticity**: Is brand seen as "for makers" or "for consumers"?
4. **Durability perception**: Does brand signal long-term reliability?
5. **Innovation expectation**: Do consumers expect category leadership from this brand?
6. **Value perception**: Fair price-quality relationship in consumer minds?

**Scoring method:**
- Claude reads sources with these dimensions in mind
- Scores 1-10 based on evidence weight and context
- Cites 3+ verbatim quotes per dimension (source traceable)
- **NOT**: Formula-based calculation

**Output:** JSON per brand + spider graph visualization

---

## Phase 4: Innovation Fit Matrix (Pure AI Reasoning)

**NOT:** Formula: `(Gap × 0.3) + (Job × 0.3) + (Brand × 0.4)`
**YES:** Claude reasons about fit across modules

### Process:
1. **Load context:**
   - Category opportunities (from retail dragnet module)
   - Consumer jobs (from video/social synthesis module)
   - Brand perceptions (from this module)

2. **Claude reasons about fit:**
   - "Would consumers believe [Brand] could solve [Consumer Job]?"
   - "Does [Brand Perception] align with [Category Opportunity]?"
   - "What are the stretch risks? What are the natural fits?"

3. **Claude generates ranked concepts with 3-part validation:**
   - Market gap evidence (from category module)
   - Consumer need evidence (from video module)
   - Brand credibility evidence (from perceptions module)

4. **Strategic guardrails via judgment:**
   - **Green zone**: High brand fit, low risk
   - **Yellow zone**: Requires brand stretch, moderate risk
   - **Red zone**: Brand mismatch, do not pursue

**Output:** Ranked innovation concepts with AI-generated strategic reasoning

---

## Phase 5: Deliverable Automation

### Auto-Generated Report (AI-written):

**Section 1: Brand Perception Profiles** (1 page per brand)
- AI-generated spider graph (not plotted data, but reasoned assessment)
- Love/hate verbatim clusters (AI-selected most representative quotes)
- Category elasticity map (AI-identified patterns)
- Garage fit score with AI rationale

**Section 2: Innovation Recommendations Matrix**
- Concept statements (AI-synthesized from cross-module data)
- 3-part fit scoring with AI reasoning (not formulas)
- Risk flags (AI-identified based on perception gaps)
- Opportunity highlights (AI-identified cross-module validation)

**Section 3: Strategic Guardrails**
- Green/yellow/red zones with AI strategic reasoning
- "Why this brand should/shouldn't pursue this innovation"

**Delivery Format:**
- Markdown → Google Docs
- All claims hyperlinked to source URLs
- Claude-generated visualizations (artifacts)

---

## Technical Architecture

### Data Collection Strategy:

**Early Stage (Filters OK):**
```python
# Use WebSearch to find sources
# Filter by: date, domain authority, relevance
# Example: "site:reddit.com Command hooks garage after:2023"
```

**Analysis Stage (AI Reasoning Required):**
```python
# NO keyword counting
# NO formulaic scoring
# YES Claude reads and reasons
# YES multi-turn questioning when gaps found
# YES source-traceable synthesis
```

### Agent Usage:

**Use Task tool with Explore agent when:**
- Need to search multiple sources recursively
- "Find me the best discussions about [Brand] garage organization"
- Agent reasons about which sources matter, not just keyword match

**Use local Claude when:**
- Synthesizing perceptions from 5-10 sources
- Scoring brand dimensions
- Generating strategic recommendations

**Use Opus (paid) when:**
- Synthesizing 20+ sources simultaneously
- Complex multi-brand comparison reasoning
- Final deliverable generation (polish)

---

## Success Criteria

**Quality > Quantity:**
- ❌ "200 data points collected"
- ✅ "Deep understanding of brand perception from high-signal sources"

**Intelligence > Automation:**
- ❌ "Keyword 'love' appears 47 times"
- ✅ "Consumers genuinely love damage-free mounting, but feel constrained by weight limits for heavier garage items like bikes and tool boards"

**Reasoning > Rules:**
- ❌ "Brand scored 7.2 based on formula"
- ✅ "Brand scores 7/10 on utility because consumers consistently cite functional performance in reviews, but 4/10 on durability because of recurring complaints about adhesive failure under heat/weight"

---

## Cost Estimate

- WebSearch: $0 (free)
- WebFetch: $0 (free)
- Local Claude (Sonnet 4.5): $0 (existing subscription)
- Opus (final synthesis): ~$5 (1-2 complex tasks)

**Total: ~$5** (vs $50 in original rigid design)

---

## Current Status

**✓ Module scaffolded**
**⏳ Phase 1: AI-driven brand scoping (ready to build)**
**⏳ Phase 2: Intelligent perception discovery (design complete)**
**⏳ Phase 3: AI synthesis (architecture defined)**
**⏳ Phase 4: Innovation fit reasoning (approach defined)**
**⏳ Phase 5: Deliverable automation (spec complete)**

---

## Next Action

Build Phase 1 script with AI-first approach:
- `scripts/01_scope_brands_ai.py` (replaces hardcoded version)
- Uses WebSearch + Claude reasoning
- Generates brands.yaml via intelligence, not rules
