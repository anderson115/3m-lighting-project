# IG App Preference Test Run – Executive Summary

## Process Snapshot
1. **Ingestion & Normalization** – 50 posts (Instagram, Reddit, X) pulled from `manual_sample_posts.json`, normalized, and retained with full URLs for audit.
2. **Atomic Coding Pass** – 136 snippets extracted manually with verbatim excerpts, agent interpretations, and rationales.
3. **Equity Tagging** – Automated heuristics scored each snippet across Connection, Discovery, Expression, Entertainment, Creativity, Content Quality, plus hypothesized drivers (Algorithm Trust, Growth Reach, etc.).
4. **Creator Detection** – Regex + lexical cues flagged creator status at snippet and post levels (>10K followers or self-identified creators).
5. **Workbook Output** – `outputs/ig_preference_manual_coding.xlsx` (tabs: README, Posts_Audit, Snippets_50, Examples10) ready for reviewer QA with dropdowns for all labels.

## Coding Coverage
- **136 snippets / 50 posts**; 10 creator-leaning posts (3 Confirmed, 20 Possible out of 50).
- **Driver mix (snippet-level top 5):** Algorithm_Trust (27), Community_Culture (21), Growth_Reach (16), Creative_Tools (12), Education_Value (11).
- **Equity signals (Strong hits):** Content Quality 20, Creativity 15, Connection 14, Discovery 6, Expression 6, Entertainment 1.
- **Post-level drivers:** Algorithm_Trust leads (14/50), followed by Growth_Reach (8) and Community_Culture (6); others cover Competitive_Positioning, Education_Value, Creative_Tools, Safety_Governance, Cross_App_Strategy, User_Experience, Monetization_Path, Ad_Ecosystem, Content_Quality.

## Emerging Topics & Hypotheses
- **Content Experience Focus** – 20 snippets explicitly demand high production values (transitions, thumb-stopping visuals, audio polish), validating the need for a Content Quality signal.
- **Algorithm Transparency** – Strong recurring pain (reach collapse, send-per-reach dynamics) plus hypothesized driver tags reinforce Algorithm_Trust as a core motivator.
- **Growth Discipline** – Snippets highlight strategic posting, share metrics, and quiz-style engagement loops, aligning with Growth_Reach + Creative_Tools hypotheses.
- **Community Trade-offs** – Users weigh comments culture (IG vs TikTok), multi-part reel fatigue, and safety concerns (graphic content), supporting Community_Culture + Safety_Governance coverage.

## Directional Read vs Existing Knowledge
- **Connection/Discovery/Expression** – Signals mirror historical learnings (Connection & Creativity strongest; Expression/Discovery present but lighter in this sample), indicating the seed taxonomy still maps to known preference motivators.
- **Entertainment** – Low incidence in this cut (1 strong) suggests we should expand sampling for pure entertainment use cases during the 10× data collection.
- **Creator Segment** – Early detection of confirmed/possible creators validates the need for dedicated creator messaging (monetization, workflow) alongside general audience insights.

## Next Steps
1. Reviewer QA on `Snippets_50` to finalize tags before scaling (focus on hypothesized drivers and creator flags).
2. Once validated, expand capture to full dataset (10× volume) and retrain tagging models per `docs/topic_modeling_strategy.md`.
3. Stand up automated reporting (driver distribution, equity signal incidence, creator splits) to benchmark new runs against this test baseline.
