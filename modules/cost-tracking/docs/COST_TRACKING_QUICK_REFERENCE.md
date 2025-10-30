# Cost Tracking Quick Reference Card

## 🚀 Quick Start (3 Steps)

### 1. Start New Project
```bash
cp projects/project_cost_template.yaml projects/client-name-project.yaml
```

### 2. Track Time & Usage
Update your project YAML file as you work:
- Log hours daily
- Note which tools you used
- Track API usage from dashboards

### 3. Calculate Costs
```bash
python scripts/calculate_project_costs.py \
  --project projects/client-name-project.yaml
```

---

## 📋 Monthly Subscription Costs

| Service | Cost | Usage |
|---------|------|-------|
| Claude Max | $200 | Analysis, reports |
| ChatGPT Pro | $20 | Scripts, coding |
| Cursor AI Pro | $20 | IDE |
| Gemini Pro | $20 | Analysis |
| Grok | $40 | Data parsing |
| Vercel Pro | $20 | Web hosting |
| Replit Core | $25 | Quick prototypes |
| Lovable Pro | $25 | Website builder |
| Apify | $49 | Video scraping |
| BrightData | $500 | Product scraping |
| Google Cloud | $50 | APIs |
| **TOTAL** | **~$989/mo** | |

---

## 💰 API Pricing (Pay-per-use)

| Service | Rate | Example Cost |
|---------|------|--------------|
| OpenAI Whisper | $0.006/min | 50 min = $0.30 |
| GPT-4 Vision | $0.00765/image | 500 images = $3.83 |
| Claude Sonnet Input | $3/M tokens | 250K = $0.75 |
| Claude Sonnet Output | $15/M tokens | 75K = $1.13 |
| BrightData | $3/1K requests | 500 = $1.50 |

---

## 🖥️ Hardware Depreciation

| Device | Monthly Cost | Note |
|--------|-------------|------|
| Mac Studio | $83.31 | 4-year depreciation |
| MacBook Pro 2024 | $72.90 | 4-year depreciation |
| Synology NAS | $20.00 | 5-year depreciation |
| Samsung S24 Ultra | $36.08 | 3-year depreciation |
| HP Printer | $6.67 | 5-year depreciation |
| **TOTAL** | **$219/mo** | |

---

## 📡 Operational Costs

| Service | Cost |
|---------|------|
| AT&T Internet | $110 |
| Google Fi | $70 |
| Electricity (compute) | $50 |
| **TOTAL** | **$230/mo** |

---

## ⏱️ Labor Rates by Task

| Task | Rate |
|------|------|
| Client Meetings | $175/hr |
| Discovery & Research | $150/hr |
| Data Analysis | $150/hr |
| Report Writing | $150/hr |
| Project Management | $150/hr |
| Data Collection | $125/hr |
| Presentation Design | $125/hr |

---

## 📊 Cost Allocation Formulas

### Subscriptions
```
Allocated = Monthly Cost × (Project Days / 20)
```
Only charge for subscriptions actually used!

### Hardware
```
Allocated = Monthly Depreciation × (Project Hours / 160)
```

### Operational
```
Allocated = (Total Operational / 160) × Project Hours
Hourly Rate = $230 / 160 = $1.44/hr
```

### APIs
```
Direct attribution from actual usage
```

---

## 💵 Pricing Formula

```
Total Direct Costs = Labor + Subscriptions + Hardware + Operational + APIs

Markup Amount = Total Direct Costs × 50%

Quoted Price = Total Direct Costs + Markup
```

**Standard Markup: 50%**

---

## 📈 Example Project Costs

**Garage Organizers Report (120 hours)**

| Category | Cost |
|----------|------|
| Labor | $16,975 |
| Subscriptions | $969 |
| Hardware | $159 |
| Operational | $173 |
| APIs | $7 |
| **Subtotal** | **$18,283** |
| Markup (50%) | $9,142 |
| **QUOTED PRICE** | **$27,425** |

**Effective Rate**: $228/hour

---

## 🔍 Where to Find API Usage

| Provider | URL |
|----------|-----|
| OpenAI | https://platform.openai.com/usage |
| Anthropic | https://console.anthropic.com/settings/usage |
| Apify | https://console.apify.com/billing |
| BrightData | https://brightdata.com/cp/reports |
| Google Cloud | https://console.cloud.google.com/apis/dashboard |

---

## ✅ Project Tracking Checklist

### Before Project
- [ ] Copy `project_cost_template.yaml`
- [ ] Fill in project name, client, estimated hours
- [ ] Set up time tracking method

### During Project
- [ ] Log time daily
- [ ] Note which tools/subscriptions used
- [ ] Track any scope changes

### After Project
- [ ] Collect API usage from dashboards
- [ ] Update project YAML with actuals
- [ ] Run cost calculator
- [ ] Review profitability
- [ ] Archive project file

---

## 🎯 Typical Project Sizes

### Small Project (40-60 hours)
- **Labor**: $5,000-$8,000
- **Overhead**: $500-$800
- **APIs**: $50-$200
- **Quote**: $8,000-$13,000

### Medium Project (80-120 hours)
- **Labor**: $11,000-$17,000
- **Overhead**: $1,000-$1,500
- **APIs**: $100-$500
- **Quote**: $18,000-$29,000

### Large Project (150-200 hours)
- **Labor**: $20,000-$30,000
- **Overhead**: $1,800-$2,500
- **APIs**: $200-$1,000
- **Quote**: $33,000-$50,000

---

## 🛠️ Commands Cheat Sheet

```bash
# Start new project
cp projects/project_cost_template.yaml projects/CLIENT-PROJECT.yaml

# Calculate costs (text output)
python scripts/calculate_project_costs.py \
  --project projects/CLIENT-PROJECT.yaml

# Calculate costs (JSON output)
python scripts/calculate_project_costs.py \
  --project projects/CLIENT-PROJECT.yaml \
  --format json \
  --output projects/CLIENT-PROJECT-costs.json

# Both formats
python scripts/calculate_project_costs.py \
  --project projects/CLIENT-PROJECT.yaml \
  --format both \
  --output projects/CLIENT-PROJECT-costs.json
```

---

## 📝 Time Tracking Tips

1. **Log daily** - Don't wait until end of week
2. **Be honest** - Track all time, including mistakes
3. **Use categories** - Match YAML categories
4. **Note scope creep** - Track separately
5. **Include everything**:
   - Research time
   - Client emails
   - Meetings
   - Rework
   - Project planning

---

## 💡 Profitability Tips

### Maximize Efficiency
- Reuse code/scripts from previous projects
- Build templates and frameworks
- Automate repetitive tasks
- Use faster/cheaper APIs when appropriate

### Control Costs
- Monitor API usage weekly
- Use local models when possible
- Batch API requests
- Cancel unused subscriptions

### Price Right
- Add 15-20% contingency to estimates
- Charge for value, not just time
- Consider project risk in markup
- Don't compete on price alone

---

## 🚨 Common Mistakes to Avoid

❌ **Not tracking time daily** → Inaccurate estimates
❌ **Forgetting API costs** → Surprise overruns
❌ **Under-pricing** → Not sustainable
❌ **Not including all overhead** → Losing money
❌ **Charging for unused tools** → Inflated costs
❌ **No contingency buffer** → Scope creep kills margin

---

## 📞 Need Help?

See full documentation:
```
docs/PROJECT_COST_TRACKING_GUIDE.md
```

Example project:
```
projects/3m-lighting-garage-organizers-costs.yaml
```

Configuration:
```
config/cost_configuration.yaml
```

---

**Last Updated**: 2025-10-30
