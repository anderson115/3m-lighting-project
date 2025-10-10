# API Credentials Setup Guide

**Time Required:** 7 minutes total

---

## 📍 **WHERE TO PUT API CREDENTIALS**

### **Step 1: Copy the Example File**

```bash
cd modules/expert-authority/config
cp .env.example .env
```

### **Step 2: Edit the .env File**

```bash
# Open in your editor
nano .env
# or
code .env
# or
vim .env
```

---

## 🔑 **HOW TO GET EACH API CREDENTIAL**

### **1. Reddit API (Required for Tier 1)**

**Time:** 5 minutes

**Steps:**
1. **Go to:** https://www.reddit.com/prefs/apps
2. **Click:** "Create App" (bottom of page)
3. **Fill in:**
   - Name: `3M Lighting Research`
   - Type: Select **"script"**
   - Description: `Research project analyzing expert lighting discussions`
   - About URL: (leave blank)
   - Redirect URI: `http://localhost:8080`
4. **Click:** "Create app"
5. **Copy credentials:**
   - `client_id`: The string under "personal use script" (14 characters)
   - `client_secret`: The string next to "secret" (27 characters)

**Paste into .env:**
```bash
REDDIT_CLIENT_ID=abc123xyz456def  # Your 14-char client_id
REDDIT_CLIENT_SECRET=abcdef1234567890abcdef123456  # Your 27-char secret
REDDIT_USER_AGENT=3M-Lighting-Research/1.0
```

---

### **2. Stack Exchange API (Optional but Recommended)**

**Time:** 2 minutes

**Steps:**
1. **Go to:** https://stackapps.com/apps/oauth/register
2. **Fill in:**
   - Application Name: `3M Lighting Research`
   - OAuth Domain: (leave blank)
   - Application Website: `https://github.com/yourusername/3m-lighting-project`
3. **Click:** "Register Your Application"
4. **Copy:** The API Key shown (32 characters)

**Paste into .env:**
```bash
STACK_EXCHANGE_API_KEY=your_32_character_key_here
```

**Benefits:**
- Without key: 300 requests/day
- With key: 10,000 requests/day

---

### **3. Anthropic API (For LLM Analysis - Tier 2+)**

**Required for:** Semantic theme discovery

**Steps:**
1. **Go to:** https://console.anthropic.com/settings/keys
2. **Click:** "Create Key"
3. **Copy:** The API key (starts with `sk-ant-`)

**Paste into .env:**
```bash
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxx
```

---

### **4. OpenAI API (For Tier 3 Extended Reasoning)**

**Required for:** Tier 3 cross-validation with GPT-4o

**Steps:**
1. **Go to:** https://platform.openai.com/api-keys
2. **Click:** "Create new secret key"
3. **Copy:** The API key (starts with `sk-`)

**Paste into .env:**
```bash
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## ✅ **VERIFICATION**

### **Test Reddit Credentials:**

```bash
cd modules/expert-authority
python -c "
import os
from dotenv import load_dotenv
import praw

load_dotenv('config/.env')

reddit = praw.Reddit(
    client_id=os.getenv('REDDIT_CLIENT_ID'),
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
    user_agent=os.getenv('REDDIT_USER_AGENT')
)

print(f'✅ Reddit API connected: {reddit.read_only}')
print(f'✅ Testing search...')

posts = list(reddit.subreddit('electricians').search('LED', limit=3))
print(f'✅ Found {len(posts)} posts')
print(f'✅ First post: {posts[0].title}')
"
```

**Expected Output:**
```
✅ Reddit API connected: True
✅ Testing search...
✅ Found 3 posts
✅ First post: [Some actual Reddit post title about LEDs]
```

---

### **Test Stack Exchange Credentials:**

```bash
python -c "
import os
import requests
from dotenv import load_dotenv

load_dotenv('config/.env')

url = 'https://api.stackexchange.com/2.3/search'
params = {
    'intitle': 'LED',
    'site': 'diy.stackexchange.com',
    'key': os.getenv('STACK_EXCHANGE_API_KEY')
}

response = requests.get(url, params=params)
data = response.json()

print(f'✅ Stack Exchange API connected')
print(f'✅ Quota remaining: {data[\"quota_remaining\"]}')
print(f'✅ Found {len(data[\"items\"])} questions')
"
```

**Expected Output:**
```
✅ Stack Exchange API connected
✅ Quota remaining: 9997
✅ Found 30 questions
```

---

## 🔒 **SECURITY**

### **Your .env file is:**
- ✅ **Ignored by git** (in `.gitignore`)
- ✅ **Never committed** to repository
- ✅ **Local only** on your machine

### **Best Practices:**
1. **Never share** your `.env` file
2. **Never commit** API keys to git
3. **Rotate keys** if accidentally exposed
4. **Use different keys** for production vs development

---

## 📂 **FILE STRUCTURE**

```
modules/expert-authority/config/
├── .env.example          # ✅ Committed (template)
├── .env                  # ❌ NOT committed (your credentials)
└── .gitignore            # ✅ Committed (protects .env)
```

---

## 🚀 **QUICK START (MINIMUM SETUP)**

### **For Tier 1 (Reddit Only):**

**Just need:**
1. Reddit API credentials (5 min)

**Then run:**
```bash
python modules/expert-authority/scripts/run_tier1.py
```

---

### **For Tier 2 (Multi-Platform):**

**Need:**
1. Reddit API credentials (5 min)
2. Stack Exchange API key (2 min)
3. Anthropic API key (if using LLM analysis)

**Then run:**
```bash
python modules/expert-authority/scripts/run_tier2.py
```

---

## ❓ **TROUBLESHOOTING**

### **Problem: "REDDIT_CLIENT_ID not found"**
**Solution:**
```bash
# Make sure .env file exists
ls modules/expert-authority/config/.env

# If not, copy from example
cp modules/expert-authority/config/.env.example modules/expert-authority/config/.env
```

### **Problem: "Invalid credentials" from Reddit**
**Solution:**
- Double-check client_id and client_secret (no extra spaces)
- Make sure you selected "script" type (not "web app")
- Verify redirect URI is `http://localhost:8080`

### **Problem: "Rate limit exceeded"**
**Solution:**
- Reddit: Wait 10 minutes, you have 600 requests/10min
- Stack Exchange: Add API key to get 10,000/day instead of 300/day

---

## 📞 **NEED HELP?**

**If credentials don't work:**
1. Verify `.env` file is in `modules/expert-authority/config/` directory
2. Check for typos (no spaces, no quotes around values)
3. Test with verification scripts above
4. Regenerate API keys if needed

---

## ✅ **READY TO GO?**

Once `.env` file is configured with Reddit credentials:

```bash
# Test with real Reddit data
python modules/expert-authority/scripts/run_tier1.py

# Expected: Scrapes real discussions, analyzes themes, generates report
```

**No more demo data - 100% real analysis from this point forward! 🚀**
