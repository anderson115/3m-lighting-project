# Category Intelligence - Data Storage Architecture

**Philosophy:** Simple, robust, and audit-ready

---

## 📁 **Storage Structure**

```
data/storage/
├── {category_name}/              # One folder per category analyzed
│   ├── sources/                  # Raw source content (HTML, JSON, etc.)
│   │   ├── 20251015_143022_a3f2e1d.html
│   │   ├── 20251015_143022_a3f2e1d.html.meta.json
│   │   ├── 20251015_143045_7b9c4f.json
│   │   └── 20251015_143045_7b9c4f.json.meta.json
│   │
│   ├── structured/               # Processed, structured data (JSON)
│   │   ├── brands_20251015_143100.json
│   │   ├── taxonomy_20251015_143130.json
│   │   ├── pricing_20251015_143200.json
│   │   ├── market_share_20251015_143230.json
│   │   └── market_size_20251015_143300.json
│   │
│   └── audit/                    # Audit logs and validation records
│       ├── audit_20251015_143000.json
│       └── audit_20251015_150000.json
│
└── smart_home_lighting/          # Example: actual category folder
    ├── sources/
    ├── structured/
    └── audit/
```

---

## 🎯 **Design Principles**

### **1. One File Per Data Point**
- No complex databases
- Easy to inspect manually
- Git-friendly
- No corruption risk

### **2. Clear Naming Conventions**
```
Format: {type}_{identifier}_{timestamp}.{ext}
Example: brands_20251015_143100.json
        pricing_amazon_20251015_143200.json
```

### **3. Timestamped Everything**
- Every file has YYYYMMDD_HHMMSS timestamp
- Easy to track data freshness
- Simple chronological sorting

### **4. Metadata Included**
- Every source file has `.meta.json` companion
- Contains: URL, save date, size, hash
- Enables auditability

---

## 💾 **File Formats**

### **Raw Sources** (`sources/`)
Exactly as downloaded from the web:
- `*.html` - Web pages
- `*.json` - API responses
- `*.txt` - Text content
- `*.pdf` - PDF documents (future)

**Companion metadata:**
```json
{
  "url": "https://example.com/page",
  "saved_at": "20251015_143022",
  "size_bytes": 45123,
  "hash": "a3f2e1d"
}
```

### **Structured Data** (`structured/`)
Processed intelligence in JSON format:

**brands.json:**
```json
{
  "_metadata": {
    "saved_at": "20251015_143100",
    "data_type": "brands",
    "identifier": null
  },
  "data": {
    "brands": [
      {
        "name": "Philips Hue",
        "url": "https://...",
        "sources": ["source_id_1", "source_id_2"]
      }
    ],
    "count": 15
  }
}
```

**pricing.json:**
```json
{
  "_metadata": {
    "saved_at": "20251015_143200",
    "data_type": "pricing"
  },
  "data": {
    "prices": [
      {
        "product": "LED Bulb A19",
        "price_usd": 12.99,
        "retailer": "Amazon",
        "url": "https://...",
        "collected_at": "2025-10-15"
      }
    ],
    "count": 73
  }
}
```

### **Audit Logs** (`audit/`)
Complete traceability:
```json
{
  "timestamp": "20251015_143000",
  "action": "brand_discovery",
  "sources_collected": 12,
  "urls_verified": 12,
  "failed_urls": 0,
  "data_saved": "brands_20251015_143100.json"
}
```

---

## 🔧 **Usage**

### **Python API**

```python
from modules.category_intelligence.utils.data_storage import DataStorage
from modules.category_intelligence.core.config import config

# Initialize storage for category
category_dir = config.get_category_storage_dir("Smart Home Lighting")
storage = DataStorage(category_dir)

# Save raw source
source_path = storage.save_source(
    content=html_content,
    url="https://example.com",
    content_type="html"
)

# Save structured data
brands_path = storage.save_brands([
    {'name': 'Philips Hue', 'url': '...'},
    {'name': 'LIFX', 'url': '...'}
])

# Save pricing data
pricing_path = storage.save_pricing([
    {'product': 'LED Bulb', 'price': 12.99, 'retailer': 'Amazon'}
])

# Save audit log
audit_path = storage.save_audit_log({
    'action': 'brand_discovery',
    'sources_collected': 12
})

# Load data back
latest_brands = storage.get_latest_file('brands')
if latest_brands:
    data = storage.load_structured_data(latest_brands)
    brands = data['data']['brands']

# Get storage stats
stats = storage.get_storage_stats()
# {'sources_count': 47, 'structured_count': 5, 'size_mb': 2.34}
```

---

## 📊 **Benefits of This Approach**

### **✅ Simple**
- No database setup
- No migration scripts
- No schema versioning
- Just files and folders

### **✅ Robust**
- No corruption risk
- No lock files
- No connection issues
- Works offline

### **✅ Transparent**
- Open any file in text editor
- Inspect with `jq` or Python
- Git-friendly diffs
- Easy debugging

### **✅ Scalable**
- Filesystem handles 100K+ files easily
- Natural partitioning by category
- Easy to archive old data
- No query performance issues

### **✅ Audit-Ready**
- Every source preserved
- Timestamps on everything
- Metadata traces data lineage
- Client can verify any claim

---

## 🔍 **Analyzing Stored Data**

### **Command Line**

```bash
# List all categories
ls data/storage/

# View latest brands data
cat data/storage/smart_home_lighting/structured/brands_*.json | jq '.data.brands'

# Count total sources
find data/storage/smart_home_lighting/sources -type f | wc -l

# Check storage size
du -sh data/storage/smart_home_lighting/

# Find all pricing data
find data/storage/*/structured -name "pricing_*.json"
```

### **Python Analysis**

```python
import json
from pathlib import Path

# Load all brands across categories
storage_dir = Path("data/storage")
all_brands = []

for category_dir in storage_dir.iterdir():
    brands_files = (category_dir / "structured").glob("brands_*.json")
    for brands_file in brands_files:
        data = json.loads(brands_file.read_text())
        all_brands.extend(data['data']['brands'])

print(f"Total brands discovered: {len(all_brands)}")
```

---

## 🧹 **Maintenance**

### **Archive Old Data**
```bash
# Archive category after 6 months
tar -czf smart_home_lighting_archive_20251015.tar.gz \
  data/storage/smart_home_lighting/

# Move to archive location
mv smart_home_lighting_archive_20251015.tar.gz /archive/

# Remove original (optional)
rm -rf data/storage/smart_home_lighting/
```

### **Cleanup Test Data**
```bash
# Remove test runs (identified by pattern)
rm -rf data/storage/test_*
```

### **Verify Data Integrity**
```python
from modules.category_intelligence.utils.data_storage import DataStorage

storage = DataStorage(Path("data/storage/smart_home_lighting"))

# Check for orphaned files
sources = storage.list_sources()
structured = storage.list_structured_files()

print(f"Sources: {len(sources)}")
print(f"Structured files: {len(structured)}")
```

---

## ⚠️ **Important Notes**

### **Do NOT**
- ❌ Edit files manually (creates inconsistency)
- ❌ Move files between categories (breaks references)
- ❌ Delete `.meta.json` files (loses traceability)
- ❌ Commit large binary files to git

### **DO**
- ✅ Use `DataStorage` API for all writes
- ✅ Keep category names consistent
- ✅ Archive old data regularly
- ✅ Add `.gitignore` for `data/storage/*` if repo-based

---

## 📝 **Example Workflow**

```python
# 1. Initialize for new category
from modules.category_intelligence.core.orchestrator import CategoryIntelligenceOrchestrator

orchestrator = CategoryIntelligenceOrchestrator()
results = orchestrator.analyze_category("Smart Home Lighting")

# Behind the scenes, this creates:
# data/storage/smart_home_lighting/
#   ├── sources/        (47 HTML files + metadata)
#   ├── structured/     (5 JSON files: brands, taxonomy, pricing, etc.)
#   └── audit/          (8 audit logs)

# 2. Analyze the data
from pathlib import Path
category_dir = Path("data/storage/smart_home_lighting")

# Count sources
sources = list((category_dir / "sources").glob("*.html"))
print(f"Collected {len(sources)} web sources")

# Load brands
brands_file = sorted((category_dir / "structured").glob("brands_*.json"))[-1]
brands_data = json.loads(brands_file.read_text())
print(f"Discovered {brands_data['data']['count']} brands")

# 3. Generate report (uses stored data)
# HTML report generated in outputs/ with references to data/storage/
```

---

## 🎓 **Best Practices**

1. **One category = One folder**: Never mix data from multiple categories
2. **Never delete sources**: Disk is cheap, audit trails are valuable
3. **Use timestamps**: Natural versioning without complexity
4. **Keep it flat**: Don't nest too deeply (max 2 levels)
5. **Document everything**: Metadata files are your friends

---

**Last Updated:** 2025-10-15
**Version:** 1.0.0
