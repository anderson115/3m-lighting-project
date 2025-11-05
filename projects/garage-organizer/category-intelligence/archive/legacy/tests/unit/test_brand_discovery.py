"""
Unit tests for BrandDiscovery collector
Tests brand discovery logic and data structures
"""

import pytest
from collectors.brand_discovery import (
    BrandDiscovery,
    Brand,
    BrandTier,
    BrandDiscoveryError
)


@pytest.mark.unit
@pytest.mark.collector
class TestBrandTier:
    """Test BrandTier enum"""

    def test_tier_values(self):
        """Test tier enum values"""
        assert BrandTier.TIER_1_NATIONAL == "tier_1_national"
        assert BrandTier.TIER_2_PRIVATE_LABEL == "tier_2_private_label"
        assert BrandTier.TIER_3_SPECIALIST == "tier_3_specialist"
        assert BrandTier.TIER_4_EMERGING == "tier_4_emerging"
        assert BrandTier.TIER_5_IMPORT == "tier_5_import"


@pytest.mark.unit
@pytest.mark.collector
class TestBrand:
    """Test Brand dataclass"""

    def test_brand_creation(self):
        """Test creating a Brand object"""
        brand = Brand(
            name="Test Brand",
            tier=BrandTier.TIER_1_NATIONAL
        )

        assert brand.name == "Test Brand"
        assert brand.tier == BrandTier.TIER_1_NATIONAL
        assert brand.distribution_channels == []
        assert brand.source_urls == []

    def test_brand_with_optional_fields(self):
        """Test Brand with all optional fields"""
        brand = Brand(
            name="Complete Brand",
            tier=BrandTier.TIER_2_PRIVATE_LABEL,
            parent_company="Parent Corp",
            estimated_revenue="$500M",
            market_share="15%",
            distribution_channels=["Amazon", "Home Depot"],
            source_urls=["https://example.com/report"]
        )

        assert brand.parent_company == "Parent Corp"
        assert brand.estimated_revenue == "$500M"
        assert brand.market_share == "15%"
        assert len(brand.distribution_channels) == 2
        assert len(brand.source_urls) == 1


@pytest.mark.unit
@pytest.mark.collector
class TestBrandDiscovery:
    """Test BrandDiscovery class"""

    def test_initialization(self, test_config):
        """Test BrandDiscovery initializes correctly"""
        discovery = BrandDiscovery(test_config)

        assert discovery.config == test_config
        assert discovery.min_brands_required == 15

    def test_brand_to_dict(self, test_config):
        """Test converting Brand object to dictionary"""
        discovery = BrandDiscovery(test_config)

        brand = Brand(
            name="Test Brand",
            tier=BrandTier.TIER_1_NATIONAL,
            estimated_revenue="$500M",
            source_urls=["https://example.com"]
        )

        brand_dict = discovery._brand_to_dict(brand)

        assert brand_dict["name"] == "Test Brand"
        assert brand_dict["tier"] == "tier_1_national"
        assert brand_dict["estimated_revenue"] == "$500M"
        assert brand_dict["source_count"] == 1

    def test_count_by_tier(self, test_config):
        """Test counting brands by tier"""
        discovery = BrandDiscovery(test_config)

        brands = [
            Brand("Brand1", BrandTier.TIER_1_NATIONAL),
            Brand("Brand2", BrandTier.TIER_1_NATIONAL),
            Brand("Brand3", BrandTier.TIER_3_SPECIALIST),
        ]

        counts = discovery._count_by_tier(brands)

        assert counts["tier_1_national"] == 2
        assert counts["tier_3_specialist"] == 1

    def test_estimate_coverage(self, test_config):
        """Test market coverage estimation"""
        discovery = BrandDiscovery(test_config)

        assert discovery._estimate_coverage(60) == "95%+"
        assert discovery._estimate_coverage(40) == "80-90%"
        assert discovery._estimate_coverage(25) == "60-80%"
        assert discovery._estimate_coverage(15) == "<60%"

    def test_generate_summary(self, test_config):
        """Test summary generation"""
        discovery = BrandDiscovery(test_config)

        brands = [
            Brand("Brand1", BrandTier.TIER_1_NATIONAL),
            Brand("Brand2", BrandTier.TIER_3_SPECIALIST),
        ]

        summary = discovery._generate_summary(brands)

        assert "Discovered 2 brands" in summary
        assert "Coverage:" in summary

    def test_deduplicate_brands(self, test_config):
        """Test brand deduplication logic"""
        discovery = BrandDiscovery(test_config)

        brands = [
            Brand("Philips Hue", BrandTier.TIER_1_NATIONAL, source_urls=["url1"]),
            Brand("PHILIPS HUE", BrandTier.TIER_1_NATIONAL, source_urls=["url1", "url2"]),
            Brand("LIFX", BrandTier.TIER_3_SPECIALIST, source_urls=["url3"]),
        ]

        unique_brands = discovery._deduplicate_brands(brands)

        # Should have 2 brands (Philips Hue deduplicated)
        assert len(unique_brands) == 2

        # Should keep the brand with more source URLs
        philips_brand = next(b for b in unique_brands if b.name.lower() == "philips hue")
        assert len(philips_brand.source_urls) == 2

    def test_deduplicate_case_insensitive(self, test_config):
        """Test deduplication is case-insensitive"""
        discovery = BrandDiscovery(test_config)

        brands = [
            Brand("Test Brand", BrandTier.TIER_1_NATIONAL),
            Brand("test brand", BrandTier.TIER_1_NATIONAL),
            Brand("TEST BRAND", BrandTier.TIER_1_NATIONAL),
        ]

        unique_brands = discovery._deduplicate_brands(brands)
        assert len(unique_brands) == 1

    def test_discover_brands_not_implemented(self, test_config):
        """Test that discover_brands raises BrandDiscoveryError when insufficient brands discovered"""
        discovery = BrandDiscovery(test_config)

        with pytest.raises(BrandDiscoveryError) as exc_info:
            discovery.discover_brands("test category")

        assert "Insufficient brands discovered" in str(exc_info.value)

    def test_check_data_sources_available(self, test_config):
        """Test checking if data sources are available"""
        discovery = BrandDiscovery(test_config)

        # Should return False until services are integrated
        available = discovery._check_data_sources_available()

        # This will be False until services are implemented
        assert isinstance(available, bool)


@pytest.mark.unit
@pytest.mark.collector
class TestBrandDiscoveryError:
    """Test BrandDiscoveryError exception"""

    def test_error_creation(self):
        """Test creating BrandDiscoveryError"""
        error = BrandDiscoveryError("Test error message")
        assert str(error) == "Test error message"

    def test_error_raising(self):
        """Test raising BrandDiscoveryError"""
        with pytest.raises(BrandDiscoveryError) as exc_info:
            raise BrandDiscoveryError("Test error")

        assert "Test error" in str(exc_info.value)
