#!/usr/bin/env python3
"""
Test Tier 2 with LLM (Claude Sonnet 4)
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'modules'))

from expert_authority.core.config import Config

print("=" * 70)
print("TIER 2 LLM CONFIGURATION TEST")
print("=" * 70)
print()

# Test configuration loading
config = Config()

print("✅ API Keys Loaded:")
print(f"   Anthropic: {'✅' if config.anthropic_api_key else '❌'} ({config.anthropic_api_key[:20]}... if config.anthropic_api_key else 'Not set')")
print(f"   OpenAI: {'✅' if config.openai_api_key else '❌'}")
print(f"   DeepSeek: {'✅' if config.deepseek_api_key else '❌'}")
print()

# Test Tier 2 configuration
print("📊 Tier 2 (Professional) Configuration:")
tier2_config = config.get_tier_config(2)
print(f"   Analyzer: {tier2_config['analyzer']}")
print(f"   Platforms: {', '.join(tier2_config['platforms'])}")
print(f"   Discussion limit: {tier2_config['discussion_limit']}")
print()

# Test LLM configuration with fallback
print("🤖 LLM Configuration for Tier 2:")
llm_config = config.get_llm_config(2)
print(f"   Primary provider: {llm_config['provider']}")
print(f"   Primary model: {llm_config['model']}")
print(f"   API key available: {'✅' if llm_config['api_key'] else '❌'}")
print(f"   Fallback models: {len(llm_config['fallback_chain'])}")
print()

if llm_config['fallback_chain']:
    print("   Fallback chain:")
    for i, fallback in enumerate(llm_config['fallback_chain'], 1):
        print(f"      {i}. {fallback['provider']}: {fallback['model']} (priority {fallback['priority']})")
    print()

# Test Tier 3 configuration
print("📊 Tier 3 (Enterprise) Configuration:")
tier3_config = config.get_tier_config(3)
print(f"   Analyzer: {tier3_config['analyzer']}")
print(f"   Features: {len(tier3_config['features'])} features")
print()

print("🤖 LLM Configuration for Tier 3:")
llm_config_t3 = config.get_llm_config(3)
print(f"   Primary provider: {llm_config_t3['provider']}")
print(f"   Primary model: {llm_config_t3['model']}")
print(f"   Use case: {llm_config_t3.get('use_case', 'general')}")
print(f"   Fallback models: {len(llm_config_t3['fallback_chain'])}")
print()

if llm_config_t3['fallback_chain']:
    print("   Fallback chain:")
    for i, fallback in enumerate(llm_config_t3['fallback_chain'], 1):
        use_case = fallback.get('use_case', 'general')
        print(f"      {i}. {fallback['provider']}: {fallback['model']} ({use_case}, priority {fallback['priority']})")
    print()

print("=" * 70)
print("✅ CONFIGURATION TEST COMPLETE")
print("=" * 70)
print()
print("🎯 Model Priority Strategy:")
print()
print("Tier 1 (Essential):")
print("   → Rule-based only (no LLM)")
print()
print("Tier 2 (Professional):")
print("   → Primary: Claude Sonnet 4 (best cost/quality balance)")
print("   → Fallback 1: GPT-4o-mini (cost-effective)")
print("   → Fallback 2: DeepSeek (emergency)")
print()
print("Tier 3 (Enterprise):")
print("   → Primary: Claude Opus 4 (highest quality)")
print("   → Cross-validation: GPT-4o")
print("   → Fallback: Claude Sonnet 4")
print("   → Emergency: DeepSeek")
print()
