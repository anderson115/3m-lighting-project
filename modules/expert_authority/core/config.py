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
        # Load .env file
        env_path = Path(__file__).parent.parent / "config" / ".env"
        load_dotenv(env_path)

        # Load credentials
        self.reddit_client_id = os.getenv("REDDIT_CLIENT_ID")
        self.reddit_client_secret = os.getenv("REDDIT_CLIENT_SECRET")
        self.reddit_user_agent = os.getenv("REDDIT_USER_AGENT", "3M-Lighting-Research/1.0")

        self.stack_exchange_api_key = os.getenv("STACK_EXCHANGE_API_KEY")
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")

        # Tier configurations
        self.tier_configs = {
            1: {
                "name": "Essential",
                "price": 299,
                "platforms": ["reddit"],
                "discussion_limit": 100,
                "analyzer": "rule_based",
                "output_formats": ["html"],
                "features": ["themes", "consensus"]
            },
            2: {
                "name": "Professional",
                "price": 799,
                "platforms": ["reddit", "stackexchange"],
                "discussion_limit": 300,
                "analyzer": "llm_semantic",
                "llm_model": "claude-sonnet-4-20250514",
                "output_formats": ["html", "excel"],
                "features": ["themes", "consensus", "controversies", "safety_warnings"]
            },
            3: {
                "name": "Enterprise",
                "price": 1999,
                "platforms": ["reddit", "stackexchange", "forums"],
                "discussion_limit": 500,
                "analyzer": "llm_extended",
                "llm_models": ["claude-opus-4-20250514", "gpt-4o"],
                "output_formats": ["html", "excel", "powerpoint", "raw_data"],
                "features": [
                    "themes", "consensus", "controversies", "safety_warnings",
                    "temporal_trends", "competitive_tracking"
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
