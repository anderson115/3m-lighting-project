#!/usr/bin/env python3
"""
Jobs-to-be-Done "Rungs of the Ladder" Analysis
Analyzes all consumer video transcripts to extract and categorize jobs
"""

from config import PATHS

import json
from pathlib import Path
from collections import defaultdict
import re

# Directory containing processed videos
PROCESSED_DIR = Path(PATHS["processed"])

class JTBDAnalyzer:
    def __init__(self):
        self.jobs = {
            "functional": [],  # Bottom rung: What they're trying to accomplish
            "emotional": [],   # Middle rungs: How they want to feel
            "social": []       # Top rungs: How they want to be perceived
        }
        self.consumer_counts = defaultdict(int)

    def load_transcript(self, transcript_path):
        """Load a transcript JSON file"""
        with open(transcript_path, 'r') as f:
            return json.load(f)

    def extract_consumer_name(self, folder_name):
        """Extract consumer name from folder"""
        # Format: ConsumerName_ActivityN_timestamp
        return folder_name.split('_')[0]

    def analyze_transcript(self, folder_path):
        """Analyze a single transcript for JTBD"""
        transcript_path = folder_path / "transcript.json"
        if not transcript_path.exists():
            return

        transcript = self.load_transcript(transcript_path)
        full_text = transcript.get("text", "")
        consumer_name = self.extract_consumer_name(folder_path.name)
        source_file = folder_path.name

        # Analyze for Functional Jobs (bottom rung)
        self.extract_functional_jobs(full_text, consumer_name, source_file)

        # Analyze for Emotional Jobs (middle rungs)
        self.extract_emotional_jobs(full_text, consumer_name, source_file)

        # Analyze for Social Jobs (top rungs)
        self.extract_social_jobs(full_text, consumer_name, source_file)

    def extract_functional_jobs(self, text, consumer, source):
        """Extract functional jobs - what they're trying to accomplish"""

        # Patterns indicating functional jobs
        functional_patterns = [
            # Lighting tasks
            (r"(?i)(add|install|put up|set up|create)\s+(?:accent\s+)?light(?:ing)?", "Install/Add Lighting"),
            (r"(?i)light(?:ing)?\s+(?:up|the)\s+(?:art|picture|painting|fireplace|mantel|wall)", "Light Up Art/Features"),
            (r"(?i)draw attention to", "Draw Attention"),
            (r"(?i)highlight(?:ing)?", "Highlight Features"),
            (r"(?i)illuminate", "Illuminate Space"),

            # Avoiding electrical work
            (r"(?i)(avoid|didn't want|don't want|no need for).*(?:electrician|electrical work|hard(?:wire|wiring)|wires)", "Avoid Electrician/Wiring"),

            # Installation/DIY
            (r"(?i)(DIY|do it myself|install myself)", "DIY Installation"),
            (r"(?i)easy\s+(?:to\s+)?install", "Easy Installation"),

            # Control/features
            (r"(?i)(motion\s+detect|remote control|control|adjust|dim)", "Control Lighting"),
            (r"(?i)(battery|rechargeable|wireless|cordless)", "Avoid Cords/Wiring"),
        ]

        for pattern, job_category in functional_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                # Get context around the match (50 chars before and after)
                start = max(0, match.start() - 100)
                end = min(len(text), match.end() + 100)
                context = text[start:end].strip()

                # Find the sentence containing the match
                sentences = re.split(r'[.!?]', text)
                matching_sentence = ""
                for sentence in sentences:
                    if match.group() in sentence:
                        matching_sentence = sentence.strip()
                        break

                if matching_sentence:
                    self.jobs["functional"].append({
                        "job": job_category,
                        "quote": matching_sentence,
                        "consumer": consumer,
                        "source": source,
                        "context": context
                    })
                    self.consumer_counts[consumer] += 1

    def extract_emotional_jobs(self, text, consumer, source):
        """Extract emotional jobs - how they want to feel"""

        emotional_patterns = [
            # Cost/affordability
            (r"(?i)(save money|inexpensive|affordable|didn't have to invest much|low cost|cost effective)", "Save Money/Be Frugal"),
            (r"(?i)(expensive|cost|thousand dollars)", "Avoid High Costs"),

            # Confidence/capability
            (r"(?i)(I can do|figured it out|wasn't too difficult|wasn't too hard|pretty easy)", "Feel Capable"),
            (r"(?i)(proud|accomplished|satisfied)", "Feel Accomplished"),

            # Aesthetics/beauty
            (r"(?i)(looks? (?:good|great|nice|cool|beautiful|finished))", "Looks Good/Finished"),
            (r"(?i)(modern|luxury|elegant|classic|sophisticated)", "Achieve Desired Aesthetic"),

            # Simplicity/ease
            (r"(?i)(simple|easy|straightforward|no hassle)", "Keep It Simple"),

            # Avoiding problems
            (r"(?i)(no wires hanging|hide (?:the )?(?:cords?|wires?)|clean look)", "Achieve Clean Look"),
            (r"(?i)(regret|wish I had|should have|would have done differently)", "Avoid Regret"),
        ]

        for pattern, job_category in emotional_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                sentences = re.split(r'[.!?]', text)
                matching_sentence = ""
                for sentence in sentences:
                    if match.group() in sentence:
                        matching_sentence = sentence.strip()
                        break

                if matching_sentence:
                    self.jobs["emotional"].append({
                        "job": job_category,
                        "quote": matching_sentence,
                        "consumer": consumer,
                        "source": source
                    })
                    self.consumer_counts[consumer] += 1

    def extract_social_jobs(self, text, consumer, source):
        """Extract social jobs - how they want to be perceived"""

        social_patterns = [
            # Identity/image
            (r"(?i)(modern|contemporary|luxury|high-end|sophisticated|upscale)", "Appear Modern/Sophisticated"),
            (r"(?i)(creative|artistic|design)", "Be Seen as Creative"),
            (r"(?i)(smart|clever|resourceful)", "Appear Resourceful"),

            # Home presentation
            (r"(?i)(showcase|show off|display|highlight)", "Showcase Home"),
            (r"(?i)(impress|wow|attention)", "Impress Visitors"),
            (r"(?i)(family photos|personal|memories)", "Display Personal Identity"),

            # Competence
            (r"(?i)(did it myself|no need (?:for|to hire)|without hiring)", "Demonstrate DIY Competence"),
        ]

        for pattern, job_category in social_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                sentences = re.split(r'[.!?]', text)
                matching_sentence = ""
                for sentence in sentences:
                    if match.group() in sentence:
                        matching_sentence = sentence.strip()
                        break

                if matching_sentence:
                    self.jobs["social"].append({
                        "job": job_category,
                        "quote": matching_sentence,
                        "consumer": consumer,
                        "source": source
                    })
                    self.consumer_counts[consumer] += 1

    def analyze_all_transcripts(self):
        """Analyze all transcripts in the processed directory"""
        folders = sorted([f for f in PROCESSED_DIR.iterdir() if f.is_dir() and not f.name.startswith('batch')])

        print(f"Analyzing {len(folders)} transcripts...")

        for i, folder in enumerate(folders, 1):
            if (i % 10) == 0:
                print(f"  Progress: {i}/{len(folders)}")
            self.analyze_transcript(folder)

        print(f"\n✓ Analysis complete!")
        print(f"  Total jobs extracted: {len(self.jobs['functional']) + len(self.jobs['emotional']) + len(self.jobs['social'])}")
        print(f"  Functional: {len(self.jobs['functional'])}")
        print(f"  Emotional: {len(self.jobs['emotional'])}")
        print(f"  Social: {len(self.jobs['social'])}")
        print(f"  Unique consumers: {len(self.consumer_counts)}")

    def deduplicate_and_consolidate(self):
        """Remove duplicates and consolidate similar jobs"""
        for rung in ["functional", "emotional", "social"]:
            # Group by job category
            by_category = defaultdict(list)
            for job in self.jobs[rung]:
                by_category[job["job"]].append(job)

            # Keep only unique quotes per category
            consolidated = []
            for category, jobs_list in by_category.items():
                # Deduplicate by quote
                seen_quotes = set()
                for job in jobs_list:
                    quote_lower = job["quote"].lower()
                    if quote_lower not in seen_quotes:
                        seen_quotes.add(quote_lower)
                        consolidated.append(job)

            self.jobs[rung] = consolidated

        print(f"\nAfter deduplication:")
        print(f"  Functional: {len(self.jobs['functional'])}")
        print(f"  Emotional: {len(self.jobs['emotional'])}")
        print(f"  Social: {len(self.jobs['social'])}")

    def get_top_jobs(self):
        """Get the most common jobs by counting occurrences"""
        for rung in ["functional", "emotional", "social"]:
            by_category = defaultdict(list)
            for job in self.jobs[rung]:
                by_category[job["job"]].append(job)

            print(f"\n{rung.upper()} Jobs (Top 10):")
            sorted_categories = sorted(by_category.items(), key=lambda x: len(x[1]), reverse=True)
            for i, (category, jobs_list) in enumerate(sorted_categories[:10], 1):
                unique_consumers = len(set(j["consumer"] for j in jobs_list))
                print(f"  {i}. {category}: {len(jobs_list)} mentions, {unique_consumers} consumers")

    def save_results(self, output_path):
        """Save analysis results to JSON"""
        results = {
            "summary": {
                "total_consumers": len(self.consumer_counts),
                "total_jobs": len(self.jobs['functional']) + len(self.jobs['emotional']) + len(self.jobs['social']),
                "by_rung": {
                    "functional": len(self.jobs['functional']),
                    "emotional": len(self.jobs['emotional']),
                    "social": len(self.jobs['social'])
                }
            },
            "jobs": self.jobs,
            "consumer_participation": dict(self.consumer_counts)
        }

        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)

        print(f"\n✓ Results saved to: {output_path}")

def main():
    analyzer = JTBDAnalyzer()
    analyzer.analyze_all_transcripts()
    analyzer.deduplicate_and_consolidate()
    analyzer.get_top_jobs()

    output_path = PROCESSED_DIR / "jtbd_analysis.json"
    analyzer.save_results(output_path)

if __name__ == "__main__":
    main()
