# MECE Validation Checklist

Use this checklist to ensure your job framework is **Mutually Exclusive, Collectively Exhaustive**.

---

## Part 1: Mutual Exclusivity Testing

**Goal:** Ensure no job overlaps with another job in core intent.

### Test Procedure

For each pair of jobs, ask:

**"Can someone be doing Job A and Job B simultaneously for the SAME progress?"**

- **If YES** → Jobs overlap, need refinement
- **If NO** → Likely mutually exclusive

### Pairwise Comparison Matrix

|           | Job 1 | Job 2 | Job 3 | Job 4 | Job 5 |
|-----------|-------|-------|-------|-------|-------|
| **Job 1** |   -   |       |       |       |       |
| **Job 2** |   ✓   |   -   |       |       |       |
| **Job 3** |   ✓   |   ✓   |   -   |       |       |
| **Job 4** |   ✓   |   ✓   |   ✓   |   -   |       |
| **Job 5** |   ✓   |   ✓   |   ✓   |   ✓   |   -   |

✓ = Mutually exclusive (no overlap)
❌ = Overlap detected (needs refinement)

### Detailed Pairwise Analysis

**Job 1 vs. Job 2:**
- Can someone be doing both for the same progress? [Yes/No]
- If overlap detected, what is it? [Description]
- Resolution: [Merge / Refine boundaries / One is sub-component of other]

**Job 1 vs. Job 3:**
- Can someone be doing both for the same progress? [Yes/No]
- If overlap detected, what is it? [Description]
- Resolution: [Merge / Refine boundaries / One is sub-component of other]

[Continue for all pairs...]

---

## Part 2: Collective Exhaustiveness Testing

**Goal:** Ensure all observed behaviors/outcomes map to at least one job.

### Coverage Analysis

**Total data points in dataset:** [N]

**Mapped to jobs:**
- Job 1: [N] data points
- Job 2: [N] data points
- Job 3: [N] data points
- Job 4: [N] data points
- Job 5: [N] data points

**Total mapped:** [N]

**Coverage percentage:** [%]

**Target:** ≥95% coverage (100% ideal)

### Orphan Signal Analysis

**Orphan signals:** Data points that don't fit any job

| Signal | Description | Count | % of Total |
|--------|-------------|-------|------------|
| [Signal 1] | [What it represents] | [N] | [%] |
| [Signal 2] | [What it represents] | [N] | [%] |

**For each orphan signal, determine:**

1. **Is this a missing job?**
   - If ≥4 unique consumers and represents distinct progress → Create new job

2. **Is this an edge case?**
   - If <5% of data → Can ignore

3. **Is this misclassified?**
   - Should it actually map to an existing job? Which one?

4. **Is this NOT a job?**
   - Is it an acquisition method, constraint, or success criterion?

**Resolution:**
- [ ] Missing job identified: [New job name]
- [ ] Edge case, can ignore (<5% of data)
- [ ] Remap to existing job: [Job number]
- [ ] Not a job (constraint/method/criterion)

---

## Part 3: Abstraction Level Validation

**Goal:** Ensure jobs are at the right level — not too specific, not too broad.

### Not-Too-Specific Test

**Question:** Does the job mention specific products, brands, or methods?

**Examples of TOO SPECIFIC:**
- ❌ "Buy a drill"
- ❌ "Use an LED strip light"
- ❌ "Install battery-powered lighting"

**Your jobs:**
- Job 1: [Pass/Fail] - [Reason]
- Job 2: [Pass/Fail] - [Reason]
- Job 3: [Pass/Fail] - [Reason]
- Job 4: [Pass/Fail] - [Reason]
- Job 5: [Pass/Fail] - [Reason]

### Not-Too-Broad Test

**Question:** Is the job so broad it could apply to any category?

**Examples of TOO BROAD:**
- ❌ "Be successful"
- ❌ "Improve my life"
- ❌ "Save time"

**Your jobs:**
- Job 1: [Pass/Fail] - [Reason]
- Job 2: [Pass/Fail] - [Reason]
- Job 3: [Pass/Fail] - [Reason]
- Job 4: [Pass/Fail] - [Reason]
- Job 5: [Pass/Fail] - [Reason]

### Solution-Agnostic Test

**Question:** Can this job be accomplished with multiple different solutions?

**Your jobs:**
- Job 1: [List 3+ different solutions]
- Job 2: [List 3+ different solutions]
- Job 3: [List 3+ different solutions]
- Job 4: [List 3+ different solutions]
- Job 5: [List 3+ different solutions]

**If you can't list 3+ solutions → Job may be too specific or solution-focused.**

---

## Part 4: Job vs. Non-Job Differentiation

**Goal:** Ensure you haven't confused jobs with acquisition methods, constraints, or success criteria.

### Acquisition Method Test

**Question:** Is this how they solve a job, rather than the job itself?

**Examples of ACQUISITION METHODS (NOT JOBS):**
- ❌ "DIY installation"
- ❌ "Hire a professional"
- ❌ "Buy online"

**Your jobs:**
- Job 1: [Is this HOW they solve it?] [Pass/Fail]
- Job 2: [Is this HOW they solve it?] [Pass/Fail]
- Job 3: [Is this HOW they solve it?] [Pass/Fail]
- Job 4: [Is this HOW they solve it?] [Pass/Fail]
- Job 5: [Is this HOW they solve it?] [Pass/Fail]

### Constraint/Barrier Test

**Question:** Is this an obstacle in the way, rather than progress sought?

**Examples of CONSTRAINTS (NOT JOBS):**
- ❌ "Avoid electrical work"
- ❌ "Stay within budget"
- ❌ "Work around existing infrastructure"

**Your jobs:**
- Job 1: [Is this a barrier?] [Pass/Fail]
- Job 2: [Is this a barrier?] [Pass/Fail]
- Job 3: [Is this a barrier?] [Pass/Fail]
- Job 4: [Is this a barrier?] [Pass/Fail]
- Job 5: [Is this a barrier?] [Pass/Fail]

### Success Criterion Test

**Question:** Is this how they judge quality, rather than the outcome?

**Examples of SUCCESS CRITERIA (NOT JOBS):**
- ❌ "Make it look professional"
- ❌ "Ensure it's level"
- ❌ "Match existing decor"

**Your jobs:**
- Job 1: [Is this a quality standard?] [Pass/Fail]
- Job 2: [Is this a quality standard?] [Pass/Fail]
- Job 3: [Is this a quality standard?] [Pass/Fail]
- Job 4: [Is this a quality standard?] [Pass/Fail]
- Job 5: [Is this a quality standard?] [Pass/Fail]

---

## Part 5: Final MECE Validation

### Summary Checklist

- [ ] All job pairs tested for mutual exclusivity
- [ ] No overlaps detected (or resolved if found)
- [ ] Coverage ≥95% (all data maps to jobs)
- [ ] Orphan signals analyzed and resolved
- [ ] All jobs pass abstraction level tests (not too specific/broad)
- [ ] All jobs are solution-agnostic
- [ ] No acquisition methods disguised as jobs
- [ ] No constraints/barriers disguised as jobs
- [ ] No success criteria disguised as jobs
- [ ] Job count: 4-7 (ideal range)

### MECE Certification

**I certify that this job framework is:**

✅ **Mutually Exclusive:** No job overlaps with another in core intent

✅ **Collectively Exhaustive:** All observed outcomes map to at least one job

✅ **Validated:** All tests passed

**Analyst Name:** [Your name]
**Date:** [Date]
**Framework:** [Category/Product]

---

## Refinement Log

**If MECE violations found, document refinements:**

### Iteration 1
**Issue:** [Description of overlap or gap]
**Resolution:** [What you changed]
**Result:** [Pass/Fail]

### Iteration 2
**Issue:** [Description of overlap or gap]
**Resolution:** [What you changed]
**Result:** [Pass/Fail]

[Continue as needed...]

---

**Use this checklist to ensure rigorous MECE compliance before finalizing your job framework.**
