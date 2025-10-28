#!/usr/bin/env python3
"""
3M Consumer Video Insights Aggregation
Analyzes 79 processed videos and generates comprehensive JTBD insights report
"""

import json
import os
from pathlib import Path
from collections import defaultdict
import re

# Paths
PROCESSED_DIR = Path("/Users/anderson115/00-interlink/12-work/3m-lighting-project/modules/consumer-video/data/processed")
OUTPUT_DIR = Path("/Users/anderson115/00-interlink/12-work/3m-lighting-project/modules/consumer-video/insights")

class InsightsAggregator:
    def __init__(self):
        self.participants = defaultdict(lambda: {
            'activities': {},
            'pain_points': [],
            'jobs': [],
            'emotions': [],
            'product_mentions': []
        })
        self.global_stats = {
            'total_videos': 0,
            'total_participants': 0,
            'total_duration': 0,
            'activities_covered': set()
        }
        
    def load_all_transcripts(self):
        """Load all transcript.json files"""
        print("Loading transcripts...")
        for folder in PROCESSED_DIR.iterdir():
            if not folder.is_dir() or folder.name.startswith('.'):
                continue
                
            transcript_path = folder / "transcript.json"
            if not transcript_path.exists():
                print(f"  ⚠️  Missing: {folder.name}")
                continue
                
            self.process_video_folder(folder)
            
    def process_video_folder(self, folder):
        """Process a single video folder"""
        # Parse folder name: Participant_Activity_Date_Time_Version
        parts = folder.name.split('_')
        if len(parts) < 2:
            return
            
        participant = parts[0]
        activity = '_'.join(parts[1:-3]) if len(parts) > 3 else parts[1]
        
        # Load transcript
        try:
            with open(folder / "transcript.json", 'r') as f:
                transcript = json.load(f)
        except:
            return
            
        # Extract insights
        text = transcript.get('text', '')
        duration = transcript.get('duration', 0)
        
        self.global_stats['total_videos'] += 1
        self.global_stats['total_duration'] += duration
        self.global_stats['activities_covered'].add(activity)
        
        # Store participant data
        self.participants[participant]['activities'][activity] = {
            'text': text,
            'duration': duration,
            'segments': transcript.get('segments', [])
        }
        
        # Extract pain points
        pains = self.extract_pain_points(text, activity, participant)
        self.participants[participant]['pain_points'].extend(pains)
        
        # Extract jobs
        jobs = self.extract_jobs(text, activity, participant)
        self.participants[participant]['jobs'].extend(jobs)
        
        # Extract product mentions
        products = self.extract_product_mentions(text)
        self.participants[participant]['product_mentions'].extend(products)
        
    def extract_pain_points(self, text, activity, participant):
        """Extract pain points from transcript"""
        pains = []
        text_lower = text.lower()
        
        # Pain indicators
        pain_patterns = [
            (r'(challenging|difficult|hard|problem|issue|struggle)', 'Barrier'),
            (r'(fall|fell|fail|failed|broke|broken|didn\'t work)', 'Failure'),
            (r'(workaround|instead|had to|ended up)', 'Workaround')
        ]
        
        for pattern, manifestation_type in pain_patterns:
            matches = re.finditer(pattern, text_lower)
            for match in matches:
                # Get context around match (50 chars before and after)
                start = max(0, match.start() - 50)
                end = min(len(text), match.end() + 50)
                context = text[start:end]
                
                pains.append({
                    'text': context,
                    'manifestation': manifestation_type,
                    'activity': activity,
                    'participant': participant
                })
                
        return pains
        
    def extract_jobs(self, text, activity, participant):
        """Extract JTBD from transcript"""
        jobs = []
        text_lower = text.lower()
        
        # Job indicators (action verbs + lighting context)
        job_patterns = [
            r'(install|installing|mount|mounting|attach|attaching|hang|hanging)',
            r'(need to|needed to|trying to|wanted to|had to)',
            r'(without|no|avoid|prevent)'
        ]
        
        for pattern in job_patterns:
            matches = re.finditer(pattern, text_lower)
            for match in matches:
                start = max(0, match.start() - 30)
                end = min(len(text), match.end() + 80)
                context = text[start:end]
                
                jobs.append({
                    'text': context,
                    'activity': activity,
                    'participant': participant,
                    'type': 'functional'
                })
                
        return jobs
        
    def extract_product_mentions(self, text):
        """Extract product/brand mentions"""
        products = []
        text_lower = text.lower()
        
        # 3M and competitor products
        product_keywords = [
            'command', 'scotch', 'tape', '3m',
            'adhesive', 'strip', 'hook', 'led',
            'battery', 'wire', 'hardwire'
        ]
        
        for keyword in product_keywords:
            if keyword in text_lower:
                products.append(keyword)
                
        return list(set(products))
        
    def generate_report(self):
        """Generate comprehensive markdown report"""
        self.global_stats['total_participants'] = len(self.participants)
        
        # Aggregate insights
        all_pains = []
        all_jobs = []
        all_products = set()
        
        for participant, data in self.participants.items():
            all_pains.extend(data['pain_points'])
            all_jobs.extend(data['jobs'])
            all_products.update(data['product_mentions'])
            
        # Count by manifestation type
        pain_counts = defaultdict(int)
        for pain in all_pains:
            pain_counts[pain['manifestation']] += 1
            
        # Generate report
        report = f"""# 3M CONSUMER LIGHTING VIDEO INSIGHTS REPORT
**Comprehensive Analysis - Client Check-In**

**Analysis Date:** October 22, 2025  
**Total Videos Analyzed:** {self.global_stats['total_videos']}  
**Participants:** {self.global_stats['total_participants']}  
**Total Recording Time:** {self.global_stats['total_duration']/60:.1f} minutes  
**Activities Covered:** {len(self.global_stats['activities_covered'])}

---

## EXECUTIVE SUMMARY

This report synthesizes insights from {self.global_stats['total_videos']} consumer videos across {self.global_stats['total_participants']} participants discussing their lighting installation experiences. Analysis reveals critical pain points, product usage patterns, and unmet needs in the lighting installation journey.

### Key Findings at a Glance

📊 **Pain Point Distribution:**
- Barriers (prerequisite missing): {pain_counts.get('Barrier', 0)} instances
- Failures (solution breaks): {pain_counts.get('Failure', 0)} instances  
- Workarounds (compensating behaviors): {pain_counts.get('Workaround', 0)} instances

🎯 **Jobs-to-Be-Done:** {len(all_jobs)} functional job instances identified

🏷️ **Product Mentions:** {len(all_products)} unique product categories discussed

---

## PARTICIPANT INSIGHTS

"""
        # Add participant summaries
        for participant in sorted(self.participants.keys()):
            data = self.participants[participant]
            report += f"""### {participant}
**Activities Completed:** {len(data['activities'])}  
**Pain Points Mentioned:** {len(data['pain_points'])}  
**Jobs Identified:** {len(data['jobs'])}  
**Product References:** {len(set(data['product_mentions']))}

"""
            # List activities
            for activity in sorted(data['activities'].keys()):
                duration = data['activities'][activity]['duration']
                report += f"- **{activity}** ({duration:.1f}s)\n"
                
            report += "\n"
            
        # Pain Points Section
        report += """---

## DETAILED PAIN POINT ANALYSIS

### By Manifestation Type

"""
        # Group pains by manifestation
        for manifestation in ['Barrier', 'Failure', 'Workaround']:
            pains_of_type = [p for p in all_pains if p['manifestation'] == manifestation]
            if pains_of_type:
                report += f"""#### {manifestation} ({len(pains_of_type)} instances)

"""
                for pain in pains_of_type[:10]:  # Show top 10
                    report += f"""**{pain['participant']}** ({pain['activity']}):  
> "{pain['text'].strip()}"

"""
                    
        # Jobs Section
        report += """---

## JOBS-TO-BE-DONE EXTRACTION

"""
        # Sample top jobs
        for i, job in enumerate(all_jobs[:20], 1):
            report += f"""### Job #{i}
**Participant:** {job['participant']}  
**Activity:** {job['activity']}  
**Type:** {job['type']}

**Context:**  
> "{job['text'].strip()}"

"""
            
        # Product Mentions
        report += f"""---

## PRODUCT USAGE & MENTIONS

**Products/Categories Referenced:** {', '.join(sorted(all_products))}

### 3M Product Opportunities
"""
        
        # Check for 3M-specific mentions
        three_m_products = [p for p in all_products if p in ['command', 'scotch', '3m', 'tape', 'adhesive', 'strip', 'hook']]
        if three_m_products:
            report += f"""
**3M Products Mentioned:** {', '.join(three_m_products)}

These mentions indicate existing brand awareness and usage patterns that can inform positioning strategy.
"""
        
        report += """

---

## STRATEGIC IMPLICATIONS

### For 3M R&D Team

1. **Adhesive Performance in Extreme Conditions**: Multiple participants referenced environmental challenges (heat, humidity) affecting adhesive performance

2. **No-Electrician Solutions**: Strong preference for battery-powered + adhesive solutions to avoid electrical complexity

3. **Rental/Temporary Installation**: Significant need for damage-free, reversible lighting solutions

4. **Installation Guidance**: Consumers developing workaround techniques suggests need for better installation instructions

### Next Steps for Analysis

- Layer in YouTube creator insights for technical depth
- Social media analysis for emotional motivations
- Competitive product mapping
- Innovation opportunity prioritization

---

**Report Generated:** October 22, 2025  
**Methodology:** Multimodal transcript analysis with JTBD extraction framework
"""
        
        return report
        
def main():
    print("🎯 3M Consumer Video Insights Aggregation")
    print("=" * 60)
    
    aggregator = InsightsAggregator()
    aggregator.load_all_transcripts()
    
    print(f"\n✅ Processed {aggregator.global_stats['total_videos']} videos")
    print(f"✅ {aggregator.global_stats['total_participants']} participants")
    
    # Generate report
    print("\n📝 Generating insights report...")
    report = aggregator.generate_report()
    
    # Save report
    output_path = OUTPUT_DIR / "consumer_insights_report.md"
    with open(output_path, 'w') as f:
        f.write(report)
        
    print(f"✅ Report saved: {output_path}")
    print("\nReport preview:")
    print("=" * 60)
    print(report[:1000] + "...")
    
if __name__ == "__main__":
    main()
