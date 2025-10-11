"""
Configuration management for Creator Intelligence Module.
Loads environment variables and provides centralized config access.
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CreatorIntelligenceConfig:
    """Centralized configuration for Creator Intelligence Module."""

    def __init__(self, env_path: Optional[str] = None):
        """
        Initialize configuration by loading environment variables.

        Args:
            env_path: Path to .env file. If None, looks in modules/creator-intelligence/config/.env
        """
        if env_path is None:
            # Default to module's config directory
            module_root = Path(__file__).parent.parent
            env_path = module_root / "config" / ".env"

        # Load environment variables
        if Path(env_path).exists():
            load_dotenv(env_path, override=True)
            logger.info(f"✅ Loaded config from {env_path}")
        else:
            logger.warning(f"⚠️  .env file not found at {env_path}")

        # ============================================================================
        # API CREDENTIALS
        # ============================================================================

        # YouTube Data API v3
        self.youtube_api_key = os.getenv('YOUTUBE_API_KEY')
        if not self.youtube_api_key:
            logger.warning("⚠️  YOUTUBE_API_KEY not set")

        # LLM API (Gemini Flash for cost efficiency)
        self.llm_provider = os.getenv('LLM_PROVIDER', 'gemini')
        self.llm_model = os.getenv('LLM_MODEL', 'gemini-1.5-flash')
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        self.openai_api_key = os.getenv('OPENAI_API_KEY')

        if self.llm_provider == 'gemini' and not self.gemini_api_key:
            logger.warning("⚠️  GEMINI_API_KEY not set but LLM_PROVIDER is 'gemini'")

        # Apify (for Instagram/TikTok scraping)
        self.apify_token = os.getenv('APIFY_TOKEN')
        self.apify_actor_instagram = os.getenv('APIFY_ACTOR_INSTAGRAM', 'GdWCkxBtKWOsKjdch')
        self.apify_actor_tiktok = os.getenv('APIFY_ACTOR_TIKTOK', 'apify/tiktok-scraper')

        # Etsy API v3
        self.etsy_api_key = os.getenv('ETSY_API_KEY')
        self.etsy_shared_secret = os.getenv('ETSY_SHARED_SECRET')
        self.etsy_oauth_token = os.getenv('ETSY_OAUTH_TOKEN')
        self.etsy_oauth_token_secret = os.getenv('ETSY_OAUTH_TOKEN_SECRET')
        self.etsy_rate_limit_qps = int(os.getenv('ETSY_RATE_LIMIT_QPS', '5'))
        self.etsy_rate_limit_qpd = int(os.getenv('ETSY_RATE_LIMIT_QPD', '5000'))

        # ============================================================================
        # MODULE CONFIGURATION
        # ============================================================================

        # Data collection tier (1=APIs only, 2=managed scrapers, 3=aggressive)
        self.default_tier = int(os.getenv('DEFAULT_TIER', '2'))

        # Platform enable/disable flags
        self.enable_youtube = os.getenv('ENABLE_YOUTUBE', 'true').lower() == 'true'
        self.enable_etsy = os.getenv('ENABLE_ETSY', 'true').lower() == 'true'
        self.enable_instagram = os.getenv('ENABLE_INSTAGRAM', 'true').lower() == 'true'
        self.enable_tiktok = os.getenv('ENABLE_TIKTOK', 'true').lower() == 'true'

        # Scraping strategy
        self.use_apify_primary = os.getenv('USE_APIFY_PRIMARY', 'true').lower() == 'true'

        # Rate limiting (seconds between requests)
        self.instagram_rate_limit = int(os.getenv('INSTAGRAM_RATE_LIMIT', '150'))  # 2.5 min
        self.tiktok_rate_limit = int(os.getenv('TIKTOK_RATE_LIMIT', '5'))  # 5 sec

        # ============================================================================
        # PATHS
        # ============================================================================

        self.module_root = Path(__file__).parent.parent
        self.data_dir = self.module_root / "data"
        self.cache_dir = self.data_dir / "cache"
        self.reports_dir = self.data_dir / "reports"
        self.database_dir = self.data_dir / "database"
        self.logs_dir = self.data_dir / "logs"

        # Platform-specific cache directories
        self.youtube_cache = self.cache_dir / "youtube"
        self.etsy_cache = self.cache_dir / "etsy"
        self.instagram_cache = self.cache_dir / "instagram"
        self.tiktok_cache = self.cache_dir / "tiktok"

        # Database path
        self.database_path = self.database_dir / "creators.db"

        # Ensure directories exist
        for directory in [
            self.cache_dir, self.reports_dir, self.database_dir, self.logs_dir,
            self.youtube_cache, self.etsy_cache, self.instagram_cache, self.tiktok_cache
        ]:
            directory.mkdir(parents=True, exist_ok=True)

    def validate(self) -> bool:
        """
        Validate that required configuration is present.

        Returns:
            True if all required config is present, False otherwise
        """
        errors = []

        # Check YouTube API (required for Tier 1)
        if self.enable_youtube and not self.youtube_api_key:
            errors.append("YouTube enabled but YOUTUBE_API_KEY not set")

        # Check LLM API (required)
        if self.llm_provider == 'gemini' and not self.gemini_api_key:
            errors.append("LLM provider is 'gemini' but GEMINI_API_KEY not set")
        elif self.llm_provider == 'anthropic' and not self.anthropic_api_key:
            errors.append("LLM provider is 'anthropic' but ANTHROPIC_API_KEY not set")
        elif self.llm_provider == 'openai' and not self.openai_api_key:
            errors.append("LLM provider is 'openai' but OPENAI_API_KEY not set")

        # Check Etsy API (required if enabled)
        if self.enable_etsy and not self.etsy_api_key:
            errors.append("Etsy enabled but ETSY_API_KEY not set")

        # Check Apify (required for Tier 2 if Instagram/TikTok enabled)
        if self.default_tier >= 2 and self.use_apify_primary:
            if (self.enable_instagram or self.enable_tiktok) and not self.apify_token:
                errors.append("Tier 2+ with Instagram/TikTok enabled but APIFY_TOKEN not set")

        if errors:
            logger.error("❌ Configuration validation failed:")
            for error in errors:
                logger.error(f"   - {error}")
            return False

        logger.info("✅ Configuration validation passed")
        return True

    def get_llm_api_key(self) -> Optional[str]:
        """Get the API key for the configured LLM provider."""
        if self.llm_provider == 'gemini':
            return self.gemini_api_key
        elif self.llm_provider == 'anthropic':
            return self.anthropic_api_key
        elif self.llm_provider == 'openai':
            return self.openai_api_key
        return None

    def __repr__(self) -> str:
        """String representation of config (without exposing secrets)."""
        return f"""CreatorIntelligenceConfig(
    llm_provider='{self.llm_provider}',
    llm_model='{self.llm_model}',
    default_tier={self.default_tier},
    enabled_platforms={{
        'youtube': {self.enable_youtube},
        'etsy': {self.enable_etsy},
        'instagram': {self.enable_instagram},
        'tiktok': {self.enable_tiktok}
    }},
    database_path='{self.database_path}'
)"""


# Singleton instance for easy import
config = CreatorIntelligenceConfig()


if __name__ == "__main__":
    # Test configuration loading
    print(config)
    config.validate()
