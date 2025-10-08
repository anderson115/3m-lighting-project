#!/usr/bin/env python3
"""
Quick API Connection Test
Tests all configured APIs with simple prompt to verify connectivity
"""
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.models.model_registry import (
    ModelRegistry, GeminiClient, OpenAIClient, AnthropicClient,
    DeepSeekAPIClient, GLM4Client, TogetherAIClient
)


def test_api(name: str, client_class, config: dict):
    """Test a single API with simple prompt"""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"{'='*60}")

    try:
        # Initialize client
        client = client_class(**config)

        # Simple test prompt
        messages = [
            {"role": "system", "content": "You are a helpful assistant. Respond with valid JSON only."},
            {"role": "user", "content": "Return a JSON object with one field: {\"status\": \"ok\"}"}
        ]

        # Send request
        response = client.chat(messages, max_tokens=50)

        # Check response
        content = response.get('message', {}).get('content', '')
        usage = response.get('usage', {})

        print(f"✅ SUCCESS")
        print(f"   Response: {content[:100]}")
        if usage:
            print(f"   Tokens: {usage.get('total_tokens', 'N/A')}")

        return {'status': 'success', 'name': name}

    except Exception as e:
        print(f"❌ FAILED: {e}")
        return {'status': 'failed', 'name': name, 'error': str(e)}


def main():
    print("=" * 60)
    print("API CONNECTION TEST")
    print("=" * 60)

    registry = ModelRegistry()
    results = []

    # Test each API
    apis_to_test = [
        ('Gemini 2.0 Flash', GeminiClient, registry.get_gemini_config()),
        ('OpenAI GPT-4o-mini', OpenAIClient, registry.get_openai_config()),
        ('Anthropic Claude 3.5', AnthropicClient, registry.get_anthropic_config()),
        ('DeepSeek API', DeepSeekAPIClient, registry.get_deepseek_api_config()),
        ('GLM-4 Flash', GLM4Client, registry.get_glm4_config()),
        ('Together AI Llama 3.3', TogetherAIClient, registry.get_togetherai_config()),
    ]

    for name, client_class, config in apis_to_test:
        result = test_api(name, client_class, config)
        results.append(result)

    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")

    successful = [r for r in results if r['status'] == 'success']
    failed = [r for r in results if r['status'] == 'failed']

    print(f"\n✅ Successful: {len(successful)}/{len(results)}")
    for r in successful:
        print(f"   - {r['name']}")

    if failed:
        print(f"\n❌ Failed: {len(failed)}/{len(results)}")
        for r in failed:
            print(f"   - {r['name']}: {r.get('error', 'Unknown error')}")

    print()


if __name__ == '__main__':
    main()
