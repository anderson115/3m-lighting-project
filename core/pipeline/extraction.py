#!/usr/bin/env python3
"""
LLM-Based JTBD Extraction Engine
Extracts Jobs-to-be-Done insights from combined transcript + visual analysis
"""
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
import yaml

from core.models.model_registry import (
    ModelRegistry, OllamaClient, GeminiClient, OpenAIClient,
    AnthropicClient, DeepSeekAPIClient, GLM4Client, TogetherAIClient
)


class LLMExtractor:
    """LLM-powered JTBD insight extraction"""

    def __init__(
        self,
        client_name: str,
        client_config_path: Optional[Path] = None,
        model_type: str = 'gemini'
    ):
        """
        Initialize extractor with client configuration

        Args:
            client_name: Client identifier (e.g., '3m_lighting')
            client_config_path: Optional path to client config directory
            model_type: Model to use:
                - Local: 'llama', 'deepseek-local'
                - API Normal: 'deepseek-api', 'glm4'
                - API Premium: 'gemini', 'openai', 'anthropic'
        """
        self.client_name = client_name
        self.model_type = model_type

        # Load client configuration
        if client_config_path is None:
            project_root = Path(__file__).parent.parent.parent
            client_config_path = project_root / 'clients' / client_name

        self.config_path = client_config_path
        self.config = self._load_config()
        self.prompts = self._load_prompts()

        # Initialize model based on type
        self.registry = ModelRegistry()
        self.llm = self._initialize_model()

    def _initialize_model(self):
        """Initialize the appropriate model client"""
        temp = self.prompts.get('temperature', 0.3)

        # Premium API Models
        if self.model_type == 'gemini':
            config = self.registry.get_gemini_config()
            return GeminiClient(
                api_key=config['api_key'],
                model=config['model'],
                temperature=temp,
                max_tokens=config.get('max_tokens', 4000)
            )
        elif self.model_type == 'openai':
            config = self.registry.get_openai_config()
            return OpenAIClient(
                api_key=config['api_key'],
                model=config['model'],
                temperature=temp,
                max_tokens=config.get('max_tokens', 4000)
            )
        elif self.model_type == 'anthropic':
            config = self.registry.get_anthropic_config()
            return AnthropicClient(
                api_key=config['api_key'],
                model=config['model'],
                temperature=temp,
                max_tokens=config.get('max_tokens', 4000)
            )
        # Normal API Models
        elif self.model_type == 'deepseek-api':
            config = self.registry.get_deepseek_api_config()
            return DeepSeekAPIClient(
                api_key=config['api_key'],
                model=config['model'],
                base_url=config['base_url'],
                temperature=temp,
                max_tokens=config.get('max_tokens', 4000)
            )
        elif self.model_type == 'glm4':
            config = self.registry.get_glm4_config()
            return GLM4Client(
                api_key=config['api_key'],
                model=config['model'],
                base_url=config['base_url'],
                temperature=temp,
                max_tokens=config.get('max_tokens', 4000)
            )
        elif self.model_type == 'togetherai':
            config = self.registry.get_togetherai_config()
            return TogetherAIClient(
                api_key=config['api_key'],
                model=config['model'],
                base_url=config['base_url'],
                temperature=temp,
                max_tokens=config.get('max_tokens', 4000)
            )
        # Local Models
        elif self.model_type == 'deepseek-local':
            config = self.registry.get_deepseek_local_config()
            return OllamaClient(
                model=config['model'],
                temperature=temp,
                format='json'
            )
        else:  # llama (default)
            config = self.registry.get_llama_config()
            return OllamaClient(
                model=config['model'],
                temperature=temp,
                format='json'
            )

    def _load_config(self) -> Dict[str, Any]:
        """Load client configuration"""
        config_file = self.config_path / 'config.yaml'
        with open(config_file) as f:
            return yaml.safe_load(f)

    def _load_prompts(self) -> Dict[str, Any]:
        """Load extraction prompts"""
        prompts_file = self.config_path / 'prompts.yaml'
        with open(prompts_file) as f:
            return yaml.safe_load(f)

    def extract_insights(
        self,
        transcript: Dict[str, Any],
        visual_analyses: List[Dict[str, Any]],
        video_metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Extract JTBD insights from combined multimodal data

        Args:
            transcript: Whisper transcription result with segments
            visual_analyses: LLaVA frame analyses with timestamps
            video_metadata: Optional video metadata

        Returns:
            Structured insights dict with pain_points, solutions, etc.
        """
        print("   💡 Extracting JTBD insights with LLM...")

        # Step 1: Merge data sources with temporal alignment
        timeline = self._merge_sources(transcript, visual_analyses)

        # Step 2: Chunk timeline for long videos
        chunks = self._chunk_timeline(timeline)

        # Step 3: Extract insights from each chunk
        all_insights = []
        for i, chunk in enumerate(chunks):
            print(f"      Processing chunk {i+1}/{len(chunks)}...")
            chunk_insights = self._extract_from_chunk(chunk)
            if chunk_insights:
                all_insights.append(chunk_insights)

        # Step 4: Merge and deduplicate
        final_insights = self._merge_insights(all_insights)

        # Step 5: Validate and format
        validated = self._validate_insights(final_insights)

        print(f"   ✅ Extracted {len(validated.get('pain_points', []))} pain points, "
              f"{len(validated.get('solutions', []))} solutions")

        return validated

    def _merge_sources(
        self,
        transcript: Dict[str, Any],
        visual_analyses: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Merge transcript and visual data into unified timeline

        Args:
            transcript: Whisper output with segments
            visual_analyses: LLaVA frame analyses

        Returns:
            Sorted timeline entries
        """
        timeline = []

        # Add transcript segments
        for segment in transcript.get('segments', []):
            timeline.append({
                'timestamp': segment['start'],
                'type': 'transcript',
                'content': segment['text'].strip()
            })

        # Add visual analyses
        for frame in visual_analyses:
            timeline.append({
                'timestamp': frame['timestamp'],
                'type': 'visual',
                'content': frame['analysis'].strip()
            })

        # Sort by timestamp
        timeline.sort(key=lambda x: x['timestamp'])

        return timeline

    def _chunk_timeline(
        self,
        timeline: List[Dict[str, Any]],
        chunk_duration: Optional[int] = None
    ) -> List[List[Dict[str, Any]]]:
        """
        Split timeline into processable chunks

        Args:
            timeline: Merged timeline
            chunk_duration: Chunk size in seconds (default from prompts)

        Returns:
            List of timeline chunks
        """
        if chunk_duration is None:
            chunk_duration = self.prompts.get('chunk_duration_seconds', 120)

        if not timeline:
            return []

        chunks = []
        current_chunk = []
        chunk_start = 0

        for entry in timeline:
            if entry['timestamp'] - chunk_start > chunk_duration and current_chunk:
                chunks.append(current_chunk)
                current_chunk = []
                chunk_start = entry['timestamp']

            current_chunk.append(entry)

        if current_chunk:
            chunks.append(current_chunk)

        return chunks

    def _format_timeline_for_llm(self, timeline: List[Dict[str, Any]]) -> str:
        """
        Format timeline chunk for LLM consumption

        Args:
            timeline: Timeline chunk

        Returns:
            Formatted string for prompt
        """
        formatted = []

        for entry in timeline:
            timestamp_str = self._format_timestamp(entry['timestamp'])
            entry_type = entry['type'].upper()
            content = entry['content']

            formatted.append(f"[{timestamp_str}] {entry_type}: {content}")

        return '\n'.join(formatted)

    def _format_timestamp(self, seconds: float) -> str:
        """Format seconds as HH:MM:SS"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"

    def _extract_from_chunk(self, chunk: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        Extract insights from a single timeline chunk using LLM

        Args:
            chunk: Timeline chunk

        Returns:
            Insights dict or None if extraction fails
        """
        # Format timeline for LLM
        timeline_context = self._format_timeline_for_llm(chunk)

        # Build prompt
        user_prompt = self.prompts['user_prompt_template'].format(
            timeline_context=timeline_context
        )

        messages = [
            {
                'role': 'system',
                'content': self.prompts['system_prompt']
            },
            {
                'role': 'user',
                'content': user_prompt
            }
        ]

        # Call LLM with retry logic
        max_retries = self.prompts.get('max_retries', 2)
        retry_delay = self.prompts.get('retry_delay_seconds', 5)

        for attempt in range(max_retries + 1):
            try:
                response = self.llm.chat(
                    messages=messages,
                    max_tokens=self.prompts.get('max_tokens', 4000)
                )

                # Parse JSON response
                content = response['message']['content']
                insights = json.loads(content)

                return insights

            except json.JSONDecodeError as e:
                print(f"      ⚠️  JSON parse error (attempt {attempt+1}/{max_retries+1}): {str(e)[:50]}")
                if attempt < max_retries:
                    import time
                    time.sleep(retry_delay)
                else:
                    print(f"      ❌ Failed to parse LLM response after {max_retries+1} attempts")
                    return None

            except Exception as e:
                print(f"      ❌ LLM error (attempt {attempt+1}/{max_retries+1}): {str(e)[:100]}")
                if attempt < max_retries:
                    import time
                    time.sleep(retry_delay)
                else:
                    return None

        return None

    def _merge_insights(self, chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Merge insights from multiple chunks

        Args:
            chunks: List of insight dicts

        Returns:
            Merged insights
        """
        merged = {
            'pain_points': [],
            'solutions': [],
            'verbatims': [],
            'golden_moments': [],
            'product_adjacencies': [],
            'metadata': {}
        }

        for chunk in chunks:
            if not chunk:
                continue

            for key in ['pain_points', 'solutions', 'verbatims', 'golden_moments', 'product_adjacencies']:
                if key in chunk:
                    merged[key].extend(chunk[key])

        # Deduplicate
        merged = self._deduplicate(merged)

        # Update metadata
        merged['metadata'] = {
            'total_pain_points': len(merged['pain_points']),
            'total_solutions': len(merged['solutions']),
            'total_verbatims': len(merged['verbatims']),
            'total_golden_moments': len(merged['golden_moments']),
            'total_product_adjacencies': len(merged['product_adjacencies'])
        }

        return merged

    def _deduplicate(self, insights: Dict[str, Any]) -> Dict[str, Any]:
        """
        Remove duplicate insights based on similarity

        Args:
            insights: Insights dict

        Returns:
            Deduplicated insights
        """
        # Simple deduplication based on description similarity
        # For now, just remove exact duplicates

        for key in ['pain_points', 'solutions', 'verbatims']:
            if key not in insights:
                continue

            seen = set()
            unique = []

            for item in insights[key]:
                # Create signature based on description/quote
                if key == 'verbatims':
                    signature = item.get('quote', '')
                else:
                    signature = item.get('description', '')

                if signature and signature not in seen:
                    seen.add(signature)
                    unique.append(item)

            insights[key] = unique

        return insights

    def _validate_insights(self, insights: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and clean insights

        Args:
            insights: Raw insights

        Returns:
            Validated insights
        """
        # Ensure all required keys exist
        validated = {
            'pain_points': insights.get('pain_points', []),
            'solutions': insights.get('solutions', []),
            'verbatims': insights.get('verbatims', []),
            'golden_moments': insights.get('golden_moments', []),
            'product_adjacencies': insights.get('product_adjacencies', []),
            'metadata': insights.get('metadata', {})
        }

        # Validate pain points have required fields
        validated['pain_points'] = [
            p for p in validated['pain_points']
            if p.get('description') and p.get('evidence')
        ]

        # Validate solutions
        validated['solutions'] = [
            s for s in validated['solutions']
            if s.get('description') and s.get('evidence')
        ]

        # Sort by timestamp (handle None values)
        for key in ['pain_points', 'solutions', 'verbatims', 'golden_moments']:
            if validated[key]:
                validated[key].sort(key=lambda x: x.get('timestamp') if x.get('timestamp') is not None else 0)

        return validated
