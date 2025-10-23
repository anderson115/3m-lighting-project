"""Entry point for the streamlined Category Intelligence pipeline."""
import argparse
from pathlib import Path
from src.pipeline.orchestrator import CategoryIntelligencePipeline
from src.pipeline.brand_collector import BrandCollector
from src.pipeline.product_catalog import ProductCatalogBuilder
from src.reporting.markdown_report import MarkdownReporter

class NotImplementedCollector(BrandCollector, ProductCatalogBuilder):
    def collect(self, category: str):
        raise NotImplementedError("Collector implementation pending. Please provide live data sources before running the pipeline.")

def main() -> None:
    parser = argparse.ArgumentParser(description="Run Category Intelligence pipeline")
    parser.add_argument("--category", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    collector = NotImplementedCollector()
    pipeline = CategoryIntelligencePipeline(collector, collector)
    try:
        results = pipeline.run(args.category)
    except RuntimeError as err:
        raise SystemExit(str(err))
    except NotImplementedError as err:
        raise SystemExit(f"Pipeline not yet configured: {err}")

    reporter = MarkdownReporter()
    output_dir = Path('outputs')
    output_dir.mkdir(exist_ok=True)
    reporter.render(args.category, results["brands"], results["products"], output_dir / f"{args.output}.md")

if __name__ == "__main__":
    main()
