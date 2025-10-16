# Integration Guide - Stage 3: Real Data Sources

**Status**: System refactored and ready for integration
**Created**: 2025-10-16
**Priority**: P0 - System non-functional until Stage 3 complete

---

## 🎯 **GOAL**

Transform the Category Intelligence system from **non-functional but well-architected** to **fully operational with real data sources**.

## 📊 **CURRENT STATE**

| Component | Status | Details |
|-----------|--------|---------|
| **Architecture** | ✅ Complete | Clean, type-safe, Oct 2025 compliant |
| **Code Quality** | ✅ Complete | 100% type hints, small functions, dataclasses |
| **Zero Fabrication** | ✅ Enforced | Preflight validation active |
| **Functionality** | ❌ **BROKEN** | All collectors raise NotImplementedError |
| **Data Sources** | ❌ **NONE** | Zero integrations complete |

**Bottom Line**: Clean architecture with zero capabilities.

---

## 🚀 **INTEGRATION ROADMAP**

### **Phase 1: Minimum Viable System** (8-12 hours)
**Goal**: Get ONE category working with real data

**Steps**:
1. Integrate Claude WebSearch (available in Claude Code)
2. Implement WebSearch in ONE collector (brand_discovery.py)
3. Test with "garage storage" category
4. Verify preflight validation passes (100 sources)

**Result**: Proof of concept with real data.

---

### **Phase 2: Full Collector Coverage** (20-30 hours)
**Goal**: All collectors functional

**Steps**:
1. Implement WebSearch in all 5 collectors
2. Add pytrends for keyword data (no API key)
3. Add basic web scraping for pricing (if ToS allows)
4. Test all collectors with multiple categories

**Result**: Fully functional system using available sources.

---

### **Phase 3: Premium Data Sources** (40+ hours)
**Goal**: Professional-grade data quality

**Steps**:
1. Integrate retailer APIs (Amazon, Walmart)
2. Add IBISWorld (requires subscription)
3. Implement SEC EDGAR parsing
4. Add FRED economic data

**Result**: Production-ready system with authoritative sources.

---

## 🔧 **INTEGRATION DETAILS**

### **1. Claude WebSearch** (HIGHEST PRIORITY)

**Status**: ✅ Available in Claude Code environment
**Cost**: Included in Claude API
**Priority**: **REQUIRED** - Start here

#### **How to Integrate**:

WebSearch is already available as a tool in Claude Code. To use it in collectors:

**Step 1: Update Collector Method**

```python
# In collectors/brand_discovery.py
def _discover_from_websearch(self, category: str) -> List[Brand]:
    """Discover brands using WebSearch (Claude API)."""

    # Call Claude WebSearch tool
    # This is done through the Claude Code environment
    # The collector would call a WebSearch service

    # For now, raise NotImplementedError with instructions
    raise NotImplementedError(
        "WebSearch integration requires implementing a WebSearch service layer. "
        "See INTEGRATION_GUIDE.md for details."
    )
```

**Step 2: Create WebSearch Service Layer**

Create `services/websearch_service.py`:

```python
"""WebSearch Service - Interface to Claude WebSearch API"""

from typing import List, Dict, Any

class WebSearchService:
    """Wrapper for Claude WebSearch functionality."""

    def search(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Search the web using Claude WebSearch.

        Args:
            query: Search query
            max_results: Maximum number of results

        Returns:
            List of search results with titles, URLs, snippets
        """
        # Implementation depends on how Claude WebSearch is accessed
        # May require subprocess call or API integration
        raise NotImplementedError(
```