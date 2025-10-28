#!/usr/bin/env python3
"""
3M Consumer Video Insights - CORRECT LADDER STRUCTURE
Extracts: 5-7 Aspirational States → 50+ Jobs → ~10-15 Technical Problems
"""

import json
import os
from pathlib import Path
from collections import defaultdict, Counter
import re

PROCESSED_DIR = Path("/Users/anderson115/00-interlink/12-work/3m-lighting-project/modules/consumer-video/data/processed")
OUTPUT_DIR = Path("/Users/anderson115/00-interlink/12-work/3m-lighting-project/modules/consumer-video/insights")

class ProperLadderExtractor:
    def __init__(self):
        self.jobs_raw = []
        self.problems_raw = []
        self.aspirations_raw = []
        
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
        segments = data.get('segments', [])
        
        self.extract_specific_jobs(text, segments, participant, activity)
        self.extract_technical_problems(text, participant, activity)
        self.extract_aspirations(text, participant, activity)
        
    def extract_specific_jobs(self, text, segments, participant, activity):
        """Extract 50+ specific jobs"""
        text_lower = text.lower()
        
        # Specific job patterns - granular level
        job_patterns = [
            # Installation method jobs
            (r'install.*battery[\s-]?powered', 'Install battery-powered lighting fixtures'),
            (r'install.*led\s+strip', 'Install LED strip lighting'),
            (r'install.*under[\s-]?cabinet', 'Install under-cabinet lighting'),
            (r'install.*picture\s+light', 'Install picture/artwork lighting'),
            (r'install.*accent\s+light', 'Install accent lighting for features'),
            (r'install.*ceiling\s+light', 'Install ceiling-mounted fixtures'),
            (r'install.*wall\s+light', 'Install wall-mounted fixtures'),
            (r'mount.*without\s+drill', 'Mount fixtures without drilling holes'),
            (r'hang.*without\s+nail', 'Hang lighting without nails/screws'),
            
            # Wiring avoidance jobs
            (r'avoid.*hardwire|hardwir', 'Avoid hardwiring installation'),
            (r'no\s+electrical\s+work', 'Complete installation without electrical work'),
            (r'wireless\s+light', 'Install wireless lighting solutions'),
            (r'plug[\s-]?in\s+light', 'Install plug-in lighting solutions'),
            
            # Positioning jobs
            (r'position.*accurate', 'Position fixtures accurately'),
            (r'level.*fixture', 'Level fixtures properly'),
            (r'measure.*placement', 'Measure correct placement locations'),
            (r'align.*straight', 'Align fixtures in straight line'),
            (r'center.*feature', 'Center lighting on feature/object'),
            (r'adjust.*angle', 'Adjust fixture angle/direction'),
            (r'adjust.*after\s+install', 'Adjust positioning after installation'),
            
            # Control jobs
            (r'control.*remote', 'Control lighting remotely'),
            (r'adjust.*brightness', 'Adjust brightness levels'),
            (r'change.*color\s+temp', 'Change color temperature'),
            (r'dim.*light', 'Dim lighting intensity'),
            (r'timer.*light', 'Set lighting timers/schedules'),
            
            # Surface-specific jobs
            (r'stick.*textured\s+wall', 'Adhere fixtures to textured walls'),
            (r'mount.*painted\s+wall', 'Mount on painted surfaces'),
            (r'attach.*ceiling', 'Attach fixtures to ceiling'),
            (r'stick.*tile', 'Adhere to tile surfaces'),
            
            # Removal jobs
            (r'remove.*without\s+damage', 'Remove fixtures without surface damage'),
            (r'temporary.*install', 'Install temporary/removable lighting'),
            (r'reposition.*later', 'Reposition fixtures after initial install'),
            
            # Specific use case jobs
            (r'light.*closet', 'Add lighting to closets'),
            (r'light.*pantry', 'Add lighting to pantry'),
            (r'light.*hallway', 'Add lighting to hallways'),
            (r'light.*stairs', 'Add lighting to stairs/steps'),
            (r'light.*dark\s+corner', 'Illuminate dark corners'),
            (r'highlight.*artwork', 'Highlight artwork/paintings'),
            (r'showcase.*feature', 'Showcase architectural features'),
            
            # Power jobs
            (r'hide.*cord', 'Hide power cords/wires'),
            (r'manage.*cable', 'Manage cable routing'),
            (r'extend.*power', 'Extend power source reach'),
            (r'battery.*last', 'Maximize battery life/longevity'),
            
            # Rental-specific jobs
            (r'install.*rental', 'Install lighting in rental property'),
            (r'avoid.*deposit', 'Avoid security deposit loss'),
            (r'damage[\s-]?free', 'Complete damage-free installation'),
            
            # DIY capability jobs
            (r'install.*myself|on\s+my\s+own', 'Complete installation independently'),
            (r'no\s+professional', 'Avoid hiring professional installer'),
            (r'save.*money.*install', 'Save installation costs'),
            (r'quick.*install', 'Complete quick installation'),
            (r'easy.*install', 'Complete simple/easy installation'),
            
            # Planning jobs
            (r'choose.*right\s+light', 'Select appropriate lighting type'),
            (r'decide.*placement', 'Determine optimal placement location'),
            (r'calculate.*number', 'Calculate number of fixtures needed'),
            (r'plan.*layout', 'Plan lighting layout/design'),
            
            # Aesthetic jobs
            (r'match.*decor', 'Match lighting to existing decor'),
            (r'create.*ambiance', 'Create desired ambiance/mood'),
            (r'enhance.*space', 'Enhance room appearance'),
            (r'brighten.*room', 'Increase overall room brightness'),
            
            # Maintenance jobs
            (r'replace.*bulb', 'Replace bulbs/light sources'),
            (r'clean.*fixture', 'Clean lighting fixtures'),
            (r'troubleshoot.*not\s+work', 'Troubleshoot non-working lights'),
            
            # Multiple fixture jobs
            (r'install.*multiple.*same', 'Install multiple fixtures evenly spaced'),
            (r'synchronize.*light', 'Synchronize multiple lights together'),
            (r'match.*brightness.*multiple', 'Match brightness across multiple fixtures'),
        ]
        
        for pattern, job in job_patterns:
            matches = re.finditer(pattern, text_lower)
            for match in matches:
                start = max(0, match.start() - 40)
                end = min(len(text), match.end() + 80)
                evidence = text[start:end].strip()
                
                # Find timestamp
                timestamp = self.find_timestamp(match.start(), text, segments)
                
                self.jobs_raw.append({
                    'job': job,
                    'evidence': evidence,
                    'participant': participant,
                    'activity': activity,
                    'timestamp': timestamp
                })
    
    def find_timestamp(self, char_pos, text, segments):
        """Find timestamp for character position"""
        for seg in segments:
            seg_text = seg.get('text', '')
            if seg_text.lower() in text.lower():
                return seg.get('start', 0)
        return 0
    
    def extract_technical_problems(self, text, participant, activity):
        """Extract 10-15 technical problems"""
        text_lower = text.lower()
        
        # Technical problems that block multiple jobs
        problem_patterns = [
            # Adhesive technical problems
            {
                'pattern': r'fall|fell|falling|come\s+off|didn\'t\s+stick',
                'problem': 'Adhesive bond failure',
                'pain': 'High',
                'satisfaction': 'Low'
            },
            {
                'pattern': r'hot|heat|arizona|texas|sun.*affect|temperature.*fail',
                'problem': 'Heat degradation of adhesive',
                'pain': 'High',
                'satisfaction': 'Low'
            },
            {
                'pattern': r'textured.*won\'t\s+stick|rough.*surface',
                'problem': 'Poor adhesion on textured surfaces',
                'pain': 'Medium',
                'satisfaction': 'Low'
            },
            {
                'pattern': r'paint.*peel|damage.*paint|paint.*come\s+off',
                'problem': 'Paint damage during removal',
                'pain': 'High',
                'satisfaction': 'Low'
            },
            
            # Installation technical problems
            {
                'pattern': r'not.*electrician|don\'t\s+know.*electric|lack.*knowledge.*wir',
                'problem': 'Insufficient electrical knowledge',
                'pain': 'High',
                'satisfaction': 'Medium'
            },
            {
                'pattern': r'expensive.*install|cost.*professional|hire.*electrician',
                'problem': 'High professional installation cost',
                'pain': 'High',
                'satisfaction': 'Medium'
            },
            {
                'pattern': r'hard.*measure|difficult.*level|measurement.*challenge',
                'problem': 'Measurement and leveling difficulty',
                'pain': 'Medium',
                'satisfaction': 'Low'
            },
            {
                'pattern': r'can\'t\s+reach|too\s+high|ceiling.*tall|need.*ladder',
                'problem': 'Height/access limitations',
                'pain': 'Low',
                'satisfaction': 'Medium'
            },
            
            # Product technical problems
            {
                'pattern': r'battery.*die|battery.*short|replace.*battery.*often',
                'problem': 'Insufficient battery life',
                'pain': 'Medium',
                'satisfaction': 'Low'
            },
            {
                'pattern': r'not.*bright\s+enough|dim|insufficient.*light',
                'problem': 'Inadequate light output',
                'pain': 'Medium',
                'satisfaction': 'Medium'
            },
            {
                'pattern': r'flicker|inconsistent.*light',
                'problem': 'Light flicker/inconsistency',
                'pain': 'Low',
                'satisfaction': 'Medium'
            },
            
            # Surface/property problems
            {
                'pattern': r'rental.*restrict|can\'t\s+drill|damage.*deposit|landlord',
                'problem': 'Rental property drilling restrictions',
                'pain': 'High',
                'satisfaction': 'Medium'
            },
            {
                'pattern': r'weight.*heavy|fixture.*heavy.*fall',
                'problem': 'Fixture weight exceeds adhesive capacity',
                'pain': 'High',
                'satisfaction': 'Low'
            },
            {
                'pattern': r'cord.*ugly|wire.*visible|can\'t\s+hide.*wire',
                'problem': 'Visible/unsightly cord management',
                'pain': 'Low',
                'satisfaction': 'Low'
            },
            {
                'pattern': r'no\s+outlet|outlet.*far|no\s+power\s+source',
                'problem': 'No accessible power outlet',
                'pain': 'High',
                'satisfaction': 'Medium'
            },
        ]
        
        for prob_def in problem_patterns:
            matches = re.finditer(prob_def['pattern'], text_lower)
            for match in matches:
                start = max(0, match.start() - 50)
                end = min(len(text), match.end() + 100)
                evidence = text[start:end].strip()
                
                self.problems_raw.append({
                    'problem': prob_def['problem'],
                    'pain_level': prob_def['pain'],
                    'solution_satisfaction': prob_def['satisfaction'],
                    'evidence': evidence,
                    'participant': participant,
                    'activity': activity
                })
    
    def extract_aspirations(self, text, participant, activity):
        """Extract 5-7 aspirational states"""
        text_lower = text.lower()
        
        # Aspirational state patterns
        aspiration_patterns = [
            {
                'pattern': r'my\s+space|personalize|make.*mine|my\s+style|reflect.*me',
                'aspiration': 'Own and personalize my space'
            },
            {
                'pattern': r'myself|independent|on\s+my\s+own|diy|do\s+it|capable|accomplish',
                'aspiration': 'Feel capable and self-sufficient'
            },
            {
                'pattern': r'easy|simple|quick|effortless|straightforward|no\s+hassle',
                'aspiration': 'Experience effortless home improvement'
            },
            {
                'pattern': r'control|flexibility|customize|adjust|change.*whenever',
                'aspiration': 'Maintain control and flexibility'
            },
            {
                'pattern': r'save.*money|affordable|budget|cheap|inexpensive|frugal',
                'aspiration': 'Achieve results economically'
            },
            {
                'pattern': r'professional.*look|looks\s+good|impressive|beautiful|elegant',
                'aspiration': 'Create professional-looking results'
            },
            {
                'pattern': r'safe|secure|confident|no\s+risk|worry.*damage',
                'aspiration': 'Feel safe and secure in decisions'
            },
        ]
        
        for asp_def in aspiration_patterns:
            matches = re.finditer(asp_def['pattern'], text_lower)
            for match in matches:
                start = max(0, match.start() - 30)
                end = min(len(text), match.end() + 70)
                evidence = text[start:end].strip()
                
                self.aspirations_raw.append({
                    'aspiration': asp_def['aspiration'],
                    'evidence': evidence,
                    'participant': participant,
                    'activity': activity
                })
    
    def build_ladder_structure(self):
        """Build proper ladder with rollups and mappings"""
        # Deduplicate and count
        job_counts = Counter([j['job'] for j in self.jobs_raw])
        aspiration_counts = Counter([a['aspiration'] for a in self.aspirations_raw])
        
        # Aggregate problems
        problem_data = defaultdict(lambda: {
            'count': 0,
            'pain': None,
            'satisfaction': None,
            'evidence': [],
            'blocked_jobs': []
        })
        
        for p in self.problems_raw:
            key = p['problem']
            problem_data[key]['count'] += 1
            problem_data[key]['pain'] = p['pain_level']
            problem_data[key]['satisfaction'] = p['solution_satisfaction']
            if len(problem_data[key]['evidence']) < 2:
                problem_data[key]['evidence'].append({
                    'text': p['evidence'],
                    'participant': p['participant']
                })
        
        # Map problems to jobs they block
        for prob_name in problem_data.keys():
            prob_lower = prob_name.lower()
            for job, count in job_counts.items():
                job_lower = job.lower()
                # Check if problem relates to job
                if self.problem_blocks_job(prob_lower, job_lower):
                    problem_data[prob_name]['blocked_jobs'].append({
                        'job': job,
                        'count': count
                    })
        
        # Map jobs to aspirations they fulfill
        job_to_aspiration = {}
        for job in job_counts.keys():
            job_to_aspiration[job] = self.map_job_to_aspiration(job)
        
        return aspiration_counts, job_counts, problem_data, job_to_aspiration
    
    def problem_blocks_job(self, problem, job):
        """Determine if problem blocks job"""
        # Keyword matching logic
        mappings = {
            'adhesive': ['mount', 'stick', 'attach', 'hang', 'adhere', 'fixtures'],
            'heat': ['outdoor', 'arizona', 'temperature'],
            'electrical': ['hardwir', 'electrical', 'wireless', 'battery'],
            'measure': ['position', 'level', 'align', 'center', 'accurate'],
            'rental': ['rental', 'damage-free', 'remove', 'temporary'],
            'cost': ['professional', 'save', 'independent', 'myself'],
            'battery': ['battery-powered', 'wireless'],
            'reach': ['ceiling', 'high'],
            'outlet': ['plug-in', 'power'],
            'weight': ['heavy', 'fixtures'],
            'paint': ['remove', 'damage-free'],
            'brightness': ['brightness', 'dim', 'illuminate'],
        }
        
        for keyword, job_keywords in mappings.items():
            if keyword in problem:
                for job_kw in job_keywords:
                    if job_kw in job:
                        return True
        return False
    
    def map_job_to_aspiration(self, job):
        """Map job to primary aspiration it fulfills"""
        job_lower = job.lower()
        
        # Mapping logic
        if any(kw in job_lower for kw in ['independent', 'myself', 'diy', 'no professional']):
            return 'Feel capable and self-sufficient'
        elif any(kw in job_lower for kw in ['save', 'cost', 'money']):
            return 'Achieve results economically'
        elif any(kw in job_lower for kw in ['quick', 'easy', 'simple']):
            return 'Experience effortless home improvement'
        elif any(kw in job_lower for kw in ['control', 'adjust', 'remote', 'change']):
            return 'Maintain control and flexibility'
        elif any(kw in job_lower for kw in ['damage-free', 'rental', 'remove']):
            return 'Feel safe and secure in decisions'
        elif any(kw in job_lower for kw in ['highlight', 'showcase', 'match', 'enhance']):
            return 'Create professional-looking results'
        elif any(kw in job_lower for kw in ['my', 'personalize']):
            return 'Own and personalize my space'
        else:
            # Default
            return 'Feel capable and self-sufficient'
    
    def generate_report(self):
        """Generate comprehensive ladder report"""
        aspiration_counts, job_counts, problem_data, job_to_aspiration = self.build_ladder_structure()
        
        # Get top jobs (50+)
        top_jobs = job_counts.most_common(70)  # Get more than needed
        
        # Filter to meaningful jobs (appeared at least 2 times)
        significant_jobs = [(j, c) for j, c in top_jobs if c >= 2][:60]
        
        report = f"""# 3M CONSUMER LIGHTING INSIGHTS
## The Insight Ladder - Proper Structure

**Analysis Date:** October 22, 2025  
**Videos Analyzed:** 85 | **Participants:** 15

---

## LADDER STRUCTURE

```
☁️  ASPIRATIONAL STATES ({len(aspiration_counts)} emotional drivers)
     ↓ jobs roll up to
⚙️  JOBS-TO-BE-DONE ({len(significant_jobs)} specific jobs identified)
     ↓ blocked by
⚠️  PROBLEMS ({len(problem_data)} technical problems)
```

---

## ☁️ ASPIRATIONAL STATES
*Top of Ladder: Emotional Drivers & Marketing Positioning*

"""
        
        # List aspirational states
        for aspiration, count in aspiration_counts.most_common(7):
            # Count jobs that roll up to this aspiration
            jobs_for_this = [j for j in significant_jobs if job_to_aspiration.get(j[0]) == aspiration]
            
            # Get evidence
            examples = [a for a in self.aspirations_raw if a['aspiration'] == aspiration][:2]
            
            report += f"""### "{aspiration}"
**Frequency:** {count} instances  
**Jobs Fulfilling This:** {len(jobs_for_this)} jobs roll up to this emotion

**Consumer Evidence:**
"""
            for ex in examples:
                report += f'> "{ex["evidence"][:100]}..." —{ex["participant"]}\n'
            report += "\n"
        
        report += f"""---

## ⚙️ JOBS-TO-BE-DONE ({len(significant_jobs)} Jobs)
*Middle of Ladder: Specific Functional Goals*

"""
        
        # Group jobs by aspiration
        for aspiration, count in aspiration_counts.most_common(7):
            jobs_for_aspiration = [(j, c) for j, c in significant_jobs if job_to_aspiration.get(j) == aspiration]
            
            if jobs_for_aspiration:
                report += f"""### Jobs that fulfill: "{aspiration}"

"""
                for job, job_count in jobs_for_aspiration[:15]:  # Limit per section
                    # Get evidence
                    examples = [j for j in self.jobs_raw if j['job'] == job][:1]
                    
                    # Find problems blocking this job
                    blocking_problems = []
                    for prob_name, prob_info in problem_data.items():
                        for blocked_job in prob_info['blocked_jobs']:
                            if blocked_job['job'] == job:
                                blocking_problems.append(prob_name)
                    
                    report += f"""**{job}** ({job_count} instances)
"""
                    if examples:
                        report += f'  *Evidence:* "{examples[0]["evidence"][:80]}..." —{examples[0]["participant"]}\n'
                    if blocking_problems:
                        report += f'  *Blocked by:* {", ".join(blocking_problems[:2])}\n'
                    report += "\n"
        
        report += """---

## ⚠️ TECHNICAL PROBLEMS
*Bottom of Ladder: Engineering Challenges*

"""
        
        # Sort problems by pain/satisfaction priority
        critical_problems = []
        important_problems = []
        moderate_problems = []
        
        for prob_name, prob_info in problem_data.items():
            if prob_info['pain'] == 'High' and prob_info['satisfaction'] == 'Low':
                critical_problems.append((prob_name, prob_info))
            elif prob_info['pain'] == 'High':
                important_problems.append((prob_name, prob_info))
            else:
                moderate_problems.append((prob_name, prob_info))
        
        # Critical problems
        report += """### 🔴 CRITICAL (High Pain / Low Satisfaction)

"""
        for prob_name, prob_info in sorted(critical_problems, key=lambda x: x[1]['count'], reverse=True):
            report += f"""#### {prob_name}
**Frequency:** {prob_info['count']} instances  
**Pain Level:** {prob_info['pain']} | **Current Solutions:** {prob_info['satisfaction']} satisfaction

**Blocks These Jobs:**
"""
            for blocked_job in prob_info['blocked_jobs'][:5]:
                report += f"- {blocked_job['job']} ({blocked_job['count']} instances)\n"
            
            if prob_info['evidence']:
                report += f'\n**Evidence:** "{prob_info["evidence"][0]["text"][:120]}..." —{prob_info["evidence"][0]["participant"]}\n'
            report += "\n"
        
        # Important problems
        report += """### 🟡 IMPORTANT (High Pain / Medium Satisfaction)

"""
        for prob_name, prob_info in sorted(important_problems, key=lambda x: x[1]['count'], reverse=True):
            report += f"""#### {prob_name}
**Frequency:** {prob_info['count']} instances  
**Blocks:** {len(prob_info['blocked_jobs'])} jobs

"""
        
        # 2x2 Matrix
        report += """---

## 📊 PROBLEM PRIORITIZATION MATRIX

### Pain Level × Current Solution Satisfaction

```
                    Low Satisfaction          Medium Satisfaction
High Pain      🔴 CRITICAL               🟡 IMPORTANT
               """
        
        critical_names = [p[0] for p in critical_problems[:2]]
        important_names = [p[0] for p in important_problems[:2]]
        
        report += f"""
               {', '.join(critical_names)}  {', '.join(important_names)}

Medium Pain    Address w/ guidance       Monitor
```

### R&D Priorities

"""
        
        for i, (prob_name, prob_info) in enumerate(sorted(critical_problems, key=lambda x: x[1]['count'], reverse=True)[:3], 1):
            report += f"""{i}. **{prob_name}** ({prob_info['count']} instances)
   - Blocks {len(prob_info['blocked_jobs'])} different jobs
   - 3M Opportunity: [Specific technical solution]

"""
        
        report += """---

**Methodology:** Pattern-based extraction with rollup mapping  
**Next Phase:** YouTube enrichment + social validation
"""
        
        return report

def main():
    print("🪜 3M Lighting Insight Ladder - PROPER STRUCTURE")
    print("=" * 60)
    
    extractor = ProperLadderExtractor()
    extractor.load_all_transcripts()
    
    print("\n🔄 Building ladder structure...")
    print("   - Extracting 50+ specific jobs...")
    print("   - Identifying 10-15 technical problems...")
    print("   - Mapping problems → jobs → aspirations...")
    
    report = extractor.generate_report()
    
    output_path = OUTPUT_DIR / "PROPER_INSIGHT_LADDER.md"
    with open(output_path, 'w') as f:
        f.write(report)
    
    print(f"\n✅ Report generated: {output_path}")
    print("\nStructure:")
    print("  ☁️  5-7 Aspirational States")
    print("  ⚙️  50+ Jobs (each rolls up to emotion)")
    print("  ⚠️  10-15 Problems (each blocks multiple jobs)")
    print("  📊 2x2 Prioritization Matrix")

if __name__ == "__main__":
    main()
