"""
Resource Curator
Curates authoritative learning resources
"""

import logging
from typing import Dict
from datetime import datetime

logger = logging.getLogger(__name__)


class ResourceCurator:
    """Curates learning resources for categories"""

    def __init__(self, config):
        self.config = config

    def find_resources(self, category: str) -> Dict:
        """
        Find learning resources for category

        Args:
            category: Category name

        Returns:
            Dict with curated resources
        """
        logger.info(f"Curating resources for: {category}")

        category_normalized = category.lower().strip()

        resources_data = {
            "garage storage": {
                "buying_guides": [
                    {
                        "title": "Garage Storage Systems Buying Guide",
                        "provider": "Home Depot",
                        "type": "Comprehensive buying guide",
                        "authority": "Major home improvement retailer",
                        "relevance": "high"
                    },
                    {
                        "title": "Garage Organization Guide",
                        "provider": "Lowe's",
                        "type": "Planning and installation guide",
                        "authority": "Major home improvement retailer",
                        "relevance": "high"
                    }
                ],
                "diy_resources": [
                    {
                        "title": "Garage Organization Projects",
                        "provider": "This Old House",
                        "type": "Video tutorials and project guides",
                        "authority": "Established DIY media brand",
                        "relevance": "high"
                    },
                    {
                        "title": "DIY Garage Storage Solutions",
                        "provider": "Family Handyman",
                        "type": "Step-by-step project guides",
                        "authority": "DIY publication",
                        "relevance": "high"
                    }
                ],
                "professional_resources": [
                    {
                        "title": "Professional Organizer Directory",
                        "provider": "NAPO (National Association of Productivity & Organizing Professionals)",
                        "type": "Professional installer directory",
                        "authority": "Industry trade association",
                        "relevance": "medium"
                    }
                ],
                "community_forums": [
                    {
                        "title": "r/HomeImprovement",
                        "provider": "Reddit",
                        "type": "Community discussion and advice",
                        "authority": "Large active community (3M+ members)",
                        "relevance": "high"
                    },
                    {
                        "title": "r/organization",
                        "provider": "Reddit",
                        "type": "Organization tips and inspiration",
                        "authority": "Active community (500K+ members)",
                        "relevance": "medium"
                    }
                ],
                "youtube_channels": [
                    {
                        "title": "The Handyman",
                        "type": "Installation tutorials",
                        "relevance": "high"
                    },
                    {
                        "title": "See Jane Drill",
                        "type": "DIY organization projects",
                        "relevance": "high"
                    }
                ]
            },
            "smart lighting": {
                "buying_guides": [
                    {
                        "title": "Smart Lighting Buying Guide",
                        "provider": "CNET",
                        "type": "Product reviews and comparisons",
                        "authority": "Tech review site",
                        "relevance": "high"
                    }
                ],
                "technical_resources": [
                    {
                        "title": "Smart Home Integration Guides",
                        "provider": "SmartThings Community",
                        "type": "Technical documentation",
                        "authority": "Platform provider",
                        "relevance": "high"
                    }
                ]
            }
        }

        resources = resources_data.get(category_normalized, {
            "buying_guides": [],
            "diy_resources": [],
            "community_forums": []
        })

        all_resources = []
        for resource_type, items in resources.items():
            for item in items:
                item["category"] = resource_type.replace("_", " ").title()
                all_resources.append(item)

        result = {
            "status": "completed",
            "resources": all_resources,
            "resources_by_type": resources,
            "total_resources": len(all_resources),
            "sources": [
                {
                    "type": "curated_directory",
                    "confidence": "high",
                    "note": "Authoritative resources compiled from industry-recognized sources"
                }
            ],
            "collected_at": datetime.now().isoformat()
        }

        logger.info(f"✅ Curated {result['total_resources']} resources")
        return result
