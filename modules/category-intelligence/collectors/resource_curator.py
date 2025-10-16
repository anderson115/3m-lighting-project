"""
Resource Curator
Curates authoritative learning resources with URLs for appendix format
"""

import logging
from typing import Dict
from datetime import datetime

logger = logging.getLogger(__name__)


class ResourceCurator:
    """Curates learning resources for categories in appendix format"""

    def __init__(self, config):
        self.config = config

    def find_resources(self, category: str) -> Dict:
        """
        Find learning resources for category with URLs

        Args:
            category: Category name

        Returns:
            Dict with curated resources including URLs for appendix format
        """
        logger.info(f"Curating resources for: {category}")

        category_normalized = category.lower().strip()

        resources_data = {
            "garage storage": self._get_garage_storage_resources(),
            "smart lighting": self._get_smart_lighting_resources()
        }

        resources = resources_data.get(category_normalized, {
            "resource_categories": []
        })

        # Flatten all resources for total count
        total_resources = sum(len(cat["resources"]) for cat in resources.get("resource_categories", []))

        result = {
            "status": "completed",
            "resource_categories": resources.get("resource_categories", []),
            "total_resources": total_resources,
            "methodology": {
                "curation_criteria": [
                    "Authority: Industry-recognized sources, major retailers, established publications",
                    "Relevance: Directly applicable to category research and consumer decision-making",
                    "Recency: Prefer resources updated within past 2 years",
                    "Accessibility: Publicly available, no paywall where possible",
                    "Actionability: Practical information consumers and industry professionals can use"
                ],
                "resource_types_included": "Industry reports, buying guides, retailer resources, trade publications, community forums, video content, manufacturer resources, professional organizations"
            },
            "sources": [
                {
                    "type": "curated_directory",
                    "confidence": "high",
                    "note": "Authoritative resources compiled from industry-recognized sources with direct URLs"
                }
            ],
            "collected_at": datetime.now().isoformat()
        }

        logger.info(f"✅ Curated {result['total_resources']} resources")
        return result

    def _get_garage_storage_resources(self) -> Dict:
        """Comprehensive garage storage resources with URLs"""

        return {
            "resource_categories": [
                {
                    "category": "Industry Reports & Market Research",
                    "description": "Professional market research and industry analysis",
                    "resources": [
                        {
                            "title": "IBISWorld - Garage Storage Manufacturing Industry Report",
                            "provider": "IBISWorld",
                            "url": "https://www.ibisworld.com/united-states/market-research-reports/storage-cabinet-manufacturing-industry/",
                            "access": "Subscription required ($1,000+)",
                            "description": "Comprehensive industry revenue, market share, trends, and forecasts. NAICS 337110 and 337122 segments.",
                            "relevance": "high",
                            "last_updated": "2024"
                        },
                        {
                            "title": "Grand View Research - Home Organization Market Report",
                            "provider": "Grand View Research",
                            "url": "https://www.grandviewresearch.com/industry-analysis/home-organization-market",
                            "access": "Paid report ($4,950)",
                            "description": "Market sizing, growth projections, competitive landscape, regional analysis",
                            "relevance": "high",
                            "last_updated": "2025"
                        },
                        {
                            "title": "Statista - Home Improvement Market Data",
                            "provider": "Statista",
                            "url": "https://www.statista.com/outlook/cmo/furniture-homeware/home-improvement/united-states",
                            "access": "Free overview, detailed data requires subscription",
                            "description": "Market size, consumer spending trends, e-commerce penetration",
                            "relevance": "medium",
                            "last_updated": "2024"
                        },
                        {
                            "title": "NPD Group - Home Improvement Tracking",
                            "provider": "NPD Group / Circana",
                            "url": "https://www.circana.com/solutions/home/",
                            "access": "Industry subscription required",
                            "description": "Consumer purchase panel data, unit sales tracking, market share estimates",
                            "relevance": "high",
                            "last_updated": "Ongoing"
                        }
                    ]
                },
                {
                    "category": "Retailer Buying Guides & Resources",
                    "description": "Major retailer guides for consumer education",
                    "resources": [
                        {
                            "title": "Home Depot - Garage Storage Buying Guide",
                            "provider": "Home Depot",
                            "url": "https://www.homedepot.com/c/ab/garage-storage-ideas/9ba683603be9fa5395fab901ca8472b1",
                            "access": "Free",
                            "description": "Product categories, installation tips, project ideas, product comparisons",
                            "relevance": "high",
                            "last_updated": "2024"
                        },
                        {
                            "title": "Lowe's - Garage Organization Ideas & Buying Guide",
                            "provider": "Lowe's",
                            "url": "https://www.lowes.com/n/buying-guide/garage-organization-and-storage-buying-guide",
                            "access": "Free",
                            "description": "Storage solutions comparison, planning tools, installation guides",
                            "relevance": "high",
                            "last_updated": "2024"
                        },
                        {
                            "title": "Amazon - Garage Organization Best Sellers",
                            "provider": "Amazon",
                            "url": "https://www.amazon.com/Best-Sellers-Home-Kitchen-Garage-Storage-Organization/zgbs/home-garden/3744131",
                            "access": "Free",
                            "description": "Top-selling products, customer reviews, price trends",
                            "relevance": "high",
                            "last_updated": "Real-time"
                        },
                        {
                            "title": "Costco - Garage & Storage Solutions",
                            "provider": "Costco",
                            "url": "https://www.costco.com/garage-storage.html",
                            "access": "Membership required",
                            "description": "Premium product selection, member reviews, seasonal offerings",
                            "relevance": "medium",
                            "last_updated": "Rotating inventory"
                        }
                    ]
                },
                {
                    "category": "DIY & How-To Resources",
                    "description": "Installation guides and project tutorials",
                    "resources": [
                        {
                            "title": "This Old House - Garage Organization Projects",
                            "provider": "This Old House",
                            "url": "https://www.thisoldhouse.com/garages/reviews/best-garage-storage-systems",
                            "access": "Free",
                            "description": "Expert reviews, video tutorials, step-by-step installation guides",
                            "relevance": "high",
                            "last_updated": "2024"
                        },
                        {
                            "title": "Family Handyman - DIY Garage Storage Solutions",
                            "provider": "Family Handyman",
                            "url": "https://www.familyhandyman.com/list/garage-storage-projects/",
                            "access": "Free",
                            "description": "DIY project ideas, building plans, tool recommendations",
                            "relevance": "high",
                            "last_updated": "2024"
                        },
                        {
                            "title": "The Spruce - Garage Organization Ideas",
                            "provider": "The Spruce",
                            "url": "https://www.thespruce.com/garage-organization-ideas-8357260",
                            "access": "Free",
                            "description": "Design inspiration, product recommendations, organization systems",
                            "relevance": "medium-high",
                            "last_updated": "2024"
                        },
                        {
                            "title": "Bob Vila - Garage Storage Ideas & Solutions",
                            "provider": "Bob Vila",
                            "url": "https://www.bobvila.com/articles/garage-storage-ideas/",
                            "access": "Free",
                            "description": "Product reviews, installation advice, before/after projects",
                            "relevance": "medium-high",
                            "last_updated": "2024"
                        }
                    ]
                },
                {
                    "category": "Trade Publications & Industry News",
                    "description": "Industry news and professional insights",
                    "resources": [
                        {
                            "title": "Hardware Retailing - Garage Storage Category Coverage",
                            "provider": "North American Hardware and Paint Association",
                            "url": "https://www.hardwareretailing.com/",
                            "access": "Free online, print subscription available",
                            "description": "Retailer perspectives, category trends, product launches, sales data",
                            "relevance": "high",
                            "last_updated": "Monthly publication"
                        },
                        {
                            "title": "Home Channel News - Storage & Organization Coverage",
                            "provider": "Home Channel News",
                            "url": "https://homechannelnews.com/",
                            "access": "Free online",
                            "description": "Retail news, market trends, executive interviews, category analysis",
                            "relevance": "high",
                            "last_updated": "Daily updates"
                        },
                        {
                            "title": "Remodeling Magazine - Cost vs. Value Report",
                            "provider": "Hanley Wood",
                            "url": "https://www.remodeling.hw.net/cost-vs-value/",
                            "access": "Free",
                            "description": "Home improvement project costs, ROI analysis (includes garage projects)",
                            "relevance": "medium",
                            "last_updated": "Annual"
                        }
                    ]
                },
                {
                    "category": "Community Forums & User-Generated Content",
                    "description": "Real-world consumer experiences and advice",
                    "resources": [
                        {
                            "title": "Reddit - r/HomeImprovement",
                            "provider": "Reddit",
                            "url": "https://www.reddit.com/r/HomeImprovement/",
                            "access": "Free",
                            "description": "Active community discussions, project photos, product recommendations, troubleshooting (3M+ members)",
                            "relevance": "high",
                            "last_updated": "Real-time"
                        },
                        {
                            "title": "Reddit - r/organization",
                            "provider": "Reddit",
                            "url": "https://www.reddit.com/r/organization/",
                            "access": "Free",
                            "description": "Organization tips, before/after photos, product reviews (500K+ members)",
                            "relevance": "medium",
                            "last_updated": "Real-time"
                        },
                        {
                            "title": "Reddit - r/GarageStorage",
                            "provider": "Reddit",
                            "url": "https://www.reddit.com/r/GarageStorage/",
                            "access": "Free",
                            "description": "Dedicated garage storage community, project showcases, advice",
                            "relevance": "high",
                            "last_updated": "Real-time"
                        },
                        {
                            "title": "GarageJournal Forums",
                            "provider": "GarageJournal Community",
                            "url": "https://www.garagejournal.com/forum/",
                            "access": "Free",
                            "description": "Enthusiast community, detailed build threads, product discussions",
                            "relevance": "high",
                            "last_updated": "Real-time"
                        },
                        {
                            "title": "Houzz - Garage & Shed Ideas",
                            "provider": "Houzz",
                            "url": "https://www.houzz.com/photos/garage-and-shed-phbr0-bp~t_713",
                            "access": "Free",
                            "description": "Professional garage photos, designer ideas, product sourcing",
                            "relevance": "medium",
                            "last_updated": "Real-time"
                        }
                    ]
                },
                {
                    "category": "Video Content & Tutorials",
                    "description": "Visual installation guides and product reviews",
                    "resources": [
                        {
                            "title": "YouTube - The Handyman Channel",
                            "provider": "Independent creators",
                            "url": "https://www.youtube.com/results?search_query=garage+storage+installation",
                            "access": "Free",
                            "description": "Installation tutorials, product reviews, comparison videos",
                            "relevance": "high",
                            "last_updated": "Continuously updated"
                        },
                        {
                            "title": "YouTube - See Jane Drill",
                            "provider": "See Jane Drill",
                            "url": "https://www.youtube.com/user/seejanedrill",
                            "access": "Free",
                            "description": "DIY garage organization projects, tool tutorials, beginner-friendly",
                            "relevance": "high",
                            "last_updated": "Active channel"
                        },
                        {
                            "title": "YouTube - Home Depot How-To",
                            "provider": "Home Depot",
                            "url": "https://www.youtube.com/user/homedepot",
                            "access": "Free",
                            "description": "Official retailer tutorials, product demonstrations, project ideas",
                            "relevance": "high",
                            "last_updated": "Active channel"
                        },
                        {
                            "title": "YouTube - Garage Organization Reviews & Comparisons",
                            "provider": "Multiple tech/home reviewers",
                            "url": "https://www.youtube.com/results?search_query=garage+storage+system+review",
                            "access": "Free",
                            "description": "Independent product testing, long-term reviews, comparison videos",
                            "relevance": "medium-high",
                            "last_updated": "Continuously updated"
                        }
                    ]
                },
                {
                    "category": "Manufacturer Resources",
                    "description": "Brand websites with product specs and installation guides",
                    "resources": [
                        {
                            "title": "Rubbermaid FastTrack System Guide",
                            "provider": "Rubbermaid",
                            "url": "https://www.rubbermaid.com/garage-storage-organization/garage-wall-organization/fasttrack-garage-organization-system.html",
                            "access": "Free",
                            "description": "Product catalog, installation guides, design tools, warranty information",
                            "relevance": "medium",
                            "last_updated": "2024"
                        },
                        {
                            "title": "Gladiator GarageWorks",
                            "provider": "Gladiator / Whirlpool",
                            "url": "https://www.gladiatorgarageworks.com/",
                            "access": "Free",
                            "description": "Premium product line, design inspiration, dealer locator",
                            "relevance": "medium",
                            "last_updated": "2024"
                        },
                        {
                            "title": "NewAge Products - Garage Solutions",
                            "provider": "NewAge Products",
                            "url": "https://www.newage.com/garage/",
                            "access": "Free",
                            "description": "Cabinet systems, modular solutions, design gallery, dealer network",
                            "relevance": "medium",
                            "last_updated": "2024"
                        },
                        {
                            "title": "FLEXIMOUNTS - Overhead Storage Guides",
                            "provider": "FLEXIMOUNTS",
                            "url": "https://www.fleximounts.com/",
                            "access": "Free",
                            "description": "Ceiling rack specifications, installation videos, weight capacity guides",
                            "relevance": "medium",
                            "last_updated": "2024"
                        }
                    ]
                },
                {
                    "category": "Professional Organizations & Associations",
                    "description": "Industry groups and professional resources",
                    "resources": [
                        {
                            "title": "NAPO - National Association of Productivity & Organizing Professionals",
                            "provider": "NAPO",
                            "url": "https://www.napo.net/",
                            "access": "Free directory, membership for professionals",
                            "description": "Professional organizer directory, industry standards, consumer resources",
                            "relevance": "medium",
                            "last_updated": "Ongoing"
                        },
                        {
                            "title": "NKBA - National Kitchen & Bath Association",
                            "provider": "NKBA",
                            "url": "https://nkba.org/",
                            "access": "Free resources, membership for professionals",
                            "description": "Design trends, industry research (includes garage/utility spaces)",
                            "relevance": "low-medium",
                            "last_updated": "Ongoing"
                        },
                        {
                            "title": "NAHB - National Association of Home Builders",
                            "provider": "NAHB",
                            "url": "https://www.nahb.org/",
                            "access": "Free resources, membership for builders",
                            "description": "Construction trends, homebuyer preferences, building standards",
                            "relevance": "low-medium",
                            "last_updated": "Ongoing"
                        }
                    ]
                },
                {
                    "category": "Consumer Reports & Product Testing",
                    "description": "Independent product testing and ratings",
                    "resources": [
                        {
                            "title": "Consumer Reports - Storage Organization Reviews",
                            "provider": "Consumer Reports",
                            "url": "https://www.consumerreports.org/",
                            "access": "Subscription required ($39/year)",
                            "description": "Independent product testing, ratings, buying advice (limited garage storage coverage)",
                            "relevance": "low-medium",
                            "last_updated": "Ongoing"
                        },
                        {
                            "title": "Wirecutter - Garage & Storage Reviews",
                            "provider": "New York Times / Wirecutter",
                            "url": "https://www.nytimes.com/wirecutter/",
                            "access": "Free (NYT subscription for some content)",
                            "description": "Tested recommendations, long-term follow-ups, best-of lists",
                            "relevance": "medium",
                            "last_updated": "Ongoing"
                        }
                    ]
                },
                {
                    "category": "Government & Economic Data",
                    "description": "Official statistics and trade data",
                    "resources": [
                        {
                            "title": "US Census Bureau - Economic Census",
                            "provider": "US Census Bureau",
                            "url": "https://www.census.gov/programs-surveys/economic-census.html",
                            "access": "Free",
                            "description": "Manufacturing revenue, employment, industry statistics (NAICS 337110, 337122)",
                            "relevance": "medium",
                            "last_updated": "Every 5 years (2022 data)"
                        },
                        {
                            "title": "Bureau of Economic Analysis - Consumer Spending",
                            "provider": "BEA",
                            "url": "https://www.bea.gov/",
                            "access": "Free",
                            "description": "PCE data, consumer spending trends, economic indicators",
                            "relevance": "low-medium",
                            "last_updated": "Monthly updates"
                        },
                        {
                            "title": "US International Trade Commission - Import Data",
                            "provider": "USITC",
                            "url": "https://dataweb.usitc.gov/",
                            "access": "Free",
                            "description": "Import/export data, trade trends, country of origin analysis",
                            "relevance": "low-medium",
                            "last_updated": "Monthly updates"
                        }
                    ]
                }
            ]
        }

    def _get_smart_lighting_resources(self) -> Dict:
        """Smart lighting resources (simplified)"""

        return {
            "resource_categories": [
                {
                    "category": "Product Reviews & Buying Guides",
                    "description": "Tech-focused reviews and comparisons",
                    "resources": [
                        {
                            "title": "CNET - Smart Lighting Buying Guide",
                            "provider": "CNET",
                            "url": "https://www.cnet.com/home/smart-home/best-smart-light-bulbs/",
                            "access": "Free",
                            "description": "Product testing, ecosystem comparisons, buying advice",
                            "relevance": "high",
                            "last_updated": "2024"
                        },
                        {
                            "title": "The Verge - Smart Home Lighting Reviews",
                            "provider": "The Verge",
                            "url": "https://www.theverge.com/smart-home",
                            "access": "Free",
                            "description": "Tech reviews, new product launches, smart home integration",
                            "relevance": "high",
                            "last_updated": "2024"
                        }
                    ]
                },
                {
                    "category": "Technical Documentation",
                    "description": "Setup guides and platform integration",
                    "resources": [
                        {
                            "title": "SmartThings Community",
                            "provider": "Samsung SmartThings",
                            "url": "https://community.smartthings.com/",
                            "access": "Free",
                            "description": "Platform documentation, integration guides, community support",
                            "relevance": "high",
                            "last_updated": "Ongoing"
                        }
                    ]
                }
            ]
        }
