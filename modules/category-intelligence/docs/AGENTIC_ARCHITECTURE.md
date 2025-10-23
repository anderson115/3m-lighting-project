# Agentic Category Intelligence Architecture

**Design Philosophy**: AI-Guided, Modular, Zero-Fabrication
**Status**: Production-Ready Design
**Last Updated**: 2025-10-16

---

## 🧠 CORE PRINCIPLES

### **1. Zero Fabrication Tolerance**
- ❌ NO placeholder data
- ❌ NO made-up numbers
- ❌ NO unverified claims
- ✅ ONLY live-acquired data
- ✅ EVERY data point traced to source
- ✅ VALIDATION before acceptance

### **2. Agentic Reasoning**
- 🤖 Agents validate data quality
- 🤖 Agents assess relevance
- 🤖 Agents identify gaps
- 🤖 Agents recommend refinements
- 🤖 Orchestrator makes final decisions

### **3. Modular Design**
- Each agent operates independently
- Agents communicate via structured protocols
- Failure in one agent doesn't break system
- Easy to add new data sources/agents

### **4. Quality-First**
- Data must pass validation before acceptance
- Confidence scoring on every data point
- Orchestrator can reject low-quality data
- Feedback loops for continuous improvement

---

## 🏗️ AGENT ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────┐
│                     ORCHESTRATOR AGENT                           │
│                                                                   │
│  Responsibilities:                                                │
│  - Coordinate all data collection agents                         │
│  - Accept/Reject/Refine data based on validation                │
│  - Track progress towards deliverable                            │
│  - Identify data gaps                                            │
│  - Request refinements from agents                               │
│  - Generate final report when quality threshold met              │
│                                                                   │
└───────────────────┬─────────────────────────────────────────────┘
                    │
        ┌───────────┴───────────────────────┐
        │                                   │
┌───────▼────────┐                 ┌───────▼────────┐
│  COLLECTION    │                 │  VALIDATION    │
│    AGENTS      │                 │    AGENTS      │
│                │                 │                │
│ - MarketAgent  │────────────────▶│ - QualityAgent │
│ - BrandAgent   │                 │ - RelevanceAgt │
│ - PricingAgent │                 │ - SourceAgt    │
│ - ScraperAgent │                 │ - GapAgent     │
│ - ResourceAgent│                 │                │
└────────────────┘                 └────────────────┘
        │                                   │
        │                                   │
        ▼                                   ▼
┌─────────────────────────────────────────────────┐
│              FEEDBACK LOOP                       │
│  - Validation failures → Refinement requests    │
│  - Gap identification → New collection tasks    │
│  - Quality issues → Data re-acquisition         │
└─────────────────────────────────────────────────┘
```

---

## 🤖 AGENT SPECIFICATIONS

### **1. OrchestratorAgent (Master Coordinator)**

**Role**: Oversee entire data collection process, ensure quality, make accept/reject decisions

**Responsibilities**:
- Initialize all collection agents
- Define data requirements (50+ brands, pricing, market size, etc.)
- Receive data from collection agents
- Submit data to validation agents
- Make accept/reject/refine decisions
- Track completeness (% of required data collected)
- Identify gaps and assign tasks to fill them
- Trigger report generation when threshold met (95%+ complete)

**Decision Framework**:
```python
def evaluate_data(self, data: DataSubmission, validation_results: ValidationResults):
    """
    Decision tree:
    1. If validation score >= 0.9 → ACCEPT
    2. If validation score 0.7-0.9 → REFINE (request improvements)
    3. If validation score < 0.7 → REJECT (re-acquire)
    4. If source untraceable → REJECT
    5. If relevance score < 0.8 → REJECT
    """
```

**Prompting Strategy**:
```
You are the Orchestrator Agent for a category intelligence system.

Your mission: Ensure ZERO fabricated data enters the system.

For each data submission, you must:
1. Verify source traceability
2. Assess data quality (completeness, accuracy, recency)
3. Check relevance to garage storage category
4. Make decision: ACCEPT, REFINE, or REJECT

Current requirements:
- 50+ brands with revenue estimates
- Pricing data from 4+ retailers
- Market size with confidence levels
- All data points must have sources

Current progress: {progress_summary}
Current gaps: {identified_gaps}

Decision needed for: {data_submission}
```

---

### **2. MarketDataAgent (Market Size & Growth)**

**Role**: Collect market sizing, growth rates, projections from verified sources

**Data Sources**:
1. WebSearch → Industry reports (IMARC, Research and Markets)
2. FRED API → Retail sales time series
3. Census Bureau → Retail trade statistics
4. World Bank API → Economic indicators

**Collection Process**:
```python
async def collect_market_data(self, category: str) -> MarketDataSubmission:
    """
    Step 1: WebSearch for recent industry reports (2024-2025)
    Step 2: Extract market size figures with confidence levels
    Step 3: Download FRED retail sales data for validation
    Step 4: Cross-reference with Census data
    Step 5: Calculate confidence score based on source agreement
    Step 6: Package with full source URLs
    Step 7: Submit to orchestrator for validation
    """
```

**Validation Criteria**:
- ✅ Multiple independent sources confirm same figure (±10%)
- ✅ Source published within 12 months
- ✅ Source is authoritative (industry analyst, government data)
- ✅ Full URL to source provided
- ✅ Methodology documented

**Output Format**:
```python
{
    "data_type": "market_size",
    "value": "$3.5B",
    "year": 2024,
    "confidence": 0.95,
    "sources": [
        {
            "url": "https://www.globenewswire.com/...",
            "publisher": "Research and Markets",
            "date": "2024-07-30",
            "excerpt": "...$3.5 billion US garage organization product industry..."
        },
        {
            "url": "https://fred.stlouisfed.org/series/RSXFS",
            "publisher": "Federal Reserve",
            "date": "2024-09-01",
            "value_extracted": 725643,
            "validation": "Consistent with reported growth trends"
        }
    ],
    "reasoning": "Two independent authoritative sources confirm $3.5B market size for 2024",
    "quality_score": 0.95
}
```

---

### **3. BrandDiscoveryAgent**

**Role**: Identify brands across all market tiers with revenue/positioning data

**Data Sources**:
1. WebSearch → Industry reports, press releases
2. SEC EDGAR → Public company filings
3. Company websites → Product catalogs, about pages
4. ZoomInfo/Owler → Company profiles (when available)

**Collection Process**:
```python
async def discover_brands(self, category: str, target_count: int = 50) -> BrandDataSubmission:
    """
    Step 1: WebSearch for "[category] market share brands"
    Step 2: Extract brand names from multiple sources
    Step 3: For each brand:
        - Identify parent company
        - Find revenue data (if available)
        - Determine market tier (revenue-based)
        - Extract positioning (premium/value/professional)
        - Find distribution channels
    Step 4: Validate each brand is relevant to category
    Step 5: Continue until 50+ brands found
    Step 6: Package with source URLs for each brand
    """
```

**Validation Criteria**:
- ✅ Brand name verified from multiple sources
- ✅ Brand confirmed to sell garage storage products
- ✅ Parent company identified (or marked as independent)
- ✅ Tier assignment based on objective criteria (revenue, market presence)
- ✅ Revenue data sourced (or marked as estimated with confidence level)

**Output Format**:
```python
{
    "brand_name": "Rubbermaid",
    "parent_company": "Newell Brands",
    "tier": 1,
    "tier_rationale": "Major national brand, confirmed in top 5 market share",
    "estimated_category_revenue": "$400M-$600M",
    "confidence": "medium",
    "positioning": "Value-oriented, mass market",
    "distribution": ["Home Depot", "Lowe's", "Amazon", "Walmart", "Target"],
    "sources": [
        {
            "url": "https://www.businesswire.com/...",
            "excerpt": "...Newell Rubbermaid...key players...",
            "date": "2024-08-05"
        }
    ],
    "quality_score": 0.85
}
```

---

### **4. PricingScraperAgent**

**Role**: Acquire real product pricing from retailer websites

**Data Sources**:
1. Scrapling → Web scraping with Camoufox
2. Retailer APIs → If available
3. Price comparison sites → Aggregated data

**Collection Process**:
```python
async def scrape_pricing(self, query: str, retailers: List[str]) -> PricingDataSubmission:
    """
    Step 1: Initialize StealthyFetcher with anti-detection
    Step 2: For each retailer:
        a. Search for query (e.g., "garage storage bins")
        b. Extract product listings (name, price, rating)
        c. Validate data extraction (ensure prices are real)
        d. Cache results
    Step 3: Aggregate pricing by product category
    Step 4: Calculate price ranges, averages
    Step 5: Package with product URLs as sources
    Step 6: Submit with confidence scores
    """
```

**Validation Criteria**:
- ✅ Prices are current (timestamp within 24 hours)
- ✅ Product URLs provided for verification
- ✅ Product names match category (relevance check)
- ✅ Prices are realistic (outlier detection)
- ✅ Multiple products per category (n >= 10)

**Output Format**:
```python
{
    "subcategory": "Storage Bins",
    "retailer": "home_depot",
    "products": [
        {
            "name": "Sterilite 27 Gal. Storage Bin",
            "price": 12.98,
            "currency": "USD",
            "url": "https://www.homedepot.com/p/...",
            "in_stock": True,
            "scraped_at": "2025-10-16T09:30:00Z"
        }
        # ... more products
    ],
    "price_range": {"min": 5.99, "max": 49.99},
    "average_price": 18.75,
    "median_price": 14.99,
    "product_count": 47,
    "quality_score": 0.92
}
```

---

### **5. ResourceCuratorAgent**

**Role**: Curate authoritative sources for validation and reference

**Data Sources**:
1. WebSearch → Industry reports, guides, tutorials
2. Data.gov → Government datasets
3. Academic sources → Research papers
4. Trade publications → Industry news

**Collection Process**:
```python
async def curate_resources(self, category: str, target_count: int = 30) -> ResourceSubmission:
    """
    Step 1: WebSearch for various resource types:
        - Industry reports
        - Retailer buying guides
        - DIY/how-to content
        - Trade publications
        - Product reviews
    Step 2: For each resource:
        - Validate URL is accessible
        - Extract title, publisher, date
        - Assess relevance to category
        - Rate authority of source
    Step 3: Organize by resource type
    Step 4: Ensure diversity (not all from one source)
    Step 5: Package with descriptions
    """
```

**Validation Criteria**:
- ✅ URL is accessible (HTTP 200)
- ✅ Content is relevant to garage storage
- ✅ Source is authoritative (known publisher)
- ✅ Content is recent (<2 years preferred)
- ✅ Diversity of source types

---

### **6. ValidationAgents (Quality Gatekeepers)**

#### **QualityValidationAgent**

**Role**: Assess data quality and completeness

**Validation Checks**:
```python
def validate_quality(self, data: DataSubmission) -> ValidationResult:
    """
    Checks:
    1. Completeness: All required fields present?
    2. Format: Data types correct?
    3. Ranges: Values within expected bounds?
    4. Consistency: Data internally consistent?
    5. Recency: Data current enough?

    Score: 0.0 (fail) to 1.0 (perfect)
    """
```

#### **RelevanceValidationAgent**

**Role**: Ensure data is relevant to garage storage category

**Validation Checks**:
```python
def validate_relevance(self, data: DataSubmission, category: str) -> ValidationResult:
    """
    Use AI reasoning to check:
    1. Does product/brand/data relate to garage storage?
    2. Is this data useful for category intelligence?
    3. Would this appear in a garage storage report?

    Examples:
    - ✅ "Rubbermaid storage bins" → Relevant
    - ❌ "Rubbermaid kitchen containers" → Not relevant
    - ✅ "Home Depot garage cabinets pricing" → Relevant
    - ❌ "Home Depot lawn mowers" → Not relevant

    Score: 0.0 (irrelevant) to 1.0 (highly relevant)
    """
```

#### **SourceValidationAgent**

**Role**: Verify every data point has a traceable source

**Validation Checks**:
```python
def validate_sources(self, data: DataSubmission) -> ValidationResult:
    """
    Checks:
    1. Source URL provided?
    2. URL is accessible?
    3. Source is authoritative?
    4. Data point traceable to source?
    5. Methodology documented?

    Fail if ANY data point lacks source.
    """
```

#### **GapIdentificationAgent**

**Role**: Identify missing data that's required for complete report

**Gap Analysis**:
```python
def identify_gaps(self, collected_data: Dict, requirements: Dict) -> List[Gap]:
    """
    Compare collected data vs. requirements:

    Requirements:
    - 50+ brands → Current: 32 → Gap: Need 18 more brands
    - Pricing from 4 retailers → Current: 2 → Gap: Need Lowe's, Walmart
    - Market size 2024 → Current: ✅ → No gap
    - 5-year historical → Current: Missing → Gap: Need historical data

    Returns prioritized list of gaps for orchestrator
    """
```

---

## 🔄 FEEDBACK LOOPS & REFINEMENT

### **Loop 1: Quality Improvement**
```
Collection Agent → Submit Data
    ↓
Validation Agent → Quality Score: 0.75 (needs improvement)
    ↓
Orchestrator → REFINE decision
    ↓
Feedback to Collection Agent: "Price data missing URLs, add sources"
    ↓
Collection Agent → Re-submit with improvements
    ↓
Validation Agent → Quality Score: 0.93 (acceptable)
    ↓
Orchestrator → ACCEPT
```

### **Loop 2: Gap Filling**
```
Gap Agent → Identifies: "Only 32 brands, need 50"
    ↓
Orchestrator → Assign task to BrandDiscoveryAgent
    ↓
BrandDiscoveryAgent → Search for 18 more brands in Tier 3-5
    ↓
Submit new brands → Validation
    ↓
Orchestrator → Track progress: Now 50 brands ✅
```

### **Loop 3: Relevance Filtering**
```
BrandDiscoveryAgent → Submits "Craftsman tools"
    ↓
RelevanceAgent → Score: 0.45 (Craftsman makes tool storage, not garage org)
    ↓
Orchestrator → REJECT, request more specific to garage storage
    ↓
BrandDiscoveryAgent → Focus on garage-specific brands
```

---

## 📊 AGENT COMMUNICATION PROTOCOL

### **Message Types**

```python
class AgentMessage(BaseModel):
    """Base class for all agent communications"""
    message_id: str
    timestamp: datetime
    sender_agent: str
    recipient_agent: str
    message_type: MessageType  # SUBMISSION, VALIDATION, DECISION, TASK, FEEDBACK
    priority: Priority  # LOW, MEDIUM, HIGH, CRITICAL

class DataSubmission(AgentMessage):
    """Collection agent submits data to orchestrator"""
    data_type: str  # "market_size", "brand_data", "pricing", etc.
    data: Dict[str, Any]
    sources: List[Source]
    confidence: float
    quality_self_assessment: float

class ValidationResult(AgentMessage):
    """Validation agent reports on data quality"""
    submission_id: str
    validation_type: str  # "quality", "relevance", "source"
    passed: bool
    score: float  # 0.0-1.0
    issues: List[str]
    recommendations: List[str]

class OrchestratorDecision(AgentMessage):
    """Orchestrator makes accept/reject/refine decision"""
    submission_id: str
    decision: Decision  # ACCEPT, REJECT, REFINE
    reasoning: str
    feedback: Optional[str]  # If REFINE, what to improve

class TaskAssignment(AgentMessage):
    """Orchestrator assigns collection task to agent"""
    task_type: str
    parameters: Dict[str, Any]
    deadline: Optional[datetime]
    priority: Priority

class ProgressReport(AgentMessage):
    """Orchestrator reports current progress"""
    completeness: float  # 0.0-1.0
    gaps: List[Gap]
    quality_distribution: Dict[str, int]  # {"accepted": 45, "refining": 5, "rejected": 2}
    estimated_completion: datetime
```

---

## 🎯 IMPLEMENTATION WORKFLOW

### **Phase 1: Initialize System**
```python
orchestrator = OrchestratorAgent(category="garage storage")

# Define requirements
orchestrator.set_requirements({
    "brands": {"min_count": 50, "tiers": [1, 2, 3, 4, 5]},
    "market_size": {"year": 2024, "confidence": "high"},
    "pricing": {"retailers": 4, "products_per_retailer": 30},
    "historical_growth": {"years": 5},
    "resources": {"min_count": 30, "diversity": True}
})

# Initialize agents
market_agent = MarketDataAgent()
brand_agent = BrandDiscoveryAgent()
pricing_agent = PricingScraperAgent()
resource_agent = ResourceCuratorAgent()

# Initialize validators
quality_agent = QualityValidationAgent()
relevance_agent = RelevanceValidationAgent()
source_agent = SourceValidationAgent()
gap_agent = GapIdentificationAgent()
```

### **Phase 2: Launch Collection**
```python
# Orchestrator assigns initial tasks
await orchestrator.assign_task(market_agent, "collect_market_size")
await orchestrator.assign_task(brand_agent, "discover_brands", limit=50)
await orchestrator.assign_task(pricing_agent, "scrape_pricing", retailers=["homedepot", "lowes"])
await orchestrator.assign_task(resource_agent, "curate_resources", target=30)

# Agents work in parallel
results = await asyncio.gather(
    market_agent.execute_task(),
    brand_agent.execute_task(),
    pricing_agent.execute_task(),
    resource_agent.execute_task()
)
```

### **Phase 3: Validation & Refinement**
```python
for submission in results:
    # Run validation
    quality_result = await quality_agent.validate(submission)
    relevance_result = await relevance_agent.validate(submission, category="garage storage")
    source_result = await source_agent.validate(submission)

    # Orchestrator makes decision
    decision = await orchestrator.evaluate(
        submission=submission,
        validations=[quality_result, relevance_result, source_result]
    )

    if decision.status == "REFINE":
        # Send feedback to agent for improvement
        await orchestrator.request_refinement(submission.agent, decision.feedback)
    elif decision.status == "REJECT":
        # Re-assign task with stricter criteria
        await orchestrator.reassign_task(submission.agent, improved_criteria)
```

### **Phase 4: Gap Analysis & Iteration**
```python
while orchestrator.completeness < 0.95:
    # Identify gaps
    gaps = await gap_agent.analyze(
        collected=orchestrator.accepted_data,
        requirements=orchestrator.requirements
    )

    # Assign tasks to fill gaps
    for gap in gaps:
        await orchestrator.assign_gap_filling_task(gap)

    # Wait for agents to complete
    await orchestrator.wait_for_submissions()

    # Re-validate
    await orchestrator.validation_round()
```

### **Phase 5: Report Generation**
```python
if orchestrator.completeness >= 0.95 and orchestrator.average_quality >= 0.90:
    # Generate final report
    report = await orchestrator.generate_report(
        template="category_intelligence_template.html",
        data=orchestrator.accepted_data,
        audit_trail=orchestrator.source_audit
    )

    print(f"✅ Report generated: {report.path}")
    print(f"   Completeness: {orchestrator.completeness:.1%}")
    print(f"   Avg Quality: {orchestrator.average_quality:.2f}")
    print(f"   Total Sources: {len(orchestrator.all_sources)}")
    print(f"   Zero Fabrication: ✅ All data traced")
else:
    print(f"⚠️ Report not ready")
    print(f"   Completeness: {orchestrator.completeness:.1%} (need 95%)")
    print(f"   Avg Quality: {orchestrator.average_quality:.2f} (need 0.90)")
```

---

## 🔒 ZERO FABRICATION ENFORCEMENT

### **Pre-submission Checks** (Collection Agents)
```python
def prepare_submission(self, data: Dict) -> DataSubmission:
    """Before submitting, agent self-validates"""

    # Check 1: Every data point has source
    for field, value in data.items():
        if not self.has_source(field):
            raise NoSourceError(f"Field '{field}' lacks source attribution")

    # Check 2: Sources are real URLs (not placeholders)
    for source in self.sources:
        if "example.com" in source.url or "placeholder" in source.url:
            raise PlaceholderDetected(f"Placeholder URL: {source.url}")

    # Check 3: Data was actually acquired (not generated)
    if data.get("_fabricated", False):
        raise FabricationDetected("Data marked as fabricated")

    return DataSubmission(data=data, sources=self.sources, ...)
```

### **Validation Checks** (Validation Agents)
```python
def validate_authenticity(self, submission: DataSubmission) -> ValidationResult:
    """Ensure data is real, not fabricated"""

    issues = []

    # Check 1: Sources are accessible
    for source in submission.sources:
        if not self.verify_url_accessible(source.url):
            issues.append(f"Source inaccessible: {source.url}")

    # Check 2: Data matches source
    for data_point in submission.data:
        if not self.verify_data_in_source(data_point, submission.sources):
            issues.append(f"Data point not found in sources: {data_point}")

    # Check 3: No statistical anomalies (too perfect = suspicious)
    if self.detect_synthetic_patterns(submission.data):
        issues.append("Data shows synthetic patterns (possible fabrication)")

    return ValidationResult(
        passed=len(issues) == 0,
        issues=issues,
        score=1.0 - (len(issues) * 0.2)
    )
```

### **Orchestrator Enforcement**
```python
def accept_data(self, submission: DataSubmission, validations: List[ValidationResult]):
    """Final check before accepting data"""

    # Requirement 1: All validations passed
    if not all(v.passed for v in validations):
        return self.reject(submission, "Failed validation")

    # Requirement 2: Source audit complete
    if not submission.sources:
        return self.reject(submission, "No sources provided")

    # Requirement 3: No fabrication markers
    if any(marker in str(submission.data) for marker in ["placeholder", "example", "TODO", "TBD"]):
        return self.reject(submission, "Fabrication markers detected")

    # Requirement 4: Quality threshold
    if submission.quality_self_assessment < 0.8:
        return self.refine(submission, "Quality below threshold")

    # ACCEPT
    self.accepted_data[submission.data_type] = submission
    self.audit_trail.append(submission.sources)
```

---

## 📈 SUCCESS METRICS

| Metric | Target | Enforcement |
|--------|--------|-------------|
| **Data Completeness** | ≥95% | Orchestrator blocks report generation until met |
| **Average Quality Score** | ≥0.90 | Orchestrator rejects low-quality submissions |
| **Source Traceability** | 100% | Validation agent fails any unsourced data |
| **Relevance Score** | ≥0.85 | Orchestrator rejects irrelevant data |
| **Fabrication Rate** | 0% | System-wide enforcement, multiple checks |
| **Validation Pass Rate** | ≥90% | Indicates agent quality, triggers training if low |

---

## 🚀 NEXT STEPS

1. ✅ Architecture designed
2. ⏳ Implement base Agent classes
3. ⏳ Implement OrchestratorAgent
4. ⏳ Implement collection agents (Market, Brand, Pricing, Resource)
5. ⏳ Implement validation agents (Quality, Relevance, Source, Gap)
6. ⏳ Implement agent communication protocol
7. ⏳ Test end-to-end workflow
8. ⏳ Generate first 100% real-data report

**Ready to implement the agentic system.**
