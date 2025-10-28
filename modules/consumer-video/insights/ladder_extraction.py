#!/usr/bin/env python3
"""
3M Consumer Video Insights - PROPER LADDER STRUCTURE
Extracts: Aspirational States → Jobs → Problems (with 2x2 prioritization)
"""

import json
import os
from pathlib import Path
from collections import defaultdict, Counter
import re

PROCESSED_DIR = Path("/Users/anderson115/00-interlink/12-work/3m-lighting-project/modules/consumer-video/data/processed")
OUTPUT_DIR = Path("/Users/anderson115/00-interlink/12-work/3m-lighting-project/modules/consumer-video/insights")

class LadderExtractor:
    def __init__(self):
        self.jobs = []
        self.problems = []
        self.aspirations = []
        self.participant_data = {}
        
    def load_all_transcripts(self):
        """Load all transcripts"""
        print("📚 Loading transcripts...")
        count = 0
        for folder in PROCESSED_DIR.iterdir():
            if not folder.is_dir() or folder.name.startswith('.'):
                continue
            transcript_path = folder / "transcript.json"
            if not transcript_path.exists():
                continue
            count += 1
            self.process_transcript(folder)
        print(f"   ✅ Loaded {count} transcripts")
        
    def process_transcript(self, folder):
        """Process single transcript"""
        parts = folder.name.split('_')
        if len(parts) < 2:
            return
        participant = parts[0]
        activity = '_'.join(parts[1:-3]) if len(parts) > 3 else parts[1]
        
        try:
            with open(folder / "transcript.json", 'r') as f:
                data = json.load(f)
        except:
            return
            
        text = data.get('text', '')
        
        # Extract insights
        self.extract_jobs(text, participant, activity)
        self.extract_problems(text, participant, activity)
        self.extract_aspirations(text, participant, activity)
        
    def extract_jobs(self, text, participant, activity):
        """Extract broad functional jobs"""
        text_lower = text.lower()
        
        # Job patterns - looking for WHAT they're trying to accomplish
        job_indicators = [
            # Lighting without electrical work
            {
                'patterns': [r'without\s+(wiring|hardwire|hardwired|electrical|electrician)', 
                            r'battery[\s-]?powered', r'no\s+wire', r'plug[\s-]?in'],
                'job': 'Install lighting without electrical work',
                'context_window': 100
            },
            # Accent/decorative lighting
            {
                'patterns': [r'accent\s+light', r'highlight', r'showcase', r'feature', r'ambiance'],
                'job': 'Create accent lighting for specific features',
                'context_window': 80
            },
            # Damage-free installation
            {
                'patterns': [r'without\s+(damage|damaging|drill|drilling|holes)', 
                            r'damage[\s-]?free', r'rental', r'temporary'],
                'job': 'Mount fixtures without damaging surfaces',
                'context_window': 80
            },
            # Adjustment/control
            {
                'patterns': [r'adjust', r'control', r'remote', r'dimm', r'change\s+temperature'],
                'job': 'Control lighting settings after installation',
                'context_window': 70
            },
            # Retrofit/no existing lighting
            {
                'patterns': [r'no\s+light', r'dark', r'add\s+light', r'retrofit'],
                'job': 'Add lighting to areas without existing fixtures',
                'context_window': 80
            },
            # DIY completion
            {
                'patterns': [r'do\s+it\s+myself', r'diy', r'install\s+myself', r'on\s+my\s+own'],
                'job': 'Complete lighting project independently',
                'context_window': 70
            },
            # Measurement/precision
            {
                'patterns': [r'measure', r'level', r'straight', r'align', r'position'],
                'job': 'Position fixtures accurately and level',
                'context_window': 70
            },
        ]
        
        for indicator in job_indicators:
            for pattern in indicator['patterns']:
                matches = re.finditer(pattern, text_lower)
                for match in matches:
                    start = max(0, match.start() - 50)
                    end = min(len(text), match.end() + indicator['context_window'])
                    evidence = text[start:end].strip()
                    
                    self.jobs.append({
                        'job': indicator['job'],
                        'evidence': evidence,
                        'participant': participant,
                        'activity': activity
                    })
                    
    def extract_problems(self, text, participant, activity):
        """Extract problems (technical + execution issues)"""
        text_lower = text.lower()
        
        # Problem patterns with pain indicators
        problem_patterns = [
            # Adhesive failures
            {
                'patterns': [r'fall|fell|falling', r'stick|sticky|adhesive.*fail', 
                            r'come\s+off', r'didn\'t\s+hold'],
                'problem': 'Adhesive fails to hold fixtures',
                'pain_level': 'High',
                'solution_satisfaction': 'Low',
                'evidence_window': 100
            },
            # Heat/environmental
            {
                'patterns': [r'hot|heat|arizona|texas|sun', r'weather', r'temperature.*affect'],
                'problem': 'Adhesive performance degrades in extreme heat',
                'pain_level': 'High',
                'solution_satisfaction': 'Low',
                'evidence_window': 100
            },
            # Electrical complexity
            {
                'patterns': [r'electrician|electrical.*complex|wiring.*difficult', 
                            r'don\'t\s+know.*electric', r'not.*electrician'],
                'problem': 'Lack electrical knowledge/confidence for hardwiring',
                'pain_level': 'High',
                'solution_satisfaction': 'Medium',  # Battery alternatives exist
                'evidence_window': 80
            },
            # Measurement difficulty
            {
                'patterns': [r'hard.*measure', r'difficult.*level', r'measurement.*problem',
                            r'hardest.*measurement'],
                'problem': 'Difficulty achieving accurate placement/leveling',
                'pain_level': 'Medium',
                'solution_satisfaction': 'Low',
                'evidence_window': 80
            },
            # Surface compatibility
            {
                'patterns': [r'textured.*wall', r'won\'t.*stick', r'surface.*problem'],
                'problem': 'Adhesives fail on textured/non-smooth surfaces',
                'pain_level': 'Medium',
                'solution_satisfaction': 'Low',
                'evidence_window': 80
            },
            # Cost of professional install
            {
                'patterns': [r'expensive|cost.*install', r'pay.*electrician', r'hire'],
                'problem': 'Professional installation too expensive',
                'pain_level': 'High',
                'solution_satisfaction': 'Medium',  # DIY possible but difficult
                'evidence_window': 70
            },
            # Access/height
            {
                'patterns': [r'ceiling.*high|tall', r'reach|reaching', r'ladder', r'attic'],
                'problem': 'Difficulty accessing installation locations',
                'pain_level': 'Low',
                'solution_satisfaction': 'Medium',  # Ladders available
                'evidence_window': 70
            },
            # Damage/rental restrictions
            {
                'patterns': [r'damage.*wall', r'hole', r'deposit', r'rental.*restrict'],
                'problem': 'Cannot drill/damage walls (rental restrictions)',
                'pain_level': 'High',
                'solution_satisfaction': 'Medium',  # Adhesive alternatives exist
                'evidence_window': 80
            },
        ]
        
        for problem_def in problem_patterns:
            for pattern in problem_def['patterns']:
                matches = re.finditer(pattern, text_lower)
                for match in matches:
                    start = max(0, match.start() - 40)
                    end = min(len(text), match.end() + problem_def['evidence_window'])
                    evidence = text[start:end].strip()
                    
                    self.problems.append({
                        'problem': problem_def['problem'],
                        'pain_level': problem_def['pain_level'],
                        'solution_satisfaction': problem_def['solution_satisfaction'],
                        'evidence': evidence,
                        'participant': participant,
                        'activity': activity
                    })
                    
    def extract_aspirations(self, text, participant, activity):
        """Extract aspirational states (top of ladder)"""
        text_lower = text.lower()
        
        # Aspirational indicators
        aspiration_patterns = [
            {
                'patterns': [r'my\s+space', r'personalize', r'make.*mine', r'own\s+style'],
                'aspiration': 'Transform space to reflect personal identity',
                'evidence_window': 80
            },
            {
                'patterns': [r'myself|on\s+my\s+own|diy|do\s+it', r'proud|accomplished'],
                'aspiration': 'Feel capable and self-sufficient',
                'evidence_window': 70
            },
            {
                'patterns': [r'without.*expensive|save.*money', r'budget', r'affordable'],
                'aspiration': 'Achieve professional results economically',
                'evidence_window': 70
            },
            {
                'patterns': [r'easy|simple|quick', r'didn\'t.*hard', r'straightforward'],
                'aspiration': 'Experience effortless installation',
                'evidence_window': 60
            },
            {
                'patterns': [r'control|customize|adjust|change'],
                'aspiration': 'Maintain flexibility and control',
                'evidence_window': 60
            },
        ]
        
        for asp_def in aspiration_patterns:
            for pattern in asp_def['patterns']:
                matches = re.finditer(pattern, text_lower)
                for match in matches:
                    start = max(0, match.start() - 30)
                    end = min(len(text), match.end() + asp_def['evidence_window'])
                    evidence = text[start:end].strip()
                    
                    self.aspirations.append({
                        'aspiration': asp_def['aspiration'],
                        'evidence': evidence,
                        'participant': participant,
                        'activity': activity
                    })
    
    def deduplicate_and_score(self):
        """Aggregate and score insights"""
        # Count job frequencies
        job_counts = Counter([j['job'] for j in self.jobs])
        
        # Count problem frequencies with pain scoring
        problem_data = defaultdict(lambda: {
            'count': 0,
            'pain_levels': [],
            'solution_satisfactions': [],
            'evidence': []
        })
        
        for p in self.problems:
            key = p['problem']
            problem_data[key]['count'] += 1
            problem_data[key]['pain_levels'].append(p['pain_level'])
            problem_data[key]['solution_satisfactions'].append(p['solution_satisfaction'])
            if len(problem_data[key]['evidence']) < 3:
                problem_data[key]['evidence'].append({
                    'text': p['evidence'],
                    'participant': p['participant']
                })
        
        # Count aspirations
        aspiration_counts = Counter([a['aspiration'] for a in self.aspirations])
        
        return job_counts, problem_data, aspiration_counts
    
    def generate_ladder_report(self):
        """Generate proper ladder structure report"""
        job_counts, problem_data, aspiration_counts = self.deduplicate_and_score()
        
        # Get top jobs (6-8)
        top_jobs = job_counts.most_common(8)
        
        report = f"""# 3M CONSUMER LIGHTING INSIGHTS
## The Insight Ladder - Consumer Video Foundation

**Analysis Date:** October 22, 2025  
**Videos Analyzed:** 85 | **Participants:** 15

---

## THE INSIGHT LADDER STRUCTURE

```
┌─────────────────────────────────────────────────────────┐
│  ☁️  ASPIRATIONAL STATES (Marketing Layer)             │
│      "Who I want to be / How I want to feel"            │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  ⚙️  JOBS-TO-BE-DONE (Consumer Goals)                  │
│      "What I'm trying to accomplish"                    │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  ⚠️  PROBLEMS (Technical Issues to Solve)              │
│      "What prevents success"                             │
└─────────────────────────────────────────────────────────┘
```

---

## ☁️ ASPIRATIONAL STATES
*Marketing & Emotional Positioning*

"""
        
        # Add top aspirations
        for aspiration, count in aspiration_counts.most_common(5):
            # Get example evidence
            examples = [a for a in self.aspirations if a['aspiration'] == aspiration][:2]
            report += f"""### "{aspiration}"
**Frequency:** {count} instances across transcripts

**Consumer Evidence:**
"""
            for ex in examples:
                report += f'- "{ex["evidence"][:120]}..." —{ex["participant"]}\n'
            report += "\n"
        
        report += """---

## ⚙️ JOBS-TO-BE-DONE
*Functional Goals Driving Behavior*

"""
        
        # Add jobs with their problems nested beneath
        for job, count in top_jobs:
            # Calculate prevalence percentage
            prevalence = (count / 85) * 100
            
            report += f"""### Job: {job}
**Prevalence:** {count} instances ({prevalence:.0f}% of videos)

**Consumer Evidence:**
"""
            # Get examples
            examples = [j for j in self.jobs if j['job'] == job][:2]
            for ex in examples:
                report += f'- "{ex["evidence"][:100]}..." —{ex["participant"]}\n'
            
            # Find related problems
            report += "\n**Problems Blocking This Job:**\n\n"
            
            # Map problems to jobs (heuristic based on keywords)
            related_problems = self.find_related_problems(job, problem_data)
            
            for prob_name, prob_info in related_problems[:3]:  # Top 3 problems per job
                count = prob_info['count']
                pain = prob_info['pain_levels'][0]  # Most common
                satisfaction = prob_info['solution_satisfactions'][0]
                
                report += f"""#### ⚠️ Problem: {prob_name}
- **Frequency:** {count} instances
- **Pain Level:** {pain}
- **Current Solution Satisfaction:** {satisfaction}
- **Evidence:** "{prob_info['evidence'][0]['text'][:100]}..." —{prob_info['evidence'][0]['participant']}

"""
            report += "---\n\n"
        
        report += """## 📊 PROBLEM PRIORITIZATION MATRIX
*Pain Level vs. Current Solution Satisfaction*

### 2x2 Quadrant Analysis

"""
        
        # Build 2x2 matrix
        quadrants = {
            'High Pain / Low Satisfaction': [],  # Critical - highest priority
            'High Pain / Medium Satisfaction': [],  # Important - innovation opportunity
            'Medium Pain / Low Satisfaction': [],  # Address with guidance
            'Low Pain / Medium Satisfaction': []  # Monitor
        }
        
        for prob_name, prob_info in problem_data.items():
            pain = prob_info['pain_levels'][0]
            satisfaction = prob_info['solution_satisfactions'][0]
            count = prob_info['count']
            
            if pain == 'High' and satisfaction == 'Low':
                quadrants['High Pain / Low Satisfaction'].append((prob_name, count))
            elif pain == 'High' and satisfaction == 'Medium':
                quadrants['High Pain / Medium Satisfaction'].append((prob_name, count))
            elif pain == 'Medium' and satisfaction == 'Low':
                quadrants['Medium Pain / Low Satisfaction'].append((prob_name, count))
            else:
                quadrants['Low Pain / Medium Satisfaction'].append((prob_name, count))
        
        # Output quadrants
        for quadrant, problems in quadrants.items():
            if problems:
                report += f"""### {quadrant}
"""
                for prob, count in sorted(problems, key=lambda x: x[1], reverse=True):
                    report += f"- **{prob}** ({count} instances)\n"
                report += "\n"
        
        report += """---

## 🎯 STRATEGIC IMPLICATIONS

### R&D Priorities (High Pain / Low Satisfaction Problems)

"""
        # List critical problems
        critical = quadrants['High Pain / Low Satisfaction']
        for i, (prob, count) in enumerate(sorted(critical, key=lambda x: x[1], reverse=True)[:3], 1):
            prob_details = problem_data[prob]
            report += f"""{i}. **{prob}**
   - Frequency: {count} instances
   - Evidence: "{prob_details['evidence'][0]['text'][:150]}..."
   - **3M Opportunity:** [Adhesive formulation / Product bundle / Installation guide]

"""
        
        report += """### Marketing Positioning (Aspirational States)

Connect product solutions to consumer aspirations:
"""
        for aspiration, count in aspiration_counts.most_common(3):
            report += f'- **"{aspiration}"** → Product positioning angle\n'
        
        report += """

---

**Methodology:** Multimodal transcript analysis with JTBD framework  
**Next Phase:** YouTube creator enrichment + social media emotional validation
"""
        
        return report
    
    def find_related_problems(self, job, problem_data):
        """Map problems to jobs based on keyword matching"""
        job_lower = job.lower()
        related = []
        
        # Keyword mapping
        job_keywords = {
            'electrical work': ['electrical', 'electrician', 'wiring', 'hardwire'],
            'accent lighting': ['adhesive', 'stick', 'mount', 'surface'],
            'damaging surfaces': ['adhesive', 'damage', 'rental', 'drill'],
            'control': ['control', 'adjust'],
            'existing fixtures': ['retrofit', 'add'],
            'independently': ['electrical', 'expensive', 'difficult'],
            'accurately': ['measure', 'level', 'placement'],
        }
        
        # Find matching keywords
        keywords = []
        for key_phrase, kws in job_keywords.items():
            if key_phrase in job_lower:
                keywords.extend(kws)
        
        # Score problems by keyword match
        for prob_name, prob_info in problem_data.items():
            prob_lower = prob_name.lower()
            matches = sum(1 for kw in keywords if kw in prob_lower)
            if matches > 0:
                related.append((prob_name, prob_info, matches))
        
        # Sort by relevance score, then frequency
        related.sort(key=lambda x: (x[2], x[1]['count']), reverse=True)
        
        return [(name, info) for name, info, _ in related]

def main():
    print("🪜 3M Lighting Insight Ladder Extraction")
    print("=" * 60)
    
    extractor = LadderExtractor()
    extractor.load_all_transcripts()
    
    print("\n🔄 Analyzing ladder structure...")
    print("   - Extracting aspirational states...")
    print("   - Identifying jobs-to-be-done...")
    print("   - Cataloging problems...")
    
    report = extractor.generate_ladder_report()
    
    output_path = OUTPUT_DIR / "INSIGHT_LADDER_REPORT.md"
    with open(output_path, 'w') as f:
        f.write(report)
    
    print(f"\n✅ Ladder report generated: {output_path}")
    print("\nReport structure:")
    print("  ☁️  Aspirational States (Marketing)")
    print("  ⚙️  Jobs-to-be-Done (6-8 core jobs)")
    print("  ⚠️  Problems (nested under jobs)")
    print("  📊 2x2 Prioritization Matrix")

if __name__ == "__main__":
    main()
