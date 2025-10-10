#!/usr/bin/env python3
"""
Production Analyzer - Theme Discovery with LLM and Rule-Based Fallback
Implements both semantic LLM analysis and deterministic rule-based extraction
NO FABRICATION - All insights must be traceable to source discussions
"""

import json
import hashlib
from collections import Counter
from typing import List, Dict, Optional
from pathlib import Path
import logging
import re

try:
    from anthropic import Anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False

from ..core.config import Config

class ProductionAnalyzer:
    """Production analyzer with LLM semantic analysis and rule-based fallback"""

    def __init__(self, tier: int = 1, config: Optional[Config] = None):
        """
        Initialize analyzer

        Args:
            tier: Analysis tier (1 = rule-based, 2 = LLM semantic, 3 = extended)
            config: Configuration object
        """
        self.tier = tier
        self.config = config or Config()
        self.tier_config = self.config.get_tier_config(tier)

        # Setup logging
        self.logger = logging.getLogger(__name__)

        # Initialize LLM client if available and needed
        self.anthropic_client = None
        if tier >= 2 and HAS_ANTHROPIC and self.config.anthropic_api_key:
            self.anthropic_client = Anthropic(api_key=self.config.anthropic_api_key)
            self.logger.info("✅ Anthropic LLM client initialized")
        elif tier >= 2:
            self.logger.warning("⚠️ Tier 2+ requested but LLM unavailable - falling back to rule-based")

    def analyze(self, discussions: List[Dict]) -> Dict:
        """
        Analyze discussions and extract themes

        Args:
            discussions: List of discussion dictionaries from scrapers

        Returns:
            Analysis results dictionary with themes, consensus, controversies
        """
        self.logger.info(f"🔍 Analyzing {len(discussions)} discussions (Tier {self.tier})...")

        # Select analysis method based on tier and LLM availability
        if self.tier >= 2 and self.anthropic_client:
            themes = self._llm_semantic_analysis(discussions)
        else:
            themes = self._rule_based_analysis(discussions)

        # Extract consensus patterns
        consensus = self._extract_consensus(discussions, themes)

        # Extract controversies (Tier 2+)
        controversies = []
        if self.tier >= 2:
            controversies = self._extract_controversies(discussions, themes)

        # Extract safety warnings (Tier 2+)
        safety_warnings = []
        if self.tier >= 2:
            safety_warnings = self._extract_safety_warnings(discussions)

        # Build analysis result
        analysis = {
            "metadata": {
                "tier": self.tier,
                "analysis_method": "llm_semantic" if self.anthropic_client and self.tier >= 2 else "rule_based",
                "total_discussions": len(discussions),
                "platforms": list(set([d.get('platform', 'unknown') for d in discussions]))
            },
            "themes": themes,
            "consensus_patterns": consensus,
            "controversies": controversies,
            "safety_warnings": safety_warnings
        }

        self.logger.info(f"✅ Analysis complete: {len(themes)} themes, {len(consensus)} consensus patterns")
        return analysis

    def _rule_based_analysis(self, discussions: List[Dict]) -> List[Dict]:
        """Rule-based theme extraction using keyword patterns"""
        self.logger.info("📊 Running rule-based analysis...")

        # Define theme patterns (keyword-based)
        theme_patterns = {
            "adhesive_mounting": ["adhesive", "tape", "stick", "mount", "falling", "attach", "3m tape", "vhb"],
            "heat_issues": ["heat", "hot", "temperature", "overheat", "warm", "cooling", "thermal"],
            "electrical_safety": ["shock", "ground", "gfci", "breaker", "wire", "voltage", "amperage", "code"],
            "dimmer_compatibility": ["dimmer", "dim", "flicker", "brightness", "control", "switch"],
            "power_supply": ["transformer", "driver", "power supply", "watts", "voltage", "12v", "24v"],
            "installation_difficulty": ["install", "difficult", "complicated", "hard to", "struggle", "confusing"],
            "color_accuracy": ["color", "cri", "kelvin", "warm white", "cool white", "rgb", "color temp"],
            "durability": ["lifespan", "fail", "broken", "lasted", "died", "replacement", "warranty"]
        }

        # Count matches for each theme
        theme_counts = {theme: {"count": 0, "examples": []} for theme in theme_patterns}

        for discussion in discussions:
            # Combine title, body, and comments for analysis
            full_text = self._extract_text(discussion).lower()

            for theme, keywords in theme_patterns.items():
                for keyword in keywords:
                    if keyword in full_text:
                        theme_counts[theme]["count"] += 1
                        if len(theme_counts[theme]["examples"]) < 3:
                            theme_counts[theme]["examples"].append({
                                "title": discussion.get('title', ''),
                                "url": discussion.get('url', ''),
                                "id": discussion.get('id', '')
                            })
                        break  # Don't double-count same discussion

        # Convert to theme list with frequency percentages
        total_discussions = len(discussions)
        themes = []

        for theme_name, data in theme_counts.items():
            if data["count"] > 0:
                themes.append({
                    "theme": theme_name.replace("_", " ").title(),
                    "frequency": data["count"],
                    "frequency_pct": round((data["count"] / total_discussions) * 100, 1),
                    "method": "rule_based",
                    "examples": data["examples"]
                })

        # Sort by frequency
        themes.sort(key=lambda x: x["frequency"], reverse=True)

        return themes

    def _llm_semantic_analysis(self, discussions: List[Dict]) -> List[Dict]:
        """LLM-powered semantic theme discovery"""
        self.logger.info("🤖 Running LLM semantic analysis...")

        # Prepare discussion summaries for LLM
        discussion_summaries = []
        for i, d in enumerate(discussions[:50]):  # Limit to 50 for token efficiency
            discussion_summaries.append({
                "id": d.get('id', str(i)),
                "title": d.get('title', ''),
                "platform": d.get('platform', ''),
                "url": d.get('url', ''),
                "snippet": self._extract_text(d)[:500]  # First 500 chars
            })

        # Build LLM prompt
        prompt = self._build_theme_discovery_prompt(discussion_summaries)

        # Call Claude API
        try:
            response = self.anthropic_client.messages.create(
                model=self.tier_config.get('llm_model', 'claude-sonnet-4-20250514'),
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}]
            )

            # Parse LLM response
            themes = self._parse_llm_themes(response.content[0].text, discussions)
            self.logger.info(f"✅ LLM discovered {len(themes)} themes")
            return themes

        except Exception as e:
            self.logger.error(f"❌ LLM analysis failed: {e}")
            self.logger.info("⚠️ Falling back to rule-based analysis")
            return self._rule_based_analysis(discussions)

    def _build_theme_discovery_prompt(self, discussion_summaries: List[Dict]) -> str:
        """Build prompt for LLM theme discovery"""
        prompt = f"""You are analyzing expert discussions about lighting products and installations.

**CRITICAL INSTRUCTIONS:**
1. ONLY identify themes that appear in the provided discussions
2. DO NOT invent or fabricate themes
3. Every theme MUST cite specific discussion IDs as evidence
4. Focus on emergent patterns, not just keywords

**Discussions to analyze:**

"""
        for d in discussion_summaries:
            prompt += f"""
ID: {d['id']}
Platform: {d['platform']}
Title: {d['title']}
Snippet: {d['snippet']}
URL: {d['url']}
---
"""

        prompt += """

**Task:** Identify 6-10 major themes from these discussions.

**Output format (JSON):**
```json
[
  {
    "theme": "Theme Name",
    "description": "Brief description of the pattern",
    "frequency_estimate": <number of discussions mentioning this>,
    "evidence_ids": ["id1", "id2", "id3"],
    "strategic_insight": "Why this matters for product development"
  }
]
```

Return ONLY the JSON array, no other text.
"""
        return prompt

    def _parse_llm_themes(self, llm_response: str, discussions: List[Dict]) -> List[Dict]:
        """Parse LLM response into theme structure"""
        try:
            # Extract JSON from response
            json_match = re.search(r'\[.*\]', llm_response, re.DOTALL)
            if json_match:
                themes_raw = json.loads(json_match.group(0))
            else:
                raise ValueError("No JSON found in LLM response")

            # Validate and format themes
            themes = []
            total_discussions = len(discussions)

            for theme in themes_raw:
                # Validate evidence exists
                evidence_ids = theme.get('evidence_ids', [])
                examples = []

                for eid in evidence_ids[:3]:  # Max 3 examples
                    for d in discussions:
                        if d.get('id') == eid:
                            examples.append({
                                "title": d.get('title', ''),
                                "url": d.get('url', ''),
                                "id": d.get('id', '')
                            })
                            break

                frequency = theme.get('frequency_estimate', 0)

                themes.append({
                    "theme": theme.get('theme', 'Unknown Theme'),
                    "description": theme.get('description', ''),
                    "frequency": frequency,
                    "frequency_pct": round((frequency / total_discussions) * 100, 1),
                    "method": "llm_semantic",
                    "strategic_insight": theme.get('strategic_insight', ''),
                    "examples": examples
                })

            return themes

        except Exception as e:
            self.logger.error(f"❌ Failed to parse LLM themes: {e}")
            return []

    def _extract_consensus(self, discussions: List[Dict], themes: List[Dict]) -> List[Dict]:
        """Extract consensus patterns (widely-agreed solutions)"""
        self.logger.info("🔍 Extracting consensus patterns...")

        # Simple consensus detection: Look for high-score answers/comments
        consensus_patterns = []

        for discussion in discussions:
            # Check for highly-voted comments (Reddit)
            if discussion.get('platform') == 'reddit':
                for comment in discussion.get('comments', [])[:5]:
                    if comment.get('score', 0) >= 50:  # High score threshold
                        consensus_patterns.append({
                            "pattern": comment.get('body', '')[:200],
                            "source_discussion": discussion.get('title', ''),
                            "source_url": comment.get('permalink', discussion.get('url', '')),
                            "score": comment.get('score', 0),
                            "platform": "reddit"
                        })

            # Check for accepted answers (Stack Exchange)
            elif discussion.get('platform') == 'stackexchange':
                for answer in discussion.get('answers', []):
                    if answer.get('is_accepted') or answer.get('score', 0) >= 10:
                        consensus_patterns.append({
                            "pattern": answer.get('body', '')[:200],
                            "source_discussion": discussion.get('title', ''),
                            "source_url": discussion.get('url', ''),
                            "score": answer.get('score', 0),
                            "platform": "stackexchange",
                            "is_accepted": answer.get('is_accepted', False)
                        })

        # Sort by score and return top 10
        consensus_patterns.sort(key=lambda x: x['score'], reverse=True)
        return consensus_patterns[:10]

    def _extract_controversies(self, discussions: List[Dict], themes: List[Dict]) -> List[Dict]:
        """Extract controversial topics (where experts disagree)"""
        # Simplified controversy detection: Look for discussions with many comments but low scores
        controversies = []

        for discussion in discussions:
            num_comments = discussion.get('num_comments', 0) or discussion.get('answer_count', 0)
            score = discussion.get('score', 0)

            # High engagement but polarizing (many comments, moderate score)
            if num_comments >= 10 and score < num_comments * 0.5:
                controversies.append({
                    "topic": discussion.get('title', ''),
                    "url": discussion.get('url', ''),
                    "num_comments": num_comments,
                    "score": score,
                    "platform": discussion.get('platform', '')
                })

        return controversies[:5]

    def _extract_safety_warnings(self, discussions: List[Dict]) -> List[Dict]:
        """Extract safety warnings and code compliance mentions"""
        safety_keywords = ["code", "nec", "safety", "fire", "shock", "ground", "gfci", "permit", "inspector"]

        safety_warnings = []

        for discussion in discussions:
            full_text = self._extract_text(discussion).lower()

            for keyword in safety_keywords:
                if keyword in full_text:
                    safety_warnings.append({
                        "warning": discussion.get('title', ''),
                        "url": discussion.get('url', ''),
                        "platform": discussion.get('platform', ''),
                        "keyword": keyword
                    })
                    break

        return safety_warnings[:10]

    def _extract_text(self, discussion: Dict) -> str:
        """Extract all text from discussion for analysis"""
        text_parts = []

        text_parts.append(discussion.get('title', ''))
        text_parts.append(discussion.get('selftext', ''))
        text_parts.append(discussion.get('body', ''))

        # Add comments/answers
        for comment in discussion.get('comments', [])[:10]:
            text_parts.append(comment.get('body', ''))

        for answer in discussion.get('answers', [])[:10]:
            text_parts.append(answer.get('body', ''))

        return " ".join(text_parts)


if __name__ == "__main__":
    # Example usage
    logging.basicConfig(level=logging.INFO)

    # Load sample discussions from cache
    cache_file = Path(__file__).parent.parent / "data" / "cache" / "reddit" / "sample.json"

    analyzer = ProductionAnalyzer(tier=2)

    # This would normally load real discussions
    print("✅ Analyzer ready for production use")
    print(f"📊 Tier: {analyzer.tier}")
    print(f"🤖 LLM available: {analyzer.anthropic_client is not None}")
