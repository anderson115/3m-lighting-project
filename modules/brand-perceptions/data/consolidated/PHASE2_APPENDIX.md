# Phase 2 Analysis: Appendix & Audit Trail

**Purpose:** This appendix provides complete audit trail for all insights in the Phase 2 report. Each table links to raw data with YouTube URLs for verification.

**Data Source:** 193 YouTube videos with transcripts
**Raw Data Location:** `phase2_raw_data.csv` (importable to Google Sheets/Excel)

---

## Appendix A: Video Type Distribution

**Methodology:** Pattern matching on title/description keywords

| Video Type | Command | Scotch | 3M Claw | Total | Example Video IDs |
|------------|---------|--------|---------|-------|-------------------|
| **tutorial** | 49 | 30 | 30 | **109** | `docWg4iJvBU`, `MXLYTvEB9M0`, `leLpogi2ytI` |
| **review** | 16 | 24 | 8 | **48** | `uIxHEvSm2IU`, `qEa_nByTsK0`, `X3P2BtttNS8` |
| **general** | 4 | 17 | 19 | **40** | `TYWZgfwzr9Y`, `UcjRnaIY370`, `u5BBfK-P1XM` |
| **comparison** | 5 | 14 | 20 | **39** | `1E_421pfNr4`, `YEU7jh2szDQ`, `4RJu41zSWbY` |
| **tips** | 13 | 9 | 8 | **30** | `xUJ6VqeYfeU`, `leLpogi2ytI`, `mY9QLFR6Ji8` |
| **problem** | 10 | 11 | 5 | **26** | `xUJ6VqeYfeU`, `MXLYTvEB9M0`, `V_lfoIByA7g` |
| **demo** | 3 | 6 | 2 | **11** | `2FuXFREKuLA`, `yk2erH1aRVk`, `XFnzQwmynAs` |

*See raw data tab for complete list*

---

## Appendix B: Sentiment Analysis Evidence

**Methodology:** Multi-stage keyword analysis with video type context

| Sentiment | Command | Scotch | 3M Claw | Total |
|-----------|---------|--------|---------|-------|
| **Positive** | 4 | 14 | 11 | **29** |
| **Negative** | 4 | 1 | 3 | **8** |
| **Mixed** | 2 | 11 | 8 | **21** |
| **Neutral** | 52 | 42 | 41 | **135** |

### Example Videos by Sentiment:

**Positive Sentiment:**
- `E82Z4LulJ5U` - Command Hook Large... (Command, 14,961 views)
- `IJ5aea7G8Wc` - 3M Command Strips Mop & Broom Holder Review – Worth It?... (Command, 8,582 views)
- `xsm6fWCDoLs` - REVIEW: Scotch-Mount Indoor Double-Sided Mounting White Tape... (Scotch, 2,563 views)
- `5ER_2YeE1Rc` - 🌵 10 Best Mounting Putties (Faber-Castell, Gorilla, and More... (Scotch, 2,238 views)
- `847dh87hrxY` - Scotch Double Sided Tape... (Scotch, 1,406 views)

**Negative Sentiment:**
- `xUJ6VqeYfeU` - Top 5 Picture Hanging Tips... (Command, 1,006,509 views)
- `f_2CGR_EopU` - Hang Heavy Frames up to 9kg with Command™ XL Picture Hanging... (Command, 263,046 views)
- `4RJu41zSWbY` - Battle of the Wall Hangers! 3M Claw vs. 3M Command Strips vs... (Command, 27,926 views)
- `po0CoRCZIuY` - 3M Command Strips X-Large Heavy Duty Hooks – Strong or Fail?... (Command, 22,278 views)
- `v8jGGEntxCo` - Top 6 Drywall Anchors Put to the TEST Can They Hold Heavy Ob... (3M Claw, 13,508 views)

**Mixed Sentiment:**
- `jDH_oJMGP_4` - 15 lb Capacity Command Hooks #commandhooks #wallhook #comman... (Command, 12,635 views)
- `MAJczST-ygg` - 3M Command Hooks - Can They Hold Curtain Rods? #shorts... (Command, 6,841 views)
- `UbXy3c2oAfA` - Which Duct Tape Brand is the Best?  Let's find out!... (Scotch, 4,851,719 views)
- `2__lmMVYS6A` - Which Masking Tape is the Best?  Frog Tape ve Duck Pro, Stik... (Scotch, 1,089,538 views)
- `_sBVEPslwZY` - Best Electrical Tape (Vinyl Tape)?  Lets find out!... (Scotch, 634,604 views)

*See raw data tab for complete sentiment classifications*

---

## Appendix C: Pain Point Detection Evidence

**Methodology:** Keyword matching with title-weighted severity scoring

| Pain Point | Total Severity | Command | Scotch | 3M Claw | Example Video IDs |
|------------|----------------|---------|--------|---------|-------------------|
| **Surface Damage** | 50 | 22 | 16 | 12 | `xUJ6VqeYfeU`, `MXLYTvEB9M0` |
| **Durability Issues** | 34 | 10 | 14 | 10 | `V1xFBYqS5uw`, `X3P2BtttNS8` |
| **Temperature Sensitive** | 15 | 1 | 13 | 1 | `KMPy704-UgE`, `u5BBfK-P1XM` |
| **Price Too High** | 10 | 2 | 5 | 3 | `PsjtpXSuBwo`, `8o0kwEFSI6s` |
| **Installation Difficulty** | 8 | 2 | 2 | 4 | `fxiu7gBwI2A`, `i5aqYXTrqdc` |
| **Adhesion Failure** | 3 | 1 | 0 | 2 | `YLyCJppyXJ4`, `tEWIVzV78WI` |
| **Weight Limitations** | 2 | 0 | 0 | 2 | `2EUbx6HB9eU`, `kdWg_AC5RN4` |

*Severity = keyword mentions + (title mentions × 2)*

*See raw data tab for complete pain point details*

---

## Appendix D: Benefit Detection Evidence

**Methodology:** Keyword matching with emphasis scoring

| Benefit | Total Emphasis | Command | Scotch | 3M Claw | Example Video IDs |
|---------|----------------|---------|--------|---------|-------------------|
| **Easy Installation** | 99 | 38 | 22 | 39 | `xUJ6VqeYfeU`, `mY9QLFR6Ji8` |
| **Strong Hold** | 68 | 18 | 27 | 23 | `docWg4iJvBU`, `f_2CGR_EopU` |
| **Time Saving** | 50 | 16 | 15 | 19 | `leLpogi2ytI`, `RXqcH1Cot6k` |
| **Value For Money** | 32 | 7 | 16 | 9 | `leLpogi2ytI`, `1E_421pfNr4` |
| **Versatile** | 29 | 7 | 10 | 12 | `YEU7jh2szDQ`, `dzekfXx-NHA` |
| **Rental Friendly** | 23 | 13 | 5 | 5 | `xUJ6VqeYfeU`, `mY9QLFR6Ji8` |
| **Professional Results** | 17 | 3 | 10 | 4 | `hR1bKoU1b04`, `tCEQXnlwBMw` |
| **Damage Free** | 11 | 9 | 2 | 0 | `hR1bKoU1b04`, `dzekfXx-NHA` |

*Emphasis = keyword mention frequency*

*See raw data tab for complete benefit details*

---

## Appendix E: Use Case Detection Evidence

**Methodology:** Keyword matching with mention counting

| Use Case | Total Mentions | Command | Scotch | 3M Claw | Example Video IDs |
|----------|----------------|---------|--------|---------|-------------------|
| **Picture Hanging** | 177 | 70 | 32 | 75 | `xUJ6VqeYfeU`, `docWg4iJvBU` |
| **Heavy Items** | 113 | 27 | 23 | 63 | `xUJ6VqeYfeU`, `MXLYTvEB9M0` |
| **Diy Projects** | 89 | 22 | 34 | 33 | `xUJ6VqeYfeU`, `MXLYTvEB9M0` |
| **Decoration** | 51 | 25 | 10 | 16 | `xUJ6VqeYfeU`, `docWg4iJvBU` |
| **Renter Friendly** | 30 | 16 | 11 | 3 | `mY9QLFR6Ji8`, `-7969X2nffo` |
| **Mirror** | 19 | 1 | 0 | 18 | `m3Zl0hbkOfU`, `jT07Bwi-Bis` |
| **Shelving** | 17 | 8 | 1 | 8 | `V_lfoIByA7g`, `1nG4IVnVQdI` |
| **Acoustic Treatment** | 16 | 8 | 8 | 0 | `leLpogi2ytI`, `PsjtpXSuBwo` |
| **Office** | 14 | 4 | 9 | 1 | `V_lfoIByA7g`, `X9v2gQS76PQ` |
| **Organization** | 14 | 10 | 2 | 2 | `hR1bKoU1b04`, `f6S4sSKiQ8o` |
| **Tv Mounting** | 13 | 3 | 6 | 4 | `V1xFBYqS5uw`, `vmyhOPlnrUE` |
| **Kitchen** | 10 | 8 | 2 | 0 | `hR1bKoU1b04`, `dzekfXx-NHA` |
| **Bathroom** | 10 | 8 | 0 | 2 | `hR1bKoU1b04`, `YEU7jh2szDQ` |
| **Curtains** | 5 | 4 | 1 | 0 | `GLMYF90YFTk`, `jWLQADP5wfg` |
| **Hooks** | 5 | 2 | 0 | 3 | `STiJxtkNckI`, `FRNCcXooxlA` |

*See raw data tab for complete use case details*

---

## Appendix F: Temperature Sensitivity - Theme Validation

**Claim:** Scotch products have unique temperature sensitivity pain point

**Evidence:**

- **Videos mentioning temperature issues:** 13 (6.7% of dataset)
- **By brand:** Command (1), Scotch (11), 3M Claw (1)

**Top Videos:**

- [3M Scotch® Extreme Double-Sided Mounting Tapeพลังการยึดติดที...](https://www.youtube.com/watch?v=u5BBfK-P1XM)
  - Video ID: `u5BBfK-P1XM`
  - Brand: Scotch | Views: 2,813,638 | Severity: 1

- [Which Masking Tape is the Best?  Frog Tape ve Duck Pro, Stik...](https://www.youtube.com/watch?v=2__lmMVYS6A)
  - Video ID: `2__lmMVYS6A`
  - Brand: Scotch | Views: 1,089,538 | Severity: 1

- [Best Electrical Tape (Vinyl Tape)?  Lets find out!...](https://www.youtube.com/watch?v=_sBVEPslwZY)
  - Video ID: `_sBVEPslwZY`
  - Brand: Scotch | Views: 634,604 | Severity: 2

- [3M Scotch® Extreme Double-Sided Mounting Tape พลังการยึดติดท...](https://www.youtube.com/watch?v=EqsXLBBBbQg)
  - Video ID: `EqsXLBBBbQg`
  - Brand: Scotch | Views: 19,400 | Severity: 1

- [Command hooks and Picture hanging strips, used and reviewed....](https://www.youtube.com/watch?v=KMPy704-UgE)
  - Video ID: `KMPy704-UgE`
  - Brand: Command | Views: 10,586 | Severity: 1

**Validation Status:** ✅ Theme present in 6.7% of dataset, primarily Scotch (11/13 videos)

---

## Appendix G: Renter-Friendly Positioning - Theme Validation

**Claim:** Command positioned as rental/apartment-friendly solution

**Evidence:**

- **Videos mentioning renter/apartment themes:** 43 (22.3% of dataset)
- **By brand:** Command (20), Scotch (16), 3M Claw (7)
- **Total mentions:** 53

**Top Videos:**

- [Introducing Scotch-Mount™ Multipurpose Gel Tape (:30)...](https://www.youtube.com/watch?v=OUB_KFvVEd0)
  - Video ID: `OUB_KFvVEd0`
  - Brand: Scotch | Views: 7,804,334 | Mentions: 1

- [Which Duct Tape Brand is the Best?  Let's find out!...](https://www.youtube.com/watch?v=UbXy3c2oAfA)
  - Video ID: `UbXy3c2oAfA`
  - Brand: Scotch | Views: 4,851,719 | Mentions: 1

- [Which Masking Tape is the Best?  Frog Tape ve Duck Pro, Stik...](https://www.youtube.com/watch?v=2__lmMVYS6A)
  - Video ID: `2__lmMVYS6A`
  - Brand: Scotch | Views: 1,089,538 | Mentions: 1

- [Top 5 Picture Hanging Tips...](https://www.youtube.com/watch?v=xUJ6VqeYfeU)
  - Video ID: `xUJ6VqeYfeU`
  - Brand: Command | Views: 1,006,509 | Mentions: 2

- [Home Staging Tips: Using Command Strips to Hang Wall Art by ...](https://www.youtube.com/watch?v=mY9QLFR6Ji8)
  - Video ID: `mY9QLFR6Ji8`
  - Brand: Command | Views: 516,325 | Mentions: 2

**Validation Status:** ✅ Theme present in 22.3% of dataset, strongest for Command (20/43 videos)

---

## Appendix H: Audit Trail Structure

**Three-Level Verification:**

1. **Insight Level (Main Report)**
   - High-level finding or claim
   - Links to relevant appendix section
   - Example: "Surface damage is #1 pain point" → See Appendix C

2. **Appendix Summary Tables (This Document)**
   - Aggregated counts and metrics
   - Example video IDs for verification
   - Links to raw data tab

3. **Raw Data Tab (CSV/Spreadsheet)**
   - Complete video-level data
   - YouTube URLs for source verification
   - All extracted insights in columns
   - File: `phase2_raw_data.csv`

**To Verify Any Claim:**
1. Find claim in main report
2. Navigate to referenced appendix section
3. Note example video IDs from summary table
4. Look up video ID in raw data CSV
5. Open YouTube URL to view original source

---

**Data Provenance Statement:**

All insights in Phase 2 Analysis Report derived exclusively from:
- 193 YouTube videos (Command: 62, Scotch: 68, 3M Claw: 63)
- Auto-generated transcripts via YouTube Data API
- Collection date: 2025-11-02
- Total views represented: 47.9M

No external data sources, prior projects, or assumptions used in analysis.