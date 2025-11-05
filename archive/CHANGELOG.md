# Changelog
All notable changes to the 3M Lighting Project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-10-28

### Added
- Complete product dataset with 9,555 unique products
- Lowe's integration with 371 products
- Professional Excel formatting with 5 analysis sheets
- Comprehensive README documentation
- Data validation and quality assurance protocols

### Changed
- Updated 04_CATEGORY_DATA_ALL_PRODUCTS.xlsx with corrected data
- Fixed category field misalignment (was showing retailer names)
- Standardized all data formats across retailers
- Improved price data formatting and validation

### Fixed
- Removed 1,029 duplicate product entries
- Corrected category assignments for all products
- Fixed data type inconsistencies in price fields
- Resolved missing brand name standardization

### Data Summary
- **Total Products:** 9,555
- **Retailers:** 5 (Walmart, Home Depot, Amazon, Target, Lowe's)
- **Categories:** 7 distinct product categories
- **Brands:** 818 unique brands
- **Data Completeness:** 86.7% for price data

### Known Issues
- Walmart bias in dataset (78.5% of products)
- Some missing review data for newer products
- Limited image URL availability

## [0.9.0] - 2024-10-27

### Added
- Initial data collection from 4 retailers
- Basic Excel export functionality
- Raw JSON data storage

### Changed
- Restructured data pipeline for efficiency
- Updated scraping methods for reliability

## [0.1.0] - 2024-10-01

### Added
- Project initialization
- Basic module structure
- Initial requirements documentation

---
*For detailed commit history, see: [GitHub Repository](https://github.com/anderson115/3m-lighting-project)*
