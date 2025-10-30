# Cost Tracking Module

## ⚠️ INTERNAL/OPERATIONAL MODULE - NOT CLIENT-FACING

**Module Type**: Internal Business Operations
**Status**: Production Ready
**Purpose**: Track project costs and calculate pricing across all client projects

---

## 🎯 What This Module Does

This is an **internal business operations module** that helps you:
- Track time and costs across client projects
- Allocate subscription and overhead costs
- Calculate accurate project pricing
- Analyze profitability
- Generate professional cost reports

**This module is NOT delivered to clients.** It's for your internal business operations only.

---

## 📂 Module Structure

```
modules/cost-tracking/
├── README.md                          # This file
├── COST_TRACKING_SYSTEM_README.md     # System overview
├── COST_SYSTEM_DELIVERY_SUMMARY.md    # What was built
│
├── config/
│   └── cost_configuration.yaml        # Master cost database
│
├── scripts/
│   └── calculate_project_costs.py     # Cost calculator
│
├── projects/
│   ├── project_cost_template.yaml     # Template for new projects
│   ├── 3m-lighting-garage-organizers-costs.yaml   # Example client project
│   ├── 3m-lighting-garage-organizers-costs.json
│   └── cost-tracking-module-development.yaml      # This R&D project
│
└── docs/
    ├── PROJECT_COST_TRACKING_GUIDE.md       # Complete guide
    └── COST_TRACKING_QUICK_REFERENCE.md     # Quick reference
```

---

## 🚀 Quick Start

### Calculate Costs for a Client Project

```bash
cd modules/cost-tracking

# Run calculator
python scripts/calculate_project_costs.py \
  --project projects/client-project-name.yaml
```

### Start Tracking a New Project

```bash
# Copy template
cp projects/project_cost_template.yaml \
   projects/new-client-project.yaml

# Edit with your time tracking
code projects/new-client-project.yaml
```

---

## 💰 What Gets Tracked

### Your Monthly Business Costs

- **Subscriptions**: $989/month (Claude, ChatGPT, Cursor, Apify, BrightData, etc.)
- **Hardware**: $219/month (Mac Studio, MacBook Pro, NAS, etc. - depreciation)
- **Operational**: $230/month (Internet, mobile, electricity)
- **APIs**: Pay-per-use (OpenAI, Anthropic, BrightData, etc.)

### Per-Project Allocation

The system allocates costs to each project based on:
- **Labor**: Tracked hours × task-specific rates ($125-175/hour)
- **Subscriptions**: Proportional usage (only tools actually used)
- **Hardware**: Time-based allocation
- **Operational**: Per-hour overhead rate
- **APIs**: Direct attribution from usage

### Pricing Formula

```
Total Direct Costs (Labor + Allocated Overhead + APIs)
× 1.50 (50% markup)
────────────────────────────────
= Quoted Price to Client
```

---

## 📊 Example: 3M Lighting Project

**Project**: Garage Organizers Category Intelligence
**Hours**: 120
**Quote**: $27,425

```
Labor:              $16,975
Subscriptions:      $   969
Hardware:           $   159
Operational:        $   173
APIs:               $     7
                    ───────
Direct Costs:       $18,283
Markup (50%):       $ 9,142
                    ═══════
QUOTED PRICE:       $27,425
```

**Effective Rate**: $228/hour

---

## 📚 Documentation

- **`COST_TRACKING_SYSTEM_README.md`** - System overview and quick start
- **`docs/PROJECT_COST_TRACKING_GUIDE.md`** - Comprehensive 5,500-word guide
- **`docs/COST_TRACKING_QUICK_REFERENCE.md`** - One-page reference
- **`COST_SYSTEM_DELIVERY_SUMMARY.md`** - What was built

---

## 🔧 Maintenance

### Update Subscription Costs

Edit `config/cost_configuration.yaml`:

```yaml
subscriptions:
  ai_tools:
    claude_max:
      cost: 200.00  # Update when price changes
```

### Update Your Rates

```yaml
labor:
  consultant_hourly_rate: 175.00  # Raise annually
```

### Add New Hardware

```yaml
hardware:
  new_device:
    purchase_price: 2000.00
    purchase_date: "2026-01-15"
    depreciation_years: 3
    monthly_depreciation: 55.56
```

---

## 🎯 Use Cases

### 1. Quote New Client Project

1. Copy `projects/project_cost_template.yaml`
2. Estimate hours based on scope
3. Run calculator
4. Use output as basis for proposal

### 2. Track Active Project

1. Log time daily in project YAML
2. Monitor API usage weekly
3. Run calculator at completion
4. Review profitability

### 3. Analyze Business Performance

1. Run calculator on all completed projects
2. Compare quoted vs actual
3. Identify most profitable project types
4. Adjust rates accordingly

---

## ⚠️ Important Notes

### This is NOT a Client Module

- **DON'T** include in client deliverables
- **DON'T** show cost breakdowns to clients
- **DO** use for internal pricing decisions
- **DO** quote fixed prices to clients (not hourly rates)

### Client Communication

**❌ Don't Say**:
- "My hourly rate is $150"
- "Here's my cost breakdown..."
- "I need to cover my subscriptions..."

**✅ Do Say**:
- "The project investment is $27,500"
- "This includes comprehensive analysis and deliverables"
- "The price reflects the strategic value and business outcomes"

### Tax & Accounting

- Keep all project YAML files for tax records
- Export to JSON for accounting integration
- Track deductible expenses (subscriptions, hardware, etc.)
- Consult your accountant for specific guidance

---

## 🔍 Module Dependencies

### Python Requirements

```bash
# Standard library only - no external dependencies
python 3.7+
pyyaml (already in project requirements.txt)
```

### File Dependencies

- Requires: `config/cost_configuration.yaml` (cost database)
- Uses: Project YAML files in `projects/` directory
- Outputs: Text reports and/or JSON files

---

## 📈 Typical Project Costs

| Size | Hours | Direct Cost | Quote | Effective Rate |
|------|-------|-------------|-------|----------------|
| Small | 40-60 | $6,500-$10,500 | $10,000-$16,000 | $200-$267/hr |
| Medium | 80-120 | $13,000-$20,000 | $20,000-$30,000 | $220-$250/hr |
| Large | 150-200 | $23,000-$35,000 | $35,000-$53,000 | $233-$265/hr |

---

## 🎓 Best Practices

### Time Tracking

- ✅ Log time daily (don't wait until project end)
- ✅ Track all activities (meetings, emails, research)
- ✅ Be honest about hours (including mistakes)
- ✅ Use predefined categories consistently

### API Cost Management

- ✅ Monitor usage weekly during projects
- ✅ Check provider dashboards after completion
- ✅ Log actual usage in project YAML
- ✅ Look for optimization opportunities

### Pricing

- ✅ Quote fixed prices based on value
- ✅ Add 15-20% contingency to estimates
- ✅ Focus on outcomes, not hours
- ✅ Raise rates annually

---

## 🚨 Common Pitfalls to Avoid

❌ **Not tracking time daily** → Inaccurate estimates
❌ **Forgetting API costs** → Surprise overruns
❌ **Under-pricing** → Unsustainable business
❌ **Showing cost breakdown to clients** → Commoditizes your work
❌ **Competing on price alone** → Race to the bottom

---

## 💡 R&D Note

This module was developed as an R&D investment to create a reusable cost tracking system for all future client projects. The development itself is tracked as:

**Project**: `projects/cost-tracking-module-development.yaml`
**Type**: R&D / Internal Development
**Billable**: Consulting time only (not implementation time)

This module will pay for itself within 2-3 client projects through:
- More accurate pricing
- Better profitability visibility
- Reduced estimation errors
- Professional cost documentation

---

## 📞 Support

For questions or issues:
1. Review `docs/PROJECT_COST_TRACKING_GUIDE.md` (comprehensive guide)
2. Check `docs/COST_TRACKING_QUICK_REFERENCE.md` (quick reference)
3. Look at example: `projects/3m-lighting-garage-organizers-costs.yaml`

---

## 🔄 Version History

- **v1.0.0** (2025-10-30): Initial release
  - Complete cost tracking system
  - Automated calculator
  - Comprehensive documentation
  - Production ready

---

**Module Type**: Internal Operations
**Status**: ✅ Production Ready
**Last Updated**: 2025-10-30
