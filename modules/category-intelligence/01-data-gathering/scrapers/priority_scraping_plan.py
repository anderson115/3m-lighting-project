#!/usr/bin/env python3
"""
Priority Scraping Plan - Category Intelligence
Based on competitive white space analysis requirements
"""

SCRAPING_PRIORITIES = {
    "priority_1": {
        "name": "Representative Category Review Sample",
        "goal": "Get reviews across all price points, installation types, capacity levels",
        "strategy": {
            "selection_criteria": {
                "price_tiers": [
                    {"range": "$5-20", "products": 30, "reviews_per": 15},  # Mass market (Rubbermaid, generic)
                    {"range": "$20-50", "products": 40, "reviews_per": 20},  # Mid-tier (Command, basic hooks)
                    {"range": "$50-120", "products": 40, "reviews_per": 25},  # Premium (Gladiator, quality systems)
                    {"range": "$120+", "products": 20, "reviews_per": 30},   # Professional (StoreWall, systems)
                ],
                "installation_types": {
                    "damage_free_adhesive": 25,  # Command-style
                    "basic_drilling": 30,         # Generic hooks
                    "complex_systems": 25,        # Gladiator/StoreWall
                    "hybrid": 20                  # Mixed approaches
                },
                "capacity_levels": {
                    "light_duty": 20,      # <20 lbs
                    "medium_duty": 40,     # 20-50 lbs
                    "heavy_duty": 30,      # 50-100 lbs
                    "professional": 10     # 100+ lbs
                }
            },
            "target_brands": [
                "Gladiator",      # Premium/Complex (top-right)
                "StoreWall",      # Premium/Complex
                "Command",        # Basic/Easy (bottom-left)
                "Rubbermaid",     # Basic/Easy
                "Generic/No-name", # Basic/Complex (bottom-right)
                "Husky",          # Mid-tier
                "RYOBI",          # Mid-tier
                "OOK",            # Basic hooks
                "Everbilt"        # Basic/commodity
            ],
            "retailers": ["Amazon", "Home Depot", "Lowes"],  # Favor full ratings/reviews
            "total_products": 130,
            "total_reviews_target": 2600,
            "estimated_time": "30 minutes",
            "estimated_cost": "$8"
        }
    },

    "priority_2": {
        "name": "3M Claw Deep Brand Perception",
        "goal": "High confidence brand positioning for smaller/newer brand",
        "strategy": {
            "product_reviews": {
                "amazon_products": 15,      # All 3M Claw products on Amazon
                "reviews_per_product": 50,  # Deep dive
                "homedepot_products": 10,
                "target_total_reviews": 750
            },
            "social_videos": {
                "youtube": {
                    "queries": [
                        "3M Claw hooks review",
                        "3M Claw installation",
                        "3M Claw test",
                        "3M Claw vs Command",
                        "3M Claw drywall",
                        "3M Claw heavy duty",
                        "3M Claw failure",
                        "3M Claw garage"
                    ],
                    "videos_per_query": 15,
                    "target_total": 120,
                    "min_views": 1000,
                    "extract_comments": True,
                    "comments_per_video": 20
                },
                "reddit": {
                    "subreddits": [
                        "HomeImprovement",
                        "DIY",
                        "homeowners",
                        "InteriorDesign",
                        "organization",
                        "Tools",
                        "fixit"
                    ],
                    "search_terms": [
                        "3M Claw",
                        "3M Claw hooks",
                        "3M Claw review",
                        "3M Claw vs Command"
                    ],
                    "target_posts": 50,
                    "target_comments": 200
                },
                "tiktok": {
                    "hashtags": ["3MClaw", "3MClawHooks", "ClawHooks"],
                    "videos_target": 30
                }
            },
            "total_content_pieces": 900,
            "estimated_time": "45 minutes",
            "estimated_cost": "$10"
        }
    },

    "priority_3": {
        "name": "Competitive Brand Positioning Data",
        "goal": "Plot all major brands on Performance/Capacity vs Installation Ease matrix",
        "strategy": {
            "brands_to_map": {
                # Premium/Complex quadrant (top-right)
                "premium_complex": ["Gladiator", "StoreWall", "Kobalt", "Proslat"],

                # Premium/Easy quadrant (top-left) - WHITE SPACE
                "premium_easy": [],  # Currently unoccupied

                # Basic/Easy quadrant (bottom-left)
                "basic_easy": ["Command", "Rubbermaid"],

                # Basic/Complex quadrant (bottom-right)
                "basic_complex": ["Generic hooks", "OOK", "Everbilt"]
            },
            "data_per_brand": {
                "products_needed": 10,
                "reviews_per_product": 20,
                "key_metrics_to_extract": [
                    "weight_capacity_mentioned",
                    "installation_difficulty_rating",
                    "tools_required",
                    "time_to_install",
                    "damage_to_wall",
                    "price_value_perception",
                    "durability_mentions",
                    "ecosystem_compatibility"
                ]
            },
            "total_brands": 10,
            "total_reviews_target": 2000,
            "estimated_time": "30 minutes",
            "estimated_cost": "$7"
        }
    }
}

# CATEGORY MAP DIMENSIONS (from screenshot)
CATEGORY_DIMENSIONS = {
    "x_axis": {
        "name": "Installation Ease",
        "scale": "Hard (complex systems) ← → Easy (damage-free)",
        "metrics": [
            "drilling_required",
            "tools_needed",
            "installation_time",
            "professional_install_needed",
            "damage_to_walls"
        ]
    },
    "y_axis": {
        "name": "Performance/Capacity",
        "scale": "Low (basic hooks) ← → High (heavy-duty systems)",
        "metrics": [
            "weight_capacity",
            "durability",
            "ecosystem_options",
            "price_point",
            "material_quality"
        ]
    },
    "white_space_target": {
        "position": "Top-left quadrant",
        "description": "Premium quality + Simple installation",
        "validation": "64% installation barrier, 65% premium revenue",
        "current_occupants": "None - unoccupied",
        "opportunity": "Damage-free premium mounting"
    }
}

if __name__ == "__main__":
    import json
    print(json.dumps(SCRAPING_PRIORITIES, indent=2))
