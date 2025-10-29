# Secret Management Solutions: 5 Options for 3M Lighting Project

**Date:** October 29, 2025
**Purpose:** Comprehensive comparison of secret management solutions
**Current Problem:** Hardcoded secrets in 8+ files blocking git push

---

## Current Secrets Inventory

### Discovered Hardcoded Secrets:

1. **Apify API Token** (4 locations):
   - `modules/category-intelligence/get_all_images.py:10`
   - `modules/category-intelligence/get_images_apify.py:11`
   - `modules/category-intelligence/scrape_lowes_menards_proxy.py:9`
   - `modules/category-intelligence/scrape_lowes_working.py:9`
   - Value: `apify_api_REDACTED` (now in 1Password)

2. **BrightData API Tokens** (2 locations):
   - `modules/category-intelligence/scrape_menards_brightdata.py:9`
   - `modules/category-intelligence/scrape_lowes_brightdata.py:9`
   - Value: `22b7b4d3REDACTED` (now in 1Password)

3. **Google OAuth Credentials** (1 location):
   - `we-are-here.md:175-176`
   - Client ID: `331228229843-REDACTED.apps.googleusercontent.com`
   - Client Secret: `GOCSPX-REDACTED`

4. **Potential Future Secrets** (documented but not in code):
   - FRED API Key (economic data)
   - Reddit API credentials
   - OpenAI API Key
   - Claude API Key
   - YouTube API credentials

**Total:** 3 active secret types, 7 files to refactor

---

## Option 1: 1Password CLI + Secrets Automation

**Type:** Commercial SaaS with CLI integration
**Pricing:** $7.99/user/month (Teams), Free for personal developer use
**Best For:** Teams already using 1Password for password management

### How It Works

```bash
# Install CLI
brew install --cask 1password/tap/1password-cli

# Sign in
eval $(op signin)

# Store secret
op item create --category="API Credential" \
  --title="Apify API Key" \
  --vault="Development" \
  api_key="apify_api_..."

# Use in scripts with secret references
export APIFY_TOKEN=$(op read "op://Development/Apify API Key/api_key")

# Or inject directly into process
op run --env-file=".env.1password" -- python scrape_lowes_working.py
```

### Secret Reference Syntax

```python
# Python script example
import os
import subprocess

# Option A: Read secret on-demand
def get_secret(reference):
    result = subprocess.run(
        ['op', 'read', reference],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()

APIFY_TOKEN = get_secret("op://Development/Apify API Key/api_key")

# Option B: Load all secrets at script start (better)
# Run with: op run -- python script.py
APIFY_TOKEN = os.getenv('APIFY_TOKEN')
```

### Pros

✅ **Automatic Secret Rotation:** Integrated with many services
✅ **GitHub Actions Integration:** Official `1password/load-secrets-action`
✅ **Secret Masking:** Automatically conceals secrets in stdout
✅ **Cross-Platform:** Works on macOS, Linux, Windows
✅ **Team Collaboration:** Approval workflows, audit logs
✅ **Easy Migration:** If you already use 1Password
✅ **Desktop App Integration:** GUI for managing secrets
✅ **Biometric Auth:** Touch ID/Face ID support

### Cons

⚠️ **Requires 1Password Account:** Additional cost if not already using
⚠️ **Internet Dependency:** Needs connection to 1Password servers
⚠️ **Vendor Lock-in:** Proprietary solution
⚠️ **Manual Setup:** Each secret must be added via CLI/GUI

### Setup Time

- **Initial:** 30 minutes (install CLI, configure vault, add secrets)
- **Per Secret:** 2 minutes to add new secret
- **Per File:** 5-10 minutes to refactor

### Automatic Rotation

🔄 **Supported Services:**
- AWS credentials
- Database passwords (PostgreSQL, MySQL)
- SSH keys

🚫 **NOT Supported (manual rotation required):**
- Apify API tokens
- BrightData API tokens
- Google OAuth (must rotate via Google Cloud Console)

### Integration Quality

✅ **GitHub Actions:** Excellent (official action)
✅ **Local Development:** Excellent (`op run` command)
✅ **CI/CD:** Good (requires service account tokens)
✅ **Team Sharing:** Excellent (built-in)

---

## Option 2: Doppler (Developer-First SaaS)

**Type:** Commercial SaaS, closed-source
**Pricing:** Free (3 users, unlimited secrets), $12/user/month (Team), $24/user/month (Enterprise)
**Best For:** Developer teams prioritizing speed and ease of use

### How It Works

```bash
# Install CLI
brew install dopplerhq/cli/doppler

# Login
doppler login

# Initialize project (one-time)
doppler setup

# Create secrets via CLI or dashboard
doppler secrets set APIFY_TOKEN="apify_api_..." --project 3m-lighting

# Use in development (automatic injection)
doppler run -- python scrape_lowes_working.py

# Or export to .env for local dev
doppler secrets download --no-file --format env > .env
```

### Python Integration

```python
# Option A: Use doppler run (recommended)
# No code changes needed, run with: doppler run -- python script.py
import os
APIFY_TOKEN = os.getenv('APIFY_TOKEN')

# Option B: Doppler SDK (if you want programmatic access)
from doppler_sdk import DopplerSDK
doppler = DopplerSDK()
APIFY_TOKEN = doppler.secrets.get("APIFY_TOKEN")
```

### Pros

✅ **Fastest Setup:** 5-10 minutes to full implementation
✅ **Best Developer Experience:** Intuitive UI + CLI
✅ **Branch-Based Secrets:** Different secrets per git branch
✅ **Real-Time Sync:** Changes propagate instantly
✅ **No Usage Limits:** Unlimited secrets, API calls (on paid plans)
✅ **Extensive Integrations:** AWS, Vercel, Heroku, GitHub Actions, etc.
✅ **Automatic Backups:** Point-in-time recovery
✅ **Secret Versioning:** Full history and rollback

### Cons

⚠️ **Closed Source:** No self-hosting option
⚠️ **Cloud-Only:** Requires internet connection
⚠️ **Flat Pricing:** Per-user cost (but simpler than usage-based)
⚠️ **No Manual Rotation:** Doesn't auto-rotate third-party API keys

### Setup Time

- **Initial:** 10 minutes (signup, install CLI, create project)
- **Per Secret:** 30 seconds (web UI) or 1 command (CLI)
- **Per File:** 5 minutes to refactor

### Automatic Rotation

🔄 **Supported Services:**
- AWS IAM credentials
- Database credentials (via plugins)

🚫 **NOT Supported:**
- Third-party API keys (Apify, BrightData, Google OAuth)

### Integration Quality

✅ **GitHub Actions:** Excellent (official action)
✅ **Local Development:** Excellent (`doppler run`)
✅ **CI/CD:** Excellent (service tokens)
✅ **Team Sharing:** Excellent (granular permissions)

### Unique Features

- **Secret Referencing:** Reference secrets from other projects
- **Dynamic Secrets:** Generate values based on other secrets
- **Audit Logging:** Complete activity history
- **Webhooks:** Trigger actions when secrets change

---

## Option 3: Infisical (Open Source Alternative)

**Type:** Open-source, self-hostable or cloud
**Pricing:** Free (Open Source), $18/user/month (Pro Cloud), Custom (Enterprise)
**Best For:** Teams wanting open-source with self-hosting option

### How It Works

```bash
# Install CLI
brew install infisical/get-cli/infisical

# Login (cloud or self-hosted)
infisical login

# Initialize project
infisical init

# Set secrets (via CLI or web dashboard)
infisical secrets set APIFY_TOKEN="apify_api_..." --env=dev

# Run with automatic injection
infisical run -- python scrape_lowes_working.py

# Or export for .env usage
infisical secrets --format=dotenv > .env
```

### Python Integration

```python
# Option A: Use infisical run (recommended)
import os
APIFY_TOKEN = os.getenv('APIFY_TOKEN')

# Option B: Python SDK (programmatic access)
from infisical_client import InfisicalClient

client = InfisicalClient(token=os.environ["INFISICAL_TOKEN"])
APIFY_TOKEN = client.get_secret("APIFY_TOKEN", environment="dev")
```

### Pros

✅ **100% Open Source:** MIT license, full code access
✅ **Self-Hostable:** Run on your infrastructure (Docker, Kubernetes)
✅ **No Vendor Lock-in:** Export and migrate anytime
✅ **Advanced Organization:** Folder structure for secrets
✅ **Unlimited Secrets:** No throttling on self-hosted
✅ **End-to-End Encryption:** Zero-knowledge architecture
✅ **Git Integration:** Sync secrets to git repos (encrypted)
✅ **Free Tier:** Generous limits on cloud version

### Cons

⚠️ **Self-Hosting Complexity:** 1-3 hours setup for on-prem
⚠️ **Longer Onboarding:** 10-15 minutes (cloud), hours (self-hosted)
⚠️ **Usage Limits (Cloud):** API throttling on free/pro tiers
⚠️ **Charges for Machine Identities:** Unlike Doppler
⚠️ **Smaller Community:** Newer than HashiCorp Vault

### Setup Time

- **Initial (Cloud):** 15 minutes
- **Initial (Self-Hosted):** 1-3 hours (Docker) to 1 day (Kubernetes)
- **Per Secret:** 1 minute (UI) or 1 command (CLI)
- **Per File:** 5-10 minutes to refactor

### Automatic Rotation

🔄 **Supported Services:**
- AWS IAM
- Database credentials
- Kubernetes secrets

🚫 **NOT Supported:**
- Third-party SaaS API keys

### Integration Quality

✅ **GitHub Actions:** Excellent (official action)
✅ **Local Development:** Excellent (`infisical run`)
✅ **CI/CD:** Good (machine identities)
✅ **Self-Hosting:** Excellent (Docker/K8s)

### Unique Features

- **Secret Rotation:** Automated rotation workflows
- **Secret Scanning:** Detect hardcoded secrets in repos
- **Point-in-Time Recovery:** Restore to any previous state
- **Approval Workflows:** Require approval for secret changes
- **Compliance:** SOC 2, HIPAA ready

---

## Option 4: Environment Variables + direnv (Local-First)

**Type:** Free, open-source, local-only
**Pricing:** Free
**Best For:** Solo developers, simple projects, those who want full control

### How It Works

```bash
# Install direnv
brew install direnv

# Add to shell (zsh example)
echo 'eval "$(direnv hook zsh)"' >> ~/.zshrc

# Create .envrc file in project root
cat > .envrc << 'EOF'
export APIFY_TOKEN="YOUR_APIFY_TOKEN_HERE"
export BRIGHTDATA_API_TOKEN="YOUR_BRIGHTDATA_TOKEN_HERE"
export GOOGLE_CLIENT_ID="YOUR_CLIENT_ID.apps.googleusercontent.com"
export GOOGLE_CLIENT_SECRET="GOCSPX-YOUR_CLIENT_SECRET_HERE"
EOF

# Allow direnv to load this file
direnv allow

# Create .env.template for git (no secrets)
cat > .env.template << 'EOF'
APIFY_TOKEN=your_apify_token_here
BRIGHTDATA_API_TOKEN=your_brightdata_token_here
GOOGLE_CLIENT_ID=your_google_client_id_here
GOOGLE_CLIENT_SECRET=your_google_client_secret_here
EOF

# Add to .gitignore
echo ".envrc" >> .gitignore
echo ".env" >> .gitignore
```

### Python Integration

```python
# All scripts automatically use environment variables
import os

APIFY_TOKEN = os.getenv('APIFY_TOKEN')
if not APIFY_TOKEN:
    raise ValueError("APIFY_TOKEN not set. Copy .env.template to .envrc and add your credentials.")

# Or use python-dotenv for .env files
from dotenv import load_dotenv
load_dotenv()

APIFY_TOKEN = os.getenv('APIFY_TOKEN')
```

### Centralized Secret Storage

```bash
# Option: Store all secrets in ~/.config/secrets/
mkdir -p ~/.config/secrets

# Create secrets file
cat > ~/.config/secrets/3m-lighting.env << 'EOF'
export APIFY_TOKEN="apify_api_..."
export BRIGHTDATA_API_TOKEN="22b7b4d3..."
export GOOGLE_CLIENT_ID="331228229843..."
export GOOGLE_CLIENT_SECRET="GOCSPX-..."
EOF

# Reference in project .envrc
echo 'source ~/.config/secrets/3m-lighting.env' > .envrc
direnv allow
```

### Pros

✅ **100% Free:** No costs ever
✅ **Complete Control:** All secrets stay local
✅ **No Internet Required:** Fully offline
✅ **Instant Setup:** 5 minutes
✅ **Zero Dependencies:** Just environment variables
✅ **Auto-Loading:** direnv loads secrets when entering directory
✅ **Simple:** Easy to understand and debug
✅ **Universal:** Works with any programming language

### Cons

⚠️ **No Team Sharing:** Manual sharing required (1Password, encrypted file, etc.)
⚠️ **No Rotation:** Completely manual
⚠️ **No Audit Trail:** No logging of secret access
⚠️ **Manual Backups:** Risk of losing secrets
⚠️ **No CI/CD Integration:** Must configure separately
⚠️ **Security Risk:** Secrets in plaintext files on disk

### Setup Time

- **Initial:** 5 minutes (install direnv, create .envrc)
- **Per Secret:** 10 seconds (add line to file)
- **Per File:** 2 minutes to refactor

### Automatic Rotation

🚫 **None:** All rotation is manual

### Integration Quality

✅ **Local Development:** Excellent (automatic loading)
⚠️ **GitHub Actions:** Manual (use GitHub Secrets)
⚠️ **CI/CD:** Manual configuration required
⚠️ **Team Sharing:** Poor (manual, insecure)

### Enhanced Security Option

```bash
# Encrypt secrets file with GPG
gpg --encrypt --recipient your@email.com ~/.config/secrets/3m-lighting.env

# Decrypt when needed
gpg --decrypt ~/.config/secrets/3m-lighting.env.gpg | source /dev/stdin

# Or use git-crypt for repo-level encryption
```

---

## Option 5: HashiCorp Vault (Enterprise-Grade)

**Type:** Open-source, self-hosted or HCP (cloud)
**Pricing:** Free (Open Source), $0.03/hour/cluster (HCP), Custom (Enterprise)
**Best For:** Large teams, multi-cloud, compliance-heavy industries

### How It Works

```bash
# Option A: HCP Vault (managed cloud)
# Sign up at portal.cloud.hashicorp.com

# Option B: Self-hosted (Docker)
docker run --cap-add=IPC_LOCK -e 'VAULT_DEV_ROOT_TOKEN_ID=myroot' -p 8200:8200 vault

# Install CLI
brew install vault

# Login
export VAULT_ADDR='http://127.0.0.1:8200'
export VAULT_TOKEN='myroot'

# Store secrets (KV v2 engine)
vault kv put secret/3m-lighting/apify token="apify_api_..." project="3m-lighting"
vault kv put secret/3m-lighting/brightdata token="22b7b4d3..."
vault kv put secret/3m-lighting/google client_id="331228229843..." client_secret="GOCSPX-..."

# Read secret
vault kv get -field=token secret/3m-lighting/apify
```

### Python Integration

```python
# Option A: HVAC library (official Python client)
import hvac
import os

client = hvac.Client(
    url=os.getenv('VAULT_ADDR'),
    token=os.getenv('VAULT_TOKEN')
)

# Read secret
secret = client.secrets.kv.v2.read_secret_version(path='3m-lighting/apify')
APIFY_TOKEN = secret['data']['data']['token']

# Option B: Environment variable injection (via vault CLI)
# Run with: vault kv get -field=token secret/3m-lighting/apify
```

### Bash Integration (for scripts)

```bash
#!/bin/bash

# Load secrets into environment
export APIFY_TOKEN=$(vault kv get -field=token secret/3m-lighting/apify)
export BRIGHTDATA_TOKEN=$(vault kv get -field=token secret/3m-lighting/brightdata)

# Run Python script
python scrape_lowes_working.py
```

### Pros

✅ **Dynamic Secrets:** Generate short-lived credentials on-demand
✅ **Enterprise Features:** Advanced policies, audit logs, HA
✅ **Multi-Cloud:** AWS, Azure, GCP, on-prem
✅ **Plugin Ecosystem:** Hundreds of integrations
✅ **Auto-Rotation:** For databases, cloud providers
✅ **Compliance:** Meets SOC 2, PCI-DSS, HIPAA
✅ **Encryption as a Service:** Encrypt data without storing keys
✅ **Identity-Based Access:** AppRole, Kubernetes, LDAP, AWS IAM auth

### Cons

⚠️ **Steep Learning Curve:** Complex to set up and maintain
⚠️ **Ops Overhead:** Requires dedicated DevOps/SRE for self-hosted
⚠️ **Overkill for Small Teams:** Too complex for simple use cases
⚠️ **Cost (HCP):** Can get expensive at scale
⚠️ **Setup Time:** Hours to days for production setup

### Setup Time

- **Initial (HCP Cloud):** 1-2 hours (managed service)
- **Initial (Self-Hosted Dev):** 30 minutes (Docker)
- **Initial (Self-Hosted Prod):** 1-3 days (HA cluster, policies, auth)
- **Per Secret:** 2 minutes (CLI) or 1 minute (UI)
- **Per File:** 10-15 minutes to refactor

### Automatic Rotation

🔄 **Supported Services (Best-in-Class):**
- AWS IAM credentials (dynamic, short-lived)
- Database credentials (PostgreSQL, MySQL, MongoDB, etc.)
- SSH certificates (short-lived)
- PKI/TLS certificates (auto-renew)
- Kubernetes service accounts

🚫 **NOT Supported:**
- Third-party SaaS APIs (Apify, BrightData) - manual rotation

### Integration Quality

✅ **Kubernetes:** Excellent (native integration)
✅ **AWS/Azure/GCP:** Excellent (dynamic credentials)
✅ **GitHub Actions:** Good (community actions)
✅ **Local Development:** Good (requires Vault agent or CLI)
✅ **Multi-Cloud:** Excellent (platform-agnostic)

### Unique Features

- **Dynamic Secrets:** Generate AWS/DB credentials on-the-fly with TTL
- **Leasing & Renewal:** Auto-revoke secrets after expiry
- **Seal/Unseal:** Encrypt secrets at rest, manual unseal required
- **Performance Replication:** Replicate across regions
- **Sentinel Policies:** Advanced policy-as-code

---

## Comparison Matrix

| Feature | 1Password CLI | Doppler | Infisical | direnv + .env | HashiCorp Vault |
|---------|---------------|---------|-----------|----------------|------------------|
| **Pricing** | $8/user/month | Free-$24/user | Free-$18/user | Free | Free-$$$$ |
| **Setup Time** | 30 min | 10 min | 15 min (cloud)<br>1-3 hrs (self-host) | 5 min | 30 min (dev)<br>1-3 days (prod) |
| **Developer Experience** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| **Team Collaboration** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐ | ⭐⭐⭐⭐ |
| **Self-Hosting** | ❌ | ❌ | ✅ | ✅ (local) | ✅ |
| **Open Source** | ❌ | ❌ | ✅ MIT | ✅ | ✅ MPL 2.0 |
| **Auto Rotation** | Limited | Limited | Limited | ❌ | ⭐⭐⭐⭐⭐ |
| **GitHub Actions** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| **Audit Logs** | ✅ | ✅ | ✅ | ❌ | ✅ |
| **Secret Masking** | ✅ | ✅ | ✅ | ❌ | ✅ |
| **Dynamic Secrets** | ❌ | ❌ | ❌ | ❌ | ⭐⭐⭐⭐⭐ |
| **Learning Curve** | Low | Low | Low-Med | Very Low | High |
| **Vendor Lock-in** | High | High | Low | None | Low |
| **Internet Required** | Yes | Yes | Yes (cloud)<br>No (self-host) | No | No (self-host) |

---

## Recommendations by Use Case

### For Solo Developer (You Right Now)

**🏆 WINNER: Option 4 - direnv + .env**

**Why:**
- ✅ Solve the git push problem in 10 minutes
- ✅ Zero cost, zero account setup
- ✅ Complete control, no internet dependency
- ✅ Can migrate to a SaaS solution later if needed

**Implementation:**
```bash
# 1. Install direnv (1 minute)
brew install direnv
echo 'eval "$(direnv hook zsh)"' >> ~/.zshrc
source ~/.zshrc

# 2. Create centralized secrets (2 minutes)
mkdir -p ~/.config/secrets
cat > ~/.config/secrets/3m-lighting.env << 'EOF'
export APIFY_TOKEN="YOUR_APIFY_TOKEN_HERE"
export BRIGHTDATA_API_TOKEN="YOUR_BRIGHTDATA_TOKEN_HERE"
export GOOGLE_CLIENT_ID="YOUR_CLIENT_ID.apps.googleusercontent.com"
export GOOGLE_CLIENT_SECRET="GOCSPX-YOUR_CLIENT_SECRET_HERE"
EOF

# 3. Link to project (1 minute)
cd /Users/anderson115/00-interlink/12-work/3m-lighting-project
echo 'source ~/.config/secrets/3m-lighting.env' > .envrc
direnv allow

# 4. Update .gitignore (1 minute)
echo ".envrc" >> .gitignore
echo ".env" >> .gitignore

# 5. Refactor 7 files (30 minutes total)
# Replace hardcoded secrets with os.getenv()

# 6. Remove secrets from we-are-here.md (2 minutes)
# Delete lines 175-176

# Total time: 37 minutes
```

---

### For Small Team (2-5 developers)

**🏆 WINNER: Option 2 - Doppler**

**Why:**
- ✅ Best developer experience (onboarding new devs in minutes)
- ✅ Free tier supports 3 users
- ✅ Branch-based environments (dev/staging/prod)
- ✅ Real-time secret sync (no "did you get the latest .env?" questions)
- ✅ GitHub Actions integration for CI/CD

**Runner-up:** Infisical (if you prefer open-source)

---

### For Medium Team with Compliance Needs (6-20 developers)

**🏆 WINNER: Option 3 - Infisical (Self-Hosted)**

**Why:**
- ✅ Open-source (satisfy compliance audits)
- ✅ Self-hosted (data stays in your infrastructure)
- ✅ Audit logs, approval workflows
- ✅ Lower cost than Doppler/1Password at scale
- ✅ No vendor lock-in

**Runner-up:** 1Password CLI (if already using 1Password for team)

---

### For Enterprise / Multi-Cloud (20+ developers)

**🏆 WINNER: Option 5 - HashiCorp Vault**

**Why:**
- ✅ Dynamic secrets (auto-expire, zero standing credentials)
- ✅ Multi-cloud (AWS, Azure, GCP)
- ✅ Enterprise compliance (SOC 2, HIPAA, PCI-DSS)
- ✅ Advanced policies and RBAC
- ✅ Industry standard

**Runner-up:** Doppler (if you prioritize ease of use over features)

---

### If You're Already Using 1Password

**🏆 WINNER: Option 1 - 1Password CLI**

**Why:**
- ✅ Leverage existing investment
- ✅ No new tools to learn
- ✅ Integrated with team's existing workflows
- ✅ Biometric auth (Touch ID)

---

## Migration Path Recommendation

### Phase 1: Immediate Fix (Today)
**Use direnv** to unblock git push and remove hardcoded secrets.

### Phase 2: Team Evaluation (Next Week)
Test Doppler and Infisical with your team. Choose based on:
- Budget (Infisical cheaper at scale)
- Self-hosting requirement (Infisical only option)
- Developer experience priority (Doppler wins)

### Phase 3: Long-term (3-6 months)
If you scale to enterprise, migrate to HashiCorp Vault for dynamic secrets and multi-cloud support.

---

## My Recommendation for 3M Lighting Project

**🎯 START WITH: Option 4 (direnv + .env)**

**Reasoning:**
1. ✅ **Unblock git push today** (10 minutes setup)
2. ✅ **Zero cost** (you're solo right now)
3. ✅ **Simple** (easy to understand and maintain)
4. ✅ **Easy migration** later (to Doppler/Infisical when team grows)

**Future-proof:**
- When you add a second developer → migrate to Doppler (2 hours)
- When you need compliance → migrate to Infisical self-hosted (1 day)
- When you go multi-cloud/enterprise → migrate to HashiCorp Vault (1 week)

---

## Next Steps

**Choose your option, and I'll:**

1. ✅ Install and configure the chosen tool
2. ✅ Refactor all 7 files to use environment variables
3. ✅ Remove hardcoded secrets from we-are-here.md
4. ✅ Create comprehensive documentation:
   - How to set up secrets (for you and future team members)
   - How to add new secrets
   - How to rotate secrets
5. ✅ Create `.env.template` for reference
6. ✅ Update `.gitignore`
7. ✅ Test all scripts still work
8. ✅ Commit and push to GitHub

**Which option do you want to use?**

**Quick decision matrix:**
- "Just fix it now, I'll think about teams later" → **Option 4 (direnv)**
- "I want best developer experience and might add team soon" → **Option 2 (Doppler)**
- "I need open-source and self-hosting" → **Option 3 (Infisical)**
- "I already use 1Password" → **Option 1 (1Password CLI)**
- "I'm building an enterprise system" → **Option 5 (HashiCorp Vault)**
