#!/usr/bin/env python3
"""
Checkpoint Validation Script - Brand Perceptions Module
Validates data quality at each checkpoint to catch issues early
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any

class CheckpointValidator:
    def __init__(self, data_path: Path):
        self.data_path = data_path
        self.errors = []
        self.warnings = []

    def validate_record_count(self, records: List[Dict], expected_min: int, source_name: str):
        """Check if we have minimum expected records"""
        actual = len(records)
        if actual < expected_min:
            self.errors.append(
                f"❌ {source_name}: Expected minimum {expected_min} records, got {actual}"
            )
        else:
            print(f"✅ {source_name}: Record count OK ({actual} >= {expected_min})")

    def validate_required_fields(self, records: List[Dict], required_fields: List[str], source_name: str):
        """Check for null/blank critical fields"""
        for i, record in enumerate(records):
            for field in required_fields:
                value = record.get(field)
                if value is None or (isinstance(value, str) and value.strip() == ""):
                    self.errors.append(
                        f"❌ {source_name} record #{i+1}: Missing required field '{field}'"
                    )

        if not any(source_name in err for err in self.errors):
            print(f"✅ {source_name}: All required fields present")

    def validate_temporal_filter(self, records: List[Dict], date_field: str, months_back: int, source_name: str):
        """Check if data is within temporal range (e.g., 24 months)"""
        cutoff_date = datetime.now() - timedelta(days=months_back * 30)
        old_records = []

        for i, record in enumerate(records):
            date_str = record.get(date_field)
            if date_str:
                try:
                    # Try parsing different date formats
                    for fmt in ["%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y/%m/%d", "%m/%d/%Y"]:
                        try:
                            record_date = datetime.strptime(date_str, fmt)
                            if record_date < cutoff_date:
                                old_records.append(i+1)
                            break
                        except ValueError:
                            continue
                except Exception as e:
                    self.warnings.append(
                        f"⚠️  {source_name} record #{i+1}: Could not parse date '{date_str}'"
                    )

        if old_records:
            self.warnings.append(
                f"⚠️  {source_name}: {len(old_records)} records older than {months_back} months (records: {old_records[:5]})"
            )
        else:
            print(f"✅ {source_name}: Temporal filter OK (all within {months_back} months)")

    def validate_brand_mention(self, records: List[Dict], text_field: str, brand_name: str, source_name: str):
        """Check if brand is actually mentioned in text (avoid false positives)"""
        missing_brand = []

        for i, record in enumerate(records):
            text = record.get(text_field, "").lower()
            if brand_name.lower() not in text:
                missing_brand.append(i+1)

        if missing_brand:
            self.errors.append(
                f"❌ {source_name}: {len(missing_brand)} records without brand mention '{brand_name}' (records: {missing_brand[:5]})"
            )
        else:
            print(f"✅ {source_name}: Brand mention validation passed")

    def validate_no_duplicates(self, records: List[Dict], id_field: str, source_name: str):
        """Check for duplicate records"""
        ids = [r.get(id_field) for r in records if r.get(id_field)]
        duplicates = len(ids) - len(set(ids))

        if duplicates > 0:
            self.errors.append(
                f"❌ {source_name}: Found {duplicates} duplicate records (by {id_field})"
            )
        else:
            print(f"✅ {source_name}: No duplicates detected")

    def validate_us_geography(self, records: List[Dict], location_field: str, source_name: str):
        """Check for non-US geography (if location available)"""
        non_us_countries = ["UK", "United Kingdom", "Australia", "Canada", "Germany", "France"]
        non_us_records = []

        for i, record in enumerate(records):
            location = record.get(location_field, "")
            if location and any(country in location for country in non_us_countries):
                non_us_records.append((i+1, location))

        if non_us_records:
            self.warnings.append(
                f"⚠️  {source_name}: {len(non_us_records)} non-US records detected (sample: {non_us_records[:3]})"
            )
        else:
            print(f"✅ {source_name}: Geography filter OK (US-only or no location data)")

    def validate_data_structure(self, records: List[Dict], source_name: str):
        """Check for consistent schema across records"""
        if not records:
            self.errors.append(f"❌ {source_name}: No records to validate")
            return

        # Get keys from first record as baseline
        baseline_keys = set(records[0].keys())

        for i, record in enumerate(records[1:], start=2):
            if set(record.keys()) != baseline_keys:
                self.errors.append(
                    f"❌ {source_name} record #{i}: Schema mismatch (expected {baseline_keys}, got {set(record.keys())})"
                )

        if not any(source_name in err for err in self.errors):
            print(f"✅ {source_name}: Data structure consistent")

    def run_checkpoint(self, checkpoint_config: Dict[str, Any]) -> bool:
        """
        Run validation checkpoint

        checkpoint_config = {
            "reddit": {
                "file": "data/raw/pass1_free/reddit/command_sample.json",
                "expected_min": 10,
                "required_fields": ["text", "date", "author"],
                "text_field": "text",
                "date_field": "date",
                "id_field": "id",
                "location_field": "author_location",
                "brand_name": "Command"
            },
            ...
        }
        """
        print("\n" + "="*60)
        print(f"🔍 CHECKPOINT VALIDATION - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60 + "\n")

        for source_name, config in checkpoint_config.items():
            print(f"\n📋 Validating {source_name.upper()}...")
            print("-" * 40)

            file_path = self.data_path / config["file"]
            if not file_path.exists():
                self.errors.append(f"❌ {source_name}: File not found: {file_path}")
                continue

            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    records = data if isinstance(data, list) else data.get("records", [])
            except Exception as e:
                self.errors.append(f"❌ {source_name}: Failed to load file: {e}")
                continue

            # Run validations
            self.validate_record_count(records, config["expected_min"], source_name)
            self.validate_required_fields(records, config["required_fields"], source_name)
            self.validate_data_structure(records, source_name)

            if config.get("date_field"):
                self.validate_temporal_filter(records, config["date_field"], 24, source_name)

            if config.get("brand_name") and config.get("text_field"):
                self.validate_brand_mention(records, config["text_field"], config["brand_name"], source_name)

            if config.get("id_field"):
                self.validate_no_duplicates(records, config["id_field"], source_name)

            if config.get("location_field"):
                self.validate_us_geography(records, config["location_field"], source_name)

        # Print summary
        print("\n" + "="*60)
        print("📊 VALIDATION SUMMARY")
        print("="*60)

        if self.warnings:
            print(f"\n⚠️  {len(self.warnings)} WARNINGS:")
            for warning in self.warnings:
                print(f"  {warning}")

        if self.errors:
            print(f"\n❌ {len(self.errors)} ERRORS:")
            for error in self.errors:
                print(f"  {error}")
            print("\n🚨 CHECKPOINT FAILED - Fix errors before proceeding\n")
            return False
        else:
            print("\n✅ CHECKPOINT PASSED - All validations successful!\n")
            if self.warnings:
                print("Note: Warnings present but non-blocking\n")
            return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python checkpoint_validator.py <checkpoint_config.json>")
        sys.exit(1)

    config_file = Path(sys.argv[1])
    if not config_file.exists():
        print(f"Error: Config file not found: {config_file}")
        sys.exit(1)

    with open(config_file, 'r') as f:
        checkpoint_config = json.load(f)

    validator = CheckpointValidator(Path.cwd())
    passed = validator.run_checkpoint(checkpoint_config)

    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
