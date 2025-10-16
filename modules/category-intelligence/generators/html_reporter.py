"""
HTML Report Generator
Generates professional client-ready HTML reports with Offbrain Insights branding
"""

import logging
from pathlib import Path
from typing import Dict
from datetime import datetime

logger = logging.getLogger(__name__)


class HTMLReporter:
    """Generates HTML category intelligence reports"""

    def __init__(self, config):
        self.config = config

    def generate_report(
        self,
        category_name: str,
        output_name: str,
        data: Dict
    ) -> Path:
        """
        Generate HTML report from analysis data

        Args:
            category_name: Category being analyzed
            output_name: Output filename base
            data: Complete analysis data

        Returns:
            Path to generated HTML file
        """
        logger.info(f"Generating HTML report for {category_name}")

        html_content = self._build_html(category_name, data)

        # Save report
        output_path = self.config.outputs_dir / f"{output_name}_Category_Intelligence.html"
        output_path.write_text(html_content, encoding='utf-8')

        logger.info(f"✅ HTML report generated: {output_path}")
        return output_path

    def _build_html(self, category_name: str, data: Dict) -> str:
        """Build complete HTML document"""

        brands = data.get('brands', {})
        taxonomy = data.get('taxonomy', {})
        pricing = data.get('pricing', {})
        market_share = data.get('market_share', {})
        market_size = data.get('market_size', {})
        resources = data.get('resources', {})

        brands_html = self._render_brands_section(brands)
        taxonomy_html = self._render_taxonomy_section(taxonomy)
        pricing_html = self._render_pricing_section(pricing)
        market_html = self._render_market_section(market_share, market_size)
        resources_html = self._render_resources_section(resources)

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{category_name} - Category Intelligence Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #1a1a1a;
            background: #f5f5f5;
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        header .subtitle {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        header .meta {{
            margin-top: 20px;
            font-size: 0.9em;
            opacity: 0.8;
        }}
        .content {{
            padding: 40px;
        }}
        .section {{
            margin-bottom: 50px;
        }}
        .section-title {{
            font-size: 1.8em;
            color: #667eea;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }}
        .section-content {{
            padding: 20px;
            background: #fafafa;
            border-radius: 8px;
        }}
        .brand-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        .brand-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .brand-name {{
            font-size: 1.3em;
            font-weight: bold;
            color: #1a1a1a;
            margin-bottom: 8px;
        }}
        .brand-tier {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.85em;
            font-weight: 600;
            margin-bottom: 10px;
        }}
        .tier-premium {{ background: #ffd700; color: #333; }}
        .tier-mid-range {{ background: #c0c0c0; color: #333; }}
        .tier-budget-friendly {{ background: #cd7f32; color: white; }}
        .brand-description {{
            color: #666;
            margin-top: 8px;
        }}
        .confidence {{
            display: inline-block;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.75em;
            margin-top: 8px;
        }}
        .confidence-high {{ background: #d4edda; color: #155724; }}
        .confidence-medium {{ background: #fff3cd; color: #856404; }}
        .confidence-low {{ background: #f8d7da; color: #721c24; }}
        .status-badge {{
            display: inline-block;
            padding: 6px 14px;
            border-radius: 6px;
            font-weight: 600;
            font-size: 0.9em;
        }}
        .status-completed {{ background: #d4edda; color: #155724; }}
        .status-not-implemented {{ background: #f8d7da; color: #721c24; }}
        footer {{
            background: #2c3e50;
            color: white;
            padding: 30px 40px;
            text-align: center;
        }}
        footer .branding {{
            font-size: 1.3em;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        footer .tagline {{
            opacity: 0.8;
            font-size: 0.95em;
        }}
        .info-box {{
            background: #e7f3ff;
            border-left: 4px solid #2196F3;
            padding: 15px;
            margin: 15px 0;
            border-radius: 4px;
        }}
        .warning-box {{
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 15px 0;
            border-radius: 4px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>{category_name}</h1>
            <div class="subtitle">Category Intelligence Report</div>
            <div class="meta">
                Generated: {data.get('analysis_date', 'N/A')} |
                Report Date: {datetime.now().strftime('%Y-%m-%d')} |
                <strong>Offbrain Insights</strong>
            </div>
        </header>

        <div class="content">
            <!-- Brands Section -->
            {brands_html}

            <!-- Taxonomy Section -->
            {taxonomy_html}

            <!-- Pricing Section -->
            {pricing_html}

            <!-- Market Analysis Section -->
            {market_html}

            <!-- Resources Section -->
            {resources_html}
        </div>

        <footer>
            <div class="branding">Offbrain Insights</div>
            <div class="tagline">Authentic Consumer Intelligence | Zero Fabrication Tolerance</div>
            <div style="margin-top: 15px; font-size: 0.85em; opacity: 0.7;">
                © 2025 Offbrain Insights. All data sourced and cited.
            </div>
        </footer>
    </div>
</body>
</html>"""

        return html

    def _render_brands_section(self, brands_data: Dict) -> str:
        """Render brands section"""
        if brands_data.get('status') == 'not_implemented':
            return """
            <div class="section">
                <h2 class="section-title">Major Brands</h2>
                <div class="warning-box">
                    <strong>⚠️ Not Implemented:</strong> Brand discovery stage pending implementation.
                </div>
            </div>
            """

        brands = brands_data.get('brands', [])
        if not brands:
            return """
            <div class="section">
                <h2 class="section-title">Major Brands</h2>
                <div class="info-box">No brand data available.</div>
            </div>
            """

        brand_cards = []
        for brand in brands:
            tier = brand.get('tier', 'unknown').replace(' ', '-')
            confidence = brand.get('confidence', 'unknown')
            brand_cards.append(f"""
                <div class="brand-card">
                    <div class="brand-name">{brand.get('name', 'Unknown')}</div>
                    <span class="brand-tier tier-{tier}">{brand.get('tier', 'Unknown').title()}</span>
                    <div class="brand-description">{brand.get('description', '')}</div>
                    <span class="confidence confidence-{confidence}">Confidence: {confidence.title()}</span>
                </div>
            """)

        status_badge = '<span class="status-badge status-completed">✅ Data Collected</span>'

        return f"""
        <div class="section">
            <h2 class="section-title">Major Brands {status_badge}</h2>
            <div class="info-box">
                <strong>Total Brands Identified:</strong> {len(brands)}
            </div>
            <div class="brand-grid">
                {''.join(brand_cards)}
            </div>
        </div>
        """

    def _render_taxonomy_section(self, taxonomy_data: Dict) -> str:
        """Render product taxonomy section"""
        status = taxonomy_data.get('status', 'not_implemented')
        if status == 'not_implemented':
            return """
            <div class="section">
                <h2 class="section-title">Product Categorization</h2>
                <div class="warning-box">
                    <strong>⚠️ Not Implemented:</strong> Product taxonomy stage pending implementation.
                </div>
            </div>
            """

        subcategories = taxonomy_data.get('subcategories', [])
        if not subcategories:
            return '<div class="section"><h2 class="section-title">Product Categorization</h2><div class="info-box">No data available.</div></div>'

        taxonomy_html = []
        for subcat in subcategories:
            products = subcat.get('product_types', [])
            products_list = ''.join([f'<li>{p}</li>' for p in products])

            taxonomy_html.append(f"""
                <div style="background: white; padding: 20px; margin-bottom: 20px; border-radius: 8px; border-left: 4px solid #667eea;">
                    <h3 style="color: #667eea; margin-bottom: 10px;">{subcat.get('name', 'Unknown')}</h3>
                    <p style="color: #666; margin-bottom: 15px;">{subcat.get('description', '')}</p>
                    <ul style="margin-left: 20px; color: #333;">
                        {products_list}
                    </ul>
                </div>
            """)

        return f"""
        <div class="section">
            <h2 class="section-title">Product Categorization <span class="status-badge status-completed">✅ Data Collected</span></h2>
            <div class="info-box">
                <strong>Total Subcategories:</strong> {len(subcategories)}
            </div>
            {''.join(taxonomy_html)}
        </div>
        """

    def _render_pricing_section(self, pricing_data: Dict) -> str:
        """Render pricing analysis section"""
        status = pricing_data.get('status', 'not_implemented')
        if status == 'not_implemented':
            return """
            <div class="section">
                <h2 class="section-title">Pricing Analysis</h2>
                <div class="warning-box">
                    <strong>⚠️ Not Implemented:</strong> Pricing collection stage pending implementation.
                </div>
            </div>
            """

        price_ranges = pricing_data.get('price_ranges', [])
        if not price_ranges:
            return '<div class="section"><h2 class="section-title">Pricing Analysis</h2><div class="info-box">No data available.</div></div>'

        pricing_cards = []
        for segment in price_ranges:
            products = segment.get('products', [])
            products_html = ''.join([
                f'<div style="margin: 8px 0;"><strong>{p.get("type", "N/A")}:</strong> {p.get("typical_price", "N/A")}</div>'
                for p in products
            ])
            brands = ', '.join(segment.get('brands', []))

            pricing_cards.append(f"""
                <div style="background: white; padding: 20px; margin-bottom: 20px; border-radius: 8px; border-left: 4px solid #667eea; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <h3 style="color: #667eea; margin-bottom: 10px;">{segment.get('segment', 'Unknown')} Segment</h3>
                    <div style="font-size: 1.3em; color: #1a1a1a; font-weight: bold; margin-bottom: 15px;">
                        {segment.get('price_range', 'N/A')}
                    </div>
                    <div style="margin-bottom: 15px;">
                        {products_html}
                    </div>
                    <div style="color: #666; font-size: 0.9em;">
                        <strong>Brands:</strong> {brands}
                    </div>
                </div>
            """)

        installation_html = ""
        installation_costs = pricing_data.get('installation_costs', {})
        if installation_costs:
            installation_html = f"""
                <div class="info-box">
                    <h4 style="margin-bottom: 10px;">Installation Costs</h4>
                    <div><strong>DIY:</strong> {installation_costs.get('diy', 'N/A')}</div>
                    <div><strong>Professional:</strong> {installation_costs.get('professional', 'N/A')}</div>
                </div>
            """

        return f"""
        <div class="section">
            <h2 class="section-title">Pricing Analysis <span class="status-badge status-completed">✅ Data Collected</span></h2>
            <div class="info-box">
                <strong>Market Segments Analyzed:</strong> {len(price_ranges)}
            </div>
            {''.join(pricing_cards)}
            {installation_html}
        </div>
        """

    def _render_market_section(self, market_share_data: Dict, market_size_data: Dict) -> str:
        """Render market analysis section"""
        share_status = market_share_data.get('status', 'not_implemented')
        size_status = market_size_data.get('status', 'not_implemented')

        if share_status == 'not_implemented' and size_status == 'not_implemented':
            return """
            <div class="section">
                <h2 class="section-title">Market Analysis</h2>
                <div class="warning-box">
                    <strong>⚠️ Not Implemented:</strong> Market research stages pending implementation.
                </div>
            </div>
            """

        # Market Share
        share_html = ""
        if share_status == 'completed':
            market_shares = market_share_data.get('market_shares', [])
            shares_cards = []
            for brand_data in market_shares:
                shares_cards.append(f"""
                    <div style="background: white; padding: 15px; margin: 10px 0; border-radius: 6px; border-left: 3px solid #667eea;">
                        <div style="font-weight: bold; color: #1a1a1a; margin-bottom: 5px;">{brand_data.get('brand', 'N/A')}</div>
                        <div style="color: #667eea; font-size: 1.2em; font-weight: bold;">{brand_data.get('estimated_share', 'N/A')}</div>
                        <div style="color: #666; font-size: 0.9em;">{brand_data.get('position', '')}</div>
                        <span class="confidence confidence-{brand_data.get('confidence', 'medium')}">Confidence: {brand_data.get('confidence', 'medium').title()}</span>
                    </div>
                """)

            market_structure = market_share_data.get('market_structure', {})
            structure_html = ""
            if market_structure:
                structure_items = ''.join([
                    f'<div style="margin: 8px 0;"><strong>{k.replace("_", " ").title()}:</strong> {v}</div>'
                    for k, v in market_structure.items()
                ])
                structure_html = f"""
                    <div class="info-box">
                        <h4 style="margin-bottom: 10px;">Market Structure</h4>
                        {structure_items}
                    </div>
                """

            disclaimer = market_share_data.get('disclaimer', '')
            disclaimer_html = f'<div class="warning-box" style="font-size: 0.9em;">{disclaimer}</div>' if disclaimer else ""

            share_html = f"""
                <h3 style="color: #667eea; margin-top: 20px; margin-bottom: 15px;">Market Share Estimates</h3>
                {''.join(shares_cards)}
                {structure_html}
                {disclaimer_html}
            """

        # Market Size
        size_html = ""
        if size_status == 'completed':
            current_size = market_size_data.get('current_size', {})
            projections = market_size_data.get('projections', [])
            growth_drivers = market_size_data.get('growth_drivers', [])
            key_trends = market_size_data.get('key_trends', [])

            current_size_html = f"""
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 8px; margin: 20px 0;">
                    <h4 style="margin-bottom: 10px; opacity: 0.9;">Current Market Size ({current_size.get('year', 'N/A')})</h4>
                    <div style="font-size: 2.5em; font-weight: bold;">{current_size.get('value_usd', 'N/A')}</div>
                    <div style="margin-top: 10px; opacity: 0.8;">Geographic Scope: {current_size.get('geographic_scope', 'N/A')}</div>
                </div>
            """

            projections_html = ""
            if projections:
                proj_cards = ''.join([
                    f"""
                    <div style="background: white; padding: 15px; margin: 10px; border-radius: 6px; border-left: 3px solid #764ba2; flex: 1; min-width: 200px;">
                        <div style="color: #666; font-size: 0.9em;">{proj.get('year', 'N/A')}</div>
                        <div style="font-size: 1.5em; font-weight: bold; color: #1a1a1a; margin: 5px 0;">{proj.get('projected_value', 'N/A')}</div>
                        <div style="color: #764ba2; font-weight: 600;">{proj.get('growth_rate', 'N/A')}</div>
                    </div>
                    """
                    for proj in projections
                ])
                projections_html = f"""
                    <h4 style="color: #667eea; margin: 20px 0 10px 0;">Market Projections</h4>
                    <div style="display: flex; flex-wrap: wrap; gap: 10px;">
                        {proj_cards}
                    </div>
                """

            drivers_html = ""
            if growth_drivers:
                drivers_list = ''.join([f'<li>{driver}</li>' for driver in growth_drivers])
                drivers_html = f"""
                    <div class="info-box">
                        <h4 style="margin-bottom: 10px;">Growth Drivers</h4>
                        <ul style="margin-left: 20px;">
                            {drivers_list}
                        </ul>
                    </div>
                """

            trends_html = ""
            if key_trends:
                trends_list = ''.join([f'<li>{trend}</li>' for trend in key_trends])
                trends_html = f"""
                    <div class="info-box" style="background: #f8f9fa; border-left-color: #764ba2;">
                        <h4 style="margin-bottom: 10px;">Key Market Trends</h4>
                        <ul style="margin-left: 20px;">
                            {trends_list}
                        </ul>
                    </div>
                """

            size_html = f"""
                <h3 style="color: #667eea; margin-top: 30px; margin-bottom: 15px;">Market Size & Growth</h3>
                {current_size_html}
                {projections_html}
                {drivers_html}
                {trends_html}
            """

        return f"""
        <div class="section">
            <h2 class="section-title">Market Analysis <span class="status-badge status-completed">✅ Data Collected</span></h2>
            {share_html}
            {size_html}
        </div>
        """

    def _render_resources_section(self, resources_data: Dict) -> str:
        """Render learning resources section"""
        status = resources_data.get('status', 'not_implemented')
        if status == 'not_implemented':
            return """
            <div class="section">
                <h2 class="section-title">Learning Resources</h2>
                <div class="warning-box">
                    <strong>⚠️ Not Implemented:</strong> Resource curation stage pending implementation.
                </div>
            </div>
            """

        resources = resources_data.get('resources', [])
        if not resources:
            return '<div class="section"><h2 class="section-title">Learning Resources</h2><div class="info-box">No data available.</div></div>'

        # Group resources by category
        resources_by_cat = {}
        for resource in resources:
            category = resource.get('category', 'Other')
            if category not in resources_by_cat:
                resources_by_cat[category] = []
            resources_by_cat[category].append(resource)

        category_sections = []
        for category, items in resources_by_cat.items():
            resource_cards = []
            for resource in items:
                relevance = resource.get('relevance', 'medium')
                relevance_color = '#d4edda' if relevance == 'high' else '#fff3cd'
                relevance_text_color = '#155724' if relevance == 'high' else '#856404'

                resource_cards.append(f"""
                    <div style="background: white; padding: 15px; margin: 10px 0; border-radius: 6px; border-left: 3px solid #667eea; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                        <div style="font-weight: bold; color: #1a1a1a; margin-bottom: 5px;">{resource.get('title', 'N/A')}</div>
                        <div style="color: #666; font-size: 0.9em; margin-bottom: 8px;">{resource.get('provider', 'N/A')}</div>
                        <div style="color: #666; font-size: 0.85em; margin-bottom: 8px;">{resource.get('type', '')}</div>
                        <div style="font-size: 0.8em; color: #666; margin-bottom: 5px;">Authority: {resource.get('authority', 'N/A')}</div>
                        <span style="display: inline-block; padding: 3px 10px; border-radius: 4px; font-size: 0.75em; background: {relevance_color}; color: {relevance_text_color};">Relevance: {relevance.title()}</span>
                    </div>
                """)

            category_sections.append(f"""
                <div style="margin-bottom: 30px;">
                    <h3 style="color: #667eea; margin-bottom: 15px;">{category}</h3>
                    {''.join(resource_cards)}
                </div>
            """)

        return f"""
        <div class="section">
            <h2 class="section-title">Learning Resources <span class="status-badge status-completed">✅ Data Collected</span></h2>
            <div class="info-box">
                <strong>Total Resources Curated:</strong> {len(resources)}
            </div>
            {''.join(category_sections)}
        </div>
        """
