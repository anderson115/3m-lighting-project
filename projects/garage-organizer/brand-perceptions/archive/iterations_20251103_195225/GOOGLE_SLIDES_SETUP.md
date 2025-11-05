# Google Slides API Setup

## 🎯 Goal
Convert HTML slides → Google Slides (fully autonomous)

---

## ⚡ Setup (5 minutes)

### Step 1: Get Google API Credentials

1. **Go to:** https://console.developers.google.com
2. **Create project** (or select existing)
   - Click "Select a project" → "NEW PROJECT"
   - Name: "3M Slides Converter"
   - Click "CREATE"

3. **Enable Google Slides API**
   - Click "Enable APIs and Services"
   - Search: "Google Slides API"
   - Click "ENABLE"

4. **Create Credentials**
   - Click "Credentials" (left sidebar)
   - Click "+ CREATE CREDENTIALS" → "OAuth client ID"
   - If asked, configure consent screen:
     - User Type: "External"
     - App name: "Slides Converter"
     - User support email: (your email)
     - Developer contact: (your email)
     - Click "SAVE AND CONTINUE" (skip scopes, test users)
   - Back to Create OAuth client ID:
     - Application type: "Desktop app"
     - Name: "Desktop Client"
     - Click "CREATE"

5. **Download Credentials**
   - Click "DOWNLOAD JSON"
   - Save file as: `credentials.json`
   - Move to: `/Users/anderson115/00-interlink/12-work/3m-lighting-project/modules/brand-perceptions/credentials.json`

---

## 🚀 Run Conversion

```bash
cd /Users/anderson115/00-interlink/12-work/3m-lighting-project/modules/brand-perceptions
source .venv/bin/activate
python3 html_to_google_slides.py
```

**First run:**
- Browser will open
- Click "Allow" (authorize app)
- Token saved to `token.json` (reused next time)

**Output:**
- Google Slides presentation created
- URL printed to console
- All HTML slides converted

---

## 📊 What It Does

1. ✅ Parses HTML slides (extracts text, structure)
2. ✅ Creates Google Slides presentation
3. ✅ Adds slides with content
4. ✅ Preserves text, layouts
5. ⚠️ Simplifies gradients/shadows (Google Slides limitations)

---

## ⏱️ Timeline

- **Setup:** 5 min (one-time)
- **Conversion:** 2 min (automated)
- **Expected fidelity:** 75-85%

---

## 🔧 Troubleshooting

### "credentials.json not found"
→ Download from Google Cloud Console (step 5 above)

### "Access blocked"
→ Add your email to test users in OAuth consent screen

### "API not enabled"
→ Enable Google Slides API in API Library

---

**READY: Follow Step 1 now, then run the script**
