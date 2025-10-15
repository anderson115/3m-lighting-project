# ✅ API Key Activation Checklist

**Module**: Patent Intelligence
**Status**: Awaiting PatentsView API Key
**Est. Time**: 10 minutes (+ 1-2 days wait)
**Generated**: 2025-10-13

---

## 📋 **QUICK START - API KEY ACTIVATION**

Follow this checklist to activate the Patent Intelligence module once the API key arrives.

---

## 🎯 **STEP 1: Register for PatentsView API Key**

### **Registration URL**
```
https://search.patentsview.org/
```

### **Required Information**
```
First Name: [Your First Name]
Last Name: [Your Last Name]
Email: [your_email@domain.com]
Organization: 3M Lighting Research
Use Case: Competitive intelligence and technology trend analysis for lighting industry patents
Expected Usage: ~100 requests per week for patent monitoring and competitor tracking
```

### **Submission**
- [ ] Visit https://search.patentsview.org/
- [ ] Find "API Access" or "Get API Key" link (usually in navigation or footer)
- [ ] Fill out registration form with above information
- [ ] Submit request
- [ ] Check email for confirmation
- [ ] **Wait 1-2 business days for approval**

### **API Key Receipt**
- [ ] Receive API key email
- [ ] Key format will be: `PVAPI-xxxxxxxxxxxxxxxxxxxxx`
- [ ] Save key securely (password manager recommended)

**⏰ Expected Wait Time**: 1-2 business days

---

## 🔧 **STEP 2: Configure Module**

### **2.1 Navigate to Module Directory**
```bash
cd /Users/anderson115/00-interlink/12-work/3m-lighting-project/modules/patent-intelligence
```

- [ ] Confirm you're in the patent-intelligence directory
- [ ] Verify with: `pwd`

### **2.2 Create .env File**
```bash
# Copy template
cp config/.env.example config/.env
```

- [ ] `.env` file created in `config/` directory
- [ ] Verify with: `ls -la config/.env`

### **2.3 Add API Key**
```bash
# Option 1: Edit with nano
nano config/.env

# Option 2: Edit with VS Code
code config/.env

# Option 3: Edit with vim
vim config/.env
```

**Add this line**:
```bash
PATENTSVIEW_API_KEY=PVAPI-your-actual-key-here
```

- [ ] API key added to `.env` file
- [ ] No spaces around `=` sign
- [ ] No quotes around key
- [ ] Key starts with `PVAPI-`

### **2.4 Save and Verify**
```bash
# Verify key is set
cat config/.env | grep PATENTSVIEW

# Should output:
# PATENTSVIEW_API_KEY=PVAPI-xxxxxxxxxxxxxxxxxxxxx
```

- [ ] File saved successfully
- [ ] API key visible in output
- [ ] No syntax errors

---

## ✅ **STEP 3: Run Checkpoint 1 Test**

### **3.1 Activate Virtual Environment**
```bash
cd /Users/anderson115/00-interlink/12-work/3m-lighting-project
source venv/bin/activate
```

- [ ] Virtual environment activated
- [ ] Prompt shows `(venv)` prefix

### **3.2 Run Test Script**
```bash
cd modules/patent-intelligence
python test_checkpoint1_data_collection.py
```

- [ ] Test script started
- [ ] No import errors
- [ ] API connection initiated

### **3.3 Monitor Test Output**
```
Expected output:
======================================================================
🔬 CHECKPOINT 1: Data Collection Test
======================================================================

📊 Step 1: Searching for 10 LED lighting patents...
✅ API returned 10 patents (total: 1,247)

📊 Step 2: Validating data quality...
   Overall Quality Score: 87.5%
   ✅ Data quality acceptable

📊 Step 3: Storing patents in database...
   ✅ Stored 10 new patents

📊 Step 4: Verifying data persistence...
   Total patents: 10
   Complete data: 9 (90.0%)

🎯 CHECKPOINT 1 COMPLETE
✅ All checkpoints passed! Ready for Checkpoint 2 (LLM Analysis)
```

- [ ] API returned 10+ patents
- [ ] Data quality > 70%
- [ ] All patents stored in database
- [ ] No errors or exceptions

**⏱️ Expected Runtime**: ~2 minutes

---

## 📊 **STEP 4: Verify Success**

### **4.1 Check Database**
```bash
python -c "from core.database import PatentDatabase; db = PatentDatabase(); print(db.get_stats())"
```

**Expected output**:
```python
{
  'total_patents': 10,
  'complete_data': 9,
  'completeness_pct': 90.0,
  'with_abstract': 10,
  'with_claims': 0,
  'with_assignees': 10,
  'data_sources': ['patentsview'],
  'date_range': {'earliest': '2024-01-15', 'latest': '2024-10-03'}
}
```

- [ ] `total_patents` = 10
- [ ] `completeness_pct` > 70%
- [ ] `with_abstract` = 10
- [ ] `with_assignees` = 10

### **4.2 Check Sample Patent**
```bash
python -c "
from core.database import PatentDatabase
import sqlite3

db = PatentDatabase()
cursor = db.conn.cursor()
cursor.execute('SELECT id, title, abstract FROM patents LIMIT 1')
patent = cursor.fetchone()

if patent:
    print(f'Patent ID: {patent[0]}')
    print(f'Title: {patent[1]}')
    print(f'Abstract: {patent[2][:200]}...')
else:
    print('❌ No patents found')
"
```

- [ ] Sample patent displayed
- [ ] Has patent ID (US-xxxxxxxx)
- [ ] Has title
- [ ] Has abstract

### **4.3 Check Database File**
```bash
ls -lh data/database/patents.db
```

- [ ] `patents.db` file exists
- [ ] File size > 0 bytes (should be ~50KB)

---

## 🎉 **SUCCESS CRITERIA**

All items below must be checked:

- [ ] PatentsView API key received
- [ ] API key added to `config/.env`
- [ ] `.env` file is gitignored (security check)
- [ ] Checkpoint 1 test executed successfully
- [ ] 10 patents stored in database
- [ ] Data quality > 70%
- [ ] Database persistence verified
- [ ] Sample patent retrieved successfully

**If all checked** ✅ → Module is ready for Phase 2 (LLM Analysis)

---

## 🐛 **TROUBLESHOOTING**

### **Error: 401 Unauthorized**
**Problem**: API key not found or invalid

**Solution**:
```bash
# Check .env file exists
ls -la config/.env

# Verify key is set
cat config/.env | grep PATENTSVIEW

# Common issues:
# - Typo in key
# - Spaces around = sign
# - Quotes around key
# - Wrong file location
```

### **Error: 410 Gone**
**Problem**: Old API endpoint

**Solution**: Already fixed in code - if you see this, verify you're using the latest version of `scrapers/patentsview_client.py`

### **Error: 429 Too Many Requests**
**Problem**: Rate limit exceeded

**Solution**: Built-in rate limiting should prevent this. If it occurs:
```python
# Edit scrapers/patentsview_client.py
# Change RATE_LIMIT_DELAY from 1.5 to 2.0
RATE_LIMIT_DELAY = 2.0
```

### **Error: No Data Returned**
**Problem**: Search query too restrictive

**Solution**:
```python
# Edit test script to use broader date range
# Change start_date from "2024-01-01" to "2023-01-01"
result = client.search_patents(
    keyword="LED lighting control",
    start_date="2023-01-01",  # Broader date range
    max_results=10
)
```

### **Error: ModuleNotFoundError**
**Problem**: Virtual environment not activated

**Solution**:
```bash
cd /Users/anderson115/00-interlink/12-work/3m-lighting-project
source venv/bin/activate
```

### **Error: Database Locked**
**Problem**: Multiple processes accessing database

**Solution**:
```bash
# Close all Python processes
pkill -f "python.*patent"

# Remove lock file if exists
rm -f data/database/patents.db-journal
```

---

## 🔒 **SECURITY CHECKLIST**

- [ ] `.env` file is in `.gitignore`
- [ ] API key not committed to git
- [ ] No API key in code comments or print statements
- [ ] `.env` file has restricted permissions: `chmod 600 config/.env`

**Verify gitignore**:
```bash
git status

# Should NOT show:
# config/.env

# Should show:
# config/.env.example
```

---

## 📞 **SUPPORT RESOURCES**

### **PatentsView Support**
- **URL**: https://search.patentsview.org/
- **Docs**: https://search.patentsview.org/docs/
- **Response Time**: 1-2 business days

### **Module Documentation**
- **README**: `README.md`
- **Status Report**: `MODULE_STATUS_REPORT.md`
- **API Guide**: `docs/API-REGISTRATION-GUIDE.md`
- **PRD**: `docs/PRD-patent-intelligence.md`

---

## ⏭️ **NEXT STEPS AFTER ACTIVATION**

Once Checkpoint 1 passes, proceed to:

### **Phase 2: LLM Analysis** (Not Yet Implemented)
- [ ] Implement `analyzers/innovation_extractor.py`
- [ ] Create Checkpoint 2 test script
- [ ] Run Checkpoint 2 with 10 patents
- [ ] Verify LLM analysis quality
- [ ] Track costs (~$0.06 for 10 patents)

### **Phase 3: Report Generation** (Not Yet Implemented)
- [ ] Implement `reporters/html_reporter.py`
- [ ] Implement `reporters/excel_reporter.py`
- [ ] Generate first weekly digest
- [ ] Test quarterly report

### **Phase 4: Production** (Not Yet Implemented)
- [ ] Implement `core/orchestrator.py`
- [ ] Add competitor tracking
- [ ] Set up weekly scheduling
- [ ] Deploy to production

---

## 📋 **QUICK COMMAND REFERENCE**

```bash
# Complete setup in one go
cd /Users/anderson115/00-interlink/12-work/3m-lighting-project/modules/patent-intelligence
cp config/.env.example config/.env
nano config/.env  # Add API key
cd /Users/anderson115/00-interlink/12-work/3m-lighting-project
source venv/bin/activate
cd modules/patent-intelligence
python test_checkpoint1_data_collection.py
```

---

**Checklist Version**: 1.0
**Last Updated**: 2025-10-13
**Est. Completion Time**: 10 minutes (after API key arrival)
**Blocking Factor**: PatentsView API key (1-2 days)
