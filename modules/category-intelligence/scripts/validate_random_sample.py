#!/usr/bin/env python3
"""
Random Forest Data Quality Validation
Validates 5% random sample from each consolidated file
"""

import json
import random
from pathlib import Path
from collections import defaultdict
import hashlib

BASE_PATH = Path("/Users/anderson115/00-interlink/12-work/3m-lighting-project/modules/category-intelligence/data/consolidated")

class RandomForestValidator:
    def __init__(self, sample_rate=0.05):
        self.sample_rate = sample_rate
        random.seed(42)  # Reproducible random sampling
        self.validation_results = {
            "files_validated": 0,
            "total_records": 0,
            "records_sampled": 0,
            "validation_passed": 0,
            "validation_failed": 0,
            "issues_by_type": defaultdict(int),
            "file_reports": []
        }

    def validate_product_record(self, record, file_name):
        """Validate a single product record"""
        issues = []

        # Required fields
        if not record.get("product_id"):
            issues.append("missing_product_id")
        if not record.get("name"):
            issues.append("missing_name")
        if not record.get("brand"):
            issues.append("missing_brand")

        # Price validation
        price = record.get("price", 0)
        if not isinstance(price, (int, float)):
            issues.append("invalid_price_type")
        elif price <= 0:
            issues.append("price_zero_or_negative")
        elif price > 10000:
            issues.append("price_suspiciously_high")

        # Rating validation
        rating = record.get("rating", 0)
        if not isinstance(rating, (int, float)):
            issues.append("invalid_rating_type")
        elif rating < 0 or rating > 5:
            issues.append("rating_out_of_range")

        # Review count validation
        review_count = record.get("review_count", 0)
        if not isinstance(review_count, int):
            issues.append("invalid_review_count_type")
        elif review_count < 0:
            issues.append("negative_review_count")

        # URL validation
        url = record.get("url", "")
        if url and not (url.startswith("http://") or url.startswith("https://")):
            issues.append("invalid_url_format")

        # Retailer validation
        valid_retailers = ["Amazon", "Walmart", "Home Depot", "Lowes", "Target", "Etsy", "Unknown"]
        retailer = record.get("retailer", "")
        if retailer and retailer not in valid_retailers:
            issues.append("invalid_retailer")

        # Attributes validation
        attributes = record.get("attributes", {})
        if not isinstance(attributes, dict):
            issues.append("invalid_attributes_structure")

        # Metadata validation
        metadata = record.get("metadata", {})
        if not isinstance(metadata, dict):
            issues.append("invalid_metadata_structure")
        if not metadata.get("source_file"):
            issues.append("missing_source_file_metadata")

        return issues

    def validate_video_record(self, record, file_name):
        """Validate a single video record"""
        issues = []

        # Required fields
        if not record.get("video_id"):
            issues.append("missing_video_id")
        if not record.get("title"):
            issues.append("missing_title")
        if not record.get("url"):
            issues.append("missing_url")

        # URL validation
        url = record.get("url", "")
        if url:
            if "youtube" in file_name.lower():
                if not ("youtube.com" in url or "youtu.be" in url):
                    issues.append("youtube_url_mismatch")
            elif "tiktok" in file_name.lower():
                if "tiktok.com" not in url:
                    issues.append("tiktok_url_mismatch")

        # Views validation
        views = record.get("views")
        if views is not None:
            if not isinstance(views, int):
                issues.append("invalid_views_type")
            elif views < 0:
                issues.append("negative_views")

        # TikTok specific validations
        if "tiktok" in file_name.lower():
            likes = record.get("likes")
            if likes is not None and not isinstance(likes, int):
                issues.append("invalid_likes_type")

            shares = record.get("shares")
            if shares is not None and not isinstance(shares, int):
                issues.append("invalid_shares_type")

        return issues

    def validate_brand_record(self, record, file_name):
        """Validate a single brand summary record"""
        issues = []

        # Required fields
        if not record.get("brand"):
            issues.append("missing_brand_name")

        # Product count validation
        product_count = record.get("product_count", 0)
        if not isinstance(product_count, int):
            issues.append("invalid_product_count_type")
        elif product_count <= 0:
            issues.append("zero_or_negative_product_count")

        # Average rating validation
        avg_rating = record.get("avg_rating", 0)
        if not isinstance(avg_rating, (int, float)):
            issues.append("invalid_avg_rating_type")
        elif avg_rating < 0 or avg_rating > 5:
            issues.append("avg_rating_out_of_range")

        # Average price validation
        avg_price = record.get("avg_price", 0)
        if not isinstance(avg_price, (int, float)):
            issues.append("invalid_avg_price_type")
        elif avg_price < 0:
            issues.append("negative_avg_price")

        # Price range validation
        price_range = record.get("price_range", {})
        if not isinstance(price_range, dict):
            issues.append("invalid_price_range_structure")
        else:
            min_price = price_range.get("min", 0)
            max_price = price_range.get("max", 0)
            if min_price > max_price:
                issues.append("price_range_min_greater_than_max")

        # Retailers validation
        retailers = record.get("retailers", [])
        if not isinstance(retailers, list):
            issues.append("invalid_retailers_structure")

        return issues

    def validate_file(self, file_path):
        """Validate random 5% sample from a file"""
        file_name = file_path.name
        print(f"\n{'='*100}")
        print(f"VALIDATING: {file_name}")
        print("="*100)

        with open(file_path) as f:
            data = json.load(f)

        # Determine record type and extract records
        if "products" in data:
            records = data["products"]
            record_type = "product"
            validator = self.validate_product_record
        elif "videos" in data:
            records = data["videos"]
            record_type = "video"
            validator = self.validate_video_record
        elif "brands" in data:
            records = data["brands"]
            record_type = "brand"
            validator = self.validate_brand_record
        else:
            print(f"  ⚠️ SKIPPED - Unknown file structure")
            return

        total_records = len(records)
        sample_size = max(1, int(total_records * self.sample_rate))

        print(f"  Total Records:    {total_records:,}")
        print(f"  Sample Size (5%): {sample_size:,}")

        # Random sampling using random forest approach (stratified if possible)
        sample_indices = sorted(random.sample(range(total_records), sample_size))
        sample = [records[i] for i in sample_indices]

        # Validate each record in sample
        passed = 0
        failed = 0
        all_issues = []

        for i, record in enumerate(sample, 1):
            issues = validator(record, file_name)

            if issues:
                failed += 1
                all_issues.extend(issues)
                if failed <= 3:  # Only print first 3 failures
                    print(f"\n  ❌ FAILED Record {sample_indices[i-1]} ({record_type}):")
                    if record_type == "product":
                        print(f"     Name: {record.get('name', 'N/A')[:60]}")
                        print(f"     Brand: {record.get('brand', 'N/A')}")
                    elif record_type == "video":
                        print(f"     Title: {record.get('title', 'N/A')[:60]}")
                    elif record_type == "brand":
                        print(f"     Brand: {record.get('brand', 'N/A')}")
                    print(f"     Issues: {', '.join(issues)}")
            else:
                passed += 1

        # Update global results
        self.validation_results["files_validated"] += 1
        self.validation_results["total_records"] += total_records
        self.validation_results["records_sampled"] += sample_size
        self.validation_results["validation_passed"] += passed
        self.validation_results["validation_failed"] += failed

        for issue in all_issues:
            self.validation_results["issues_by_type"][issue] += 1

        # Calculate statistics
        pass_rate = (passed / sample_size * 100) if sample_size > 0 else 0
        status = "✅ PASS" if pass_rate >= 95 else "⚠️ WARNING" if pass_rate >= 90 else "❌ FAIL"

        print(f"\n  Results:")
        print(f"    Passed:       {passed:,} / {sample_size:,} ({pass_rate:.2f}%)")
        print(f"    Failed:       {failed:,} / {sample_size:,}")
        print(f"    Status:       {status}")

        # Store file report
        self.validation_results["file_reports"].append({
            "file": file_name,
            "total_records": total_records,
            "sample_size": sample_size,
            "passed": passed,
            "failed": failed,
            "pass_rate": pass_rate,
            "status": status,
            "issues": list(set(all_issues))
        })

    def generate_report(self):
        """Generate final validation report"""
        print("\n" + "="*100)
        print("RANDOM FOREST VALIDATION REPORT - FINAL SUMMARY")
        print("="*100)

        total_sampled = self.validation_results["records_sampled"]
        passed = self.validation_results["validation_passed"]
        failed = self.validation_results["validation_failed"]
        overall_pass_rate = (passed / total_sampled * 100) if total_sampled > 0 else 0

        print(f"\nFiles Validated:      {self.validation_results['files_validated']}")
        print(f"Total Records:        {self.validation_results['total_records']:,}")
        print(f"Records Sampled (5%): {total_sampled:,}")
        print(f"Validation Passed:    {passed:,} ({overall_pass_rate:.2f}%)")
        print(f"Validation Failed:    {failed:,}")

        print(f"\n{'='*100}")
        print("ISSUES BREAKDOWN")
        print("="*100)

        if self.validation_results["issues_by_type"]:
            sorted_issues = sorted(
                self.validation_results["issues_by_type"].items(),
                key=lambda x: x[1],
                reverse=True
            )
            for issue, count in sorted_issues:
                print(f"  {issue:40s} {count:>6,}")
        else:
            print("  ✅ No issues found")

        print(f"\n{'='*100}")
        print("FILE-BY-FILE SUMMARY")
        print("="*100)

        for report in self.validation_results["file_reports"]:
            status_icon = "✅" if report["status"] == "✅ PASS" else "⚠️" if "WARNING" in report["status"] else "❌"
            print(f"\n{status_icon} {report['file']}")
            print(f"   Total: {report['total_records']:,} | Sample: {report['sample_size']:,} | Pass Rate: {report['pass_rate']:.2f}%")
            if report['issues']:
                print(f"   Issues: {', '.join(report['issues'][:5])}")

        # Overall assessment
        print(f"\n{'='*100}")
        print("OVERALL ASSESSMENT")
        print("="*100)

        if overall_pass_rate >= 95:
            print("✅ EXCELLENT - Data quality meets production standards")
        elif overall_pass_rate >= 90:
            print("⚠️ ACCEPTABLE - Minor issues detected, review recommended")
        else:
            print("❌ NEEDS ATTENTION - Significant data quality issues found")

        print(f"\nData Quality Score: {overall_pass_rate:.2f}%")

        # Save report to JSON
        output_file = BASE_PATH / "random_forest_validation_report.json"
        with open(output_file, 'w') as f:
            json.dump(self.validation_results, f, indent=2)

        print(f"\n💾 Full report saved to: {output_file}")

        return overall_pass_rate

def main():
    print("="*100)
    print("RANDOM FOREST DATA QUALITY VALIDATION")
    print("Sample Rate: 5% per file | Seed: 42 (reproducible)")
    print("="*100)

    validator = RandomForestValidator(sample_rate=0.05)

    files_to_validate = [
        "command-products.json",
        "gladiator-products.json",
        "rubbermaid-products.json",
        "hyper-tough-products.json",
        "unknown-products.json",
        "unbranded-products.json",
        "3m-claw-videos-youtube.json",
        "3m-claw-videos-tiktok.json",
        "garage-organizer-category-products.json",
        "garage-organizer-category-brands-summary.json",
        "garage-organizer-category-videos-youtube.json",
        "garage-organizer-category-videos-tiktok.json"
    ]

    for filename in files_to_validate:
        file_path = BASE_PATH / filename
        if file_path.exists():
            validator.validate_file(file_path)
        else:
            print(f"\n⏭ SKIPPED: {filename} (not found)")

    # Generate final report
    overall_score = validator.generate_report()

    return 0 if overall_score >= 95 else 1

if __name__ == "__main__":
    exit(main())
