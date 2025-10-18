# Expert Review Guide: JTBD Analyst Skill

**For:** Frontier LLM peer reviewers (Claude Opus, GPT-4, Gemini Ultra, etc.)
**Version:** 1.0.0
**Review Type:** Methodology validation, enhancement suggestions, edge case identification
**Framework:** Clayton Christensen Jobs-to-be-Done

---

## Review Objectives

This skill is designed for expert-level JTBD analysis on qualitative consumer research. Your review should assess:

1. **Methodology Rigor:** Does the 8-step process align with Christensen's framework?
2. **MECE Compliance:** Are validation procedures sufficient?
3. **Practical Applicability:** Can this skill handle real-world datasets?
4. **Output Quality:** Do deliverables meet enterprise standards?
5. **Edge Cases:** What scenarios might break or challenge this skill?

---

## Review Structure

### Phase 1: Framework Compliance Review
**Estimated Time:** 30 minutes

Read SKILL.md and assess:

#### 1.1 Core JTBD Principles
- [ ] Definition of "job" aligns with Christensen (progress in context, not task/solution)
- [ ] Three dimensions (functional, emotional, social) properly explained
- [ ] Solution-agnostic principle clearly articulated
- [ ] Distinction from needs, solutions, features is clear

**Assessment:** [Pass / Needs Refinement]

**Notes:**
[Your observations on framework alignment]

**Suggested Enhancements:**
[Specific improvements to core principles section]

---

#### 1.2 Job Statement Format
- [ ] "When... I want to... So I can..." format matches Christensen standard
- [ ] Component explanations (circumstance, motivation, outcome) are clear
- [ ] Examples demonstrate proper abstraction level
- [ ] Common mistakes (too broad, too specific) are addressed

**Assessment:** [Pass / Needs Refinement]

**Notes:**
[Your observations on job statement guidance]

**Suggested Enhancements:**
[Improvements to format specification]

---

#### 1.3 MECE Requirements
- [ ] Mutual exclusivity testing procedure is rigorous
- [ ] Collective exhaustiveness verification is thorough
- [ ] Abstraction level balance guidance is practical
- [ ] Edge cases (overlapping jobs, orphan signals) are addressed

**Assessment:** [Pass / Needs Refinement]

**Notes:**
[Your observations on MECE methodology]

**Critical Question:** Can you identify a scenario where the MECE testing would fail to catch overlap?

**Suggested Enhancements:**
[Improvements to MECE validation]

---

### Phase 2: Methodology Review
**Estimated Time:** 45 minutes

Evaluate the 8-step analysis process:

#### 2.1 Data Preparation & Immersion (Step 1)
- [ ] Data source characteristics checklist is comprehensive
- [ ] Initial scan criteria cover key indicators
- [ ] Minimum data requirements (20 consumers) are justified

**Assessment:** [Pass / Needs Refinement]

**Edge Case Identified:**
[What happens with <20 consumers? What if data quality is poor?]

**Suggested Enhancements:**
[Improvements to data prep stage]

---

#### 2.2 Signal Extraction (Step 2)
- [ ] Four signal types (circumstantial, motivation, outcome, dimensional) are comprehensive
- [ ] Extraction guidance is practical for LLM implementation
- [ ] Examples help clarify what to look for

**Assessment:** [Pass / Needs Refinement]

**Edge Case Identified:**
[What if signals are implicit rather than explicit? How to handle ambiguous language?]

**Suggested Enhancements:**
[Improvements to signal extraction]

---

#### 2.3 Pattern Identification (Step 3)
- [ ] Clustering approach (circumstance & outcome) is sound
- [ ] Cross-referencing methodology is clear
- [ ] Guidance on identifying patterns vs. noise is adequate

**Assessment:** [Pass / Needs Refinement]

**Edge Case Identified:**
[What if patterns are weak or contradictory?]

**Suggested Enhancements:**
[Improvements to pattern identification]

---

#### 2.4 Job Candidate Generation (Step 4)
- [ ] Process for creating initial candidates (8-12) is clear
- [ ] Evidence requirements (4+ consumers) are justified
- [ ] Documentation standards are sufficient

**Assessment:** [Pass / Needs Refinement]

**Edge Case Identified:**
[What if no jobs meet 4+ consumer threshold?]

**Suggested Enhancements:**
[Improvements to candidate generation]

---

#### 2.5 MECE Refinement (Step 5)
- [ ] Testing procedure for mutual exclusivity is rigorous
- [ ] Collective exhaustiveness verification is thorough
- [ ] Guidance on merging/splitting jobs is clear
- [ ] Distinction from sub-jobs, methods, constraints is explained

**Assessment:** [Pass / Needs Refinement]

**Critical Question:** How does the skill handle jobs that are legitimately correlated but not overlapping?

**Suggested Enhancements:**
[Improvements to refinement process]

---

#### 2.6 Final Job Framework (Step 6)
- [ ] Convergence to 4-7 jobs is justified
- [ ] Final validation criteria are comprehensive
- [ ] Quality bar is appropriate

**Assessment:** [Pass / Needs Refinement]

**Edge Case Identified:**
[What if 8+ jobs all meet quality criteria? Force merge or allow?]

**Suggested Enhancements:**
[Improvements to final framework stage]

---

#### 2.7 Consumer Insight Development (Step 7)
- [ ] P&G CMK format is correctly specified
- [ ] WHO + WHERE + WHAT + EMOTION + TENSION + MOTIVATION structure is clear
- [ ] Examples demonstrate proper execution

**Assessment:** [Pass / Needs Refinement]

**Note:** P&G CMK is a specific framework. Is this too prescriptive, or should skill offer alternative insight formats?

**Suggested Enhancements:**
[Alternative formats or improvements]

---

#### 2.8 Prioritization Framework (Step 8)
- [ ] 2x2 matrix (commonality × pain) is appropriate
- [ ] Quadrant definitions are actionable
- [ ] Pain level scoring guidance is calibrated

**Assessment:** [Pass / Needs Refinement]

**Alternative Approach:** Should the skill also support Ulwick's ODI prioritization (importance × satisfaction)?

**Suggested Enhancements:**
[Improvements to prioritization]

---

### Phase 3: Output Specification Review
**Estimated Time:** 20 minutes

Assess deliverable specifications:

#### 3.1 Deliverable 1: Executive Summary
- [ ] One-page format is practical
- [ ] Key elements (jobs table, findings, priorities) are appropriate
- [ ] Methodology note provides adequate transparency

**Assessment:** [Pass / Needs Refinement]

**Suggested Enhancements:**

---

#### 3.2 Deliverable 2: Full Job Framework
- [ ] Job template is comprehensive
- [ ] Evidence requirements are clear
- [ ] Verbatim citation standards are rigorous

**Assessment:** [Pass / Needs Refinement]

**Suggested Enhancements:**

---

#### 3.3 Deliverable 3: MECE Validation Report
- [ ] Validation checks are thorough
- [ ] Transparency requirements are appropriate
- [ ] Audit trail supports peer review

**Assessment:** [Pass / Needs Refinement]

**Suggested Enhancements:**

---

### Phase 4: Quality Criteria Review
**Estimated Time:** 15 minutes

Evaluate the quality checklist:

#### 4.1 Job Statement Quality
- [ ] 5 criteria are sufficient
- [ ] Criteria are measurable/verifiable

**Missing Criteria:**
[Any quality dimensions not covered?]

---

#### 4.2 Evidence Sufficiency
- [ ] 4 criteria are sufficient
- [ ] Minimum thresholds (4 consumers) are justified

**Question:** Should the skill require evidence from multiple data collection methods (triangulation)?

---

#### 4.3 Dimensional Coverage
- [ ] Functional, emotional, social coverage requirements are clear
- [ ] Primary dimension identification is useful

**Suggested Enhancement:**

---

#### 4.4 MECE Compliance
- [ ] 3 criteria are sufficient
- [ ] Testing procedures are linked

**Suggested Enhancement:**

---

#### 4.5 Differentiation Clarity
- [ ] 4 criteria distinguish jobs from non-jobs
- [ ] Examples are helpful

**Edge Case:** What about jobs that ARE acquisition methods in certain contexts (e.g., "install it myself for the satisfaction of DIY")?

---

### Phase 5: Common Pitfalls Review
**Estimated Time:** 10 minutes

Assess the 6 pitfalls:

- [ ] Pitfall 1 (confusing with solutions): Clear and helpful
- [ ] Pitfall 2 (too broad): Clear and helpful
- [ ] Pitfall 3 (too narrow): Clear and helpful
- [ ] Pitfall 4 (confusing with constraints): Clear and helpful
- [ ] Pitfall 5 (mixing with success criteria): Clear and helpful
- [ ] Pitfall 6 (overlapping jobs): Clear and helpful

**Missing Pitfalls:**
[Any common errors not addressed?]

**Suggested Additions:**
1. [Pitfall 7 idea]
2. [Pitfall 8 idea]

---

### Phase 6: Progressive Disclosure Review
**Estimated Time:** 10 minutes

Evaluate chunked analysis strategy:

- [ ] 4-phase approach (sample → expansion → synthesis → validation) is sound
- [ ] Sample size (20 consumers) for Phase 1 is appropriate
- [ ] Strategy handles large datasets (100+ consumers) effectively

**Edge Case:** How does this work with continuous data collection (rolling analysis)?

**Suggested Enhancements:**

---

### Phase 7: Real-World Application Review
**Estimated Time:** 30 minutes

Read EXAMPLES.md and assess:

#### 7.1 Example Quality
- [ ] Consumer lighting example demonstrates methodology effectively
- [ ] All 8 steps are visible in the execution
- [ ] Challenges/pivots are documented (validation issue, hybrid approach)

**Assessment:** [Pass / Needs Refinement]

---

#### 7.2 Output Quality
- [ ] 5 jobs identified are properly formatted
- [ ] MECE structure is validated
- [ ] Evidence meets quality standards
- [ ] Prioritization is data-driven

**Critical Review:** Do you agree with the 5-job structure? Are there overlaps or gaps?

**Your Assessment:**
[Detailed analysis of the 5 jobs from the lighting example]

---

#### 7.3 Lessons Learned
- [ ] "What worked" insights are valuable
- [ ] "What didn't work" transparency is helpful
- [ ] Key insights generalize beyond this example

**Additional Lessons:**
[What else should future analysts learn from this example?]

---

### Phase 8: Template Review
**Estimated Time:** 20 minutes

Evaluate templates in TEMPLATES/ folder:

#### 8.1 Job Statement Template
- [ ] Comprehensive and easy to follow
- [ ] Quality checklist is practical
- [ ] Pitfall examples are clear

**Suggested Improvements:**

---

#### 8.2 MECE Validation Checklist
- [ ] Pairwise comparison matrix is thorough
- [ ] Orphan signal analysis is well-structured
- [ ] Abstraction level tests are practical

**Suggested Improvements:**

---

#### 8.3 Prioritization Matrix Template
- [ ] 2x2 matrix is clearly explained
- [ ] Pain level calibration guide is useful
- [ ] Implications by function provide actionable guidance

**Suggested Improvements:**

---

## Overall Assessment

### Strengths

**Top 3 Strengths:**
1. [Strength 1]
2. [Strength 2]
3. [Strength 3]

---

### Weaknesses

**Top 3 Weaknesses:**
1. [Weakness 1]
2. [Weakness 2]
3. [Weakness 3]

---

### Critical Gaps

**What's Missing:**
1. [Gap 1: What the skill doesn't address but should]
2. [Gap 2]
3. [Gap 3]

---

### Edge Cases & Failure Modes

**Scenarios Where This Skill Might Fail:**

1. **Edge Case 1:** [Description]
   - **Why it fails:** [Explanation]
   - **Suggested fix:** [Solution]

2. **Edge Case 2:** [Description]
   - **Why it fails:** [Explanation]
   - **Suggested fix:** [Solution]

3. **Edge Case 3:** [Description]
   - **Why it fails:** [Explanation]
   - **Suggested fix:** [Solution]

---

### Enhancement Recommendations

**Priority 1 (Must Add):**
1. [Enhancement 1]
   - **Why:** [Rationale]
   - **How:** [Implementation approach]

2. [Enhancement 2]
   - **Why:** [Rationale]
   - **How:** [Implementation approach]

**Priority 2 (Should Add):**
1. [Enhancement]
2. [Enhancement]

**Priority 3 (Nice to Have):**
1. [Enhancement]
2. [Enhancement]

---

### Framework Extensions

**Integration Opportunities:**

1. **Tony Ulwick's ODI (Outcome-Driven Innovation):**
   - [How to integrate]
   - [What value it adds]

2. **Bob Moesta's Forces of Progress:**
   - [How to integrate]
   - [What value it adds]

3. **Other frameworks:**
   - [Framework name]
   - [Integration approach]

---

### Comparison to Alternative Approaches

**How does this skill compare to:**

1. **Traditional user research methods:**
   - [Comparison]
   - [Advantages/disadvantages]

2. **Quantitative JTBD surveys (Ulwick ODI):**
   - [Comparison]
   - [When to use each]

3. **Switch interview methodology (Moesta):**
   - [Comparison]
   - [Complementary or overlapping?]

---

## Certification

**Reviewer:** [Your model name/version]
**Date:** [Review date]
**Review Duration:** [Total time spent]

**Overall Rating:** [1-10]

**Recommendation:**
- [ ] Ready for production use as-is
- [ ] Ready with minor refinements (Priority 3 enhancements)
- [ ] Needs important updates (Priority 2 enhancements)
- [ ] Requires critical fixes (Priority 1 enhancements)

**Signature/Model ID:** [Your identifier]

---

## Appendix: Reviewer Self-Assessment

**Your Expertise in JTBD:**
- [ ] Expert (deep knowledge of Christensen, Ulwick, Moesta)
- [ ] Proficient (familiar with core concepts and applications)
- [ ] Competent (understand basics, some application experience)
- [ ] Learning (reviewing to deepen understanding)

**Your Expertise in Qualitative Research:**
- [ ] Expert (extensive experience with qual analysis methods)
- [ ] Proficient (solid foundation in qual research)
- [ ] Competent (some qual research experience)
- [ ] Learning (limited qual experience)

**Potential Biases:**
[Any biases or perspectives that might influence your review]

**Areas of Uncertainty:**
[Aspects of this skill where you lack confidence in your assessment]

---

## Review Submission

**Please submit your review to:** [Project contact]

**Expected Output Format:**
- Completed review guide (this document)
- Annotated SKILL.md with inline comments (optional)
- Revised sections (if you're proposing major changes)
- Example edge cases with test data (if applicable)

**Thank you for contributing to the quality and rigor of this JTBD analysis skill!**
