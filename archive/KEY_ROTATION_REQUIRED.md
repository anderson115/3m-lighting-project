# API Key Rotation Required

**Date Noted:** October 29, 2025
**Priority:** Medium
**Reason:** Secrets exposed in git history (commits c02ea5f, 8106e2a)

---

## Keys That Need Rotation

### 1. Apify API Token
- **Current Status:** Exposed in commits c02ea5f (4 files)
- **1Password Item:** `Apify_API_Key` (Development vault)
- **Rotation Steps:**
  1. Generate new API token at https://console.apify.com/account/integrations
  2. Update in 1Password: `op item edit Apify_API_Key "credential=NEW_TOKEN" --vault Development`
  3. Test with: `op run --env-file=.env.template -- python modules/category-intelligence/scrape_lowes_working.py`
  4. Revoke old token in Apify console

### 2. BrightData API Token
- **Current Status:** Not exposed in commits, but good practice to rotate
- **1Password Item:** `BrightData_API_Token` (Development vault)
- **Rotation Steps:**
  1. Generate new API token at BrightData dashboard
  2. Update in 1Password: `op item edit BrightData_API_Token "credential=NEW_TOKEN" --vault Development`
  3. Test with: `op run --env-file=.env.template -- python modules/category-intelligence/scrape_menards_brightdata.py`
  4. Revoke old token in BrightData dashboard

### 3. Google OAuth Credentials
- **Current Status:** Exposed in commit 8106e2a (we-are-here.md lines 175-176)
- **1Password Item:** `Google_OAuth_3M_Lighting` (Development vault)
- **Rotation Steps:**
  1. Go to https://console.cloud.google.com/apis/credentials
  2. Delete existing OAuth client "3M Lighting Project"
  3. Create new OAuth 2.0 Client ID
  4. Update in 1Password:
     ```bash
     op item edit Google_OAuth_3M_Lighting \
       "username=NEW_CLIENT_ID" \
       "password=NEW_CLIENT_SECRET" \
       --vault Development
     ```
  5. Test Google Drive integration
  6. Delete old credentials from Google Cloud Console

---

## Timeline

- **Immediate:** Can continue using current keys (they work fine)
- **Recommended:** Rotate within 7 days
- **Required:** Rotate before any suspected compromise

---

## Advantages of 1Password Rotation

No code changes needed! Just update the values in 1Password:

```bash
# Update any secret
op item edit ITEM_NAME "FIELD=NEW_VALUE" --vault Development

# All code automatically uses new value on next run
op run --env-file=.env.template -- python your_script.py
```

---

## Verification After Rotation

Run the test script to verify all secrets load correctly:

```bash
op run --env-file=.env.template -- python /tmp/test_secrets.py
```

Expected output:
```
Testing 1Password secret injection...
APIFY_TOKEN: ✅ Loaded (XX chars)
BRIGHTDATA_API_TOKEN: ✅ Loaded (XX chars)
GOOGLE_CLIENT_ID: ✅ Loaded (XX chars)
GOOGLE_CLIENT_SECRET: ✅ Loaded (XX chars)

✅ All secrets loaded successfully from 1Password!
```

---

## Notes

- Rotation can be done independently for each key
- No git commits needed (secrets stored in 1Password only)
- Test thoroughly after each rotation
- Document rotation date in 1Password item notes for audit trail
