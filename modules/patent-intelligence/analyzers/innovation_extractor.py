"""
LLM-Powered Innovation Extractor
Extracts actionable insights from patent data using Claude Sonnet 4
"""

import os
import json
import anthropic
from typing import Dict, List, Optional
from pathlib import Path

class InnovationExtractor:
    """Extract innovation insights from patents using LLM"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize innovation extractor

        Args:
            api_key: Anthropic API key (or set CLAUDE_API_KEY env var)
        """
        self.api_key = api_key or os.getenv('CLAUDE_API_KEY')
        if not self.api_key:
            raise ValueError("CLAUDE_API_KEY not found in environment or config")

        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = "claude-sonnet-4-20250514"

        # Track costs
        self.total_input_tokens = 0
        self.total_output_tokens = 0

    def analyze_patent(self, patent: Dict) -> Dict:
        """
        Analyze single patent and extract innovation insights

        Args:
            patent: Patent data dict with title, abstract, claims, assignees

        Returns:
            Dict with innovation insights
        """
        # Build analysis prompt
        prompt = self._build_innovation_prompt(patent)

        # Call Claude API
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1500,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )

        # Track usage
        self.total_input_tokens += response.usage.input_tokens
        self.total_output_tokens += response.usage.output_tokens

        # Parse JSON response
        try:
            content = response.content[0].text
            # Extract JSON from response (may have markdown code blocks)
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()

            insights = json.loads(content)

            # Add metadata
            insights['patent_id'] = patent['id']
            insights['analysis_model'] = self.model
            insights['input_tokens'] = response.usage.input_tokens
            insights['output_tokens'] = response.usage.output_tokens

            return insights

        except json.JSONDecodeError as e:
            print(f"⚠️ Failed to parse LLM response for {patent['id']}: {e}")
            print(f"Raw response: {response.content[0].text[:500]}")
            return self._empty_analysis(patent['id'], error=str(e))

    def analyze_batch(self, patents: List[Dict], progress_callback=None) -> List[Dict]:
        """
        Analyze multiple patents in batch

        Args:
            patents: List of patent dicts
            progress_callback: Optional callback function(current, total, patent_id)

        Returns:
            List of innovation insights
        """
        results = []

        for i, patent in enumerate(patents, 1):
            if progress_callback:
                progress_callback(i, len(patents), patent['id'])

            try:
                insights = self.analyze_patent(patent)
                results.append(insights)
            except Exception as e:
                print(f"❌ Error analyzing {patent['id']}: {e}")
                results.append(self._empty_analysis(patent['id'], error=str(e)))

        return results

    def _build_innovation_prompt(self, patent: Dict) -> str:
        """Build analysis prompt for patent"""

        # Get assignee name (company)
        assignees = patent.get('assignees', [])
        assignee_str = assignees[0] if assignees else "Unknown"

        # Get CPC codes for technology classification
        cpc_codes = patent.get('cpc_codes', [])
        cpc_str = ", ".join(cpc_codes[:3]) if cpc_codes else "Not specified"

        prompt = f"""You are a patent intelligence analyst for 3M Corporation, analyzing lighting technology patents.

**Task**: Analyze this patent and extract actionable innovation intelligence.

**Patent Information**:
- Patent ID: {patent['id']}
- Title: {patent['title']}
- Assignee: {assignee_str}
- Technology Classification (CPC): {cpc_str}
- Filing Date: {patent.get('filing_date', 'Unknown')}

**Abstract**:
{patent.get('abstract', 'No abstract available')[:1500]}

**Claims** (if available):
{patent.get('claims_text', 'Claims not available')[:1000]}

---

**Extract the following insights**:

1. **Core Innovation** (1-2 sentences): What is the key technical breakthrough or novel approach?

2. **Problem Solved** (1-2 sentences): What specific customer or technical problem does this address?

3. **Market Potential** (1-10 score with reasoning):
   - 1-3: Niche research, limited commercial potential
   - 4-6: Specialized applications, moderate market
   - 7-8: Significant commercial opportunity
   - 9-10: Game-changing, mass market potential

4. **Technology Readiness**:
   - "research_stage": Early R&D, years from production
   - "pilot_stage": Prototyping, 1-2 years from production
   - "production_ready": Mature technology, ready for manufacturing

5. **Applications** (3-5 use cases): List specific product applications or market segments.

6. **Competitive Position**: How does this compare to 3M's position? Are we ahead, behind, or on par with this innovation?

7. **Threat Level** (if not 3M patent):
   - "low": Different technology direction, no overlap
   - "medium": Adjacent technology, potential future competition
   - "high": Direct competition, could block 3M products or markets

8. **Recommended Action** (1-2 sentences): What should 3M do in response?

---

**Output Format** (JSON only, no additional text):

{{
  "core_innovation": "...",
  "problem_solved": "...",
  "market_potential": {{
    "score": 7,
    "reasoning": "..."
  }},
  "technology_readiness": "pilot_stage",
  "applications": [
    "Hospital lighting systems",
    "Senior living facilities",
    "Hotel room automation"
  ],
  "competitive_position": "...",
  "threat_level": "medium",
  "recommended_action": "..."
}}

**Important**: Output ONLY valid JSON. No additional commentary.
"""

        return prompt

    def _empty_analysis(self, patent_id: str, error: str = "") -> Dict:
        """Return empty analysis structure on error"""
        return {
            'patent_id': patent_id,
            'core_innovation': None,
            'problem_solved': None,
            'market_potential': {'score': 0, 'reasoning': 'Analysis failed'},
            'technology_readiness': None,
            'applications': [],
            'competitive_position': None,
            'threat_level': None,
            'recommended_action': None,
            'error': error
        }

    def get_cost_summary(self) -> Dict:
        """
        Get cost summary for all analyses

        Returns:
            Dict with token counts and estimated cost
        """
        # Claude Sonnet 4 pricing (as of 2025)
        # Input: $3 per 1M tokens
        # Output: $15 per 1M tokens
        input_cost = (self.total_input_tokens / 1_000_000) * 3.0
        output_cost = (self.total_output_tokens / 1_000_000) * 15.0
        total_cost = input_cost + output_cost

        return {
            'input_tokens': self.total_input_tokens,
            'output_tokens': self.total_output_tokens,
            'total_tokens': self.total_input_tokens + self.total_output_tokens,
            'input_cost_usd': round(input_cost, 4),
            'output_cost_usd': round(output_cost, 4),
            'total_cost_usd': round(total_cost, 4)
        }

    def reset_cost_tracking(self):
        """Reset cost counters"""
        self.total_input_tokens = 0
        self.total_output_tokens = 0


# Example usage
if __name__ == "__main__":
    # Test with sample patent
    sample_patent = {
        'id': 'US-10000000',
        'title': 'Circadian rhythm LED lighting control system',
        'abstract': 'A lighting system that automatically adjusts color temperature and intensity based on time of day to support natural circadian rhythms...',
        'assignees': ['Philips Lighting'],
        'filing_date': '2024-01-15',
        'cpc_codes': ['F21K9/00', 'H05B45/00']
    }

    extractor = InnovationExtractor()
    insights = extractor.analyze_patent(sample_patent)

    print(json.dumps(insights, indent=2))
    print(f"\nCost: ${extractor.get_cost_summary()['total_cost_usd']}")
