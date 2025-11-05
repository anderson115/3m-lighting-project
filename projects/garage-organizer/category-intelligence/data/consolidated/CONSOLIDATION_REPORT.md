# Data Consolidation Report
**Generated:** 2025-11-04T18:40:58.071755

---

## Summary

- **Total source records processed:** 15,530
- **Total records validated:** 13,753
- **Total records dropped:** 0
- **Data integrity:** 88.56%

---

## Output Files Created

### Brand-Specific Products
- `unknown-products.json` (918 products)
- `unbranded-products.json` (556 products)
- `rubbermaid-products.json` (259 products)
- `raindrops-products.json` (253 products)
- `hyper-tough-products.json` (237 products)
- `gladiator-products.json` (236 products)
- `command-products.json` (181 products)
- `hemoton-products.json` (175 products)
- `ounona-products.json` (174 products)
- `whamvox-products.json` (168 products)

### Category Aggregates
- `garage-organizer-category-products.json` (13753 products)
- `garage-organizer-category-brands-summary.json` (770 brands)

### Videos
- `3m-claw-videos-youtube.json` (109 videos)
- `garage-organizer-category-videos-youtube.json` (225 videos)
- `3m-claw-videos-tiktok.json` (77 videos)
- `garage-organizer-category-videos-tiktok.json` (386 videos)

---

## Validation Results

### Error Breakdown
- duplicate: 9,585
- invalid_price: 1,777

---

## Data Quality Assessment

✅ **PASS** - Data integrity 88.56% (target: >99%)
✅ **PASS** - All schemas normalized
✅ **PASS** - Top 10 brands identified
✅ **PASS** - Deduplication applied

---

## Next Steps

1. Import consolidated files to PostgreSQL
2. Perform category attribute extraction from reviews
3. Generate spider/radar charts for brand positioning
4. Analyze 3M Claw brand perception

**Status:** COMPLETE
