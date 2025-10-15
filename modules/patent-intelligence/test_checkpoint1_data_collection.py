#!/usr/bin/env python3
"""
Checkpoint 1: Test Data Collection with PatentsView API
- Collect 10 sample patents
- Validate data quality
- Store in database
- Generate validation report
"""

import sys
from pathlib import Path

# Add parent directory to path
module_dir = Path(__file__).parent
sys.path.insert(0, str(module_dir))

from scrapers.patentsview_client import PatentsViewClient
from core.database import PatentDatabase

def main():
    print("=" * 70)
    print("🔬 CHECKPOINT 1: Data Collection Test")
    print("=" * 70)

    # Initialize
    client = PatentsViewClient()
    db = PatentDatabase()

    print("\n📊 Step 1: Searching for 10 LED lighting patents...")
    print("-" * 70)

    # Search for recent LED lighting patents
    result = client.search_patents(
        keyword="LED lighting control",
        start_date="2024-01-01",
        max_results=10
    )

    patents = result['patents']
    metadata = result['metadata']

    print(f"\n✅ API returned {len(patents)} patents")
    print(f"   Total available: {metadata.get('total', 'unknown')}")
    print(f"   Query: {metadata.get('query')}")
    print(f"   Date range: {metadata.get('start_date')} to present")

    if not patents:
        print("\n❌ No patents found! Check API connection.")
        return

    # Validate data quality BEFORE storing
    print("\n📊 Step 2: Validating data quality...")
    print("-" * 70)

    quality = client.validate_data_quality(patents)
    print(f"\n Data Quality Report:")
    print(f"   Total patents: {quality['total_patents']}")
    print(f"   Has title: {quality['has_title']} ({quality['title_pct']}%)")
    print(f"   Has abstract: {quality['has_abstract']} ({quality['abstract_pct']}%)")
    print(f"   Has assignees: {quality['has_assignees']} ({quality['assignees_pct']}%)")
    print(f"   Has CPC codes: {quality['has_cpc_codes']} ({quality['cpc_codes_pct']}%)")
    print(f"   Has filing date: {quality['has_filing_date']} ({quality['filing_date_pct']}%)")
    print(f"\n   📈 Overall Quality Score: {quality['quality_score']}%")

    if quality['quality_score'] < 70:
        print(f"\n   ⚠️ WARNING: Data quality below 70%")
    else:
        print(f"\n   ✅ Data quality acceptable")

    # Store in database
    print("\n📊 Step 3: Storing patents in database...")
    print("-" * 70)

    stored_count = 0
    duplicate_count = 0

    for patent in patents:
        success = db.insert_patent(patent)
        if success:
            stored_count += 1
            print(f"   ✅ Stored: {patent['id']} - {patent['title'][:50]}...")
        else:
            duplicate_count += 1
            print(f"   ⏭️  Duplicate: {patent['id']}")

    print(f"\n✅ Stored {stored_count} new patents")
    if duplicate_count > 0:
        print(f"   ⏭️  Skipped {duplicate_count} duplicates")

    # Log collection
    db.log_collection(
        search_query="LED lighting control",
        found=len(patents),
        stored=stored_count,
        api_source="patentsview",
        notes="Checkpoint 1 test"
    )

    # Verify data persistence
    print("\n📊 Step 4: Verifying data persistence...")
    print("-" * 70)

    db_stats = db.get_stats()
    print(f"\n Database Statistics:")
    print(f"   Total patents: {db_stats['total_patents']}")
    print(f"   Complete data: {db_stats['complete_data']} ({db_stats['completeness_pct']}%)")
    print(f"   With abstract: {db_stats['with_abstract']}")
    print(f"   With claims: {db_stats['with_claims']}")
    print(f"   With assignees: {db_stats['with_assignees']}")
    print(f"   Data sources: {db_stats['data_sources']}")
    print(f"   Date range: {db_stats['date_range']['earliest']} to {db_stats['date_range']['latest']}")

    # Sample patent details
    print("\n📊 Step 5: Sample patent details...")
    print("-" * 70)

    if patents:
        sample = patents[0]
        print(f"\n Sample Patent: {sample['id']}")
        print(f"   Title: {sample['title']}")
        print(f"   Abstract: {sample['abstract'][:200]}...")
        print(f"   Filing Date: {sample['filing_date']}")
        print(f"   Grant Date: {sample['grant_date']}")
        print(f"   Assignees: {', '.join(sample['assignees'][:3])}")
        print(f"   CPC Codes: {', '.join(sample['cpc_codes'][:5])}")
        print(f"   Citations: {len(sample['backward_citations'])} backward, {len(sample['forward_citations'])} forward")

    # Final checkpoint
    print("\n" + "=" * 70)
    print("🎯 CHECKPOINT 1 COMPLETE")
    print("=" * 70)

    success_criteria = [
        ("API Connection", len(patents) > 0),
        ("Data Quality", quality['quality_score'] >= 70),
        ("Database Storage", stored_count > 0),
        ("Data Persistence", db_stats['total_patents'] >= stored_count)
    ]

    print("\n✅ Success Criteria:")
    all_pass = True
    for criterion, passed in success_criteria:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {status}: {criterion}")
        if not passed:
            all_pass = False

    if all_pass:
        print("\n🎉 All checkpoints passed! Ready for Checkpoint 2 (LLM Analysis)")
    else:
        print("\n⚠️  Some checkpoints failed. Review above for details.")

    # Close database
    db.close()

if __name__ == "__main__":
    main()
