"""
Content classifier using Gemini Flash LLM.
Analyzes creator content for relevance to lighting industry.
"""

import json
import logging
from typing import Dict, List, Optional
import google.generativeai as genai

logger = logging.getLogger(__name__)


class ContentClassifier:
    """
    LLM-powered content classifier using Gemini Flash.
    Classifies content relevance and extracts pain points and consumer language.
    """

    CLASSIFICATION_PROMPT = """You are analyzing creator content for the lighting industry.

Content to analyze:
Title: {title}
Description: {description}
Platform: {platform}

Task: Classify this content and extract insights.

Respond with valid JSON only (no markdown, no explanation):
{{
  "classification": "highly_relevant" | "relevant" | "tangentially_relevant" | "not_relevant",
  "relevance_score": 0.0-1.0,
  "relevance_reasoning": "brief explanation",
  "pain_points": ["pain point 1", "pain point 2"],
  "consumer_language": ["phrase 1", "phrase 2"],
  "lighting_topics": ["LED strips", "ambient lighting", etc],
  "job_to_be_done": "what job is the content helping with"
}}

Classification guide:
- highly_relevant: Directly about lighting products, installation, or use cases
- relevant: Home improvement with lighting as key element
- tangentially_relevant: Home decor/DIY where lighting could apply
- not_relevant: No connection to lighting

Pain points: Problems, frustrations, or challenges mentioned
Consumer language: Exact phrases consumers use (not technical jargon)
"""

    def __init__(self, api_key: str, model: str = "gemini-1.5-flash"):
        """
        Initialize content classifier.

        Args:
            api_key: Gemini API key
            model: Model name (default: gemini-1.5-flash for cost efficiency)
        """
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)
        self.total_tokens_used = 0
        logger.info(f"✅ ContentClassifier initialized with {model}")

    def classify_content(self, content: Dict) -> Dict:
        """
        Classify single piece of content.

        Args:
            content: Content dictionary with title, description, platform

        Returns:
            Classification results
        """
        try:
            prompt = self.CLASSIFICATION_PROMPT.format(
                title=content.get('title', '')[:500],
                description=content.get('description', '')[:2000],
                platform=content.get('platform', 'unknown')
            )

            logger.debug(f"Classifying content: {content.get('title', 'Untitled')[:50]}")

            response = self.model.generate_content(prompt)
            self.total_tokens_used += response.usage_metadata.total_token_count if hasattr(response, 'usage_metadata') else 0

            # Parse JSON response
            response_text = response.text.strip()
            # Remove markdown code blocks if present
            if response_text.startswith('```'):
                response_text = response_text.split('```')[1]
                if response_text.startswith('json'):
                    response_text = response_text[4:]
                response_text = response_text.strip()

            result = json.loads(response_text)

            logger.debug(f"Classification: {result.get('classification')} (score: {result.get('relevance_score')})")

            return {
                'content_id': content.get('content_id'),
                'platform': content.get('platform'),
                'classification': result.get('classification'),
                'relevance_score': result.get('relevance_score', 0.0),
                'relevance_reasoning': result.get('relevance_reasoning', ''),
                'pain_points': result.get('pain_points', []),
                'consumer_language': result.get('consumer_language', []),
                'lighting_topics': result.get('lighting_topics', []),
                'job_to_be_done': result.get('job_to_be_done', '')
            }

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response: {e}")
            logger.error(f"Response was: {response.text[:200]}")
            return self._fallback_classification(content)

        except Exception as e:
            logger.error(f"Content classification failed: {e}")
            return self._fallback_classification(content)

    def classify_batch(self, contents: List[Dict]) -> List[Dict]:
        """
        Classify multiple pieces of content.

        Args:
            contents: List of content dictionaries

        Returns:
            List of classification results
        """
        results = []
        for i, content in enumerate(contents):
            logger.info(f"Classifying {i+1}/{len(contents)}")
            result = self.classify_content(content)
            results.append(result)

        logger.info(f"✅ Classified {len(results)} pieces of content")
        logger.info(f"📊 Total tokens used: {self.total_tokens_used}")

        return results

    def _fallback_classification(self, content: Dict) -> Dict:
        """Fallback classification using keyword matching."""
        text = f"{content.get('title', '')} {content.get('description', '')}".lower()

        lighting_keywords = [
            'light', 'led', 'lamp', 'bulb', 'fixture', 'ambient', 'task lighting',
            'strip light', 'chandelier', 'sconce', 'dimmer', 'lumens', 'watt',
            'brightness', 'illumination', 'glow', 'neon'
        ]

        matches = sum(1 for keyword in lighting_keywords if keyword in text)

        if matches >= 3:
            classification = 'highly_relevant'
            score = 0.8
        elif matches >= 1:
            classification = 'relevant'
            score = 0.5
        else:
            classification = 'not_relevant'
            score = 0.1

        logger.warning(f"Using fallback classification: {classification}")

        return {
            'content_id': content.get('content_id'),
            'platform': content.get('platform'),
            'classification': classification,
            'relevance_score': score,
            'relevance_reasoning': 'Fallback keyword matching',
            'pain_points': [],
            'consumer_language': [],
            'lighting_topics': [],
            'job_to_be_done': ''
        }


if __name__ == "__main__":
    # Test content classifier
    from creator_intelligence.core.config import config

    classifier = ContentClassifier(
        api_key=config.gemini_api_key,
        model=config.llm_model
    )

    # Test content
    test_content = {
        'content_id': 'test123',
        'platform': 'youtube',
        'title': 'How to Install LED Strip Lights Under Kitchen Cabinets',
        'description': 'In this tutorial, I show you how to install LED strip lights under your kitchen cabinets. The lighting was too dim before and now it\'s perfect for food prep. Easy DIY project that anyone can do!'
    }

    result = classifier.classify_content(test_content)
    print(json.dumps(result, indent=2))
