"""
HTML Report Generator - Refactored with Jinja2
Generates professional consulting-grade category intelligence reports
"""

import logging
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, Template

logger = logging.getLogger(__name__)


class HTMLReporter:
    """
    Generates professional consulting-grade HTML category intelligence reports.

    Uses Jinja2 templating for clean separation of logic and presentation.
    All methods kept under 50 lines following Oct 2025 standards.
    """

    def __init__(self, config):
        """
        Initialize HTML reporter with Jinja2 environment.

        Args:
            config: Configuration object with outputs_dir
        """
        self.config = config
        self.templates_dir = Path(__file__).parent / "templates"
        self.env = Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
            autoescape=True,
            trim_blocks=True,
            lstrip_blocks=True
        )
        logger.info(f"HTML Reporter initialized with templates from {self.templates_dir}")

    def generate_report(
        self,
        category_name: str,
        output_name: str,
        data: Dict[str, Any]
    ) -> Path:
        """
        Generate professional HTML report.

        Args:
            category_name: Category name (e.g., "Smart Lighting")
            output_name: Output file name prefix
            data: Complete analysis data from orchestrator

        Returns:
            Path to generated HTML file
        """
        logger.info(f"Generating professional report for {category_name}")

        # Prepare template context
        context = self._build_context(category_name, data)

        # Render template
        template = self.env.get_template("report.html.j2")
        html_content = template.render(**context)

        # Write output
        output_path = self.config.outputs_dir / f"{output_name}_Category_Intelligence.html"
        output_path.write_text(html_content, encoding='utf-8')

        file_size_kb = output_path.stat().st_size / 1024
        logger.info(f"✅ Report generated: {output_path} ({file_size_kb:.1f} KB)")
        return output_path

    def _build_context(self, category_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Build complete template context from analysis data.

        Args:
            category_name: Category name
            data: Analysis data

        Returns:
            Template context dictionary
        """
        return {
            "category_name": category_name.title(),
            "generation_date": datetime.now().strftime('%B %d, %Y'),

            # Executive summary context
            **self._prepare_executive_summary(data),

            # Section contexts
            **self._prepare_brands_context(data),
            **self._prepare_taxonomy_context(data),
            **self._prepare_pricing_context(data),
            **self._prepare_market_context(data),
            **self._prepare_resources_context(data),
        }

    def _prepare_executive_summary(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare executive summary context.

        Args:
            data: Complete analysis data

        Returns:
            Executive summary context
        """
        market_size = data.get('market_size', {})
        market_share = data.get('market_share', {})
        taxonomy = data.get('taxonomy', {})
        brands = data.get('brands', {})

        current_size = market_size.get('current_size', {})
        market_shares = market_share.get('market_shares', [])
        projections = market_size.get('projections', [])
        market_structure = market_share.get('market_structure', {})

        top_brand = market_shares[0] if market_shares else {}
        next_year = projections[0] if projections else {}
        concentration = market_structure.get('concentration_ratio', {})

        return {
            "market_size_value": current_size.get('value_midpoint', current_size.get('value_usd', 'N/A')),
            "projected_growth": next_year.get('growth_rate', 'N/A'),
            "leader_share": top_brand.get('estimated_market_share', 'N/A'),
            "leader_name": top_brand.get('brand', 'N/A'),
            "concentration": concentration.get('cr4', 'N/A'),
            "brands_count": len(brands.get('brands', [])),
            "subcategories_count": len(taxonomy.get('subcategories', [])),
            "market_shares_count": len(market_shares),
        }

    def _prepare_brands_context(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare brands section context.

        Args:
            data: Complete analysis data

        Returns:
            Brands section context
        """
        brands_data = data.get('brands', {})
        market_share_data = data.get('market_share', {})

        brands = brands_data.get('brands', [])
        market_shares = market_share_data.get('market_shares', [])

        # Merge and prepare brand data
        brands_merged = self._merge_brand_data(brands, market_shares)

        # Competitive landscape
        competitive_landscape = market_share_data.get('competitive_landscape', {})
        factors = competitive_landscape.get('key_competitive_factors', [])[:5]
        threats = competitive_landscape.get('emerging_threats', [])[:5]

        return {
            "brands": brands_merged,
            "brands_count": len(brands),
            "competitive_factors": factors,
            "emerging_threats": threats,
        }

    def _merge_brand_data(
        self,
        brands: List[Dict[str, Any]],
        market_shares: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Merge brand and market share data.

        Args:
            brands: Brand list
            market_shares: Market share list

        Returns:
            Merged and sorted brand data
        """
        # Create lookup
        market_share_lookup = {
            ms.get('brand', '').lower(): ms
            for ms in market_shares
        }

        # Merge data
        brands_merged = []
        for brand in brands:
            brand_merged = self._extract_brand_data(brand)

            # Match market share data
            brand_name_lower = brand.get('name', '').lower()
            for key in market_share_lookup:
                if key in brand_name_lower or brand_name_lower in key:
                    brand_merged.update(self._extract_market_share_data(market_share_lookup[key]))
                    break

            brands_merged.append(brand_merged)

        # Sort by tier and market share
        return self._sort_brands(brands_merged)

    def _extract_brand_data(self, brand: Dict[str, Any]) -> Dict[str, Any]:
        """Extract and format brand data for template."""
        tier = brand.get('tier', 'tier_5_import')
        tier_num = tier.split('_')[1] if '_' in tier else '5'

        return {
            "name": brand.get('name', 'Unknown'),
            "tier_num": tier_num,
            "market_share": brand.get('estimated_market_share', brand.get('market_share_percent', '—')),
            "revenue": brand.get('estimated_category_revenue', brand.get('estimated_revenue_usd', '—')),
            "position": brand.get('position', '—'),
            "confidence": brand.get('confidence', 'medium'),
            "tier": tier,
        }

    def _extract_market_share_data(self, market_share: Dict[str, Any]) -> Dict[str, Any]:
        """Extract market share data for merging."""
        return {
            "market_share": market_share.get('estimated_market_share', '—'),
            "position": market_share.get('position', '—'),
        }

    def _sort_brands(self, brands: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Sort brands by tier and market share."""
        tier_order = {
            'tier_1_national': 1,
            'tier_2_private_label': 2,
            'tier_3_specialist': 3,
            'tier_4_emerging': 4,
            'tier_5_import': 5
        }

        return sorted(
            brands,
            key=lambda x: (
                tier_order.get(x.get('tier', 'tier_5_import'), 5),
                -self._parse_share(x.get('market_share', '0'))
            )
        )

    def _parse_share(self, share_str: str) -> float:
        """Parse market share percentage for sorting."""
        try:
            match = re.search(r'(\d+)', str(share_str))
            return float(match.group(1)) if match else 0.0
        except Exception:
            return 0.0

    def _prepare_taxonomy_context(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare taxonomy section context.

        Args:
            data: Complete analysis data

        Returns:
            Taxonomy section context
        """
        taxonomy_data = data.get('taxonomy', {})
        subcategories = taxonomy_data.get('subcategories', [])
        category_keywords = taxonomy_data.get('category_keywords', {})

        return {
            "subcategories_count": len(subcategories),
            "consumer_keywords": category_keywords.get('consumer_language', [])[:10],
            "industry_keywords": category_keywords.get('industry_language', [])[:10],
            "subcategories": [
                self._format_subcategory(subcat)
                for subcat in subcategories
            ],
        }

    def _format_subcategory(self, subcat: Dict[str, Any]) -> Dict[str, Any]:
        """Format subcategory data for template."""
        return {
            "name": subcat.get('name', 'Unknown'),
            "market_size": subcat.get('subcategory_market_size_usd', '—'),
            "category_share": subcat.get('market_share_of_category', '—'),
            "units": subcat.get('estimated_units_sold_annually', '—'),
            "brands": subcat.get('number_of_active_brands', '—'),
            "avg_price": subcat.get('average_price_point', '—'),
            "growth": subcat.get('growth_rate_yoy', '—'),
            "keywords": ', '.join(subcat.get('consumer_keywords', [])[:4]),
        }

    def _prepare_pricing_context(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare pricing section context.

        Args:
            data: Complete analysis data

        Returns:
            Pricing section context
        """
        pricing_data = data.get('pricing', {})
        subcategory_pricing = pricing_data.get('subcategory_pricing', [])
        category_dynamics = pricing_data.get('category_price_dynamics', {})

        return {
            "overall_price_range": category_dynamics.get('overall_category_price_range', 'N/A'),
            "avg_transaction": category_dynamics.get('category_average_transaction_value', 'N/A'),
            "dominant_retailers": ', '.join(category_dynamics.get('dominant_retailers', [])[:4]) if category_dynamics.get('dominant_retailers') else 'N/A',
            "pricing_subcategories": [
                self._format_pricing_subcategory(subcat)
                for subcat in subcategory_pricing[:6]  # Limit for space
            ],
        }

    def _format_pricing_subcategory(self, subcat: Dict[str, Any]) -> Dict[str, Any]:
        """Format pricing subcategory for template."""
        top_brands_subcat = subcat.get('top_brands', [])
        brands_text = ', '.join([
            f"{b.get('brand', 'Unknown')} ({b.get('price_range', 'N/A')})"
            for b in top_brands_subcat[:3]
        ]) if top_brands_subcat else ''

        return {
            "name": subcat.get('name', 'Unknown'),
            "top_brands": brands_text,
            "products": [
                self._format_product_pricing(pp)
                for pp in subcat.get('product_pricing', [])[:4]  # Top 4 per subcategory
            ],
        }

    def _format_product_pricing(self, product: Dict[str, Any]) -> Dict[str, Any]:
        """Format product pricing for template."""
        top_brands = product.get('top_brands', [])
        brands_cell = ', '.join([
            b.get('brand', 'Unknown')
            for b in top_brands[:3]
        ]) if top_brands else '—'

        return {
            "type": product.get('product_type', 'Unknown'),
            "price_range": product.get('typical_price_range', '—'),
            "average": product.get('average_price', '—'),
            "units": product.get('units_sold_annually', '—'),
            "top_brands": brands_cell,
        }

    def _prepare_market_context(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare market section context.

        Args:
            data: Complete analysis data

        Returns:
            Market section context
        """
        market_size_data = data.get('market_size', {})
        current_size = market_size_data.get('current_size', {})
        historical = market_size_data.get('historical_growth', [])
        projections = market_size_data.get('projections', [])
        growth_drivers = market_size_data.get('growth_drivers', [])[:5]
        growth_inhibitors = market_size_data.get('growth_inhibitors', [])[:5]

        return {
            "current_size_value": current_size.get('value_usd', 'N/A'),
            "current_size_year": current_size.get('year', 2024),
            "geographic_scope": current_size.get('geographic_scope', 'United States'),
            "historical": [
                {"year": h.get('year', '—'), "size": h.get('market_size_usd', '—'), "growth": h.get('yoy_growth', '—')}
                for h in historical
            ],
            "projections": [
                {
                    "year": p.get('year', '—'),
                    "value": p.get('projected_value', '—'),
                    "growth": p.get('growth_rate', '—'),
                    "confidence": p.get('confidence', 'medium')
                }
                for p in projections
            ],
            "growth_drivers": [
                {
                    "name": d.get("driver", "Unknown"),
                    "impact": d.get("impact", "—"),
                    "description": d.get("description", "")[:90]
                }
                for d in growth_drivers
            ],
            "growth_inhibitors": [
                {
                    "name": i.get("inhibitor", "Unknown"),
                    "impact": i.get("impact", "—"),
                    "description": i.get("description", "")[:90]
                }
                for i in growth_inhibitors
            ],
        }

    def _prepare_resources_context(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare resources section context.

        Args:
            data: Complete analysis data

        Returns:
            Resources section context
        """
        resources_data = data.get('resources', {})
        resource_categories = resources_data.get('resource_categories', [])

        return {
            "total_resources": resources_data.get('total_resources', 0),
            "categories_count": len(resource_categories),
            "resource_categories": [
                {
                    "name": cat.get('category', 'Unknown'),
                    "resources": [
                        {
                            "title": r.get('title', 'Unknown'),
                            "provider": r.get('provider', '—'),
                            "url": r.get('url', '#'),
                            "relevance": r.get('relevance', '—')
                        }
                        for r in cat.get('resources', [])[:5]  # Top 5 per category
                    ]
                }
                for cat in resource_categories[:5]  # Top 5 categories
            ],
        }
