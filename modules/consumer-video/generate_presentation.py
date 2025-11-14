#!/usr/bin/env python3
"""
Generate PowerPoint presentation from JTBD analysis
"""

from config import PATHS

import json
import subprocess
from pathlib import Path

# Load analysis results
PROCESSED_DIR = Path(PATHS["processed"])
ANALYSIS_PATH = PROCESSED_DIR / "jtbd_analysis.json"
SKILL_PATH = Path("/Users/anderson115/.claude/skills/slide-text-to-pptx/skill.py")

def load_analysis():
    with open(ANALYSIS_PATH, 'r') as f:
        return json.load(f)

def generate_slide_text(analysis):
    """Generate text for PowerPoint slides"""

    slides_text = []

    # Slide 1: Title
    slides_text.append("""
Title: 3M Lighting Consumer Research
Jobs-to-be-Done Analysis
Rungs of the Ladder Framework

Note: Brief client check-in on consumer insights. Focus on opportunities, not technical process.
""")

    # Slide 2: Research Overview
    slides_text.append(f"""
Slide 1: Research Overview

- {analysis['summary']['total_consumers']} consumers analyzed across 82 video interviews
- {analysis['summary']['total_jobs']} distinct jobs extracted from verbatim quotes
- Framework: Jobs-to-be-Done "Rungs of the Ladder"
- Focus: Understanding not just what consumers do, but why they care

Note: Emphasize depth of analysis - real consumer voices, not survey data.
All insights are directly quoted and verifiable.
""")

    # Slide 3: Rungs of the Ladder Framework
    slides_text.append("""
Slide 2: The Rungs of the Ladder Approach

Bottom Rung - Functional Jobs:
- What consumers are trying to accomplish
- Example: Install accent lighting, illuminate artwork

Middle Rungs - Emotional Jobs:
- How consumers want to feel
- Example: Feel capable, keep it simple, avoid regret

Top Rungs - Social Jobs:
- How consumers want to be perceived
- Example: Appear modern/sophisticated, demonstrate competence

Note: Higher rungs reveal the true value drivers.
Consumers don't just want lighting - they want to feel capable and appear resourceful.
""")

    # Slide 4: Key Findings - Functional Jobs
    slides_text.append("""
Slide 3: Functional Jobs - What They're Trying to Do

Top Functional Jobs:
- Control Lighting (7 consumers): Remote, timers, motion sensors
- Avoid Cords/Wiring (9 consumers): Battery, rechargeable solutions
- Illuminate Space (5 consumers): Light up art, features
- Highlight Features (3 consumers): Draw attention to design elements

Consumer Voice:
"I didn't want wires hanging on walls... no ability to create electrical work inside walls" - GeneK

Note: Wireless/battery solutions are table stakes, not differentiators.
Control features serve multiple jobs simultaneously.
""")

    # Slide 5: Key Findings - Emotional Jobs
    slides_text.append("""
Slide 4: Emotional Jobs - How They Want to Feel

Top Emotional Jobs:
- Keep It Simple (7 consumers): Avoid hassle, maintain control
- Achieve Desired Aesthetic (6 consumers): Modern, luxury, elegant look
- Avoid High Costs (4 consumers): "$1000 every time electrician comes"
- Feel Capable (6 consumers): Pride in DIY accomplishment
- Avoid Regret (3 consumers): Get it right the first time

Consumer Voice:
"It still gives me that modern luxury aspect... didn't have to invest much money" - TylrD
"Process wasn't too difficult... I really like the way they turned out" - DianaL

Note: Emotional jobs often drive more value than functional jobs.
Aesthetic is non-negotiable, but must be achievable.
""")

    # Slide 6: Key Findings - Social Jobs
    slides_text.append("""
Slide 5: Social Jobs - How They Want to Be Perceived

Top Social Jobs:
- Be Seen as Creative (7 consumers): Design-conscious choices
- Showcase Home (5 consumers): Impress visitors, display identity
- Appear Modern/Sophisticated (5 consumers): Tech-savvy, upscale
- Display Personal Identity (3 consumers): Family photos, art collection
- Demonstrate DIY Competence (multiple consumers): "No need to hire"

Consumer Voice:
"Motion detected... still get that same look as modern and classic design" - TylrD

Note: Social signaling matters - lighting is a design statement.
DIY capability creates pride when achievable but not trivial.
""")

    # Slide 7: Opportunity Map (2x2 Matrix)
    slides_text.append("""
Slide 6: Opportunity Map

Table: Opportunity Matrix (Ease of Implementation vs Aspirational Value)

HIGH Ease, HIGH Aspirational:
- Wireless Premium Positioning
- Smart Control as Standard
- Design-Forward DIY

HIGH Ease, LOW Aspirational:
- Basic battery lights (commodity)
- Simple plug-in fixtures

LOW Ease, HIGH Aspirational:
- Hardwired luxury solutions
- Integrated smart home systems

LOW Ease, LOW Aspirational:
- Traditional contractor-grade
- Basic functional lighting

Note: Sweet spot is HIGH Ease + HIGH Aspirational quadrant.
Current market forces consumers to choose between "easy install" and "high-end look."
3M opportunity: Premium DIY solutions that don't sacrifice aesthetic quality.
""")

    # Slide 8: All Jobs Summary
    slides_text.append("""
Slide 7: Jobs Summary by Priority

Table: Top Priority Jobs

| Job | Type | Consumers | Priority |
|-----|------|-----------|----------|
| Avoid Cords/Wiring | Functional | 9 | HIGH |
| Control Lighting | Functional | 7 | HIGH |
| Keep It Simple | Emotional | 7 | HIGH |
| Be Seen as Creative | Social | 7 | HIGH |
| Achieve Desired Aesthetic | Emotional | 6 | HIGH |
| Feel Capable | Emotional | 6 | HIGH |
| Showcase Home | Social | 5 | MEDIUM |
| Appear Modern/Sophisticated | Social | 5 | MEDIUM |
| Illuminate Space | Functional | 5 | MEDIUM |

Note: Priority based on consumer diversity and mention frequency.
Jobs with 5+ consumers represent validated opportunities.
""")

    # Slide 9: Recommended Focus Areas
    slides_text.append("""
Slide 8: Recommended Focus Areas

1. Wireless Premium Positioning:
   - Premium battery solutions without sacrificing aesthetic
   - Serves: Avoid electrician + Look finished + Appear modern

2. Smart Control as Standard:
   - Make remote, timers, dimming standard features
   - Serves: Control flexibility + Feel capable + Signal sophistication

3. Installation Confidence System:
   - Tools/guides for right product selection and placement
   - Serves: Feel capable + Avoid regret + Demonstrate competence

4. Design-Forward DIY:
   - Position as choice for design-conscious DIYers
   - Serves: Achieve aesthetic + Be creative + Showcase home

Note: Each opportunity serves multiple ladder rungs simultaneously.
Gap exists between "contractor-grade ugly" and "designer-grade expensive."
""")

    # Slide 10: Key Insights
    slides_text.append("""
Slide 9: Key Insights & Patterns

Pattern 1: The Electrician Avoidance
- 9 of 15 consumers explicitly avoided electricians
- Not just cost - it's about control, speed, DIY pride

Pattern 2: Control as Feature Multiplier
- Remote, timers, motion sensors serve multiple jobs
- Functional + Emotional + Social value simultaneously

Pattern 3: Regret is Real
- 3 consumers expressed regret about choices
- Opportunity for better upfront guidance

Pattern 4: Aesthetic Non-Negotiable
- 6 consumers used "modern," "luxury," "elegant"
- Lighting is a design statement, not just illumination

Note: These patterns reveal unmet needs and innovation opportunities.
""")

    # Slide 11: Next Steps
    slides_text.append("""
Slide 10: Next Steps

Immediate (2 weeks):
- Internal workshop with product and marketing teams
- Opportunity prioritization vote
- Competitive mapping against opportunity matrix

Short Term (4-6 weeks):
- Concept development for high-priority jobs
- Consumer validation with 20-30 participants
- Messaging framework addressing emotional/social jobs

Medium Term (3 months):
- Prototype development for top 2-3 opportunities
- In-home testing and extended trials
- Go-to-market planning based on ladder insights

Note: All 82 videos and transcripts available for deeper exploration.
Source files verifiable for any insight cited.
""")

    return "\n\n".join(slides_text)

def main():
    print("Loading JTBD analysis...")
    analysis = load_analysis()

    print("Generating slide content...")
    slide_text = generate_slide_text(analysis)

    print("Creating PowerPoint presentation...")

    # Call the PowerPoint skill
    result = subprocess.run(
        ["python3", str(SKILL_PATH), slide_text],
        capture_output=True,
        text=True,
        timeout=60
    )

    if result.returncode == 0:
        print(f"\n✓ PowerPoint created successfully!")
        print(result.stdout)
        print(f"\nPresentation saved in current directory")
    else:
        print(f"\n✗ Error creating PowerPoint:")
        print(result.stderr)

if __name__ == "__main__":
    main()
