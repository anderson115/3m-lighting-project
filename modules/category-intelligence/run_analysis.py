"""Entry point for the streamlined Category Intelligence pipeline."""
from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

from src.analysis.summary import compute_summary
from src.analysis.keyword_language import (
    compute_keyword_language_summary,
    write_keyword_language_summary,
)
from src.pipeline.collectors.shopify import ShopifyAPI, ShopifyBrandCollector, ShopifyProductCatalog, ShopifyStoreConfig
from src.pipeline.collectors.target import TargetBrandCollector, TargetProductCatalog, TargetScraper, TargetParser
from src.pipeline.collectors import CompositeBrandCollector, CompositeProductCatalog
from src.pipeline.orchestrator import CategoryIntelligencePipeline
from src.reporting.markdown_report import MarkdownReporter
from src.storage.filesystem import FilesystemWriter
from src.storage.postgres import PostgresWriter
from src.storage.duckdb_writer import DuckDBWriter

_LOGGER = logging.getLogger("category_intelligence")
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


def _default_shopify_stores() -> list[ShopifyStoreConfig]:
    return [
        ShopifyStoreConfig(name="Total Garage", base_url="https://totalgarage.myshopify.com"),
        ShopifyStoreConfig(name="Hello Garage Shop", base_url="https://hellogarageshop.myshopify.com"),
        ShopifyStoreConfig(name="HomeSmart", base_url="https://homesmart.myshopify.com", collection_path="/collections/hooks-hardware"),
        ShopifyStoreConfig(name="Garage Variety", base_url="https://xr1m6f-te.myshopify.com", collection_path="/collections/hooks"),
        ShopifyStoreConfig(name="Moonlight Industries", base_url="https://moonlight-inds.myshopify.com"),
        ShopifyStoreConfig(name="Garage Essentials", base_url="https://0cj1ie-gg.myshopify.com"),
        ShopifyStoreConfig(name="Compact Storage", base_url="https://0jftst-ey.myshopify.com"),
        ShopifyStoreConfig(name="Minimal Hooks", base_url="https://sg6wp1-zk.myshopify.com"),
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Category Intelligence pipeline")
    parser.add_argument("--category", required=True, help="Category label (e.g. 'garage organization')")
    parser.add_argument("--output", required=True, help="Output stem for markdown report")
    parser.add_argument("--data-dir", default="/Volumes/DATA/consulting/category-intelligence/garage_organizer_beta/data", help="Filesystem directory for JSON exports")
    parser.add_argument("--postgres-dsn", default=None, help="Optional Postgres DSN for persistence (e.g., postgresql://user:pass@host/db)")
    parser.add_argument("--duckdb-path", default="/Volumes/DATA/storage/duckdb/category_intel.duckdb", help="Optional DuckDB file path for persistence")
    parser.add_argument("--min-brands", type=int, default=15, help="Minimum number of brands required for a successful run")
    parser.add_argument("--min-products", type=int, default=150, help="Minimum number of products required for a successful run")
    parser.add_argument(
        "--ad-snapshots",
        nargs="*",
        default=[],
        help="Optional Bright Data ad snapshot JSON files for keyword analysis",
    )
    parser.add_argument(
        "--community-snapshots",
        nargs="*",
        default=[],
        help="Optional community language JSON files (e.g., Reddit) for keyword analysis",
    )
    args = parser.parse_args()

    stores = _default_shopify_stores()
    api = ShopifyAPI()
    brand_collector = ShopifyBrandCollector(stores, api)
    product_catalog = ShopifyProductCatalog(stores, api)
    target_brand = TargetBrandCollector(TargetScraper(), TargetParser())
    target_catalog = TargetProductCatalog(TargetScraper(), TargetParser())
    composite_brand = CompositeBrandCollector([brand_collector, target_brand])
    composite_catalog = CompositeProductCatalog([product_catalog, target_catalog])
    pipeline = CategoryIntelligencePipeline(composite_brand, composite_catalog, min_brands=args.min_brands)

    _LOGGER.info("Collecting live data for category '%s' across %d Shopify stores + Target", args.category, len(stores))
    results = pipeline.run(args.category)
    brands = list(results["brands"])
    products = list(results["products"])

    if len(brands) < args.min_brands:
        raise RuntimeError(f"Insufficient brands: {len(brands)} < {args.min_brands}")
    if len(products) < args.min_products:
        raise RuntimeError(f"Insufficient products: {len(products)} < {args.min_products}")

    # Persist structured data
    data_dir = Path(args.data_dir)
    writer = FilesystemWriter(data_dir)
    writer.write_brands(args.category, brands)
    writer.write_products(args.category, products)

    duckdb_writer = None
    if args.duckdb_path:
        duckdb_path = Path(args.duckdb_path)
        try:
            duckdb_writer = DuckDBWriter(duckdb_path)
            duckdb_writer.write_brands(args.category, brands)
            duckdb_writer.write_products(args.category, products)
            duckdb_writer.close()
            _LOGGER.info("Persisted records to DuckDB at %s", duckdb_path)
        except Exception as exc:  # pragma: no cover
            _LOGGER.error("Failed to persist to DuckDB: %s", exc)

    summary = compute_summary(brands, products)
    summary_path = data_dir / f"{args.category.replace(' ', '_')}_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    _LOGGER.info("Retailer coverage: %s", summary.get("retailer_counts"))
    _LOGGER.info("Segment mix: %s", summary.get("segment_counts"))
    load_info = summary.get("load_capacity", {})
    _LOGGER.info("Products with load capacity: %s (max %s lbs)", load_info.get("with_capacity"), load_info.get("max_capacity"))

    if args.postgres_dsn:
        try:
            pg_writer = PostgresWriter(args.postgres_dsn)
            pg_writer.write_brands(args.category, brands)
            pg_writer.write_products(args.category, products)
            _LOGGER.info("Persisted records to Postgres")
        except RuntimeError as err:
            _LOGGER.error("Postgres writer unavailable: %s", err)
        except Exception as exc:  # pragma: no cover - unexpected DB error
            _LOGGER.error("Failed to persist to Postgres: %s", exc)

    # Render markdown summary
    outputs_dir = Path('outputs')
    outputs_dir.mkdir(exist_ok=True)
    reporter = MarkdownReporter()
    reporter.render(args.category, brands, products, outputs_dir / f"{args.output}.md", summary=summary)

    _LOGGER.info("Collected %d brands and %d products", len(brands), len(products))
    _LOGGER.info("Markdown report written to %s", outputs_dir / f"{args.output}.md")

    if args.ad_snapshots and args.community_snapshots:
        ad_paths = [Path(p) for p in args.ad_snapshots]
        community_paths = [Path(p) for p in args.community_snapshots]
        keyword_summary = compute_keyword_language_summary(ad_paths, community_paths)
        keyword_output = outputs_dir / f"{args.output}_keyword_language.json"
        keyword_payload = write_keyword_language_summary(keyword_summary, keyword_output)
        keyword_store_path = writer.write_keyword_summary(
            args.category,
            keyword_payload,
        )
        _LOGGER.info(
            "Keyword & language summary written to %s and %s",
            keyword_output,
            keyword_store_path,
        )


if __name__ == "__main__":
    main()
