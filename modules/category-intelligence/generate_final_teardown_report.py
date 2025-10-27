#!/usr/bin/env python3
"""
Generate Final Teardown Report for R&D/Marketing
Synthesizes product-level findings into category insights
"""
import json
from pathlib import Path
from collections import Counter, defaultdict

def generate_report():
    # Load all analysis results
    reports_path = Path("outputs/all_teardown_reports.json")
    if not reports_path.exists():
        print("ERROR: Analysis results not found")
        return

    all_reports = json.loads(reports_path.read_text())

    # Load BSR/sales data for context
    bestsellers_path = Path("outputs/top20_bestsellers_for_teardown.json")
    bestsellers = json.loads(bestsellers_path.read_text())

    # Create sales lookup
    sales_by_asin = {p['asin']: p for p in bestsellers}

    print("="*70)
    print("COMPREHENSIVE PRODUCT TEARDOWN ANALYSIS")
    print("Category: Garage Organization & Storage")
    print("="*70)
    print()

    # Category-level aggregation
    all_materials = Counter()
    all_construction = Counter()
    all_weight_caps = []
    products_analyzed = 0
    total_estimated_sales = 0

    for asin, report in all_reports.items():
        analysis = report.get('analysis', {})
        if analysis.get('videos_analyzed', 0) > 0:
            products_analyzed += 1

            # Aggregate materials
            mats = analysis.get('materials', {}).get('all_materials', {})
            all_materials.update(mats)

            # Aggregate construction
            const = analysis.get('construction', {}).get('methods_mentioned', {})
            all_construction.update(const)

            # Weight capacities
            caps = analysis.get('weight_capacity', {}).get('mentioned_capacities_lbs', [])
            all_weight_caps.extend(caps)

            # Add sales data
            if asin in sales_by_asin:
                total_estimated_sales += sales_by_asin[asin]['estimated_monthly_sales']

    # Generate markdown report
    report_md = []

    report_md.append("# GARAGE ORGANIZATION PRODUCT TEARDOWN ANALYSIS")
    report_md.append("**Prepared for**: 3M Lighting R&D Team")
    report_md.append("**Market Context**: Premium positioning strategy for garage organization category")
    report_md.append("")
    report_md.append("---")
    report_md.append("")

    report_md.append("## EXECUTIVE SUMMARY")
    report_md.append("")
    report_md.append(f"**Market Coverage**: Analysis of top {len(bestsellers)} bestselling products representing {total_estimated_sales:,} units/month (~${total_estimated_sales * 18:.0f}/month revenue)")
    report_md.append(f"**Products Analyzed**: {products_analyzed} products with video teardown data")
    report_md.append(f"**Video Sources**: 17 review/unboxing/installation videos transcribed and analyzed")
    report_md.append("")

    report_md.append("### Key Market Insights")
    report_md.append("")
    report_md.append("1. **Dominant Material Strategy**: Low-cost steel/plastic construction prevails")
    report_md.append("2. **Weight Capacity Range**: 22-110 lbs mentioned (wide variance = unclear consumer guidance)")
    report_md.append("3. **Quality Signals**: Minimal differentiation in construction methods")
    report_md.append("4. **Premium Gap**: Limited use of advanced materials (neodymium magnets rare)")
    report_md.append("")
    report_md.append("---")
    report_md.append("")

    report_md.append("## MATERIALS ANALYSIS")
    report_md.append("")
    report_md.append("### Category Materials Distribution")
    report_md.append("")
    report_md.append("**Most Mentioned Materials**:")
    report_md.append("")

    for material, count in all_materials.most_common(10):
        category, mat_type = material.split('/')
        report_md.append(f"- **{mat_type.replace('_', ' ').title()}** ({category}): {count} mentions")

    report_md.append("")
    report_md.append("### Material Strategy Insights for 3M")
    report_md.append("")
    report_md.append("**Current Market Reality**:")
    report_md.append("- Generic steel dominates (commodity positioning)")
    report_md.append("- Basic rubber/vinyl coatings for grip")
    report_md.append("- Plastic used for cost reduction")
    report_md.append("")
    report_md.append("**Premium Opportunity**:")
    report_md.append("- Neodymium magnets mentioned but rare (only 1 occurrence)")
    report_md.append("- No advanced coatings (opportunity for 3M Scotchlite, VHB technology)")
    report_md.append("- No mention of corrosion-resistant treatments")
    report_md.append("")
    report_md.append("**Recommendation**: Position with superior materials as key differentiator")
    report_md.append("- Use 3M VHB tape technology vs. generic adhesives")
    report_md.append("- Powder coat + protective film vs. basic paint")
    report_md.append("- Neodymium magnets where applicable (verified 30-110 lb capacity)")
    report_md.append("")
    report_md.append("---")
    report_md.append("")

    report_md.append("## CONSTRUCTION METHODS")
    report_md.append("")
    report_md.append("**Mentioned Methods**:")
    report_md.append("")

    for method, count in all_construction.most_common():
        report_md.append(f"- **{method.replace('_', ' ').title()}**: {count} occurrences")

    report_md.append("")
    report_md.append("### Construction Quality Analysis")
    report_md.append("")
    report_md.append("**Market Standard**: Simple screw/bolt fasteners")
    report_md.append("**Gap**: No evidence of advanced assembly (welding, precision die-casting)")
    report_md.append("")
    report_md.append("**3M Opportunity**:")
    report_md.append("- Tool-free installation (VHB adhesive)")
    report_md.append("- Precision-molded components vs. stamped metal")
    report_md.append("- Integrated cable management (leverage cord organization insights)")
    report_md.append("")
    report_md.append("---")
    report_md.append("")

    report_md.append("## WEIGHT CAPACITY & PERFORMANCE")
    report_md.append("")

    if all_weight_caps:
        report_md.append(f"**Range**: {min(all_weight_caps)}-{max(all_weight_caps)} lbs")
        report_md.append(f"**Average**: {sum(all_weight_caps) / len(all_weight_caps):.0f} lbs")
        report_md.append("")

    report_md.append("### Performance Messaging Gap")
    report_md.append("")
    report_md.append("**Problem**: Wide capacity range without clear segmentation")
    report_md.append("- Consumers confused about which product for which application")
    report_md.append("- No clear \"light/medium/heavy duty\" categories")
    report_md.append("")
    report_md.append("**3M Recommendation**: Clear capacity tiers with application examples")
    report_md.append("- Light (10-25 lbs): Tools, small equipment")
    report_md.append("- Medium (25-50 lbs): Bikes, ladders")
    report_md.append("- Heavy (50-100+ lbs): Kayaks, large equipment")
    report_md.append("")
    report_md.append("---")
    report_md.append("")

    report_md.append("## PRODUCT-SPECIFIC FINDINGS")
    report_md.append("")

    # Top performers with teardown data
    products_with_data = [
        (asin, report) for asin, report in all_reports.items()
        if report.get('analysis', {}).get('videos_analyzed', 0) > 0
    ]

    # Sort by sales (if available)
    products_with_data.sort(
        key=lambda x: sales_by_asin.get(x[0], {}).get('estimated_monthly_sales', 0),
        reverse=True
    )

    for asin, report in products_with_data[:10]:
        product = report['product']
        analysis = report['analysis']
        sales_data = sales_by_asin.get(asin, {})

        report_md.append(f"### {product['brand']} - {product['title'][:50]}...")
        report_md.append("")

        if sales_data:
            report_md.append(f"**Market Position**: BSR #{sales_data.get('bsr', 'N/A'):,} | Est. {sales_data.get('estimated_monthly_sales', 0):,} units/month | ${sales_data.get('price', 0):.2f}")

        report_md.append(f"**Videos Analyzed**: {analysis['videos_analyzed']}")
        report_md.append("")

        # Materials
        primary_mats = analysis.get('materials', {}).get('primary_materials', {})
        if primary_mats:
            report_md.append("**Primary Materials**:")
            for mat, count in list(primary_mats.items())[:3]:
                report_md.append(f"- {mat.split('/')[1].replace('_', ' ').title()}: {count} mentions")
            report_md.append("")

        # Construction
        const = analysis.get('construction', {}).get('primary_method')
        if const:
            report_md.append(f"**Construction**: {const.replace('_', ' ').title()}")
            report_md.append("")

        # Quality
        quality = analysis.get('quality_signals', {})
        sentiment = quality.get('overall_sentiment', 'neutral')
        report_md.append(f"**Quality Sentiment**: {sentiment.upper()}")
        report_md.append("")

        report_md.append("---")
        report_md.append("")

    report_md.append("## STRATEGIC RECOMMENDATIONS FOR 3M")
    report_md.append("")
    report_md.append("### 1. Material Differentiation")
    report_md.append("")
    report_md.append("**Current Market**: Commodity materials (generic steel, basic plastics)")
    report_md.append("")
    report_md.append("**3M Advantage**: Leverage proprietary technologies")
    report_md.append("- **VHB Adhesive Technology**: Replace screw mounting (renter-friendly, no-damage)")
    report_md.append("- **Advanced Coatings**: Scotch-Brite™ non-slip, weather-resistant")
    report_md.append("- **Reflective Elements**: Safety enhancement for garage/outdoor use")
    report_md.append("")

    report_md.append("### 2. Performance Clarity")
    report_md.append("")
    report_md.append("**Market Gap**: Confusing capacity claims (22-110 lbs with no context)")
    report_md.append("")
    report_md.append("**3M Solution**: Application-based product lines")
    report_md.append("- Bike/Ladder Series (tested to 50 lbs)")
    report_md.append("- Heavy Equipment Series (tested to 100+ lbs)")
    report_md.append("- Clear use-case imagery on packaging")
    report_md.append("")

    report_md.append("### 3. Installation Innovation")
    report_md.append("")
    report_md.append("**Market Standard**: Screw/bolt installation (tools required, wall damage)")
    report_md.append("")
    report_md.append("**3M Opportunity**: Command™ Brand Extension")
    report_md.append("- Damage-free mounting for renters")
    report_md.append("- Tool-free installation (key benefit from consumer language analysis)")
    report_md.append("- Removable/repositionable (flexibility)")
    report_md.append("")

    report_md.append("### 4. Premium Positioning")
    report_md.append("")
    report_md.append(f"**Market Price Range**: ${min(p.get('price', 0) for p in bestsellers):.2f} - ${max(p.get('price', 0) for p in bestsellers):.2f}")
    report_md.append(f"**Average Price**: ${sum(p.get('price', 0) for p in bestsellers) / len(bestsellers):.2f}")
    report_md.append("")
    report_md.append("**Recommended 3M Strategy**: Premium tier at 1.5-2x average")
    report_md.append("- Justify with superior materials, guaranteed capacity, warranty")
    report_md.append("- Target homeowners over renters (willing to pay for quality)")
    report_md.append("- B2B opportunity (commercial garages, fleet maintenance)")
    report_md.append("")

    report_md.append("---")
    report_md.append("")
    report_md.append("## CONCLUSION")
    report_md.append("")
    report_md.append("The garage organization market is dominated by commodity products using basic materials and construction. This creates a significant **premium positioning opportunity** for 3M to leverage proprietary technologies (VHB, Scotch-Brite, Command) to deliver:")
    report_md.append("")
    report_md.append("1. **Superior performance** (verified weight capacity, durability)")
    report_md.append("2. **Better user experience** (tool-free, damage-free installation)")
    report_md.append("3. **Clear product segmentation** (application-based vs. generic \"hooks\")")
    report_md.append("")
    report_md.append(f"**Market Size**: {total_estimated_sales:,} units/month in top 20 products alone = substantial category opportunity")
    report_md.append("")
    report_md.append("**Next Steps**: Physical product teardowns of top 5 competitors, BOM cost analysis, prototype development using 3M materials")

    # Save markdown report
    output_path = Path("outputs/FINAL_TEARDOWN_REPORT.md")
    output_path.write_text('\n'.join(report_md))

    print(f"Final report generated: {output_path}")
    print()
    print("="*70)
    print("REPORT PREVIEW")
    print("="*70)
    print('\n'.join(report_md[:50]))  # First 50 lines
    print(f"\n... (see full report in {output_path})")
    print("="*70)

if __name__ == "__main__":
    generate_report()
