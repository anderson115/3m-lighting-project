# Clayton Christensen Jobs-to-be-Done Expert Analyst

**Version:** 1.0.0
**Created:** October 17, 2025
**Framework:** Clayton Christensen JTBD Methodology
**Skill Type:** Qualitative Research Analysis → MECE Job Framework Generation

---

## Skill Metadata

```yaml
name: JTBD Expert Analyst
version: 1.0.0
framework: Clayton Christensen Jobs-to-be-Done
purpose: Analyze open-ended consumer responses to identify mutually exclusive, collectively exhaustive (MECE) jobs
input_types:
  - Transcripts (interview, video, audio)
  - Open-ended survey responses
  - Customer feedback
  - Behavioral observations
  - Contextual inquiry data
output_types:
  - MECE job framework (4-7 core jobs)
  - Job statements in Christensen format
  - Consumer insights
  - Evidence mapping
  - Prioritization recommendations
requirements:
  - Minimum 20 unique consumer data points
  - Context-rich qualitative data
  - Behavioral observation (what people DO, not just say)
progressive_disclosure: true
context_window_strategy: chunked_analysis_with_synthesis
```

---

## Core JTBD Principles (Christensen Framework)

### Definition of a "Job"

A **job** is **the progress a person wants to achieve under specific circumstances**.

**NOT:**
- ❌ A task or activity
- ❌ A product feature
- ❌ A demographic segment
- ❌ A universal need
- ❌ A specific solution

**IS:**
- ✅ Progress sought in a specific context
- ✅ Outcome-focused (what success looks like)
- ✅ Solution-agnostic (doesn't prescribe HOW)
- ✅ Stable over time
- ✅ Multi-dimensional (functional + emotional + social)

---

## Job Statement Format (Christensen Standard)

```
When [CIRCUMSTANCE/SITUATION],
I want to [MOTIVATION/PROGRESS SOUGHT],
So I can [DESIRED OUTCOME].
```

### Components Explained

1. **WHEN (Circumstance):** Specific context, triggering event, or situation
   - Time-based, location-based, or state-based
   - Example: "When I'm commuting to work by car in the morning"

2. **I WANT TO (Motivation):** The progress or change sought
   - Solution-agnostic verb + object
   - Focus on progress, not product
   - Example: "eat something that doesn't distract me from driving"

3. **SO I CAN (Outcome):** The end benefit or desired state
   - Why this progress matters
   - Includes functional, emotional, social dimensions
   - Example: "work until lunch without feeling hungry"

---

## Three Dimensions of Progress

Every job has three interconnected dimensions:

### 1. Functional Dimension
- **What:** The task or objective progress
- **Question:** "What are they trying to accomplish?"
- **Example:** Get from point A to B, find information, complete a transaction

### 2. Emotional Dimension
- **What:** How they want to feel
- **Question:** "How do they want to feel during and after?"
- **Example:** Feel confident, avoid anxiety, experience delight, maintain control

### 3. Social Dimension
- **What:** How they want to be perceived
- **Question:** "What do they want others to think about them?"
- **Example:** Signal competence, demonstrate status, show care, maintain identity

**Critical:** All three dimensions must be considered, even if one dominates.

---

## MECE Requirements (Mutually Exclusive, Collectively Exhaustive)

### Mutually Exclusive (No Overlap)
- Each job represents a DISTINCT progress/outcome
- Jobs should not overlap in their core intent
- Test: "Can someone be doing Job A and Job B simultaneously for the SAME progress?"
  - If YES → jobs overlap, need refinement
  - If NO → likely mutually exclusive

### Collectively Exhaustive (Complete Coverage)
- All observed behaviors/outcomes map to at least one job
- No "orphan" data points that don't fit anywhere
- Test: "Does every consumer signal in the data fit into one of these jobs?"
  - If NO → missing job categories

### Abstraction Level Balance
- Not too specific (product-level): ❌ "Buy a milkshake"
- Not too broad (universal need): ❌ "Satisfy hunger"
- Just right (contextual progress): ✅ "Fill time during boring commute with something I can consume while driving"

---

## Analysis Methodology

### STEP 1: Data Preparation & Immersion
1. **Load all qualitative data** (transcripts, responses, observations)
2. **Identify data source characteristics:**
   - Number of unique consumers
   - Data richness (context depth)
   - Behavioral vs. attitudinal data
   - Temporal coverage (snapshot vs. longitudinal)

3. **Initial scan for:**
   - Circumstances/contexts mentioned
   - Verbs indicating progress sought
   - Outcomes/benefits described
   - Emotional language
   - Social signals

### STEP 2: Signal Extraction
Extract **progress indicators** from data:

**A. Circumstantial Signals**
- "When I..." statements
- Context descriptions (time, place, state)
- Triggering events or situations

**B. Motivation Signals**
- "I wanted to..." / "I was trying to..."
- Goals mentioned
- Problems being solved
- Frustrations expressed

**C. Outcome Signals**
- "So I can..." / "So that..."
- Benefits described
- Success criteria mentioned
- Desired end states

**D. Dimensional Evidence**
- **Functional:** Task completion, efficiency, effectiveness
- **Emotional:** Feelings, anxieties, desires, relief
- **Social:** Others' perceptions, identity, status

### STEP 3: Pattern Identification
Look for **recurring patterns** across consumers:

1. **Circumstance Clustering:**
   - What similar contexts appear repeatedly?
   - What triggers the same progress-seeking behavior?

2. **Outcome Clustering:**
   - What similar end states are people seeking?
   - What types of progress recur?

3. **Cross-Reference:**
   - Which circumstances lead to which outcomes?
   - Are there distinct circumstance→outcome patterns?

### STEP 4: Job Candidate Generation
Create **initial job candidates** (typically 8-12):

For each pattern:
1. Write preliminary job statement in Christensen format
2. Identify evidence supporting this job (minimum 4 unique consumers)
3. Note functional, emotional, social dimensions
4. Document specific verbatim examples

### STEP 5: MECE Refinement
**Test for Mutual Exclusivity:**
1. Compare each pair of job candidates
2. Identify overlaps in intent/outcome
3. Merge or refine jobs that overlap
4. Distinguish true jobs from:
   - Sub-dimensions of another job
   - Acquisition methods (HOW they get the job done)
   - Constraints/barriers (obstacles to the job)
   - Success criteria (quality standards)

**Test for Collective Exhaustiveness:**
1. Map all data signals to jobs
2. Identify "orphan" signals
3. Determine if orphans represent:
   - A missing job (create new job)
   - Edge cases (can ignore if <5% of data)
   - Misclassified signals (remap to existing jobs)

### STEP 6: Final Job Framework
Converge on **4-7 core jobs**:

- **4 jobs:** Highly consolidated, high-level categories
- **5-6 jobs:** Sweet spot for most categories
- **7 jobs:** Maximum before becoming unwieldy

Each final job must have:
- ✅ Clean Christensen-format statement
- ✅ 4+ unique consumers as evidence
- ✅ Functional, emotional, social dimensions documented
- ✅ Verbatim quotes with citations
- ✅ Clear differentiation from other jobs

### STEP 7: Consumer Insight Development
For each job, create **behavioral consumer insight**:

**Format (P&G CMK Style):**
```
[WHO] + [WHERE/WHEN] + [WHAT THEY DO] + [EMOTION] + [TENSION] + [MOTIVATION]
```

**Example:**
"Commuters stuck in traffic (WHO) sit in their cars during boring morning drives (WHERE/WHEN), looking for something to fill the time that won't distract them from driving (WHAT THEY DO). They feel frustrated by the tedium and want to arrive at work energized (EMOTION). Without the right solution, they either arrive hungry or waste time with something unsatisfying (TENSION). They need a convenient, engaging option that provides both sustenance and entertainment without requiring attention (MOTIVATION)."

### STEP 8: Prioritization Framework
Create **2x2 prioritization matrix:**

**X-Axis:** Commonality (% of consumers experiencing this job)
**Y-Axis:** Pain Level (intensity of frustration/importance)

**Quadrants:**
1. **Must Solve:** High commonality + High pain
2. **Important:** High on one dimension
3. **Strategic:** Lower on both dimensions
4. **Niche:** Very low commonality (may still be high-value)

---

## Output Specification

### Deliverable 1: Executive Summary (One-Page)

**Structure:**
1. **Framework Overview** (2-3 sentences)
2. **The [N] Core Jobs** (table format):
   - Job name
   - Job statement
   - Commonality %
   - Pain level
   - Priority quadrant
3. **Key Finding** (1-2 top insights)
4. **Strategic Priorities** (by quadrant)
5. **Methodology Note** (data source, framework, validation)

### Deliverable 2: Full Job Framework

**For Each Job:**

```markdown
## JOB [N]: [Job Name]

**Job Statement:**
When [circumstance],
I want to [motivation],
So I can [outcome].

**Evidence:**
- Unique consumers: [N] ([%] of total)
- Total signals: [N]
- Video/Response IDs: [list]

**Dimensions:**

**Functional:**
[What task/progress they're trying to accomplish]

**Emotional:**
[How they want to feel / avoid feeling]

**Social:**
[How they want to be perceived by others]

**Consumer Insight:**
[WHO] + [WHERE/WHEN] + [WHAT THEY DO] + [EMOTION] + [TENSION] + [MOTIVATION]

**Verbatim Evidence (Sample):**
1. [Consumer ID]: "[Quote showing circumstance and motivation]"
2. [Consumer ID]: "[Quote showing desired outcome]"
3. [Consumer ID]: "[Quote showing emotional/social dimension]"
[... 5-10 total quotes]

**Prioritization:**
- Commonality: [%]
- Pain Level: [/100]
- Quadrant: [Must Solve / Important / Strategic / Niche]
```

### Deliverable 3: MECE Validation Report

**Structure:**
1. **Mutual Exclusivity Check:**
   - Job pair comparison matrix
   - Overlap identification
   - Refinement justification

2. **Collective Exhaustiveness Check:**
   - Coverage percentage
   - Orphan signal analysis
   - Edge case handling

3. **Abstraction Level Validation:**
   - Not-too-specific test
   - Not-too-broad test
   - Solution-agnostic test

---

## Quality Criteria Checklist

Every job must pass ALL criteria:

### ✅ Job Statement Quality
- [ ] Uses "When... I want to... So I can..." format
- [ ] Circumstance is specific and observable
- [ ] Motivation is solution-agnostic (no product mentions)
- [ ] Outcome describes progress/benefit, not just completion
- [ ] Statement is 1-3 sentences, not overly complex

### ✅ Evidence Sufficiency
- [ ] Minimum 4 unique consumers
- [ ] Verbatim quotes with source citations
- [ ] Cross-validation from multiple data types (if available)
- [ ] Behavioral evidence (what they DO), not just attitudinal (what they SAY)

### ✅ Dimensional Coverage
- [ ] Functional dimension clearly documented
- [ ] Emotional dimension identified (even if secondary)
- [ ] Social dimension considered (even if absent)
- [ ] Primary dimension identified

### ✅ MECE Compliance
- [ ] No overlap with other jobs (mutual exclusivity)
- [ ] All data maps to at least one job (collective exhaustiveness)
- [ ] Appropriate abstraction level (not product, not universal need)

### ✅ Differentiation Clarity
- [ ] Not an acquisition method (HOW they solve it)
- [ ] Not a constraint/barrier (obstacle in the way)
- [ ] Not a success criterion (quality standard)
- [ ] True progress/outcome (what they're trying to achieve)

---

## Common Pitfalls to Avoid

### ❌ PITFALL 1: Confusing Jobs with Solutions
**Wrong:** "Buy a drill"
**Right:** "Make a hole to hang something"

**How to Fix:** Ask "Why?" repeatedly until you reach the progress sought

### ❌ PITFALL 2: Jobs That Are Too Broad
**Wrong:** "Be successful"
**Right:** "Demonstrate competence to my new team in first 90 days"

**How to Fix:** Add specific circumstances and context

### ❌ PITFALL 3: Jobs That Are Too Narrow
**Wrong:** "Print a document on an HP LaserJet"
**Right:** "Share information in a format others can review offline"

**How to Fix:** Abstract one level up from the specific product/method

### ❌ PITFALL 4: Confusing Jobs with Constraints
**Wrong:** "Install it myself without hiring someone"
**Right:** "Complete the project on my timeline without external dependencies"

**Distinction:** Constraints are barriers; jobs are outcomes

### ❌ PITFALL 5: Mixing Functional Jobs with Success Criteria
**Wrong:** "Make it look professional"
**Right:** "Complete installation in a way that signals competence"

**Distinction:** "Look professional" is HOW you judge success; the job is demonstrating competence

### ❌ PITFALL 6: Creating Jobs That Overlap
**Overlap Example:**
- Job A: "Showcase my artwork"
- Job B: "Make my home feel complete"

**Why It's a Problem:** Showcasing artwork COULD be a way to make home feel complete

**How to Fix:** Determine if one is a sub-component of the other, or if they represent different core outcomes

---

## Progressive Disclosure Strategy

Given large datasets (50+ consumers, 100+ pages of transcripts), use **chunked analysis**:

### Phase 1: Sample Analysis (First 20 consumers)
- Identify initial job candidates
- Establish pattern recognition criteria
- Create coding framework

### Phase 2: Expansion (Next 30 consumers)
- Validate initial jobs
- Identify new patterns
- Refine job statements

### Phase 3: Synthesis (Remaining data)
- Confirm job prevalence
- Finalize MECE structure
- Extract comprehensive verbatims

### Phase 4: Cross-Validation
- Map all data to final jobs
- Verify MECE compliance
- Strengthen evidence base

---

## Expert Review Preparation

This skill is designed for peer review by expert frontier LLMs. When preparing output for review, include:

### 1. Methodology Transparency
- Data characteristics (N, source, richness)
- Analysis approach (systematic vs. interpretive)
- Coding framework (if used)
- Analyst decisions and rationale

### 2. Evidence Chain
- Raw data → Signal → Pattern → Job candidate → Final job
- Traceability from verbatim to job statement
- Alternative interpretations considered

### 3. MECE Justification
- Mutual exclusivity testing results
- Collective exhaustiveness verification
- Abstraction level calibration

### 4. Limitations & Confidence
- Data gaps or biases identified
- Low-confidence jobs flagged
- Suggested areas for deeper inquiry

---

## Skill Invocation

To use this skill, provide:

**Required:**
1. Qualitative consumer data (transcripts, responses, observations)
2. Number of unique consumers in dataset
3. Category/product context

**Optional but Recommended:**
4. Specific research questions or hypotheses
5. Existing frameworks or taxonomies to validate against
6. Minimum job count preference (default: 4-6)
7. Output format preference (markdown, JSON, HTML)

**Example Invocation:**

```
I have transcripts from 79 consumer videos about lighting installation.
Please analyze these using the Clayton Christensen JTBD framework to identify
4-6 core functional jobs that are mutually exclusive and collectively exhaustive.

Provide:
1. Job statements in "When... I want to... So I can..." format
2. Consumer insights for each job
3. MECE validation
4. Prioritization matrix (commonality vs. pain)
5. Evidence with verbatim citations

Data: [attach transcripts or provide file paths]
```

---

## Skill Maintenance & Updates

**Version History:**
- v1.0.0 (Oct 2025): Initial comprehensive JTBD analyst skill based on Christensen methodology

**Planned Enhancements:**
- Integration with Tony Ulwick's ODI (Outcome-Driven Innovation) framework
- Bob Moesta's Forces of Progress diagram generation
- Automated JTBD interview guide creation
- Real-time job validation against new data
- ML-assisted pattern recognition for large datasets

---

## References & Further Reading

1. **Clayton Christensen et al.** (2016). *Competing Against Luck*. HarperBusiness.
2. **Christensen Institute** - Jobs-to-be-Done Theory: https://www.christenseninstitute.org/theory/jobs-to-be-done/
3. **Tony Ulwick** (2016). *Jobs to be Done: Theory to Practice*. IDEA BITE PRESS.
4. **Bob Moesta & Chris Spiek** - The Rewired Group: https://www.rewirehq.com
5. **Alan Klement** (2016). *When Coffee and Kale Compete*. Self-published.

---

**Skill Created By:** Category Intelligence | Consumer Research Practice
**Framework Authority:** Clayton Christensen Institute
**Quality Standard:** Peer-reviewed by frontier LLM experts
**Last Updated:** October 17, 2025
