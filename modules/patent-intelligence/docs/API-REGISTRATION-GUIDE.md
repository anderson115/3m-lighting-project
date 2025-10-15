# Patent Intelligence - API Registration Guide

**Last Updated**: 2025-10-13
**Est. Time**: 10 minutes (+ 1-2 days wait)

---

## 🎯 **Required APIs**

### **✅ PatentsView API** (Primary - Required)
- **Status**: Requires free registration
- **Cost**: FREE unlimited
- **Wait Time**: 1-2 business days
- **Priority**: HIGH - Must complete first

### **✅ EPO OPS API** (Backup - Optional)
- **Status**: Requires free registration
- **Cost**: FREE 4GB/month
- **Wait Time**: Instant approval
- **Priority**: LOW - Can add later

---

## 📋 **Step 1: PatentsView API Registration**

### **Registration URL**
https://search.patentsview.org/

### **Steps**
1. **Visit Homepage**
   - Go to https://search.patentsview.org/
   - Look for "API Access" or "Get API Key" link
   - Usually in top navigation or footer

2. **Fill Out Form**
   ```
   First Name: [Your First Name]
   Last Name: [Your Last Name]
   Email: [your_email@domain.com]
   Organization: 3M Lighting Research
   Use Case: Competitive intelligence and technology trend analysis for lighting industry patents
   Expected Usage: ~100 requests per week for patent monitoring and competitor tracking
   ```

3. **Submit Request**
   - Click "Submit" or "Request API Key"
   - Check email for confirmation
   - **Wait**: 1-2 business days for approval

4. **Receive API Key**
   - Check email for API key
   - Key format: `PVAPI-xxxxxxxxxxxxxxxxxxxxx`
   - Save key securely

---

## 🔧 **Step 2: Configure Module**

### **Add API Key to Environment**

1. **Navigate to config directory**
   ```bash
   cd /Users/anderson115/00-interlink/12-work/3m-lighting-project/modules/patent-intelligence/config
   ```

2. **Create .env file** (if it doesn't exist)
   ```bash
   cp .env.example .env
   ```

3. **Edit .env file**
   ```bash
   # Open in your editor
   nano .env  # or: code .env
   ```

4. **Add your API key**
   ```bash
   # PatentsView API (Primary)
   PATENTSVIEW_API_KEY=PVAPI-your-actual-key-here

   # Claude AI (for LLM analysis)
   CLAUDE_API_KEY=your_anthropic_key

   # EPO OPS API (Backup - Optional)
   EPO_CONSUMER_KEY=your_epo_key_here
   EPO_CONSUMER_SECRET=your_epo_secret_here
   ```

5. **Save and close**
   - Ctrl+X, then Y, then Enter (in nano)
   - Or Command+S (in VS Code)

---

## ✅ **Step 3: Test API Connection**

### **Run Checkpoint 1**

```bash
# From patent-intelligence directory
cd /Users/anderson115/00-interlink/12-work/3m-lighting-project/modules/patent-intelligence

# Activate virtual environment
source ../../venv/bin/activate

# Run test
python test_checkpoint1_data_collection.py
```

### **Expected Output**
```
======================================================================
🔬 CHECKPOINT 1: Data Collection Test
======================================================================
✅ Database initialized

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
✅ All checkpoints passed! Ready for Checkpoint 2
```

---

## 🐛 **Troubleshooting**

### **Error: 401 Unauthorized**
**Problem**: API key not found or invalid

**Solution**:
1. Check `.env` file exists: `ls -la config/.env`
2. Verify key is set: `cat config/.env | grep PATENTSVIEW`
3. Check for typos in key
4. Verify key hasn't expired (re-register if needed)

### **Error: 410 Gone**
**Problem**: Old API endpoint (already fixed in code)

**Solution**: Already resolved - code uses new endpoint

### **Error: 429 Too Many Requests**
**Problem**: Rate limit exceeded (45/minute)

**Solution**: Built-in rate limiting should prevent this. If it occurs:
- Increase `RATE_LIMIT_DELAY` in `scrapers/patentsview_client.py`
- Change from `1.5` to `2.0` seconds

### **No Data Returned**
**Problem**: Search query too restrictive

**Solution**:
1. Check if date range is too recent
2. Try broader keywords
3. Verify patents exist for search term

---

## 📊 **Optional: EPO OPS API** (Backup)

### **Why Add This?**
- Global patent coverage (not just US)
- Failover if PatentsView is down
- Access to full-text documents
- Legal status information

### **Registration**

1. **Visit**: https://developers.epo.org/

2. **Create Account**
   - Click "Register"
   - Fill out account form
   - Confirm email

3. **Register Application**
   - Log in to Developer Portal
   - Click "My Apps"
   - Click "Register new application"
   - Fill out:
     ```
     App Name: 3M Lighting Patent Intelligence
     Description: Patent monitoring and competitive intelligence
     ```

4. **Get Credentials**
   - Consumer Key: `xxxxxxxxxx`
   - Consumer Secret: `yyyyyyyyyyyy`

5. **Add to .env**
   ```bash
   EPO_CONSUMER_KEY=your_consumer_key
   EPO_CONSUMER_SECRET=your_consumer_secret
   ```

---

## 🎉 **Success Checklist**

- [ ] PatentsView API key requested
- [ ] Email confirmation received
- [ ] API key added to `.env` file
- [ ] `.env` file is gitignored (security check)
- [ ] Checkpoint 1 test passed
- [ ] 10 patents in database
- [ ] Data quality > 70%
- [ ] (Optional) EPO OPS credentials added

---

## 📞 **Support**

### **PatentsView Support**
- **Email**: Contact through https://search.patentsview.org/
- **Docs**: https://search.patentsview.org/docs/
- **Response Time**: 1-2 business days

### **EPO OPS Support**
- **Email**: helpdesk@epo.org
- **Docs**: https://ops.epo.org/3.2/
- **Response Time**: 24 hours

---

## 🔒 **Security Notes**

1. **Never commit `.env` file to git**
   - Already in `.gitignore`
   - Double-check: `git status` should not show `.env`

2. **Rotate keys periodically**
   - PatentsView: Request new key yearly
   - EPO OPS: Can regenerate in portal

3. **Share keys securely**
   - Use password manager
   - Don't email or Slack keys
   - Use encrypted channels if needed

---

## ⏭️ **Next Steps After Registration**

1. ✅ **Run Checkpoint 1** - Validate data collection
2. ✅ **Implement Checkpoint 2** - Build LLM analysis
3. ✅ **Generate First Report** - Test end-to-end
4. ✅ **Set Up Scheduling** - Weekly automated runs
5. ✅ **Add Competitors** - Configure tracking list

---

**Registration complete? Return to**: `README.md` → Quick Start Guide → Step 2

**Questions?** Review `docs/PRD-patent-intelligence.md` for full technical details
