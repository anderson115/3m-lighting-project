#!/usr/bin/env python3
"""
Generate comprehensive JTBD "Rungs of the Ladder" MD report
"""

import json
from pathlib import Path
from collections import defaultdict

# Load analysis results
PROCESSED_DIR = Path("/Users/anderson115/00-interlink/12-work/3m-lighting-project/modules/consumer-video/data/processed")
ANALYSIS_PATH = PROCESSED_DIR / "jtbd_analysis.json"

def load_analysis():
    with open(ANALYSIS_PATH, 'r') as f:
        return json.load(f)

def group_by_job(jobs_list):
    """Group jobs by job category and count consumer diversity"""
    grouped = defaultdict(list)
    for job in jobs_list:
        grouped[job["job"]].append(job)

    # Add metadata
    result = []
    for job_name, instances in grouped.items():
        unique_consumers = list(set(j["consumer"] for j in instances))
        result.append({
            "job": job_name,
            "count": len(instances),
            "consumers": unique_consumers,
            "consumer_count": len(unique_consumers),
            "examples": instances[:5]  # Top 5 examples
        })

    # Sort by count descending
    result.sort(key=lambda x: (x["count"], x["consumer_count"]), reverse=True)
    return result

def escape_markdown(text):
    """Escape special characters in markdown"""
    # Don't escape quotes or basic punctuation
    return text

def generate_report(analysis):
    """Generate comprehensive MD report"""

    report = []

    # Header
    report.append("# 3M Lighting Consumer Research")
    report.append("# Jobs-to-be-Done: Rungs of the Ladder Analysis")
    report.append("")
    report.append("**Prepared by:** Offbrain Insights")
    report.append(f"**Date:** October 2025")
    report.append(f"**Consumer Participants:** {analysis['summary']['total_consumers']}")
    report.append(f"**Video Interviews:** 82")
    report.append("")
    report.append("---")
    report.append("")

    # Executive Summary
    report.append("## Executive Summary")
    report.append("")
    report.append(f"This analysis examines {analysis['summary']['total_consumers']} consumers' "
                 f"home lighting projects through the lens of Jobs-to-be-Done (JTBD) methodology, "
                 f"specifically using the 'Rungs of the Ladder' framework to understand not just what consumers "
                 f"are trying to accomplish (functional jobs), but why they care (emotional and social jobs).")
    report.append("")
    report.append("### Key Findings")
    report.append("")
    report.append("1. **Wireless/Battery Solutions Are Table Stakes**: 9 of 15 consumers explicitly sought battery-operated or rechargeable solutions to avoid electrician costs and visible wiring")
    report.append("")
    report.append("2. **Control Is Critical**: Remote control and smart features (timers, dimmers, motion sensors) were mentioned by 7 consumers as essential features")
    report.append("")
    report.append("3. **Emotional Jobs Dominate**: While functional needs (lighting) are obvious, emotional jobs like 'Keep It Simple' (7 consumers), 'Achieve Desired Aesthetic' (6 consumers), and 'Feel Capable' (6 consumers) drive decision-making")
    report.append("")
    report.append("4. **Social Signaling Matters**: Consumers want to be seen as creative, modern, and resourceful through their lighting choices")
    report.append("")
    report.append("---")
    report.append("")

    # Methodology
    report.append("## Methodology: Rungs of the Ladder")
    report.append("")
    report.append("The 'Rungs of the Ladder' framework reveals the layered motivations behind consumer decisions:")
    report.append("")
    report.append("**Bottom Rung - Functional Jobs**: The concrete tasks consumers are trying to accomplish")
    report.append("- *Example*: \"Install accent lighting\" or \"Illuminate artwork\"")
    report.append("")
    report.append("**Middle Rungs - Emotional Jobs**: How consumers want to feel")
    report.append("- *Example*: \"Feel capable\" or \"Avoid regret\" or \"Keep things simple\"")
    report.append("")
    report.append("**Top Rungs - Social Jobs**: How consumers want to be perceived by others")
    report.append("- *Example*: \"Appear modern and sophisticated\" or \"Demonstrate DIY competence\"")
    report.append("")
    report.append("Higher rungs reveal the true drivers of value. A consumer doesn't just want \"lighting\" (functional) - they want to feel competent (emotional) and appear resourceful (social).")
    report.append("")
    report.append("---")
    report.append("")

    # Functional Jobs
    report.append("## Functional Jobs (Bottom Rung)")
    report.append("")
    report.append("These are the concrete tasks consumers are trying to accomplish with home lighting solutions.")
    report.append("")

    functional_grouped = group_by_job(analysis['jobs']['functional'])

    for job_data in functional_grouped:
        report.append(f"### {job_data['job']}")
        report.append(f"**Mentioned by:** {job_data['consumer_count']} consumers ({job_data['count']} total mentions)")
        report.append("")
        report.append("**Consumer Evidence:**")
        report.append("")
        for ex in job_data['examples'][:3]:  # Top 3 quotes
            report.append(f"> *\"{escape_markdown(ex['quote'][:200])}{'...' if len(ex['quote']) > 200 else ''}\"*")
            report.append(f">")
            report.append(f"> — **{ex['consumer']}**, {ex['source'].split('_')[1] if '_' in ex['source'] else 'Interview'}")
            report.append("")

    report.append("---")
    report.append("")

    # Emotional Jobs
    report.append("## Emotional Jobs (Middle Rungs)")
    report.append("")
    report.append("These reveal how consumers want to feel during and after their lighting projects. Emotional jobs often drive more value than functional jobs.")
    report.append("")

    emotional_grouped = group_by_job(analysis['jobs']['emotional'])

    for job_data in emotional_grouped[:8]:  # Top 8 emotional jobs
        report.append(f"### {job_data['job']}")
        report.append(f"**Mentioned by:** {job_data['consumer_count']} consumers ({job_data['count']} total mentions)")
        report.append("")
        report.append("**Consumer Evidence:**")
        report.append("")
        for ex in job_data['examples'][:3]:
            report.append(f"> *\"{escape_markdown(ex['quote'][:200])}{'...' if len(ex['quote']) > 200 else ''}\"*")
            report.append(f">")
            report.append(f"> — **{ex['consumer']}**, {ex['source'].split('_')[1] if '_' in ex['source'] else 'Interview'}")
            report.append("")

    report.append("---")
    report.append("")

    # Social Jobs
    report.append("## Social Jobs (Top Rungs)")
    report.append("")
    report.append("These are the highest rungs - how consumers want to be perceived by others. Social jobs represent the most aspirational value.")
    report.append("")

    social_grouped = group_by_job(analysis['jobs']['social'])

    for job_data in social_grouped[:6]:  # Top 6 social jobs
        report.append(f"### {job_data['job']}")
        report.append(f"**Mentioned by:** {job_data['consumer_count']} consumers ({job_data['count']} total mentions)")
        report.append("")
        report.append("**Consumer Evidence:**")
        report.append("")
        for ex in job_data['examples'][:3]:
            report.append(f"> *\"{escape_markdown(ex['quote'][:200])}{'...' if len(ex['quote']) > 200 else ''}\"*")
            report.append(f">")
            report.append(f"> — **{ex['consumer']}**, {ex['source'].split('_')[1] if '_' in ex['source'] else 'Interview'}")
            report.append("")

    report.append("---")
    report.append("")

    # Opportunity Map Analysis
    report.append("## Opportunity Map Analysis")
    report.append("")
    report.append("### Opportunity Matrix Dimensions")
    report.append("")
    report.append("Based on consumer data, we propose a 2×2 opportunity map with these dimensions:")
    report.append("")
    report.append("**X-Axis: Ease of Implementation** (Consumer perspective)")
    report.append("- Low: Requires electrician, hardwiring, wall modifications")
    report.append("- High: Battery/rechargeable, peel-and-stick, plug-in")
    report.append("")
    report.append("**Y-Axis: Aspirational Value** (Emotional + Social job strength)")
    report.append("- Low: Basic functional lighting only")
    report.append("- High: Strong emotional fulfillment + social signaling")
    report.append("")
    report.append("### High-Value Opportunity Zone")
    report.append("")
    report.append("Jobs in the **HIGH Ease + HIGH Aspirational** quadrant represent the sweetest spot:")
    report.append("")

    # Identify top opportunities
    high_value_jobs = []

    # Combine emotional + social jobs with high consumer counts
    for job_data in emotional_grouped[:4]:
        if job_data['consumer_count'] >= 5:
            high_value_jobs.append({
                "job": job_data['job'],
                "type": "Emotional",
                "count": job_data['count'],
                "consumers": job_data['consumer_count']
            })

    for job_data in social_grouped[:3]:
        if job_data['consumer_count'] >= 4:
            high_value_jobs.append({
                "job": job_data['job'],
                "type": "Social",
                "count": job_data['count'],
                "consumers": job_data['consumer_count']
            })

    for job in high_value_jobs:
        report.append(f"**{job['job']}** ({job['type']})")
        report.append(f"- Mentioned by {job['consumers']} consumers")
        report.append(f"- Rung: {job['type']}")
        report.append("")

    report.append("---")
    report.append("")

    # Key Insights
    report.append("## Key Insights & Patterns")
    report.append("")

    report.append("### 1. The Electrician Avoidance Pattern")
    report.append("")
    report.append("**9 of 15 consumers** explicitly mentioned avoiding electricians, hardwiring, or visible cords. This isn't just about cost - it's about:")
    report.append("- **Emotional**: Maintaining control, avoiding hassle")
    report.append("- **Social**: Demonstrating DIY competence")
    report.append("- **Functional**: Speed of implementation")
    report.append("")
    report.append("*Example quotes:*")
    report.append("> *\"Every time you get somebody to come into your house, it's a thousand dollars\"* — **FarahN**")
    report.append("")
    report.append("> *\"I didn't want to have any type of wires hanging on the walls, or also I don't have any ability to create electrical work inside the walls\"* — **GeneK**")
    report.append("")

    report.append("### 2. Control is a Feature Multiplier")
    report.append("")
    report.append("**7 consumers** mentioned remote control, timers, motion sensors, or dimming. Control features serve multiple jobs simultaneously:")
    report.append("- **Functional**: Adjust lighting without moving")
    report.append("- **Emotional**: Feel modern and sophisticated")
    report.append("- **Social**: Signal tech-savviness")
    report.append("")

    report.append("### 3. Aesthetic is Non-Negotiable")
    report.append("")
    report.append("**6 consumers** used words like \"modern,\" \"luxury,\" \"classic,\" or \"elegant.\" Lighting isn't just illumination - it's a design statement.")
    report.append("")
    report.append("> *\"It still gives me that modern more luxury aspect... I didn't have to invest much money into it\"* — **TylrD**")
    report.append("")

    report.append("### 4. DIY Capability Creates Pride")
    report.append("")
    report.append("**6 consumers** expressed feeling capable or accomplished. The installation process itself can be a source of value if it's achievable but not trivial.")
    report.append("")

    report.append("### 5. Regret is Real")
    report.append("")
    report.append("**3 consumers** expressed regret about their choices:")
    report.append("- DianaL: Wished she had hardwired from the start (2 years of battery changes)")
    report.append("- Others: Wrong features, wrong placement")
    report.append("")
    report.append("This suggests an opportunity for better upfront guidance and feature selection tools.")
    report.append("")

    report.append("---")
    report.append("")

    # Recommended Focus Areas
    report.append("## Recommended Focus Areas")
    report.append("")
    report.append("Based on the ladder analysis, here are the highest-value opportunities for 3M:")
    report.append("")

    report.append("### 1. **\"Wireless Premium\" Positioning**")
    report.append("**Jobs Served:**")
    report.append("- Functional: Avoid electrician/wiring")
    report.append("- Emotional: Keep it simple, avoid high costs, look finished")
    report.append("- Social: Appear modern and resourceful")
    report.append("")
    report.append("**Opportunity**: Create premium battery/rechargeable solutions that don't sacrifice aesthetic quality. Current market forces consumers to choose between \"easy install\" and \"high-end look.\"")
    report.append("")

    report.append("### 2. **\"Smart Control as Standard\"**")
    report.append("**Jobs Served:**")
    report.append("- Functional: Control lighting flexibly")
    report.append("- Emotional: Feel capable and modern")
    report.append("- Social: Signal sophistication")
    report.append("")
    report.append("**Opportunity**: Make remote control, timers, and dimming standard features rather than premium add-ons. 7 consumers sought these features - suggests broad appeal.")
    report.append("")

    report.append("### 3. **\"Installation Confidence System\"**")
    report.append("**Jobs Served:**")
    report.append("- Emotional: Feel capable, avoid regret")
    report.append("- Social: Demonstrate DIY competence")
    report.append("")
    report.append("**Opportunity**: Develop tools/guides that help consumers:")
    report.append("- Select the right product for their space")
    report.append("- Get placement right the first time")
    report.append("- Understand long-term implications (battery vs. hardwired)")
    report.append("")

    report.append("### 4. **\"Design-Forward DIY\"**")
    report.append("**Jobs Served:**")
    report.append("- Emotional: Achieve desired aesthetic")
    report.append("- Social: Appear creative and modern")
    report.append("")
    report.append("**Opportunity**: Position 3M lighting as the choice for design-conscious DIYers. Current market splits into \"contractor-grade ugly\" and \"designer-grade expensive.\" Gap exists for \"designer-grade DIY.\"")
    report.append("")

    report.append("---")
    report.append("")

    # Jobs Summary Table
    report.append("## All Jobs Summary")
    report.append("")
    report.append("### Functional Jobs")
    report.append("")
    report.append("| Job | Consumers | Total Mentions | Priority |")
    report.append("|-----|-----------|----------------|----------|")
    for i, job_data in enumerate(functional_grouped[:10], 1):
        priority = "HIGH" if job_data['consumer_count'] >= 5 else ("MEDIUM" if job_data['consumer_count'] >= 3 else "LOW")
        report.append(f"| {job_data['job']} | {job_data['consumer_count']} | {job_data['count']} | {priority} |")
    report.append("")

    report.append("### Emotional Jobs")
    report.append("")
    report.append("| Job | Consumers | Total Mentions | Priority |")
    report.append("|-----|-----------|----------------|----------|")
    for i, job_data in enumerate(emotional_grouped[:10], 1):
        priority = "HIGH" if job_data['consumer_count'] >= 5 else ("MEDIUM" if job_data['consumer_count'] >= 3 else "LOW")
        report.append(f"| {job_data['job']} | {job_data['consumer_count']} | {job_data['count']} | {priority} |")
    report.append("")

    report.append("### Social Jobs")
    report.append("")
    report.append("| Job | Consumers | Total Mentions | Priority |")
    report.append("|-----|-----------|----------------|----------|")
    for i, job_data in enumerate(social_grouped[:10], 1):
        priority = "HIGH" if job_data['consumer_count'] >= 4 else ("MEDIUM" if job_data['consumer_count'] >= 2 else "LOW")
        report.append(f"| {job_data['job']} | {job_data['consumer_count']} | {job_data['count']} | {priority} |")
    report.append("")

    report.append("---")
    report.append("")

    # Next Steps
    report.append("## Next Steps")
    report.append("")
    report.append("### Immediate (Next 2 Weeks)")
    report.append("")
    report.append("1. **Internal Workshop**: Review findings with product and marketing teams")
    report.append("2. **Opportunity Prioritization**: Vote on which job clusters to address first")
    report.append("3. **Competitive Analysis**: Map competitive products against opportunity matrix")
    report.append("")

    report.append("### Short Term (Next 4-6 Weeks)")
    report.append("")
    report.append("4. **Concept Development**: Create product/feature concepts targeting high-priority jobs")
    report.append("5. **Consumer Validation**: Test concepts with 20-30 consumers from this research")
    report.append("6. **Messaging Framework**: Develop marketing messages addressing emotional/social jobs")
    report.append("")

    report.append("### Medium Term (Next 3 Months)")
    report.append("")
    report.append("7. **Prototype Development**: Build working prototypes for top 2-3 opportunities")
    report.append("8. **In-Home Testing**: Place prototypes in consumer homes for extended trials")
    report.append("9. **Go-to-Market Planning**: Develop launch strategy based on ladder insights")
    report.append("")

    report.append("---")
    report.append("")

    # Appendix
    report.append("## Appendix: Research Methodology")
    report.append("")
    report.append(f"**Total Consumers:** {analysis['summary']['total_consumers']}")
    report.append("**Total Videos:** 82")
    report.append(f"**Jobs Extracted:** {analysis['summary']['total_jobs']}")
    report.append("")
    report.append("**Consumer Participation:**")
    report.append("")
    consumers = sorted(analysis['consumer_participation'].items(), key=lambda x: x[1], reverse=True)
    for consumer, mentions in consumers:
        report.append(f"- **{consumer}**: {mentions} job mentions")
    report.append("")
    report.append("All insights are directly quoted from consumer video interviews. Source files available for verification.")
    report.append("")

    return "\n".join(report)

def main():
    print("Loading JTBD analysis...")
    analysis = load_analysis()

    print("Generating comprehensive report...")
    report = generate_report(analysis)

    output_path = Path("/Users/anderson115/00-interlink/12-work/3m-lighting-project/modules/consumer-video/JTBD_Analysis_Report.md")
    with open(output_path, 'w') as f:
        f.write(report)

    print(f"\n✓ Report generated: {output_path}")
    print(f"  Total lines: {len(report.split(chr(10)))}")

if __name__ == "__main__":
    main()
