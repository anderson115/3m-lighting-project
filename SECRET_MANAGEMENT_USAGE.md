# 1Password Secret Management - Usage Guide

**Date:** October 29, 2025
**Project:** 3M Lighting Project
**Vault:** Development

---

## ✅ Setup Complete

All secrets are now securely stored in 1Password and removed from code.

### What Was Done:

1. ✅ Created "Development" vault in 1Password
2. ✅ Added 3 secrets to vault:
   - `Apify_API_Key` - Apify API token for web scraping
   - `BrightData_API_Token` - BrightData proxy API token
   - `Google_OAuth_3M_Lighting` - Google OAuth credentials
3. ✅ Refactored 7 files to use environment variables
4. ✅ Removed hardcoded secrets from `we-are-here.md`
5. ✅ Created `.env.template` with 1Password secret references

---

## 🚀 How to Use Secrets

### Method 1: Run Scripts with `op run` (Recommended)

**Best for:** Running Python scripts, commands that need secrets

```bash
# Run any script with automatic secret injection
op run --env-file=.env.template -- python scrape_lowes_working.py
op run --env-file=.env.template -- python get_all_images.py
op run --env-file=.env.template -- python scrape_menards_brightdata.py

# Works with any command
op run --env-file=.env.template -- npm start
op run --env-file=.env.template -- ./my-script.sh
```

**How it works:**
- `op run` loads secrets from 1Password
- Injects them as environment variables
- Runs your command
- Secrets never touch disk

---

### Method 2: Generate `.env` File

**Best for:** Development, when you need a persistent `.env` file

```bash
# Generate .env file (NEVER commit this!)
op inject -i .env.template -o .env

# Then run scripts normally
python scrape_lowes_working.py

# Or load in shell
source .env
```

**⚠️ Warning:** `.env` file contains actual secrets - it's in `.gitignore` but be careful!

---

### Method 3: Load in Current Shell

**Best for:** Setting environment variables in your current terminal session

```bash
# Load secrets into current shell
eval $(op inject -i .env.template)

# Now secrets are available
echo $APIFY_TOKEN
python scrape_lowes_working.py
```

---

## 📂 Vault Structure

**Vault Name:** Development
**Location:** 1Password account (anderson115@gmail.com)

| Item Name | Type | Fields | Usage |
|-----------|------|--------|-------|
| `Apify_API_Key` | API Credential | `credential` | Apify web scraping API |
| `BrightData_API_Token` | API Credential | `credential` | BrightData proxy API |
| `Google_OAuth_3M_Lighting` | Login | `username`, `password` | Google Drive OAuth (ID + Secret) |

---

## 🔐 Secret References

**Format:** `op://VAULT/ITEM/FIELD`

### Current References:

```bash
# Apify
APIFY_TOKEN=op://Development/Apify_API_Key/credential

# BrightData
BRIGHTDATA_API_TOKEN=op://Development/BrightData_API_Token/credential

# Google OAuth
GOOGLE_CLIENT_ID=op://Development/Google_OAuth_3M_Lighting/username
GOOGLE_CLIENT_SECRET=op://Development/Google_OAuth_3M_Lighting/password
```

### Manual Access:

```bash
# Read a single secret
op read "op://Development/Apify_API_Key/credential"

# Get full item details
op item get Apify_API_Key --vault Development

# Reveal secret value
op item get Apify_API_Key --vault Development --reveal
```

---

## 📝 Files Refactored

All these files now use `os.getenv()` instead of hardcoded secrets:

1. `modules/category-intelligence/get_all_images.py`
2. `modules/category-intelligence/get_images_apify.py`
3. `modules/category-intelligence/scrape_lowes_menards_proxy.py`
4. `modules/category-intelligence/scrape_lowes_working.py`
5. `modules/category-intelligence/scrape_menards_brightdata.py`
6. `modules/category-intelligence/scrape_lowes_brightdata.py`
7. `we-are-here.md` (secrets removed, reference to 1Password added)

### Example Code Pattern:

```python
import os

# Load from environment (will be set by op run)
APIFY_TOKEN = os.getenv('APIFY_TOKEN')
if not APIFY_TOKEN:
    raise ValueError("APIFY_TOKEN environment variable not set. Run with: op run -- python script.py")

# Use the secret
client = ApifyClient(APIFY_TOKEN)
```

---

## 🔧 Troubleshooting

### Error: "environment variable not set"

**Problem:** Script run without `op run`
**Solution:** Use `op run --env-file=.env.template -- python script.py`

### Error: "vault not found"

**Problem:** Not signed in to 1Password CLI
**Solution:**
```bash
op account list  # Check if signed in
op signin       # Sign in if needed
```

### Error: "invalid secret reference"

**Problem:** Typo in secret reference
**Solution:** Check vault/item/field names match exactly (case-sensitive, use underscores)

### Secrets not loading

**Problem:** Biometric unlock may be required
**Solution:**
```bash
# Unlock 1Password with Touch ID/password
op vault list  # This will prompt for unlock
```

---

## 🔄 Adding New Secrets

### Step 1: Add to 1Password

```bash
# Create new API credential
op item create \
  --category="API Credential" \
  --title="My_New_API_Key" \
  --vault="Development" \
  "credential=YOUR_SECRET_HERE" \
  --tags="3m-lighting"

# Create new login (for username+password)
op item create \
  --category="Login" \
  --title="My_Service_Login" \
  --vault="Development" \
  username="my-username" \
  password="my-password" \
  --tags="3m-lighting"
```

### Step 2: Add to `.env.template`

```bash
# Add secret reference
echo "MY_NEW_SECRET=op://Development/My_New_API_Key/credential" >> .env.template
```

### Step 3: Use in code

```python
import os

MY_NEW_SECRET = os.getenv('MY_NEW_SECRET')
if not MY_NEW_SECRET:
    raise ValueError("MY_NEW_SECRET not set")
```

---

## 🔄 Rotating Secrets

### When to Rotate:
- Every 90 days (recommended)
- After suspected exposure
- When team members leave
- Best practice for security

### How to Rotate:

```bash
# 1. Generate new secret at provider (Apify, BrightData, etc.)

# 2. Update in 1Password
op item edit Apify_API_Key "credential=NEW_TOKEN_HERE" --vault Development

# 3. Test
op run --env-file=.env.template -- python scrape_lowes_working.py

# 4. Revoke old secret at provider
```

**✅ No code changes needed!** - Secret references stay the same

---

## 📊 Verification

### Test All Secrets Loaded:

```python
# Create test_secrets.py
import os

secrets = {
    'APIFY_TOKEN': os.getenv('APIFY_TOKEN'),
    'BRIGHTDATA_API_TOKEN': os.getenv('BRIGHTDATA_API_TOKEN'),
    'GOOGLE_CLIENT_ID': os.getenv('GOOGLE_CLIENT_ID'),
    'GOOGLE_CLIENT_SECRET': os.getenv('GOOGLE_CLIENT_SECRET')
}

for name, value in secrets.items():
    status = '✅' if value else '❌'
    length = len(value) if value else 0
    print(f"{status} {name}: {length} chars")
```

```bash
# Run test
op run --env-file=.env.template -- python test_secrets.py

# Expected output:
# ✅ APIFY_TOKEN: 46 chars
# ✅ BRIGHTDATA_API_TOKEN: 64 chars
# ✅ GOOGLE_CLIENT_ID: 72 chars
# ✅ GOOGLE_CLIENT_SECRET: 35 chars
```

---

## 🎯 Quick Reference

### Most Common Commands:

```bash
# Run a Python script with secrets
op run --env-file=.env.template -- python your_script.py

# Generate .env file
op inject -i .env.template -o .env

# Read a single secret
op read "op://Development/Apify_API_Key/credential"

# List all items in vault
op item list --vault Development

# View secret details (hidden)
op item get Apify_API_Key --vault Development

# View secret details (revealed)
op item get Apify_API_Key --vault Development --reveal

# Edit a secret
op item edit Apify_API_Key "credential=NEW_VALUE" --vault Development
```

---

## 🔒 Security Best Practices

✅ **Do:**
- Use `op run` for running scripts (secrets never written to disk)
- Commit `.env.template` (safe, contains only references)
- Rotate secrets every 90 days
- Use biometric unlock when available
- Keep 1Password desktop app updated

❌ **Don't:**
- Commit `.env` file (it's in `.gitignore` but be careful!)
- Share raw secrets via Slack/email
- Hardcode secrets in code
- Use same secrets across projects
- Store secrets in plain text files

---

## 📚 Additional Resources

**1Password CLI Documentation:**
- https://developer.1password.com/docs/cli/
- https://developer.1password.com/docs/cli/secret-references/

**This Project:**
- `.env.template` - Secret references (safe to commit)
- `SECRET_MANAGEMENT_COMPREHENSIVE_RANKING.md` - Tool comparison
- `VAULTWARDEN_VS_1PASSWORD_COMPARISON.md` - Why we chose 1Password

---

## ✅ Status

**Setup Date:** October 29, 2025
**Secrets Secured:** 3 (Apify, BrightData, Google OAuth)
**Files Refactored:** 7
**Status:** ✅ PRODUCTION READY

**All secrets are now secure!** 🎉
