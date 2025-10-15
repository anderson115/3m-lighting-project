#!/usr/bin/env python3
"""Test LLM integration directly"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'modules'))

from expert_authority.core.config import Config
from anthropic import Anthropic

# Load config
config = Config()

print("=" * 70)
print("LLM API TEST")
print("=" * 70)
print()

# Check API key
print(f"✅ API Key loaded: {config.anthropic_api_key[:20]}...{config.anthropic_api_key[-10:]}")
print(f"📏 Key length: {len(config.anthropic_api_key)}")
print()

# Get LLM config
llm_config = config.get_llm_config(2)
print(f"🤖 Model: {llm_config['model']}")
print(f"🔑 Provider: {llm_config['provider']}")
print()

# Test API call
print("🧪 Testing Anthropic API call...")
try:
    client = Anthropic(api_key=config.anthropic_api_key)

    response = client.messages.create(
        model=llm_config['model'],
        max_tokens=100,
        messages=[{
            "role": "user",
            "content": "Say 'API test successful' in exactly 3 words."
        }]
    )

    result = response.content[0].text
    print(f"✅ API call successful!")
    print(f"📝 Response: {result}")
    print()
    print("=" * 70)
    print("✅ LLM INTEGRATION WORKING PERFECTLY")
    print("=" * 70)

except Exception as e:
    print(f"❌ API call failed: {e}")
    print()
    print("Debugging info:")
    print(f"   Error type: {type(e).__name__}")
    print(f"   Error details: {str(e)}")
