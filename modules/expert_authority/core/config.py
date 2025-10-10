#!/usr/bin/env python3
"""
Configuration Manager for Expert Authority Module
Loads credentials from .env and provides tier-specific configs
"""

import os
from pathlib import Path
from typing import Dict, Optional
from dotenv import load_dotenv

class Config:
    """Configuration manager with .env support"""

    def __init__(self):
        # Load .env file (override=True forces loading from file even if env var exists)
        env_path = Path(__file__).parent.parent / "config" / ".env"
        load_dotenv(env_path, override=True)

        # Load credentials - Data Sources
        self.reddit_client_id = os.getenv("REDDIT_CLIENT_ID")
        self.reddit_client_secret = os.getenv("REDDIT_CLIENT_SECRET")
        self.reddit_user_agent = os.getenv("REDDIT_USER_AGENT", "3M-Lighting-Research/1.0")
        self.stack_exchange_api_key = os.getenv("STACK_EXCHANGE_API_KEY")

        # Load credentials - LLM APIs (Primary)
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")

        # Load credentials - LLM APIs (Fallback)
        self.deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.togetherai_api_key = os.getenv("TOGETHERAI_API_KEY")

        # Tier configurations with model fallback priorities
        self.tier_configs = {
            1: {
                "name": "Essential",
                "price": 299,
                "platforms": ["reddit"],
                "discussion_limit": 100,
                "analyzer": "rule_based",
                "llm_models": [],  # No LLM for Tier 1 (rule-based only)
                "output_formats": ["html"],
                "features": ["themes", "consensus"]
            },
            2: {
                "name": "Professional",
                "price": 799,
                "platforms": ["reddit", "stackexchange"],
                "discussion_limit": 300,
                "analyzer": "llm_semantic",
                "llm_models": [
                    # Priority 1: Claude Sonnet 4 (best balance of cost/quality)
                    {"provider": "anthropic", "model": "claude-sonnet-4-20250514", "priority": 1},
                    # Priority 2: GPT-4o-mini (cost-effective fallback)
                    {"provider": "openai", "model": "gpt-4o-mini", "priority": 2},
                    # Priority 3: DeepSeek (cheap fallback)
                    {"provider": "deepseek", "model": "deepseek-chat", "priority": 3},
                ],
                "output_formats": ["html", "excel"],
                "features": ["themes", "consensus", "controversies", "safety_warnings"]
            },
            3: {
                "name": "Enterprise",
                "price": 1999,
                "platforms": ["reddit", "stackexchange", "forums"],
                "discussion_limit": 500,
                "analyzer": "llm_extended",
                "llm_models": [
                    # Priority 1: Claude Opus 4 (highest quality, main analysis)
                    {"provider": "anthropic", "model": "claude-opus-4-20250514", "priority": 1, "use_case": "primary_analysis"},
                    # Priority 2: GPT-4o (cross-validation)
                    {"provider": "openai", "model": "gpt-4o", "priority": 2, "use_case": "cross_validation"},
                    # Priority 3: Claude Sonnet 4 (quality fallback)
                    {"provider": "anthropic", "model": "claude-sonnet-4-20250514", "priority": 3, "use_case": "fallback"},
                    # Priority 4: DeepSeek (emergency fallback)
                    {"provider": "deepseek", "model": "deepseek-chat", "priority": 4, "use_case": "emergency_fallback"},
                ],
                "output_formats": ["html", "excel", "powerpoint", "raw_data"],
                "features": [
                    "themes", "consensus", "controversies", "safety_warnings",
                    "temporal_trends", "competitive_tracking", "cross_model_validation"
                ]
            }
        }

    def get_tier_config(self, tier: int) -> Dict:
        """Get configuration for specific tier"""
        if tier not in self.tier_configs:
            raise ValueError(f"Invalid tier: {tier}. Must be 1, 2, or 3")
        return self.tier_configs[tier]

    def validate_credentials(self, tier: int) -> bool:
        """Validate that required credentials are present for tier"""
        config = self.get_tier_config(tier)

        # Reddit credentials (required for all tiers)
        if "reddit" in config["platforms"]:
            if not self.reddit_client_id or not self.reddit_client_secret:
                raise ValueError(
                    "Reddit credentials missing. "
                    "Set REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET in config/.env"
                )

        # Stack Exchange API key (recommended for Tier 2+)
        if "stackexchange" in config["platforms"]:
            if not self.stack_exchange_api_key:
                print("⚠️  Warning: STACK_EXCHANGE_API_KEY not set. Rate limit: 300/day instead of 10,000/day")

        # Anthropic API key (for LLM analysis Tier 2+)
        if config["analyzer"] in ["llm_semantic", "llm_extended"]:
            if not self.anthropic_api_key:
                print("⚠️  Warning: ANTHROPIC_API_KEY not set. Falling back to rule-based analysis")

        # OpenAI API key (for Tier 3 extended reasoning)
        if tier == 3 and not self.openai_api_key:
            print("⚠️  Warning: OPENAI_API_KEY not set. Extended reasoning unavailable")

        return True

    def get_reddit_config(self) -> Dict:
        """Get Reddit API configuration"""
        return {
            "client_id": self.reddit_client_id,
            "client_secret": self.reddit_client_secret,
            "user_agent": self.reddit_user_agent
        }

    def get_stack_exchange_config(self) -> Dict:
        """Get Stack Exchange API configuration"""
        return {
            "api_key": self.stack_exchange_api_key
        }

    def get_llm_config(self, tier: int) -> Dict:
        """
        Get LLM API configuration for the specified tier with fallback chain

        Returns dict with provider, model, api_key, and fallback chain
        """
        tier_config = self.get_tier_config(tier)
        llm_models = tier_config.get("llm_models", [])

        if not llm_models:
            return {"provider": None, "model": None, "api_key": None, "fallback_chain": []}

        # Build fallback chain with available API keys
        available_models = []
        for model_config in llm_models:
            provider = model_config["provider"]
            api_key = self._get_api_key_for_provider(provider)

            if api_key:
                available_models.append({
                    "provider": provider,
                    "model": model_config["model"],
                    "api_key": api_key,
                    "priority": model_config["priority"],
                    "use_case": model_config.get("use_case", "general")
                })

        # Sort by priority and return primary + fallback chain
        available_models.sort(key=lambda x: x["priority"])

        if available_models:
            primary = available_models[0]
            return {
                "provider": primary["provider"],
                "model": primary["model"],
                "api_key": primary["api_key"],
                "use_case": primary.get("use_case", "general"),
                "fallback_chain": available_models[1:] if len(available_models) > 1 else []
            }

        return {"provider": None, "model": None, "api_key": None, "fallback_chain": []}

    def _get_api_key_for_provider(self, provider: str) -> Optional[str]:
        """Get API key for specified provider"""
        provider_map = {
            "anthropic": self.anthropic_api_key,
            "openai": self.openai_api_key,
            "deepseek": self.deepseek_api_key,
            "gemini": self.gemini_api_key,
            "togetherai": self.togetherai_api_key,
        }
        return provider_map.get(provider)
