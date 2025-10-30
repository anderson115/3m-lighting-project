# Brand Perceptions Module - Development Plan

**Last Updated:** 2024-10-30
**Status:** Preflight - Ready for Phase 1 Development

---

## 🎯 Northstar Principles

### 1. No Placeholders, No Fabrication
- **NEVER** use dummy data or placeholder text
- **NEVER** generate fake quotes or fabricated statistics
- **ALWAYS** use real, verifiable data from actual sources
- **ALWAYS** include source URLs for every claim

### 2. Verifiable Checkpoints
- Live data validation at end of each phase
- User reviews actual outputs before proceeding
- No "black box" processing - show your work
- Intermediate outputs saved for inspection

### 3. Scalable & Stable
- Claude can execute without human intervention (after approval)
- Handles API failures gracefully (retry logic)
- Works with 1 brand or 10 brands (no hardcoding)
- Outputs are versioned and reproducible

### 4. Powerful & Insight-Rich
- AI reasoning, not keyword counting
- Multi-source synthesis, not single-source summaries
- Strategic implications, not just observations
- Actionable recommendations with clear reasoning

### 5. Realistic, Not Overengineered
- Use tools Claude already has (WebSearch, WebFetch)
- Avoid complex external dependencies
- Simple data structures (JSON, YAML, Markdown)
- If it requires 10 steps, simplify to 5

---

## 📋 Preflight Checklist

### Environment Setup
- [ ] 1Password CLI configured and working
- [ ] WebSearch available (test query)
- [ ] WebFetch available (test URL read)
- [ ] Claude Code session active
- [ ] Git repository clean (no uncommitted changes blocking work)

### Module Structure
- [x] Directory structure created
- [x] Config files in place
- [x] Documentation written
- [x] .gitignore configured
- [ ] Test brand configuration created

### Dependencies
- [ ] No external API keys required for Phase 1
- [ ] Python 3.13 available
- [ ] PyYAML installed (for config reading)
- [ ] No paid services needed yet

---

## 🔄 Development Phases (with Checkpoints)

### Phase 1: AI-Driven Brand Scoping

**Goal:** Identify 5-8 3M brands with garage organization relevance using AI reasoning

**Process:**
1. **WebSearch**: "3M consumer brands 2024"
2. **Claude reads** top results and reasons about brand portfolio
3. **WebSearch per brand**: "[Brand] consumer perception home organization"
4. **Claude synthesizes** garage relevance for each brand
5. **Generate** `config/brands.yaml` with AI rationale

**Output Files:**
- `config/brands.yaml` (AI-generated brand list)
- `data/outputs/phase1_brand_scoping.md` (AI reasoning log)

**Checkpoint 1: Brand List Validation**
```
User reviews:
- Are these the right 3M brands?
- Is the rationale sound?
- Should any be added/removed?

User approves before Phase 2
```

**Success Criteria:**
- 5-8 brands identified (no placeholder brands)
- Each brand has strategic rationale (not generic)
- All reasoning is traceable to web sources
- User validates brand selection

**Estimated Time:** 30 minutes (AI research + user review)

---

### Phase 2: Intelligent Perception Discovery

**Goal:** For each approved brand, gather high-signal consumer perception data using AI-guided research

**Process (per brand):**
1. **WebSearch**: "[Brand] garage organization reviews"
2. **Claude reads** top 5 results, identifies patterns
3. **If gaps found**, Claude requests targeted search:
   - "Found weight limit complaints - need more detail"
   - WebSearch: "[Brand] weight limit garage"
4. **WebFetch** 3-5 most relevant URLs for deep analysis
5. **Claude synthesizes** perception map with verbatim quotes

**Output Files (per brand):**
- `data/raw/{brand}/sources.json` (URLs + metadata)
- `data/processed/{brand}/perception_notes.md` (AI analysis)
- `data/processed/{brand}/verbatims.json` (extracted quotes with sources)

**Checkpoint 2: Source Quality Validation** (after first brand)
```
User reviews first brand's data:
- Are sources credible?
- Are quotes real and relevant?
- Is AI reasoning sound?

User approves approach before processing remaining brands
```

**Success Criteria:**
- Minimum 10 real sources per brand (with URLs)
- Minimum 20 verbatim quotes per brand (with source links)
- AI identifies love/hate/elasticity patterns (not keywords)
- All data is verifiable (user can click source URLs)

**Estimated Time:** 2 hours total (15 min per brand + checkpoint)

---

### Phase 3: AI Perception Synthesis

**Goal:** For each brand, generate multi-dimensional perception profile using AI reasoning

**Process (per brand):**
1. **Claude reads** all perception notes + verbatims
2. **Core Perception Extraction**:
   - What 5-10 words capture this brand?
   - AI reasons from context, not keyword frequency
3. **Love/Hate Clustering**:
   - What genuinely delights consumers? (with quotes)
   - What genuinely frustrates? (with quotes)
4. **Brand Elasticity Mapping**:
   - What adjacent uses appear?
   - What unmet needs emerge?
5. **6-Dimension Garage Fit Scoring**:
   - Utility strength (1-10, with evidence)
   - Aesthetic credibility (1-10, with evidence)
   - DIY authenticity (1-10, with evidence)
   - Durability perception (1-10, with evidence)
   - Innovation expectation (1-10, with evidence)
   - Value perception (1-10, with evidence)

**Output Files (per brand):**
- `data/outputs/{brand}_profile.json` (structured perception data)
- `data/outputs/{brand}_profile.md` (human-readable summary)
- `data/outputs/{brand}_spider_graph_data.json` (for visualization)

**Checkpoint 3: Perception Profile Validation** (after first brand)
```
User reviews first brand's profile:
- Do scores make sense given evidence?
- Are quotes representative?
- Is elasticity analysis insightful?

User approves approach before processing remaining brands
```

**Success Criteria:**
- Each score (1-10) has 3+ supporting quotes
- Love/hate clusters have real verbatims (not summaries)
- Elasticity mapping shows specific adjacent uses
- No fabricated data - everything traceable

**Estimated Time:** 1.5 hours total (12 min per brand + checkpoint)

---

### Phase 4: Innovation Fit Matrix

**Goal:** Cross-reference brand perceptions with category gaps and consumer jobs to generate innovation concepts

**Process:**
1. **Load context from other modules**:
   - Category opportunities (from category-intelligence)
   - Consumer jobs (from social-video-collection)
   - Brand perceptions (from this module)
2. **Claude reasons about fit** (per brand × opportunity):
   - Would consumers believe this brand could solve this job?
   - Does brand perception align with opportunity characteristics?
   - What are stretch risks vs natural fits?
3. **Generate innovation concepts** with 3-part validation:
   - Market gap evidence (category data)
   - Consumer need evidence (video data)
   - Brand credibility evidence (perception data)
4. **Strategic guardrails**:
   - Green zone: High fit, low risk
   - Yellow zone: Moderate stretch, moderate risk
   - Red zone: Brand mismatch, do not pursue

**Output Files:**
- `data/outputs/innovation_concepts.json` (ranked concepts)
- `data/outputs/fit_matrix.md` (strategic analysis)
- `data/outputs/guardrails.json` (green/yellow/red zones)

**Checkpoint 4: Innovation Concept Validation**
```
User reviews:
- Do concepts make strategic sense?
- Is evidence compelling?
- Are guardrails defensible?

User approves final recommendations
```

**Success Criteria:**
- Minimum 10 innovation concepts generated
- Each concept has evidence from all 3 modules
- Guardrails have clear strategic reasoning
- No generic "innovation theater" concepts

**Estimated Time:** 1 hour (AI synthesis + user review)

---

### Phase 5: Deliverable Automation

**Goal:** Generate client-ready report with AI-written strategic recommendations

**Process:**
1. **Claude writes** brand perception profiles (1 page each)
2. **Claude writes** innovation recommendations matrix
3. **Claude writes** strategic guardrails section
4. **Format** as Markdown with:
   - Embedded spider graphs (data visualization)
   - Hyperlinked sources (every claim)
   - Executive summary (AI-written)

**Output Files:**
- `data/outputs/FINAL_REPORT.md` (complete deliverable)
- `data/outputs/FINAL_REPORT.pdf` (if export needed)
- `data/outputs/deliverable_metadata.json` (version, timestamp, sources)

**Checkpoint 5: Deliverable Quality Review**
```
User reviews final report:
- Is writing quality high?
- Are recommendations actionable?
- Is evidence strong?

User approves for delivery
```

**Success Criteria:**
- Report is client-ready (no "AI slop" language)
- All claims hyperlinked to sources
- Strategic recommendations have clear reasoning
- Visualizations are professional

**Estimated Time:** 45 minutes (AI writing + user review)

---

## 🔍 Preflight Tests (Run Before Development)

### Test 1: WebSearch Functionality
```bash
# Test query
"3M Command brand consumer perception 2024"

# Expected: 10+ search results with titles/URLs
# Verify: Results are real, recent, relevant
```

### Test 2: WebFetch Functionality
```bash
# Test URL (example)
https://www.reddit.com/r/HomeImprovement/...

# Expected: Page content extracted
# Verify: Can read text, extract quotes
```

### Test 3: Config File Reading
```python
import yaml
with open('config/brands_example.yaml') as f:
    config = yaml.safe_load(f)
print(config)

# Expected: YAML parses correctly
# Verify: Structure matches expected schema
```

### Test 4: Output File Writing
```python
import json
test_data = {"test": "data", "timestamp": "2024-10-30"}
with open('data/outputs/test.json', 'w') as f:
    json.dump(test_data, f, indent=2)

# Expected: File created successfully
# Verify: Can read back written data
```

---

## 📊 Progress Tracking

### Phase Completion Tracker
```json
{
  "phase1_brand_scoping": {
    "status": "not_started",
    "checkpoint_approved": false,
    "output_files": []
  },
  "phase2_perception_discovery": {
    "status": "not_started",
    "checkpoint_approved": false,
    "brands_completed": [],
    "output_files": []
  },
  "phase3_perception_synthesis": {
    "status": "not_started",
    "checkpoint_approved": false,
    "brands_completed": [],
    "output_files": []
  },
  "phase4_innovation_fit": {
    "status": "not_started",
    "checkpoint_approved": false,
    "output_files": []
  },
  "phase5_deliverable": {
    "status": "not_started",
    "checkpoint_approved": false,
    "output_files": []
  }
}
```

Save to: `data/outputs/progress.json` (auto-update after each phase)

---

## 🚨 Failure Handling

### If WebSearch Fails:
- Retry 3x with exponential backoff
- Log failure to `data/errors.log`
- Skip to next search query
- Continue with available data

### If WebFetch Fails:
- Retry 3x with exponential backoff
- Log failure with URL to `data/errors.log`
- Skip to next source
- Continue with available sources

### If Insufficient Data:
- Claude requests targeted follow-up search
- Max 3 follow-up searches per brand
- If still insufficient, flag brand for manual review
- Document limitation in output

### If User Rejects Checkpoint:
- Save current progress to `data/checkpoints/`
- Request specific feedback
- Revise approach based on feedback
- Re-run phase with adjustments
- Submit for re-approval

---

## ✅ Quality Gates

### Before Phase 1 → Phase 2:
- [ ] 5-8 brands identified (real, not placeholder)
- [ ] Each brand has strategic rationale
- [ ] User approved brand list

### Before Phase 2 → Phase 3:
- [ ] First brand has 10+ real sources
- [ ] First brand has 20+ verbatim quotes
- [ ] User approved data quality

### Before Phase 3 → Phase 4:
- [ ] First brand has complete perception profile
- [ ] All scores have supporting evidence
- [ ] User approved analysis quality

### Before Phase 4 → Phase 5:
- [ ] Innovation concepts generated
- [ ] Concepts have 3-part validation
- [ ] User approved strategic fit

### Before Delivery:
- [ ] Report is client-ready
- [ ] All sources hyperlinked
- [ ] User approved final deliverable

---

## 🎯 Success Metrics

**Quantitative:**
- 5-8 brands profiled
- 50+ sources per brand (minimum 10 deep-read)
- 100+ verbatim quotes total
- 10+ innovation concepts
- 100% claims source-traceable

**Qualitative:**
- AI reasoning is sound (user validates)
- Insights are actionable (user confirms)
- Evidence is compelling (user approves)
- Writing is professional (client-ready)

---

## 📝 Next Action

**Run Preflight Tests** (all 4 tests above)

**If all tests pass:**
- Begin Phase 1: AI-Driven Brand Scoping
- Target: 30 minutes to Checkpoint 1

**If any test fails:**
- Debug issue before proceeding
- Do not begin development with broken tools
