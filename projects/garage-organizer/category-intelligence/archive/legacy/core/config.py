"""
Category Intelligence Configuration
Central configuration for all module settings
"""

from datetime import datetime
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field


class CategoryConfig(BaseModel):
    """Configuration for category intelligence module"""

    # Core Settings
    module_name: str = "category-intelligence"
    version: str = "1.0.0"
    current_date: str = datetime.now().strftime("%Y-%m-%d")

    # Research Parameters
    max_brands_to_discover: int = Field(25, description="Maximum brands to identify")
    max_products_per_subcategory: int = Field(50, description="Product samples per subcategory")
    max_search_results_per_query: int = Field(20, description="Web search result limit")

    # Source Quality Standards
    min_sources_per_claim: int = Field(2, description="Minimum sources for key claims")
    max_source_age_months: int = Field(12, description="Maximum age for current data")
    require_working_urls: bool = Field(True, description="All URLs must be accessible")

    # Data Collection
    enable_web_search: bool = True
    enable_web_scraping: bool = True
    enable_source_archiving: bool = True

    # Output Options
    generate_html_report: bool = True
    generate_json_data: bool = True
    create_audit_trail: bool = True

    # Directories
    module_dir: Path = Field(
        default_factory=lambda: Path(__file__).parent.parent
    )

    @property
    def storage_dir(self) -> Path:
        """Central storage directory for all collected data"""
        path = self.module_dir / "data" / "storage"
        path.mkdir(exist_ok=True, parents=True)
        return path

    @property
    def data_dir(self) -> Path:
        """Data output directory (JSON structured data)"""
        path = self.storage_dir / "structured"
        path.mkdir(exist_ok=True, parents=True)
        return path

    @property
    def sources_dir(self) -> Path:
        """Raw source content directory"""
        path = self.storage_dir / "sources"
        path.mkdir(exist_ok=True, parents=True)
        return path

    @property
    def audit_dir(self) -> Path:
        """Audit trail directory"""
        path = self.storage_dir / "audit"
        path.mkdir(exist_ok=True, parents=True)
        return path

    @property
    def outputs_dir(self) -> Path:
        """Final report outputs directory"""
        path = self.module_dir / "outputs"
        path.mkdir(exist_ok=True, parents=True)
        return path

    def get_category_storage_dir(self, category_name: str) -> Path:
        """Get organized storage directory for specific category"""
        # Sanitize category name for filesystem
        safe_name = "".join(c if c.isalnum() or c in ('-', '_') else '_' for c in category_name)
        safe_name = safe_name.lower().strip('_')

        category_dir = self.storage_dir / safe_name
        category_dir.mkdir(exist_ok=True, parents=True)

        # Create subdirectories
        (category_dir / "sources").mkdir(exist_ok=True)
        (category_dir / "structured").mkdir(exist_ok=True)
        (category_dir / "audit").mkdir(exist_ok=True)

        return category_dir

    # HTTP Settings
    request_timeout: int = Field(30, description="HTTP request timeout (seconds)")
    max_retries: int = Field(3, description="Max retry attempts for failed requests")
    user_agent: str = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Offbrain Insights Bot"

    # Confidence Levels
    confidence_high_threshold: float = 0.8
    confidence_medium_threshold: float = 0.5

    class Config:
        arbitrary_types_allowed = True


# Global config instance
config = CategoryConfig()
