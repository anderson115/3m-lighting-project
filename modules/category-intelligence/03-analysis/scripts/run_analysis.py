"""Entry point for the streamlined Category Intelligence pipeline."""
from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path
import yaml

from src.analysis.summary import compute_summary
from src.analysis.keyword_language import (
    compute_keyword_language_summary,
    write_keyword_language_summary,
)
from src.pipeline.collectors.shopify import ShopifyAPI, ShopifyBrandCollector, ShopifyProductCatalog, ShopifyStoreConfig
from src.pipeline.collectors.target import (
    TargetBrandCollector,
    TargetProductCatalog,
    TargetScraper,
    TargetParser,
    TargetRequestConfig,
)
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


def _load_config(path: str | None) -> dict:
    if not path:
        return {}
    config_path = Path(path)
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    return yaml.safe_load(config_path.read_text()) or {}


def _build_shopify_configs(collection_settings: dict) -> list[ShopifyStoreConfig]:
    storefronts = collection_settings.get("shopify_storefronts", [])
    stores: list[ShopifyStoreConfig] = []
    for store in storefronts:
        try:
            stores.append(
                ShopifyStoreConfig(
                    name=store["name"],
                    base_url=store["base_url"],
                    collection_path=store.get("collection_path"),
                    tag_filter=store.get("tag_filter"),
                    include_only=tuple(store.get("include_only", [])),
                )
            )
        except KeyError as exc:
            raise ValueError(f"Invalid Shopify storefront config: {store}") from exc
    return stores


def _target_request_config(collection_settings: dict) -> TargetRequestConfig:
    return TargetRequestConfig(
        query=collection_settings.get("target_query", "garage hooks"),
        max_pages=int(collection_settings.get("target_max_pages", 4)),
        delay_seconds=float(collection_settings.get("target_delay_seconds", 1.0)),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Category Intelligence pipeline")
    parser.add_argument("--category", required=True, help="Category label (e.g. 'garage organization')")
    parser.add_argument("--output", required=True, help="Output stem for markdown report")
    parser.add_argument("--config", default=None, help="Optional YAML config path")
    parser.add_argument("--data-dir", default=None, help="Filesystem directory for JSON exports")
    parser.add_argument("--postgres-dsn", default=None, help="Optional Postgres DSN for persistence (e.g., postgresql://user:pass@host/db)")
    parser.add_argument("--duckdb-path", default=None, help="Optional DuckDB file path for persistence")
    parser.add_argument("--min-brands", type=int, default=15, help="Minimum number of brands required for a successful run")
    parser.add_argument("--min-products", type=int, default=150, help="Minimum number of products required for a successful run")
    parser.add_argument("--project-key", default=None, help="Project identifier for manifests + storage tables")
    parser.add_argument("--project-client", default=None, help="Client label stored with the project key")
    parser.add_argument("--project-name", default=None, help="Project name stored with the project key")
    parser.add_argument("--project-description", default=None, help="Optional description for the project lookup table")
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

    config = _load_config(args.config)
    collection_settings = config.get("retailers", {}).get("collection_settings", {})
    if not args.project_key:
        args.project_key = config.get("project_key")
    if not args.project_client:
        args.project_client = config.get("client", {}).get("name")
    if not args.project_name:
        args.project_name = config.get("client", {}).get("project")
    if not args.project_description:
        args.project_description = config.get("client", {}).get("description")
    if not args.duckdb_path:
        args.duckdb_path = (
            config.get("outputs", {}).get("duckdb_path")
            or "/Volumes/DATA/storage/duckdb/category_intel.duckdb"
        )
    if not args.data_dir:
        args.data_dir = (
            config.get("outputs", {}).get("data_dir")
            or "/Volumes/DATA/consulting/category-intelligence/garage_organizer_beta/data"
        )

    stores = _build_shopify_configs(collection_settings)
    if not stores and collection_settings.get("use_default_shopify", True):
        stores = _default_shopify_stores()
    api = ShopifyAPI()
    collectors = []
    catalogs = []
    if stores:
        collectors.append(ShopifyBrandCollector(stores, api))
        catalogs.append(ShopifyProductCatalog(stores, api))

    target_config = _target_request_config(collection_settings)
    target_scraper = TargetScraper(target_config)
    target_parser = TargetParser()
    target_filters = collection_settings.get("target_filters", {})
    include_terms = target_filters.get("include_terms", [])
    exclude_terms = target_filters.get("exclude_terms", [])
    collectors.append(
        TargetBrandCollector(
            target_scraper,
            target_parser,
            include_terms=include_terms,
            exclude_terms=exclude_terms,
        )
    )
    catalogs.append(
        TargetProductCatalog(
            target_scraper,
            target_parser,
            include_terms=include_terms,
            exclude_terms=exclude_terms,
        )
    )
    composite_brand = CompositeBrandCollector(collectors)
    composite_catalog = CompositeProductCatalog(catalogs)
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
            duckdb_writer = DuckDBWriter(duckdb_path, project_key=args.project_key)
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
            project_metadata = None
            if args.project_key:
                project_metadata = {
                    "client": args.project_client,
                    "project_name": args.project_name,
                    "description": args.project_description,
                }
            pg_writer = PostgresWriter(
                args.postgres_dsn,
                project_key=args.project_key,
                project_metadata=project_metadata,
            )
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
