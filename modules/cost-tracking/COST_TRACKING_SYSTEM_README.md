# Project Cost Tracking & Pricing System

## 🎯 Overview

A comprehensive cost tracking and pricing system for calculating accurate project costs across all your category intelligence and market research projects. This system provides complete visibility into:

- **Labor costs** (your time investment)
- **Subscription allocation** (SaaS tools distributed across projects)
- **Hardware depreciation** (equipment amortization)
- **Operational overhead** (internet, utilities, mobile)
- **Direct API costs** (pay-per-use services)

**Result**: Professional cost analysis and pricing recommendations for client projects.

---

## 📦 What's Included

### Core Files

1. **`config/cost_configuration.yaml`**
   - Master database of all costs
   - Subscription prices
   - API pricing rates
   - Hardware depreciation schedules
   - Labor rates by task type
   - Cost allocation methodologies

2. **`scripts/calculate_project_costs.py`**
   - Automated cost calculator
   - Generates professional reports
   - JSON export for further analysis
   - Command-line interface

3. **`projects/project_cost_template.yaml`**
   - Reusable template for new projects
   - Structured time tracking
   - API usage tracking
   - Deliverables documentation

4. **`projects/3m-lighting-garage-organizers-costs.yaml`**
   - Real project example
   - Shows completed tracking
   - Demonstrates proper usage

### Documentation

5. **`docs/PROJECT_COST_TRACKING_GUIDE.md`**
   - Complete 5,000+ word guide
   - Step-by-step instructions
   - Cost allocation methodologies
   - Pricing strategies
   - FAQ and troubleshooting

6. **`docs/COST_TRACKING_QUICK_REFERENCE.md`**
   - One-page quick reference
   - Common commands
   - Pricing tables
   - Checklists

---

## 🚀 Quick Start (5 Minutes)

### 1. Start Your Next Project

```bash
# Copy the template
cp projects/project_cost_template.yaml projects/acme-widget-analysis.yaml

# Open in your editor
code projects/acme-widget-analysis.yaml
```

### 2. Track Your Time

As you work on the project, log hours in the YAML file:

```yaml
time_tracking:
  hours:
    discovery_research: 6.0
    data_collection: 25.0
    data_analysis: 30.0
    report_writing: 12.0
    presentation_design: 8.0
    client_meetings: 4.0
    project_management: 3.0
```

### 3. Track API Usage

Get usage data from provider dashboards after project completion:

```yaml
api_usage:
  whisper_minutes: 35.0          # From OpenAI dashboard
  gpt4_vision_images: 420        # From OpenAI dashboard
  claude_input_tokens: 200000    # From Anthropic dashboard
  claude_output_tokens: 60000    # From Anthropic dashboard
  apify_results: 120             # From Apify dashboard
  brightdata_requests: 400       # From BrightData dashboard
```

### 4. Calculate Costs & Get Quote

```bash
python scripts/calculate_project_costs.py \
  --project projects/acme-widget-analysis.yaml
```

**Output**:
```
================================================================================
PROJECT COST ANALYSIS: ACME - Widget Market Analysis
================================================================================
Client: ACME Corporation
Calculated: 2025-10-30

COST SUMMARY
--------------------------------------------------------------------------------
  Labor (#88.0 hours):        $   12,300.00
  Subscriptions:              $      723.00
  Hardware Depreciation:      $      121.28
  Operational Overhead:       $      126.72
  API Usage:                  $        5.85
                              ────────────────────
  TOTAL DIRECT COSTS:         $   13,276.85

  Markup (50%):              $    6,638.43
                              ════════════════════
  QUOTED PRICE:               $   19,915.28

KEY METRICS
--------------------------------------------------------------------------------
  Effective Hourly Rate:      $      226.31
  Cost Per Hour:              $      150.87
  Overhead %:                          7.9%
```

**Your quote to client**: **$20,000** (rounded)

---

## 💰 Your Current Cost Structure

### Monthly Subscriptions: $989

| Category | Services | Monthly Cost |
|----------|----------|--------------|
| **AI Tools** | Claude Max, ChatGPT Pro, Cursor AI, Gemini Pro, Grok | $300 |
| **Development** | Vercel Pro, Replit Core, Lovable Pro | $70 |
| **Data/Scraping** | Apify, BrightData | $549 |
| **Cloud** | Google Cloud APIs | $50 |

### Hardware Depreciation: $219/month

| Device | Purchase Price | Monthly |
|--------|---------------|---------|
| Mac Studio | $3,999 | $83.31 |
| MacBook Pro 2024 | $3,499 | $72.90 |
| Synology NAS | $1,200 | $20.00 |
| Samsung S24 Ultra | $1,299 | $36.08 |
| HP Printer | $400 | $6.67 |

### Operational Costs: $230/month

- AT&T Internet: $110
- Google Fi: $70
- Electricity (compute): $50

### Total Fixed Monthly Costs: $1,438

This gets allocated to projects based on actual usage.

---

## 📊 Real Project Example

### 3M Lighting - Garage Organizers Category Intelligence

**Scope**:
- 45 calendar days (30 active work days)
- 120 billable hours
- Comprehensive category intelligence report
- 1,500+ products analyzed across 5 retailers
- 42 social videos collected and analyzed
- PowerPoint presentation with insights

**Costs**:
```
Labor:              $16,975.00  (120 hours)
Subscriptions:      $   969.00  (allocated)
Hardware:           $   159.22  (allocated)
Operational:        $   172.50  (allocated)
API Usage:          $     7.48  (direct)
                    ──────────
TOTAL DIRECT:       $18,283.20

Markup (50%):       $ 9,141.60
                    ══════════
QUOTED PRICE:       $27,424.80
```

**Result**: Effective rate of **$228.54/hour**

---

## 🎓 How the System Works

### Cost Allocation Methodology

#### 1. Labor Costs (Direct)
- Tracked hours × task-specific rates
- Different rates for different work types
- Client meetings: $175/hr (premium)
- Analysis/research: $150/hr (core value)
- Data collection: $125/hr (operational)

#### 2. Subscription Allocation (Proportional)
- Only charge for subscriptions actually used
- Allocated based on project duration
- Formula: `Monthly Cost × (Project Days / 20)`
- Example: Claude Max for 30-day project = $200 × 1.5 = $300

#### 3. Hardware Depreciation (Time-based)
- Allocated based on hours worked
- Formula: `Monthly Depreciation × (Project Hours / 160)`
- Example: 120 project hours = $219 × 0.75 = $164.25

#### 4. Operational Overhead (Per-hour)
- Distributed across all billable hours
- Formula: `($230 / 160) × Project Hours`
- Hourly operational rate: $1.44/hour

#### 5. API Costs (Direct Attribution)
- Exactly what you used from provider dashboards
- No allocation needed - direct pass-through
- OpenAI Whisper: $0.006/minute
- GPT-4 Vision: $0.00765/image
- Claude Sonnet: $3/M input tokens, $15/M output tokens

### Pricing Formula

```
1. Calculate all direct costs
2. Add 50% markup (industry standard)
3. Round to nearest $500 for cleaner quote
```

**50% Markup Covers**:
- Marketing & sales time
- Proposal development
- Professional development
- Business insurance
- Accounting & legal
- Bad debt risk
- Bench time
- Profit margin

---

## 📈 Project Size Guidelines

### Small Project (40-60 hours)
- **Duration**: 2-3 weeks
- **Example**: Single category analysis, basic research
- **Cost Range**: $8,000 - $13,000
- **Deliverable**: Report + basic presentation

### Medium Project (80-120 hours)
- **Duration**: 4-6 weeks
- **Example**: Comprehensive category intelligence
- **Cost Range**: $18,000 - $29,000
- **Deliverable**: Full analysis + presentation + data files

### Large Project (150-200 hours)
- **Duration**: 8-12 weeks
- **Example**: Multi-category analysis, ongoing research
- **Cost Range**: $33,000 - $50,000
- **Deliverable**: Comprehensive strategic report + ongoing insights

---

## 🔍 API Usage Tracking

### Where to Find Usage Data

| Provider | Dashboard URL | What to Track |
|----------|--------------|---------------|
| **OpenAI** | platform.openai.com/usage | Whisper minutes, GPT-4V images |
| **Anthropic** | console.anthropic.com/settings/usage | Input/output tokens |
| **Apify** | console.apify.com/billing | Results scraped, compute units |
| **BrightData** | brightdata.com/cp/reports | Requests made, GB transferred |
| **Google Cloud** | console.cloud.google.com/apis | API requests (usually free tier) |

### When to Check

- **Weekly during project**: Monitor for unexpected spikes
- **End of project**: Get final totals for cost calculation
- **Monthly**: Review overall usage trends

---

## 💡 Best Practices

### Time Tracking

✅ **DO**:
- Log time every day
- Be honest about hours (including mistakes)
- Track all activities (meetings, emails, research)
- Use the predefined categories
- Note scope creep separately

❌ **DON'T**:
- Wait until end of project to reconstruct
- Inflate hours to justify price
- Forget non-coding work
- Combine unrelated activities

### API Cost Management

✅ **DO**:
- Monitor usage weekly during projects
- Use batch processing when possible
- Consider local models for bulk processing
- Cache results to avoid re-processing
- Set budget alerts in provider dashboards

❌ **DON'T**:
- Ignore API costs until bill arrives
- Over-process (analyze more than needed)
- Forget to track in project YAML
- Use expensive APIs when cheap ones suffice

### Pricing

✅ **DO**:
- Quote fixed prices based on scope
- Include 15-20% contingency in estimates
- Focus on value delivered, not hours
- Be transparent about process
- Round to clean numbers ($29,500 not $29,337)

❌ **DON'T**:
- Quote pure hourly rates
- Underprice to win business
- Hide costs in markup
- Compete solely on price
- Give discounts without reason

---

## 📁 File Organization

```
project-root/
├── config/
│   └── cost_configuration.yaml          # Master cost database
│
├── scripts/
│   └── calculate_project_costs.py       # Cost calculator
│
├── projects/
│   ├── project_cost_template.yaml       # Template for new projects
│   ├── 3m-lighting-garage-organizers-costs.yaml  # Example project
│   ├── client-a-project-costs.yaml      # Your projects...
│   ├── client-b-project-costs.yaml
│   └── client-c-project-ESTIMATE.yaml   # Use for estimates too
│
└── docs/
    ├── PROJECT_COST_TRACKING_GUIDE.md   # Full documentation
    └── COST_TRACKING_QUICK_REFERENCE.md # Quick reference card
```

---

## 🛠️ Common Commands

```bash
# Start new project
cp projects/project_cost_template.yaml projects/CLIENT-PROJECT.yaml

# Calculate costs (console output)
python scripts/calculate_project_costs.py --project projects/CLIENT-PROJECT.yaml

# Export to JSON
python scripts/calculate_project_costs.py \
  --project projects/CLIENT-PROJECT.yaml \
  --format json \
  --output projects/CLIENT-PROJECT-costs.json

# Both formats
python scripts/calculate_project_costs.py \
  --project projects/CLIENT-PROJECT.yaml \
  --format both \
  --output projects/CLIENT-PROJECT-costs.json

# Custom config location
python scripts/calculate_project_costs.py \
  --project projects/CLIENT-PROJECT.yaml \
  --config config/cost_configuration_2026.yaml
```

---

## 🔧 Customization

### Update Subscription Costs

Edit `config/cost_configuration.yaml`:

```yaml
subscriptions:
  ai_tools:
    claude_max:
      cost: 250.00  # Update when price changes
```

### Adjust Your Rates

```yaml
labor:
  consultant_hourly_rate: 175.00  # Raise annually

  task_categories:
    client_meetings: 200.00  # Premium rate
    data_analysis: 175.00
    # ... etc
```

### Add New Hardware

```yaml
hardware:
  new_device:
    purchase_price: 2000.00
    purchase_date: "2026-01-15"
    depreciation_years: 3
    monthly_depreciation: 55.56
    notes: "New equipment"
```

### Add New API Service

```yaml
api_pricing:
  new_service:
    cost_per_unit: 0.05
    unit: "requests"
    notes: "New API description"
```

---

## 📊 Using Cost Data

### For Tax Purposes

Export project costs to JSON for accounting:

```bash
python scripts/calculate_project_costs.py \
  --project projects/completed-project.yaml \
  --format json \
  --output tax-docs/2025/project-name.json
```

Keep for tax records:
- Project YAML files (time tracking)
- Cost calculation JSON (expenses)
- API usage receipts
- Subscription receipts

### For Business Analysis

Aggregate costs across projects:
- Which projects are most profitable?
- What's your effective hourly rate?
- Are you under/over-pricing?
- Which APIs cost the most?

### For Client Proposals

Use historical data for estimates:
```bash
# Run calculation on estimate YAML
python scripts/calculate_project_costs.py \
  --project projects/prospect-company-ESTIMATE.yaml
```

Use output to create proposal with confidence.

---

## 🚨 Troubleshooting

### "KeyError: 'hours'" Error
- Check that your project YAML has `time_tracking` section
- Ensure all task categories are present (even if 0.0 hours)

### "FileNotFoundError: config/cost_configuration.yaml"
- Run command from project root directory
- Or use `--config` flag to specify path

### Costs Seem Too High/Low
- Review `cost_configuration.yaml` prices
- Check that `tools_used` only lists what you actually used
- Verify API usage numbers from dashboards
- Review time tracking for accuracy

### API Costs Show $0
- Make sure API usage fields have values in project YAML
- Check that field names match calculator expectations
- Review `api_usage` section in your project file

---

## 📚 Additional Resources

- **Full Documentation**: `docs/PROJECT_COST_TRACKING_GUIDE.md`
- **Quick Reference**: `docs/COST_TRACKING_QUICK_REFERENCE.md`
- **Example Project**: `projects/3m-lighting-garage-organizers-costs.yaml`
- **Template**: `projects/project_cost_template.yaml`

---

## 📝 Next Steps

1. **Review** the example project: `projects/3m-lighting-garage-organizers-costs.yaml`
2. **Test** the calculator with the example
3. **Create** your next project file from template
4. **Track** time and costs as you work
5. **Calculate** costs when complete
6. **Review** profitability and adjust rates if needed

---

## 🎯 Summary

You now have a **professional cost tracking and pricing system** that:

✅ Tracks all project costs accurately
✅ Allocates overhead fairly across projects
✅ Provides defensible pricing for clients
✅ Gives visibility into profitability
✅ Scales across all your client projects
✅ Produces professional cost reports
✅ Supports tax documentation
✅ Enables data-driven pricing decisions

**Your effective hourly rate** will typically be **$220-250/hour** using this system with 50% markup.

**Your quoted projects** will be competitive and profitable.

**Your cost tracking** will be accurate and defensible.

---

**Start using the system on your next project!**

Questions? See `docs/PROJECT_COST_TRACKING_GUIDE.md` for comprehensive details.

---

**System Version**: 1.0.0
**Created**: 2025-10-30
**For**: Category Intelligence & Market Research Projects
