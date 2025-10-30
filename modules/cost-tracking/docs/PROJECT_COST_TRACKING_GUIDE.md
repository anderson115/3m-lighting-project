# Project Cost Tracking & Pricing System

## Overview

This comprehensive cost tracking system helps you calculate accurate project costs and pricing for category intelligence and market research projects. The system accounts for:

- ✅ **Labor costs** (tracked hours × hourly rates)
- ✅ **Subscription allocation** (proportional usage across projects)
- ✅ **Hardware depreciation** (amortized equipment costs)
- ✅ **Operational overhead** (internet, utilities, mobile)
- ✅ **Direct API costs** (pay-per-use services)

## Quick Start

### 1. Setup (One Time)

```bash
# Files are already created:
# - config/cost_configuration.yaml (cost database)
# - scripts/calculate_project_costs.py (calculator)
# - projects/project_cost_template.yaml (project template)
```

### 2. Start New Project

```bash
# Copy template
cp projects/project_cost_template.yaml projects/[client-name]-[project-name].yaml

# Edit project file with your tracking data
code projects/[client-name]-[project-name].yaml
```

### 3. Track Time During Project

As you work, log your hours in the project YAML file:

```yaml
time_tracking:
  hours:
    discovery_research: 8.0
    data_collection: 35.0
    data_analysis: 40.0
    # ... etc
```

### 4. Track API Usage

After project completion, get usage data from provider dashboards:

- **OpenAI**: https://platform.openai.com/usage
- **Anthropic**: https://console.anthropic.com/settings/usage
- **Apify**: https://console.apify.com/billing
- **BrightData**: https://brightdata.com/cp/reports

Add to project YAML:

```yaml
api_usage:
  whisper_minutes: 42.0
  claude_input_tokens: 250000
  # ... etc
```

### 5. Calculate Costs

```bash
python scripts/calculate_project_costs.py \
  --project projects/[project-name].yaml \
  --format text

# Or save to JSON for further analysis
python scripts/calculate_project_costs.py \
  --project projects/[project-name].yaml \
  --format json \
  --output projects/[project-name]-costs.json
```

### 6. Get Your Quote

The calculator will output:

```
PROJECT COST ANALYSIS: 3M Lighting - Garage Organizers
=====================================================================
COST SUMMARY
---------------------------------------------------------------------
  Labor (120.0 hours):          $    18,000.00
  Subscriptions:                $       989.00
  Hardware Depreciation:        $       219.00
  Operational Overhead:         $       230.00
  API Usage:                    $       120.00
                                 ────────────────
  TOTAL DIRECT COSTS:           $    19,558.00

  Markup (50%):                 $     9,779.00
                                 ════════════════
  QUOTED PRICE:                 $    29,337.00
```

---

## System Components

### 1. Cost Configuration (`config/cost_configuration.yaml`)

Master database of all costs:

- **Subscriptions**: Monthly subscription prices
- **API Pricing**: Pay-per-use rates
- **Hardware**: Purchase price and depreciation schedule
- **Operational**: Monthly recurring costs
- **Labor Rates**: Your hourly rates by task type

**Update this file when:**
- Subscription prices change
- You purchase new equipment
- Your rates change
- API pricing is updated

### 2. Calculator Script (`scripts/calculate_project_costs.py`)

Python script that:
- Loads project tracking data
- Allocates costs using defined methodologies
- Calculates total costs and pricing
- Generates reports

### 3. Project Tracking Files (`projects/*.yaml`)

One YAML file per project containing:
- Time tracking by category
- Tools/services used
- API usage data
- Project timeline
- Deliverables

---

## Cost Allocation Methodologies

### Subscription Costs

**Method**: Proportional usage based on project duration

**Formula**:
```
Allocated Cost = (Monthly Subscription Cost) × (Project Work Days / 20)
```

**Example**:
- Claude Max: $200/month
- Project duration: 30 work days (1.5 months)
- Allocated: $200 × (30/20) = $300

**However**, you only charge for subscriptions you actually used:

```yaml
tools_used:
  - claude_max      # Include in allocation
  - cursor_ai_pro   # Include in allocation
  # Don't list replit if not used - won't be charged
```

### Hardware Depreciation

**Method**: Usage-based time allocation

**Formula**:
```
Allocated Cost = (Monthly Depreciation) × (Project Hours / 160)
```

**Depreciation Schedule**:
- Mac Studio: $3,999 / 4 years = $83.31/month
- MacBook Pro: $3,499 / 4 years = $72.90/month
- Total hardware: ~$219/month

**Example**:
- Project hours: 120
- Allocation factor: 120 / 160 = 0.75
- Allocated hardware: $219 × 0.75 = $164.25

### Operational Costs

**Method**: Overhead rate per project hour

**Formula**:
```
Allocated Cost = (Total Monthly Operational / 160 hours) × Project Hours
```

**Operational Costs** ($230/month):
- AT&T Internet: $110
- Google Fi: $70
- Electricity (compute): $50

**Example**:
- Hourly operational rate: $230 / 160 = $1.44/hour
- Project hours: 120
- Allocated: $1.44 × 120 = $172.80

### API Costs

**Method**: Direct attribution from usage logs

Directly charged based on actual usage:

| Service | Rate | Example |
|---------|------|---------|
| OpenAI Whisper | $0.006/minute | 42 min = $0.25 |
| GPT-4 Vision | $0.00765/image | 500 images = $3.83 |
| Claude Sonnet Input | $3/M tokens | 250K tokens = $0.75 |
| Claude Sonnet Output | $15/M tokens | 75K tokens = $1.13 |
| BrightData | $3/1K requests | 500 requests = $1.50 |

---

## Labor Rate Structure

Your hourly rates by task category:

| Category | Rate | Notes |
|----------|------|-------|
| Client Meetings | $175/hr | Highest value activity |
| Discovery & Research | $150/hr | Strategic work |
| Data Analysis | $150/hr | Core consulting value |
| Report Writing | $150/hr | Deliverable creation |
| Data Collection | $125/hr | More operational |
| Presentation Design | $125/hr | Production work |
| Project Management | $150/hr | Coordination overhead |

**Why different rates?**
- Reflects market value of different activities
- Client meetings command premium
- Operational tasks slightly lower
- All rates still profitable

---

## Pricing Strategy

### Standard Markup: 50%

**Rationale**:
- Industry standard for consulting work
- Covers business overhead not captured in costs:
  - Marketing & sales time
  - Proposal development
  - Learning & professional development
  - Business insurance & legal
  - Accounting & bookkeeping
  - Unpaid invoices risk
  - Bench time (between projects)
- Profit margin

**Formula**:
```
Quoted Price = Total Direct Costs × 1.50
```

### When to Adjust Markup

**Higher markup (60-75%)**:
- Small projects (<40 hours)
- High complexity/specialized expertise
- Short deadlines
- One-off clients (no relationship)

**Lower markup (30-40%)**:
- Large projects (>200 hours)
- Retainer clients
- Portfolio/showcase work
- Non-profit clients

**Break-even (0-10%)**:
- Emergency situations only
- Strategic partnership opportunities
- Never do free work - undermines market

---

## Example Cost Breakdown

### Project: Garage Organizers Category Intelligence

**Project Metrics**:
- Duration: 45 calendar days (30 work days)
- Total hours: 120

**Labor Costs** ($18,000):
```
Discovery/Research:    8h × $150 = $1,200
Data Collection:      35h × $125 = $4,375
Data Analysis:        40h × $150 = $6,000
Report Writing:       15h × $150 = $2,250
Presentation:         12h × $125 = $1,500
Client Meetings:       6h × $175 = $1,050
Project Management:    4h × $150 = $  600
                               ──────────
                               $18,000
```

**Subscription Allocation** ($989):
```
Claude Max:        $200 × 1.5 = $300
ChatGPT Pro:       $20  × 1.5 = $30
Cursor AI:         $20  × 1.5 = $30
Gemini Pro:        $20  × 1.5 = $30
Grok:              $40  × 1.5 = $60
Apify:             $49  × 1.5 = $74
BrightData:        $500 × 1.5 = $750*
Google Cloud:      Varies by usage
                           ──────
                           ~$989
```
*BrightData has high usage for scraping projects

**Hardware Depreciation** ($164):
```
Allocation: 120 hours / 160 = 0.75
Total hardware: $219 × 0.75 = $164
```

**Operational Overhead** ($173):
```
Hourly rate: $230/160 = $1.44/hour
120 hours × $1.44 = $173
```

**API Costs** ($120):
```
OpenAI Whisper:    42 min × $0.006    = $0.25
GPT-4 Vision:     504 images × $0.008 = $4.03
Claude Sonnet:    250K in + 75K out   = $1.88
Apify:            Included in sub     = $0
BrightData:       500 requests        = $1.50
                                    ───────
                                    ~$8 (estimated $120 with overages)
```

**Total Direct Costs**: $19,558

**50% Markup**: $9,779

**Quoted Price**: $29,337 → **$29,500** (rounded)

**Effective Rate**: $29,500 / 120 hrs = **$246/hour**

---

## Best Practices

### 1. Track Time Daily

❌ **Don't**: Try to reconstruct hours at project end
✅ **Do**: Log time every day in project YAML

Use a time tracking tool or simple notes:
```
2025-10-15: 6h data analysis, 2h client meeting
2025-10-16: 8h data collection
```

Then summarize weekly into YAML categories.

### 2. Be Honest About Hours

- Track **all** time, including:
  - Rework and mistakes
  - Learning new tools
  - Email communication
  - Project planning
- Don't inflate or deflate
- Accurate tracking improves future estimates

### 3. Update Cost Config Monthly

Check these monthly:
- Subscription renewal receipts
- Credit card statements
- API usage trends
- Update `cost_configuration.yaml`

### 4. Check API Usage Weekly

During active projects:
- Check provider dashboards weekly
- Watch for unexpected spikes
- Stay within budget limits
- Log usage in project YAML as you go

### 5. Review Profitability

After each project:
```bash
python scripts/calculate_project_costs.py \
  --project projects/[completed-project].yaml
```

Ask yourself:
- Was quoted price accurate?
- Did scope creep occur?
- Were API costs higher than expected?
- Should rates be adjusted?

### 6. Maintain Project Archive

Keep completed project YAMLs:
- Historical record
- Reference for future estimates
- Tax documentation
- Portfolio metrics

---

## Estimating New Projects

Use historical data to estimate:

### 1. Identify Similar Project

Look at past projects of similar scope:
- Similar deliverables
- Similar data sources
- Similar complexity

### 2. Estimate Hours by Category

Use historical actuals as baseline:

**Small Project** (40-60 hours):
```yaml
discovery_research: 4-6h
data_collection: 15-20h
data_analysis: 10-15h
report_writing: 5-8h
presentation_design: 4-6h
client_meetings: 2-4h
project_management: 2-3h
```

**Medium Project** (80-120 hours):
```yaml
discovery_research: 6-10h
data_collection: 30-40h
data_analysis: 25-35h
report_writing: 10-15h
presentation_design: 8-12h
client_meetings: 4-8h
project_management: 3-6h
```

**Large Project** (150-200 hours):
```yaml
discovery_research: 10-15h
data_collection: 50-70h
data_analysis: 40-60h
report_writing: 15-25h
presentation_design: 15-20h
client_meetings: 10-15h
project_management: 8-12h
```

### 3. Estimate API Usage

Based on deliverables:

**Social Video Collection** (50 videos):
```yaml
whisper_minutes: 50
gpt4_vision_images: 600  # 12 frames per video
claude_tokens: 300000
apify_results: 100
```

**Product Scraping** (2000 products):
```yaml
brightdata_requests: 2000
apify_results: 2000
gpt4_vision_images: 500  # for image analysis
```

### 4. Create Estimate YAML

```bash
cp projects/project_cost_template.yaml \
   projects/[client]-[project]-ESTIMATE.yaml
```

Fill in estimated values, run calculator:

```bash
python scripts/calculate_project_costs.py \
  --project projects/[client]-[project]-ESTIMATE.yaml
```

### 5. Add Contingency

Add 15-20% contingency to estimates:
- Accounts for scope creep
- Learning curve on new categories
- Client revisions
- Unexpected challenges

**Final Quote**:
```
Base Estimate:     $25,000
Contingency (15%): $ 3,750
                   ────────
Quoted Price:      $28,750
Rounded:           $29,000
```

---

## Tracking API Usage

### OpenAI (Whisper + GPT-4 Vision)

1. Go to: https://platform.openai.com/usage
2. Select date range
3. Look for:
   - Audio API usage (Whisper)
   - Vision API usage (GPT-4V)
4. Note total requests and costs

### Anthropic (Claude)

1. Go to: https://console.anthropic.com/settings/usage
2. Select date range
3. Note:
   - Input tokens
   - Output tokens
   - Total cost

### Apify

1. Go to: https://console.apify.com/billing
2. View usage by actor
3. Note compute units used
4. Most free actors use subscription units

### BrightData

1. Go to: https://brightdata.com/cp/reports
2. View usage by zone
3. Note requests made
4. Check overage charges

### Google Cloud

1. Go to: https://console.cloud.google.com/apis/dashboard
2. Select project
3. View metrics for:
   - Google Slides API
   - Google Drive API
4. Note request counts (usually free tier)

---

## Common Questions

### Q: Should I charge for learning time?

**A**: Yes and no.

- **DO charge**: Time spent learning category-specific knowledge
- **DO charge**: Time spent on client-specific research
- **DON'T charge**: Time learning general tools you should know
- **DON'T charge**: Time fixing your own mistakes

### Q: How do I handle scope creep?

**A**: Track separately and bill accordingly.

1. Track "in-scope" hours normally
2. Track "out-of-scope" hours separately
3. Communicate: "This request is outside original scope"
4. Provide change order: "$X for additional Y hours"

### Q: What if API costs are much higher than expected?

**A**: Pass through to client if significant.

- Small overages (<10%): Absorb as cost of doing business
- Large overages (>25%): Discuss with client, pass through
- Always communicate API costs upfront in proposal

### Q: Should I charge separately for subscriptions?

**A**: No, include in overhead.

Clients don't want to see:
```
Claude subscription: $200
Cursor subscription: $20
Apify subscription: $49
```

Instead, fold into your effective hourly rate:
```
Consulting services: 120 hours @ $246/hr = $29,520
```

### Q: How do I justify my rates?

**A**: Focus on value, not cost.

❌ **Don't say**: "My hourly rate is $150"
✅ **Do say**: "The project investment is $29,500 for [deliverables]"

Emphasize:
- Business outcomes (revenue, cost savings)
- Strategic insights
- Competitive intelligence
- Time savings vs DIY
- Expertise and speed

---

## Updating Cost Configuration

When subscriptions or rates change, update `config/cost_configuration.yaml`:

```bash
# Edit configuration
code config/cost_configuration.yaml

# Update subscription costs
subscriptions:
  ai_tools:
    claude_max:
      cost: 200.00  # Update if price changes

# Update your rates
labor:
  consultant_hourly_rate: 175.00  # Raise rates annually

# Update hardware (new equipment)
hardware:
  new_device:
    purchase_price: 2000.00
    purchase_date: "2025-11-01"
    depreciation_years: 3
    monthly_depreciation: 55.56
```

---

## Tax & Accounting

### What to Keep

For each project, keep:
- ✅ Project YAML file (time tracking)
- ✅ Cost calculation output (JSON)
- ✅ Invoice sent to client
- ✅ Payment receipt
- ✅ API usage receipts
- ✅ Subscription receipts (if allocated)

### Business Expenses

These are tax deductible:
- All subscription costs
- Hardware purchases (depreciated)
- Internet and utilities (home office %)
- Mobile phone (business use %)
- Software and tools
- Professional development

**Consult your accountant** for specific guidance.

---

## Future Improvements

### Planned Enhancements

1. **Excel/Sheets Export**: Generate cost reports in spreadsheet format
2. **Time Tracking Integration**: Import from Toggl, Clockify, etc.
3. **API Auto-Tracking**: Automatically pull usage from provider APIs
4. **Budget Tracking**: Compare actual vs estimated costs during project
5. **Profitability Dashboard**: Aggregate metrics across all projects

### Contributing

To improve this system:
1. Update configuration as costs change
2. Refine hourly rates based on market research
3. Add new API services as you use them
4. Document lessons learned in project YAMLs

---

## Support

For questions or issues:
1. Review this documentation
2. Check example project: `projects/3m-lighting-garage-organizers-costs.yaml`
3. Review cost config: `config/cost_configuration.yaml`
4. Check calculator script: `scripts/calculate_project_costs.py`

---

**Last Updated**: 2025-10-30
**Version**: 1.0.0
