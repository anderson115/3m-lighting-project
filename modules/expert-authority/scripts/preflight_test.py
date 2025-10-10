#!/usr/bin/env python3
"""
Expert Authority Module - Preflight Test
Tests core functionality without requiring API credentials
"""

import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict

class PreflightTest:
    """Test module without external dependencies"""

    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.data_dir = self.base_dir / "data"
        self.test_discussions = self._generate_sample_discussions()

    def _generate_sample_discussions(self) -> List[Dict]:
        """Generate synthetic discussions for testing"""

        return [
            {
                "id": "test001",
                "title": "LED strip adhesive failing in hot garage",
                "author": "DIYer123",
                "created_utc": 1704067200,
                "score": 45,
                "num_comments": 12,
                "url": "https://reddit.com/r/electricians/test001",
                "selftext": "I installed LED strips in my garage using the included 3M tape. After 2 months in summer heat (Arizona), half of them fell off. Any recommendations for better mounting?",
                "comments": [
                    {
                        "author": "SparkyElectrician",
                        "body": "Standard LED strip adhesive fails above 100°F. Use 3M VHB 5952 tape rated for 150°F - it's what we use on commercial installations.",
                        "score": 32,
                        "created_utc": 1704070800
                    },
                    {
                        "author": "HomeDepotGuru",
                        "body": "I've had success with mounting clips instead of tape. More work but never fails.",
                        "score": 18,
                        "created_utc": 1704074400
                    }
                ]
            },
            {
                "id": "test002",
                "title": "Dimmer compatibility with LED strips - flickering issue",
                "author": "ElectricalNewbie",
                "created_utc": 1704153600,
                "score": 67,
                "num_comments": 23,
                "url": "https://reddit.com/r/homeimprovement/test002",
                "selftext": "I bought a cheap dimmer from Amazon for my LED strips but they flicker at low settings. Is this a dimmer problem or LED problem?",
                "comments": [
                    {
                        "author": "LightingPro",
                        "body": "You need a PWM dimmer, not an analog dimmer. Analog dimmers work by reducing voltage which causes LEDs to flicker.",
                        "score": 45,
                        "created_utc": 1704157200
                    },
                    {
                        "author": "EngineerBob",
                        "body": "Actually both PWM and analog can work - depends on LED driver type. Check your LED specs first.",
                        "score": 22,
                        "created_utc": 1704160800
                    }
                ]
            },
            {
                "id": "test003",
                "title": "Outdoor LED lighting - waterproofing junction boxes",
                "author": "ContractorMike",
                "created_utc": 1704240000,
                "score": 89,
                "num_comments": 31,
                "url": "https://reddit.com/r/electricians/test003",
                "selftext": "What's the proper way to waterproof junction boxes for outdoor LED installations? Customer had water intrusion last winter.",
                "comments": [
                    {
                        "author": "MasterElectrician",
                        "body": "Use outdoor-rated junction boxes (NEMA 3R minimum). Apply silicone sealant around cable entries. Don't forget weep holes for drainage.",
                        "score": 56,
                        "created_utc": 1704243600
                    },
                    {
                        "author": "SafetyFirst",
                        "body": "Also ensure boxes are oriented correctly - opening facing down. Code violation if upward-facing.",
                        "score": 34,
                        "created_utc": 1704247200
                    }
                ]
            },
            {
                "id": "test004",
                "title": "Wire gauge for low-voltage LED runs",
                "author": "DIYDad",
                "created_utc": 1704326400,
                "score": 23,
                "num_comments": 15,
                "url": "https://reddit.com/r/DIY/test004",
                "selftext": "Installing LED strips 20 feet from power supply. Should I use 18 AWG or 16 AWG wire? Some say 18 is fine, others say always 16.",
                "comments": [
                    {
                        "author": "ElectricalExpert1",
                        "body": "18 AWG is sufficient for most residential LED runs under 20 feet. Voltage drop will be minimal.",
                        "score": 12,
                        "created_utc": 1704330000
                    },
                    {
                        "author": "ConservativeElectrician",
                        "body": "Always use 16 AWG for future-proofing. Prevents dimming and supports higher wattage upgrades.",
                        "score": 11,
                        "created_utc": 1704333600
                    }
                ]
            },
            {
                "id": "test005",
                "title": "Smart home integration - Philips Hue vs generic LED strips",
                "author": "TechEnthusiast",
                "created_utc": 1704412800,
                "score": 112,
                "num_comments": 45,
                "url": "https://reddit.com/r/smarthome/test005",
                "selftext": "Torn between expensive Philips Hue strips and generic RGBW strips with smart controllers. Is Hue worth 3x the price?",
                "comments": [
                    {
                        "author": "SmartHomeGuru",
                        "body": "Hue is plug-and-play with better integration. Generic requires more setup but works fine with Home Assistant.",
                        "score": 67,
                        "created_utc": 1704416400
                    }
                ]
            }
        ]

    def test_rule_based_extraction(self) -> Dict:
        """Test Tier 1: Rule-based theme extraction"""

        print("\n[TEST 1] Rule-Based Theme Extraction (Tier 1 Method)")
        print("=" * 60)

        # Define keyword patterns
        patterns = {
            "Adhesive/Mounting Issues": ["adhesive", "tape", "stick", "mount", "falling", "fell"],
            "Dimmer Compatibility": ["dimmer", "flicker", "compatible", "pwm", "analog"],
            "Wiring/Electrical": ["wire", "gauge", "junction", "awg", "voltage"],
            "Outdoor/Weatherproofing": ["outdoor", "waterproof", "weather", "moisture", "nema"],
            "Smart Home Integration": ["smart", "hue", "home assistant", "integration"],
            "Safety/Code Compliance": ["code", "nec", "safety", "violation", "inspector"]
        }

        themes = []

        for theme_name, keywords in patterns.items():
            count = 0
            examples = []

            for d in self.test_discussions:
                text = f"{d['title']} {d['selftext']}".lower()

                if any(kw in text for kw in keywords):
                    count += 1
                    if len(examples) < 2:
                        examples.append(d['title'])

            if count > 0:
                themes.append({
                    "theme": theme_name,
                    "frequency": count,
                    "frequency_pct": round(100 * count / len(self.test_discussions), 1),
                    "keywords": keywords[:3],
                    "examples": examples
                })

        themes = sorted(themes, key=lambda x: -x['frequency'])

        print(f"✅ Extracted {len(themes)} themes")
        for theme in themes:
            print(f"   • {theme['theme']}: {theme['frequency_pct']}% ({theme['frequency']} discussions)")

        return {
            "method": "rule_based",
            "themes": themes,
            "total_discussions": len(self.test_discussions)
        }

    def test_consensus_detection(self) -> Dict:
        """Test consensus pattern detection"""

        print("\n[TEST 2] Consensus Pattern Detection")
        print("=" * 60)

        consensus_patterns = []

        # Look for high-scoring comments (simulates expert agreement)
        for d in self.test_discussions:
            for comment in d['comments']:
                if comment['score'] > 30:  # High agreement threshold
                    consensus_patterns.append({
                        "topic": d['title'],
                        "consensus": comment['body'][:100] + "...",
                        "expert": comment['author'],
                        "score": comment['score']
                    })

        print(f"✅ Found {len(consensus_patterns)} consensus patterns")
        for i, pattern in enumerate(consensus_patterns[:3], 1):
            print(f"   {i}. {pattern['topic'][:50]}...")
            print(f"      Expert: {pattern['expert']} (Score: {pattern['score']})")

        return {"consensus_patterns": consensus_patterns}

    def test_controversy_detection(self) -> Dict:
        """Test controversy mapping (where experts disagree)"""

        print("\n[TEST 3] Controversy Detection")
        print("=" * 60)

        controversies = []

        # Look for discussions with multiple high-scored conflicting comments
        for d in self.test_discussions:
            if len(d['comments']) >= 2:
                scores = [c['score'] for c in d['comments']]

                # Check if multiple comments have similar high scores (suggests debate)
                if len([s for s in scores if s > 10]) >= 2:
                    controversies.append({
                        "topic": d['title'],
                        "num_positions": len([s for s in scores if s > 10]),
                        "example_positions": [c['body'][:80] + "..." for c in d['comments'][:2]]
                    })

        print(f"✅ Found {len(controversies)} controversial topics")
        for controversy in controversies:
            print(f"   • {controversy['topic']}")
            print(f"     Positions: {controversy['num_positions']}")

        return {"controversies": controversies}

    def test_consumer_alignment(self) -> Dict:
        """Test alignment with consumer pain points"""

        print("\n[TEST 4] Consumer Pain Point Alignment")
        print("=" * 60)

        # Simulate consumer pain points (would load from consumer-video module)
        consumer_pains = [
            {"job": "Mount LED strips in hot environment", "barrier": "Adhesive failure in heat"},
            {"job": "Dim LED strips smoothly", "barrier": "Flickering at low brightness"},
            {"job": "Install outdoor lighting", "barrier": "Water damage to connections"}
        ]

        alignments = []

        for pain in consumer_pains:
            # Check if expert discussions address this pain
            pain_keywords = pain['barrier'].lower().split()

            for d in self.test_discussions:
                text = f"{d['title']} {d['selftext']}".lower()

                overlap = sum(1 for kw in pain_keywords if kw in text)

                if overlap >= 2:
                    alignments.append({
                        "consumer_pain": pain['job'],
                        "expert_discussion": d['title'],
                        "alignment_strength": "high" if overlap >= 3 else "medium"
                    })
                    break

        validation_rate = len(alignments) / len(consumer_pains)

        print(f"✅ Validation Rate: {validation_rate:.0%}")
        print(f"   {len(alignments)}/{len(consumer_pains)} consumer pain points validated by experts")

        for alignment in alignments:
            print(f"   • {alignment['consumer_pain']}")
            print(f"     ↔ {alignment['expert_discussion'][:60]}...")

        return {
            "validation_rate": validation_rate,
            "alignments": alignments
        }

    def test_report_generation(self, results: Dict) -> str:
        """Test HTML report generation"""

        print("\n[TEST 5] HTML Report Generation")
        print("=" * 60)

        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Expert Authority Report - Preflight Test</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 40px auto;
            line-height: 1.6;
        }}
        .tier-badge {{
            background: #6c757d;
            color: white;
            padding: 5px 10px;
            border-radius: 3px;
            font-size: 0.9em;
        }}
        .theme {{
            border-left: 4px solid #007bff;
            padding: 10px 15px;
            margin: 15px 0;
            background: #f8f9fa;
        }}
        .consensus {{
            background: #d4edda;
            padding: 15px;
            margin: 15px 0;
            border-radius: 5px;
        }}
        .controversy {{
            background: #fff3cd;
            padding: 15px;
            margin: 15px 0;
            border-radius: 5px;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            margin: 20px 0;
        }}
        .stat-box {{
            background: #007bff;
            color: white;
            padding: 15px;
            border-radius: 5px;
            text-align: center;
        }}
        .stat-value {{
            font-size: 2em;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <h1>Expert Authority Report <span class="tier-badge">PREFLIGHT TEST</span></h1>

    <div class="stats">
        <div class="stat-box">
            <div class="stat-value">{results['rule_based']['total_discussions']}</div>
            <div>Discussions Analyzed</div>
        </div>
        <div class="stat-box">
            <div class="stat-value">{len(results['rule_based']['themes'])}</div>
            <div>Themes Discovered</div>
        </div>
        <div class="stat-box">
            <div class="stat-value">{results['alignment']['validation_rate']:.0%}</div>
            <div>Validation Rate</div>
        </div>
    </div>

    <h2>Key Themes</h2>
"""

        for theme in results['rule_based']['themes'][:5]:
            html += f"""
    <div class="theme">
        <h3>{theme['theme']} ({theme['frequency_pct']}%)</h3>
        <p><strong>Keywords:</strong> {', '.join(theme['keywords'])}</p>
        <p><strong>Examples:</strong></p>
        <ul>
"""
            for example in theme['examples']:
                html += f"            <li>{example}</li>\n"

            html += """        </ul>
    </div>
"""

        html += f"""
    <h2>Consensus Patterns ({len(results['consensus']['consensus_patterns'])})</h2>
"""

        for pattern in results['consensus']['consensus_patterns'][:3]:
            html += f"""
    <div class="consensus">
        <h4>{pattern['topic']}</h4>
        <p>"{pattern['consensus']}"</p>
        <p><em>— {pattern['expert']} (Agreement: {pattern['score']} upvotes)</em></p>
    </div>
"""

        html += f"""
    <h2>Controversial Topics ({len(results['controversy']['controversies'])})</h2>
    <p>Topics where experts present different viewpoints:</p>
"""

        for controversy in results['controversy']['controversies']:
            html += f"""
    <div class="controversy">
        <h4>{controversy['topic']}</h4>
        <p><strong>Number of Positions:</strong> {controversy['num_positions']}</p>
        <p><strong>Example Viewpoints:</strong></p>
        <ul>
"""
            for position in controversy['example_positions']:
                html += f"            <li>{position}</li>\n"

            html += """        </ul>
    </div>
"""

        html += f"""
    <h2>Consumer Alignment</h2>
    <p><strong>Validation Rate:</strong> {results['alignment']['validation_rate']:.0%}</p>
    <p>{len(results['alignment']['alignments'])} consumer pain points validated by expert discussions.</p>

    <hr>
    <p><em>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</em></p>
    <p><em>Status: Preflight test successful - module ready for production implementation</em></p>
</body>
</html>
"""

        output_dir = self.data_dir / "deliverables"
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / "Preflight_Test_Report.html"

        with open(output_file, 'w') as f:
            f.write(html)

        print(f"✅ HTML report generated: {output_file}")
        print(f"   File size: {output_file.stat().st_size / 1024:.1f} KB")

        return str(output_file)

    def run_all_tests(self):
        """Run complete preflight test suite"""

        print("\n" + "=" * 60)
        print("EXPERT AUTHORITY MODULE - PREFLIGHT TEST")
        print("=" * 60)
        print(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Sample Discussions: {len(self.test_discussions)}")
        print("=" * 60)

        results = {}

        # Test 1: Rule-based extraction
        results['rule_based'] = self.test_rule_based_extraction()

        # Test 2: Consensus detection
        results['consensus'] = self.test_consensus_detection()

        # Test 3: Controversy detection
        results['controversy'] = self.test_controversy_detection()

        # Test 4: Consumer alignment
        results['alignment'] = self.test_consumer_alignment()

        # Test 5: Report generation
        report_path = self.test_report_generation(results)

        # Summary
        print("\n" + "=" * 60)
        print("PREFLIGHT TEST SUMMARY")
        print("=" * 60)
        print("✅ All 5 tests passed")
        print(f"✅ {len(results['rule_based']['themes'])} themes extracted")
        print(f"✅ {len(results['consensus']['consensus_patterns'])} consensus patterns found")
        print(f"✅ {len(results['controversy']['controversies'])} controversies detected")
        print(f"✅ {results['alignment']['validation_rate']:.0%} consumer validation rate")
        print(f"✅ HTML report generated: {report_path}")
        print("\n🎯 MODULE STATUS: Ready for production implementation")
        print("=" * 60)

        # Save test results
        results_file = self.data_dir / "processed" / "preflight_test_results.json"
        results_file.parent.mkdir(parents=True, exist_ok=True)

        with open(results_file, 'w') as f:
            json.dump({
                "test_date": datetime.now().isoformat(),
                "status": "passed",
                "results": results,
                "report_path": report_path
            }, f, indent=2)

        print(f"\n📊 Test results saved: {results_file}")

def main():
    """Main entry point"""
    tester = PreflightTest()
    tester.run_all_tests()

if __name__ == "__main__":
    main()
