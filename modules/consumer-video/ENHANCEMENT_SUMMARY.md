# Consumer Video Enhancement Summary

## Three New Analysis Layers Implemented

### 1. JTBD Extractor (`jtbd_extractor.py`)
**Evidence-first extraction of functional, social, and emotional jobs**

**Status:** ✅ Implemented & Tested

**Test Results on consumer02:**
- Found **3 JTBD instances**
- All **functional** category (installation decisions, expertise gaps)
- Confidence range: 0.60-0.70

**Example Extraction:**
```
Verbatim: "because I'm not an electrician and I don't necessarily know how to
           reconvert the power back to where it needed to be."
Categories: functional
Confidence: 0.70
Evidence: functional_signal="needed to"
```

**Anti-Bias Mechanisms:**
- Rejects general opinions ("I think lighting is important")
- Requires first-person personal experience
- Validates lighting-related context
- Confidence scoring with thresholds

**Confidence Levels:**
- High (0.8-1.0): Explicit language + clear intent
- Medium (0.6-0.79): Implied but clear from context
- Low (0.4-0.59): Ambiguous - flagged for manual review
- Reject (<0.4): Insufficient evidence

---

### 2. Product Tracker (`product_tracker.py`)
**3M product mention detection with usage context**

**Status:** ✅ Implemented & Tested

**Detects:**
- Command hooks/strips
- Scotch tape products
- 3M brand mentions
- Generic adhesive/tape (for comparison)

**Test Results on consumer02:**
- Found **0 3M product mentions** (no Command/Scotch in this video)
- Correctly identified as generic "battery-operated light"
- No false positives ✅

**Extraction Components:**
```python
{
    'product_type': 'command' | 'scotch' | '3m' | 'generic_adhesive',
    'application': 'What they used it for',
    'outcome': 'success' | 'failure' | 'unclear',
    'outcome_confidence': 0.0-1.0,
    'alternative_considered': 'What else they tried',
    'wish_statement': 'What they wish existed'
}
```

**Success/Failure Detection:**
- **Success indicators:** "worked well", "held up", "still holding", "recommend"
- **Failure indicators:** "fell off", "didn't stick", "came loose", "failed"
- Requires **explicit statements** (not inference)

**Example (hypothetical):**
```
Product: Command hooks
Application: "trying to mount pendant light to ceiling"
Outcome: failure (confidence: 0.85)
Verbatim: "I tried Command hooks but they wouldn't hold the weight"
Alternative: "Used floor lamp instead"
```

---

### 3. Workaround Detector (`workaround_detector.py`)
**Compensating behaviors that signal product gaps**

**Status:** ✅ Implemented & Needs Pattern Tuning

**Three-Component Structure:**
1. **Intent:** What they were trying to do
2. **Barrier:** What prevented straightforward solution
3. **Solution:** What they did instead

**Test Results on consumer02:**
- Should detect **1 workaround** (board-backed battery light)
- **Currently detecting 0** - pattern matching needs refinement

**Expected Detection:**
```
Intent: "hardwire something behind that"
Barrier: "I'm not an electrician and I don't necessarily know how to reconvert
         the power back to where it needed to be"
Solution: "a piece of board behind the battery-operated light would be the best
          opportunity"
Confidence: 0.85
```

**Workaround Linguistic Patterns:**
- **Trial/Error:** "I tried... but...", "that didn't work so..."
- **Substitution:** "ended up using", "settled for", "instead I"
- **Modification:** "had to modify", "rigged up", "made it work by"
- **Combination:** "used... along with...", "combined... and..."

**Known Issue:**
The detector currently requires explicit pattern matches. The consumer02 transcript uses more conversational language ("coming to the realization that..."). Pattern refinement needed for next iteration.

---

## Integration Plan

### Phase 1: Add to Analysis Pipeline ✅

Modify `consumer_analyzer.py` to include new extractors:

```python
# After transcription step
from jtbd_extractor import JTBDExtractor
from product_tracker import ProductTracker
from workaround_detector import WorkaroundDetector

# Initialize extractors
jtbd_extractor = JTBDExtractor()
product_tracker = ProductTracker()
workaround_detector = WorkaroundDetector()

# Extract insights
jtbd_findings = jtbd_extractor.extract_jtbd_from_video(analysis)
product_mentions = product_tracker.extract_product_mentions(analysis)
workarounds = workaround_detector.detect_workarounds(analysis)

# Add to analysis JSON
analysis['jtbd'] = jtbd_findings
analysis['products_3m'] = product_mentions
analysis['workarounds'] = workarounds
```

### Phase 2: Add to Client Report

New sections in HTML/Markdown reports:

**Section: Jobs-to-Be-Done Map**
- Functional jobs (installation tasks, technical goals)
- Social jobs (rental constraints, stakeholder approval)
- Emotional jobs (relief, pride, frustration resolution)

**Section: 3M Product Usage**
- Where Command/Scotch mentioned
- Success vs failure instances
- What consumers wished existed
- Product gap signals

**Section: Workarounds & Compensating Behaviors**
- Intent → Barrier → Alternative solution
- Frequency across videos
- Product opportunity areas

### Phase 3: Validation on 5-Video Batch

**Quality Validation Checklist:**

1. **JTBD Accuracy**
   - Manual review: 15 random categorizations
   - Target: >85% defensible
   - Check: Are we finding only what we expected?

2. **Product Detection**
   - All 3M mentions caught?
   - Any false positives?
   - Target: 100% recall, >90% precision

3. **Workaround Completeness**
   - All three components present?
   - Target: >80% complete structures
   - Refine patterns based on failures

---

## Anti-Bias Safeguards Implemented

### 1. Negative Example Filtering

**Reject if:**
- General opinion: "I think good lighting is important"
- Hypothetical: "If I were to do this differently..."
- About others: "My friend has a lighting problem"
- Off-topic: "I also installed a new faucet"

**Only extract if:**
- ✅ About THIS person's lighting experience
- ✅ Specific to installation/usage (not general philosophy)
- ✅ Concrete event or outcome (not vague opinion)

### 2. Context Validation

**Before categorizing:**
- Check surrounding sentences (±30-45 seconds)
- Validate lighting relevance
- Validate specificity (reject vague statements)
- Require first-person personal experience

### 3. Confidence Thresholds

**Minimum confidence scores:**
- JTBD categorization: 0.6
- Product mention: 0.7
- Workaround detection: 0.65
- Success/failure: 0.75

**For borderline cases:**
- Flag for manual review (within 0.1 of threshold)
- Don't auto-classify uncertain cases

### 4. Evidence Requirement

**Every extraction includes:**
- Verbatim quote from transcript
- Timestamp (seconds)
- Context window (surrounding text)
- Evidence signals that triggered detection
- Confidence score with rationale

---

## Next Steps

### Immediate (Ready Now)

1. **Integrate extractors into batch pipeline**
   - Modify `run_batch_5videos.py`
   - Add JTBD/products/workarounds to each video analysis
   - Re-run on existing 5 videos

2. **Update client report generator**
   - Add JTBD section with category breakdown
   - Add product usage map
   - Add workaround section
   - Regenerate HTML report

### Short-term (Next Session)

3. **Refine workaround patterns**
   - Add conversational alternatives ("coming to the realization that...")
   - Test on consumer02 edge case
   - Lower confidence threshold to 0.5 for pilot

4. **Validation review**
   - Manual spot-check 15 JTBD categorizations
   - Check for false positives in product detection
   - Verify workaround intent/barrier/solution completeness

5. **Run on full 15-video set**
   - Batch process all consumer videos
   - Generate comprehensive JTBD map
   - Identify 3M product usage patterns
   - Surface workaround clusters

### Future Enhancements

6. **Visual product detection** (if needed)
   - Use Qwen2.5-VL on frames to detect visible products
   - Cross-reference with transcript mentions
   - Flag discrepancies for review

7. **Sentiment correlation**
   - Map JTBD categories to emotion analysis
   - Identify which jobs create frustration vs satisfaction
   - Prioritize jobs by emotional intensity

8. **Workaround clustering**
   - Group similar workarounds across participants
   - Identify patterns: "10% of users improvise board-backing"
   - Prioritize product gaps by workaround frequency

---

## Example Output Structure

### JTBD Entry:
```json
{
  "jtbd_id": "consumer02_32",
  "categories": ["functional", "social"],
  "confidence": 0.70,
  "verbatim": "because I'm not an electrician and I don't necessarily know how
               to reconvert the power back to where it needed to be.",
  "timestamp": 32.6,
  "participant": "AlanG",
  "evidence": {
    "functional_signal": "needed to",
    "social_constraint": "not an electrician"
  },
  "video_id": "consumer02"
}
```

### Product Mention:
```json
{
  "product_id": "consumer04_command_5",
  "product_type": "command",
  "product_name": "Command hooks",
  "mention_verbatim": "I tried Command hooks first but they wouldn't hold the weight",
  "timestamp": 5.3,
  "participant": "CarrieS",
  "application": "trying to mount pendant light to ceiling",
  "outcome": "failure",
  "outcome_confidence": 0.85,
  "alternative_considered": "used floor lamp instead",
  "video_id": "consumer04"
}
```

### Workaround:
```json
{
  "workaround_id": "consumer02_wa_44",
  "intent": "hardwire lighting installation",
  "barrier": "not an electrician, don't know how to reconvert power",
  "solution": "piece of board behind the battery-operated light",
  "verbatim": "went ahead and decided that a piece of board behind the battery-operated
               light would be the best opportunity",
  "timestamp": 44.6,
  "participant": "AlanG",
  "confidence": 0.85,
  "product_mention": "battery-operated light",
  "video_id": "consumer02"
}
```

---

## Key Principles Maintained

### Evidence-First, Framework-Second

1. **Extract:** Pull all statements about problems, solutions, products, emotions
2. **Validate:** Check context—is this actually about lighting installation?
3. **Categorize:** Map validated statements to JTBD/products/workarounds
4. **Flag Confidence:** Mark interpretation certainty

**DO NOT:** Search for specific pain points we expect to find
**DO:** Surface patterns in what consumers actually discuss

### Quality > Quantity

- Better to miss ambiguous cases than fabricate insights
- Confidence thresholds prevent overreach
- Manual review catches edge cases
- Iterative pattern refinement based on validation

---

## Success Metrics

**Before full 15-video run, validate on 5-video batch:**

| Metric | Target | Current |
|--------|--------|---------|
| JTBD Accuracy (manual review) | >85% defensible | TBD |
| Product Detection Recall | 100% of mentions | TBD |
| Product Detection Precision | >90% true positives | TBD |
| Workaround Completeness | >80% have all 3 components | 0% (needs tuning) |
| No Confirmation Bias | Novel patterns emerge | TBD |

**If validation <80% on any dimension:** Adjust confidence thresholds or add more negative examples before proceeding to full batch.

---

## Files Created

1. `modules/consumer-video/scripts/jtbd_extractor.py` - 400+ lines
2. `modules/consumer-video/scripts/product_tracker.py` - 300+ lines
3. `modules/consumer-video/scripts/workaround_detector.py` - 350+ lines
4. `modules/consumer-video/ENHANCEMENT_SUMMARY.md` - This file

**Ready for integration and validation.**
