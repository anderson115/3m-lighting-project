# Expert Authority Module - Technical Architecture v2.0

**Purpose:** Production-grade expert discussion analysis system
**Design Principles:** Stable, Scalable, Modular, Maintainable, Claude-Buildable

---

## 🎯 **DESIGN PHILOSOPHY**

### **Core Principles**
1. **Modular Components** - Each stage is independent, swappable, testable
2. **Graceful Degradation** - Works even when APIs fail (cached fallbacks)
3. **Incremental Scalability** - Start small (5 discussions), scale to thousands
4. **Zero External Training** - No ML models to train, just API calls
5. **Observable Pipeline** - Every stage logs progress, errors, metrics
6. **Deterministic Fallbacks** - Rule-based backup for every LLM operation

---

## 🏗️ **SYSTEM ARCHITECTURE**

### **3-Layer Architecture**

```
┌─────────────────────────────────────────────────────┐
│                  ORCHESTRATOR LAYER                 │
│  - Pipeline coordinator                             │
│  - Error handling & retry logic                     │
│  - Progress tracking & logging                      │
└─────────────────────────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
┌───────────────┐  ┌──────────────┐  ┌──────────────┐
│  DATA LAYER   │  │ ANALYSIS     │  │ OUTPUT       │
│               │  │ LAYER        │  │ LAYER        │
│ - Scrapers    │  │ - Theme      │  │ - Report     │
│ - Validators  │  │   Extractor  │  │   Generator  │
│ - Cache       │  │ - Consensus  │  │ - Exporter   │
│               │  │   Detector   │  │ - Validator  │
└───────────────┘  └──────────────┘  └──────────────┘
```

---

## 📦 **MODULE STRUCTURE**

```
modules/expert-authority/
├── core/                          # Core engine (stable)
│   ├── __init__.py
│   ├── orchestrator.py           # Pipeline coordinator
│   ├── config.py                 # Configuration manager
│   └── logger.py                 # Structured logging
│
├── scrapers/                      # Data collection (swappable)
│   ├── __init__.py
│   ├── base_scraper.py           # Abstract base class
│   ├── reddit_scraper.py         # PRAW-based Reddit
│   ├── demo_scraper.py           # Synthetic data (demo mode)
│   └── cache_manager.py          # Response caching
│
├── analyzers/                     # Analysis engines (swappable)
│   ├── __init__.py
│   ├── base_analyzer.py          # Abstract base class
│   ├── rule_based.py             # Tier 1: Pattern matching
│   ├── llm_semantic.py           # Tier 2: Claude Sonnet
│   ├── llm_extended.py           # Tier 3: Opus + GPT-4o
│   └── consensus_detector.py     # Shared logic
│
├── validators/                    # Citation validation
│   ├── __init__.py
│   ├── citation_validator.py     # URL + quote verification
│   ├── integrity_checker.py      # Hash validation
│   └── audit_trail.py            # Proof generation
│
├── reporters/                     # Output generation (swappable)
│   ├── __init__.py
│   ├── base_reporter.py          # Abstract base class
│   ├── html_reporter.py          # HTML report
│   ├── excel_exporter.py         # Excel tables (Tier 2+)
│   └── pptx_generator.py         # PowerPoint (Tier 3)
│
├── utils/                         # Shared utilities
│   ├── __init__.py
│   ├── text_processing.py        # Normalization, cleaning
│   ├── url_utils.py              # URL validation
│   └── metrics.py                # Performance tracking
│
├── config/                        # Configuration files
│   ├── settings.yaml             # Global settings
│   ├── tier_configs.yaml         # Tier-specific configs
│   └── patterns.yaml             # Theme patterns (rule-based)
│
├── data/                          # Data storage
│   ├── raw/                      # Scraped discussions
│   ├── processed/                # Analysis results
│   ├── deliverables/             # Client reports
│   └── cache/                    # Response cache
│
├── tests/                         # Unit & integration tests
│   ├── test_scrapers.py
│   ├── test_analyzers.py
│   ├── test_validators.py
│   └── test_e2e.py
│
└── scripts/                       # Entry points
    ├── run_tier1.py              # Tier 1 pipeline
    ├── run_tier2.py              # Tier 2 pipeline
    └── run_tier3.py              # Tier 3 pipeline
```

---

## 🔌 **MODULAR INTERFACES**

### **1. Base Scraper Interface**
```python
# scrapers/base_scraper.py
from abc import ABC, abstractmethod
from typing import List, Dict

class BaseScraper(ABC):
    """Abstract scraper - any platform can implement"""

    @abstractmethod
    def scrape(self, query: str, limit: int) -> List[Dict]:
        """Scrape discussions matching query"""
        pass

    @abstractmethod
    def validate_response(self, response: Dict) -> bool:
        """Validate scraped data structure"""
        pass

    def add_validation_metadata(self, discussion: Dict) -> Dict:
        """Add citation validation metadata (shared logic)"""
        discussion['validation_hash'] = self._compute_hash(discussion)
        discussion['scraped_at'] = datetime.now().isoformat()
        return discussion
```

**Implementations:**
- `RedditScraper(BaseScraper)` - PRAW API
- `DemoScraper(BaseScraper)` - Synthetic data
- `QuoraScraper(BaseScraper)` - Selenium-based (Tier 2)
- `StackExchangeScraper(BaseScraper)` - REST API (Tier 2)

### **2. Base Analyzer Interface**
```python
# analyzers/base_analyzer.py
from abc import ABC, abstractmethod

class BaseAnalyzer(ABC):
    """Abstract analyzer - rule-based or LLM-based"""

    @abstractmethod
    def extract_themes(self, discussions: List[Dict]) -> List[Dict]:
        """Extract themes from discussions"""
        pass

    @abstractmethod
    def detect_consensus(self, discussions: List[Dict]) -> List[Dict]:
        """Find consensus patterns"""
        pass

    def validate_output(self, themes: List[Dict], discussions: List[Dict]) -> bool:
        """Verify themes exist in source data (anti-hallucination)"""
        for theme in themes:
            if not self._verify_evidence(theme, discussions):
                raise HallucinationError(f"Theme {theme['theme']} has no evidence")
        return True
```

**Implementations:**
- `RuleBasedAnalyzer(BaseAnalyzer)` - Tier 1: Keyword patterns
- `LLMSemanticAnalyzer(BaseAnalyzer)` - Tier 2: Claude Sonnet
- `LLMExtendedAnalyzer(BaseAnalyzer)` - Tier 3: Opus + GPT-4o

### **3. Base Reporter Interface**
```python
# reporters/base_reporter.py
from abc import ABC, abstractmethod

class BaseReporter(ABC):
    """Abstract reporter - any output format"""

    @abstractmethod
    def generate(self, analysis: Dict, tier: int) -> str:
        """Generate report, return file path"""
        pass

    def validate_citations(self, analysis: Dict) -> bool:
        """Verify all citations before report generation"""
        validator = CitationValidator()
        return validator.validate_all(analysis)
```

**Implementations:**
- `HTMLReporter(BaseReporter)` - All tiers
- `ExcelExporter(BaseReporter)` - Tier 2+
- `PowerPointGenerator(BaseReporter)` - Tier 3

---

## ⚙️ **ORCHESTRATOR PATTERN**

### **Pipeline Coordinator**
```python
# core/orchestrator.py
class ExpertAuthorityOrchestrator:
    """
    Coordinates entire pipeline with error handling
    """

    def __init__(self, tier: int, config: Dict):
        self.tier = tier
        self.config = config
        self.logger = StructuredLogger("orchestrator")

        # Load tier-specific components
        self.scraper = self._load_scraper()
        self.analyzer = self._load_analyzer()
        self.reporter = self._load_reporter()
        self.validator = CitationValidator()

    def run_pipeline(self, query: str) -> Dict:
        """
        Execute full pipeline with graceful degradation
        """
        try:
            # Stage 1: Data collection
            discussions = self._run_scraping(query)

            # Stage 2: Analysis
            analysis = self._run_analysis(discussions)

            # Stage 3: Validation
            self._run_validation(analysis)

            # Stage 4: Report generation
            report_path = self._run_reporting(analysis)

            return {
                'status': 'success',
                'report_path': report_path,
                'metrics': self._get_metrics()
            }

        except Exception as e:
            return self._handle_failure(e)

    def _run_scraping(self, query: str) -> List[Dict]:
        """Scrape with fallback to cache"""
        try:
            discussions = self.scraper.scrape(query, self.config['discussion_limit'])
            self._cache_discussions(discussions)
            return discussions
        except APIError as e:
            self.logger.warning(f"API failed, using cache: {e}")
            return self._load_cached_discussions(query)

    def _run_analysis(self, discussions: List[Dict]) -> Dict:
        """Analyze with fallback to rule-based"""
        try:
            themes = self.analyzer.extract_themes(discussions)
            consensus = self.analyzer.detect_consensus(discussions)

            # Validate output (anti-hallucination)
            self.analyzer.validate_output(themes, discussions)

            return {
                'themes': themes,
                'consensus': consensus,
                'discussions': discussions
            }
        except LLMError as e:
            self.logger.warning(f"LLM failed, using rule-based fallback: {e}")
            fallback_analyzer = RuleBasedAnalyzer()
            return {
                'themes': fallback_analyzer.extract_themes(discussions),
                'consensus': fallback_analyzer.detect_consensus(discussions),
                'discussions': discussions
            }

    def _run_validation(self, analysis: Dict) -> None:
        """Validate citations (fail fast if <95%)"""
        validation_rate = self.validator.validate_all(analysis)
        if validation_rate < 0.95:
            raise ValidationError(f"Only {validation_rate*100}% citations verified")

    def _load_scraper(self) -> BaseScraper:
        """Load tier-appropriate scraper"""
        if self.tier == 1:
            return RedditScraper(self.config['reddit'])
        elif self.tier == 2:
            return MultiPlatformScraper([
                RedditScraper(self.config['reddit']),
                QuoraScraper(self.config['quora']),
                StackExchangeScraper(self.config['stackexchange'])
            ])
        else:  # Tier 3
            return MultiPlatformScraper([...])  # All platforms
```

---

## 📊 **CONFIGURATION MANAGEMENT**

### **Tier-Specific Configs**
```yaml
# config/tier_configs.yaml
tier1:
  name: "Essential"
  price: 299
  platforms:
    - reddit
  discussion_limit: 100
  analyzer: "rule_based"
  output_formats:
    - html
  features:
    - themes
    - consensus

tier2:
  name: "Professional"
  price: 799
  platforms:
    - reddit
    - quora
    - stackexchange
  discussion_limit: 300
  analyzer: "llm_semantic"
  llm_model: "claude-sonnet-4-20250514"
  output_formats:
    - html
    - excel
  features:
    - themes
    - consensus
    - controversies
    - safety_warnings

tier3:
  name: "Enterprise"
  price: 1999
  platforms:
    - reddit
    - quora
    - stackexchange
    - electrician_talk
    - contractor_talk
  discussion_limit: 500
  analyzer: "llm_extended"
  llm_models:
    - "claude-opus-4-20250514"
    - "gpt-4o"
  output_formats:
    - html
    - excel
    - powerpoint
    - raw_data
  features:
    - themes
    - consensus
    - controversies
    - safety_warnings
    - temporal_trends
    - competitive_tracking
```

### **Pattern Definitions (Rule-Based)**
```yaml
# config/patterns.yaml
theme_patterns:
  adhesive_mounting:
    keywords:
      - adhesive
      - tape
      - stick
      - mount
      - falling
      - fell
      - hold
    category: pain_point

  dimmer_compatibility:
    keywords:
      - dimmer
      - flicker
      - compatible
      - pwm
      - triac
    category: pain_point

  # ... more patterns
```

---

## 🔄 **SCALABILITY STRATEGY**

### **Incremental Scaling**
```python
# Start small, scale gradually
class ScalableOrchestrator(ExpertAuthorityOrchestrator):
    """
    Handles scaling from 5 → 100 → 1000+ discussions
    """

    def run_pipeline(self, query: str) -> Dict:
        # Auto-detect optimal batch size
        batch_size = self._calculate_batch_size()

        if self.config['discussion_limit'] <= 100:
            # Small: Single-batch processing
            return super().run_pipeline(query)
        else:
            # Large: Batched processing with progress tracking
            return self._run_batched_pipeline(query, batch_size)

    def _run_batched_pipeline(self, query: str, batch_size: int) -> Dict:
        """Process in batches to avoid memory issues"""
        total = self.config['discussion_limit']
        batches = (total + batch_size - 1) // batch_size

        all_themes = []
        all_consensus = []

        for i in range(batches):
            self.logger.info(f"Processing batch {i+1}/{batches}")

            offset = i * batch_size
            discussions = self.scraper.scrape(query, batch_size, offset=offset)

            # Analyze batch
            batch_analysis = self._run_analysis(discussions)
            all_themes.extend(batch_analysis['themes'])
            all_consensus.extend(batch_analysis['consensus'])

        # Merge and deduplicate results
        return self._merge_results(all_themes, all_consensus)
```

---

## 🛡️ **ERROR HANDLING & RESILIENCE**

### **Graceful Degradation Chain**
```python
# utils/resilience.py
class ResilientOperation:
    """
    Retry with exponential backoff + fallback
    """

    def execute(self, primary_fn, fallback_fn, max_retries=3):
        """
        Try primary function, fall back if fails
        """
        for attempt in range(max_retries):
            try:
                return primary_fn()
            except Exception as e:
                if attempt == max_retries - 1:
                    self.logger.warning(f"Primary failed after {max_retries} attempts, using fallback")
                    return fallback_fn()
                else:
                    wait_time = 2 ** attempt
                    self.logger.info(f"Retry {attempt+1}/{max_retries} after {wait_time}s")
                    time.sleep(wait_time)

# Usage example
resilient_op = ResilientOperation()
themes = resilient_op.execute(
    primary_fn=lambda: llm_analyzer.extract_themes(discussions),
    fallback_fn=lambda: rule_based_analyzer.extract_themes(discussions)
)
```

### **Circuit Breaker for APIs**
```python
# utils/circuit_breaker.py
class CircuitBreaker:
    """
    Prevent cascading failures from API outages
    """

    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.state = 'closed'  # closed, open, half_open
        self.last_failure_time = None

    def call(self, fn):
        if self.state == 'open':
            if time.time() - self.last_failure_time > self.timeout:
                self.state = 'half_open'
            else:
                raise CircuitOpenError("API circuit is open")

        try:
            result = fn()
            if self.state == 'half_open':
                self.state = 'closed'
                self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()

            if self.failure_count >= self.failure_threshold:
                self.state = 'open'
                self.logger.error(f"Circuit opened after {self.failure_count} failures")

            raise e
```

---

## 📈 **OBSERVABILITY & MONITORING**

### **Structured Logging**
```python
# core/logger.py
import structlog

class StructuredLogger:
    """
    JSON-formatted logs for parsing/analysis
    """

    def __init__(self, component: str):
        self.log = structlog.get_logger().bind(component=component)

    def track_stage(self, stage: str, **kwargs):
        """Log pipeline stage with metrics"""
        self.log.info(
            "stage_complete",
            stage=stage,
            **kwargs
        )

# Usage
logger = StructuredLogger("scraper")
logger.track_stage("scraping",
    platform="reddit",
    discussions_found=150,
    duration_seconds=12.3
)

# Output (JSON):
{
    "event": "stage_complete",
    "component": "scraper",
    "stage": "scraping",
    "platform": "reddit",
    "discussions_found": 150,
    "duration_seconds": 12.3,
    "timestamp": "2025-10-09T18:52:00Z"
}
```

### **Performance Metrics**
```python
# utils/metrics.py
class PerformanceTracker:
    """
    Track pipeline performance metrics
    """

    def __init__(self):
        self.metrics = {}

    @contextmanager
    def track_duration(self, operation: str):
        """Time an operation"""
        start = time.time()
        yield
        duration = time.time() - start
        self.metrics[f"{operation}_duration"] = duration

    def get_report(self) -> Dict:
        return {
            'total_duration': sum(v for k, v in self.metrics.items() if 'duration' in k),
            'stages': self.metrics
        }

# Usage
tracker = PerformanceTracker()

with tracker.track_duration("scraping"):
    discussions = scraper.scrape(...)

with tracker.track_duration("analysis"):
    themes = analyzer.extract_themes(...)

print(tracker.get_report())
# {'total_duration': 45.2, 'stages': {'scraping_duration': 30.1, 'analysis_duration': 15.1}}
```

---

## ✅ **TESTING STRATEGY**

### **Unit Tests (Each Component)**
```python
# tests/test_analyzers.py
import pytest

def test_rule_based_analyzer():
    """Test rule-based theme extraction"""
    analyzer = RuleBasedAnalyzer()
    discussions = load_fixture('demo_discussions.json')

    themes = analyzer.extract_themes(discussions)

    assert len(themes) > 0
    assert all('theme' in t for t in themes)
    assert all('evidence' in t for t in themes)

def test_llm_analyzer_fallback():
    """Test LLM analyzer falls back to rules on failure"""
    analyzer = LLMSemanticAnalyzer()

    # Mock LLM failure
    with patch('anthropic.Anthropic.messages.create', side_effect=APIError):
        themes = analyzer.extract_themes(discussions)
        # Should return rule-based results
        assert themes is not None
```

### **Integration Tests (End-to-End)**
```python
# tests/test_e2e.py
def test_tier1_pipeline():
    """Test complete Tier 1 pipeline"""
    orchestrator = ExpertAuthorityOrchestrator(tier=1, config=load_config('tier1'))

    result = orchestrator.run_pipeline("LED strip installation")

    assert result['status'] == 'success'
    assert Path(result['report_path']).exists()
    assert result['metrics']['validation_rate'] >= 0.95
```

---

## 🚀 **IMPLEMENTATION ROADMAP**

### **Phase 1: Core Infrastructure (Week 1)**
- [ ] Base interfaces (BaseScraper, BaseAnalyzer, BaseReporter)
- [ ] Orchestrator with error handling
- [ ] Configuration manager
- [ ] Structured logging
- [ ] Citation validator
- [ ] Unit tests for core components

### **Phase 2: Tier 1 Production (Week 2)**
- [ ] Reddit scraper with PRAW
- [ ] Rule-based analyzer (production-ready)
- [ ] HTML reporter (enhanced from demo)
- [ ] Cache manager
- [ ] Integration tests
- [ ] Demo mode (synthetic data)

### **Phase 3: Tier 2 Features (Week 3)**
- [ ] Quora scraper (Selenium)
- [ ] Stack Exchange scraper (API)
- [ ] LLM semantic analyzer (Claude Sonnet)
- [ ] Excel exporter
- [ ] Multi-platform orchestration

### **Phase 4: Tier 3 Advanced (Week 4)**
- [ ] Professional forum scrapers
- [ ] LLM extended analyzer (Opus + GPT-4o)
- [ ] PowerPoint generator
- [ ] Temporal trend analysis
- [ ] Competitive tracking

---

## 📋 **SUCCESS CRITERIA**

**Stability:**
- [ ] 95%+ uptime (handles API failures gracefully)
- [ ] Zero data loss (all responses cached)
- [ ] Deterministic fallbacks work correctly

**Scalability:**
- [ ] Handles 5 → 100 → 1000+ discussions
- [ ] Memory usage stays under 2GB
- [ ] Processing time scales linearly

**Modularity:**
- [ ] Can swap scrapers without touching analyzers
- [ ] Can swap analyzers without touching reporters
- [ ] Each component has <200 lines of code

**Maintainability:**
- [ ] 80%+ test coverage
- [ ] All functions have type hints
- [ ] Clear error messages with actionable solutions

**Claude-Buildable:**
- [ ] No complex ML pipelines
- [ ] No external services to configure
- [ ] All dependencies pip-installable
- [ ] Complete in <2000 lines of code

---

## 🎯 **NEXT STEPS**

Ready to build this architecture! Recommend starting with:

1. **Phase 1** (Core Infrastructure) - Build foundation
2. **Validate with Tier 1** - Prove architecture works
3. **Scale to Tier 2/3** - Add features incrementally

Confirm this approach meets your requirements for stability, scalability, and maintainability?
