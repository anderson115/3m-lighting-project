#!/usr/bin/env python3
"""
Tier Manager - Subscription-based Model Selection
Manages model access based on subscription tier (Standard/Pro/Admin)
"""
from pathlib import Path
from typing import Dict, List, Optional
import yaml


class TierManager:
    """Manages model tier access and selection"""

    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize tier manager

        Args:
            config_path: Path to model_tiers.yaml
        """
        if config_path is None:
            project_root = Path(__file__).parent.parent.parent
            config_path = project_root / 'config' / 'model_tiers.yaml'

        with open(config_path) as f:
            self.config = yaml.safe_load(f)

    def get_available_models(self, subscription_tier: str) -> List[Dict]:
        """
        Get list of available models for a subscription tier

        Args:
            subscription_tier: 'free', 'standard', 'pro', or 'admin'

        Returns:
            List of model configs sorted by priority
        """
        tier_access = self.config['tier_access'].get(subscription_tier)

        if not tier_access:
            raise ValueError(f"Unknown subscription tier: {subscription_tier}")

        allowed_tiers = tier_access.get('allowed_tiers', [])

        if not allowed_tiers:
            return []

        # Collect models from all allowed tiers
        models = []
        for tier_name in allowed_tiers:
            tier_config = self.config['tiers'].get(tier_name)
            if tier_config:
                for model in tier_config['models']:
                    if model.get('status') == 'active':
                        models.append({
                            **model,
                            'tier': tier_name,
                            'tier_display': tier_config['display_name']
                        })

        # Sort by priority (lower = better)
        models.sort(key=lambda x: x.get('priority', 999))

        return models

    def get_default_model(self, subscription_tier: str) -> str:
        """
        Get default model name for a subscription tier

        Args:
            subscription_tier: 'free', 'standard', 'pro', or 'admin'

        Returns:
            Model name (e.g., 'togetherai', 'gemini', 'llama')
        """
        tier_access = self.config['tier_access'].get(subscription_tier)

        if not tier_access:
            raise ValueError(f"Unknown subscription tier: {subscription_tier}")

        default_model = tier_access.get('default_model')

        if not default_model:
            # No access
            raise PermissionError(
                tier_access.get('message', 'No access to AI extraction')
            )

        return default_model

    def validate_model_access(self, subscription_tier: str, model_name: str) -> bool:
        """
        Check if user has access to a specific model

        Args:
            subscription_tier: User's subscription tier
            model_name: Model to check (e.g., 'gemini', 'llama')

        Returns:
            True if access allowed, False otherwise
        """
        available_models = self.get_available_models(subscription_tier)
        return any(m['name'] == model_name for m in available_models)

    def get_model_info(self, model_name: str) -> Optional[Dict]:
        """
        Get detailed info about a model

        Args:
            model_name: Model name (e.g., 'gemini')

        Returns:
            Model config dict or None if not found
        """
        for tier_name, tier_config in self.config['tiers'].items():
            for model in tier_config['models']:
                if model['name'] == model_name:
                    return {
                        **model,
                        'tier': tier_name,
                        'tier_display': tier_config['display_name']
                    }
        return None

    def select_model(
        self,
        subscription_tier: str,
        preferred_model: Optional[str] = None,
        admin_override: bool = False
    ) -> str:
        """
        Select best model based on tier and preferences

        Args:
            subscription_tier: User's subscription tier
            preferred_model: Optional user preference
            admin_override: If True, allow admin to use any model

        Returns:
            Selected model name

        Raises:
            PermissionError: If user lacks access
            ValueError: If preferred model invalid
        """
        # Admin override
        if admin_override and subscription_tier == 'admin':
            if preferred_model:
                model_info = self.get_model_info(preferred_model)
                if model_info:
                    return preferred_model
                raise ValueError(f"Model '{preferred_model}' not found")
            # Admin default
            return self.get_default_model('admin')

        # Get available models
        available = self.get_available_models(subscription_tier)

        if not available:
            raise PermissionError(
                self.config['tier_access'][subscription_tier].get(
                    'message',
                    'No access to AI extraction'
                )
            )

        # User preference
        if preferred_model:
            if self.validate_model_access(subscription_tier, preferred_model):
                return preferred_model
            raise PermissionError(
                f"Model '{preferred_model}' not available in {subscription_tier} tier"
            )

        # Default for tier
        return self.get_default_model(subscription_tier)

    def get_tier_pricing(self, subscription_tier: str) -> Dict[str, str]:
        """Get cost estimates for a tier"""
        return self.config.get('cost_estimates', {}).get(subscription_tier, {})

    def get_tier_description(self, tier_name: str) -> str:
        """Get description of a tier"""
        tier = self.config['tiers'].get(tier_name)
        return tier['description'] if tier else "Unknown tier"
