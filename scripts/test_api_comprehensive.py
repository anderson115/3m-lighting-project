#!/usr/bin/env python3
"""
Comprehensive API vision model testing with quality scoring
Tests multiple models per provider at different price/performance points
Scores: cost, speed, breadth, depth, uniqueness, accuracy
"""

import os
import sys
import time
import base64
import random
import json
from pathlib import Path
from typing import Dict, List, Tuple
from dotenv import load_dotenv

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
load_dotenv(project_root / '.env')

import google.generativeai as genai
from openai import OpenAI
import subprocess


def encode_image_base64(image_path: Path) -> str:
    """Encode image to base64"""
    with open(image_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')


# Model configurations with provider, model name, cost per 1M tokens
MODELS = {
    # Gemini models
    'gemini-2.0-flash': {
        'provider': 'gemini',
        'model_name': 'gemini-2.0-flash-exp',
        'cost_per_1m_input': 0.0,  # Free tier
        'cost_per_1m_output': 0.0,
        'tier': 'fast'
    },
    'gemini-1.5-pro': {
        'provider': 'gemini',
        'model_name': 'gemini-1.5-pro',
        'cost_per_1m_input': 1.25,
        'cost_per_1m_output': 5.0,
        'tier': 'premium'
    },

    # OpenAI models
    'gpt-4o-mini': {
        'provider': 'openai',
        'model_name': 'gpt-4o-mini',
        'cost_per_1m_input': 0.15,
        'cost_per_1m_output': 0.60,
        'tier': 'fast'
    },
    'gpt-4o': {
        'provider': 'openai',
        'model_name': 'gpt-4o',
        'cost_per_1m_input': 2.50,
        'cost_per_1m_output': 10.0,
        'tier': 'premium'
    },

    # GLM models
    'glm-4v-flash': {
        'provider': 'glm',
        'model_name': 'glm-4v-flash',
        'cost_per_1m_input': 0.001,
        'cost_per_1m_output': 0.001,
        'tier': 'fast'
    },
    'glm-4v-plus': {
        'provider': 'glm',
        'model_name': 'glm-4v-plus',
        'cost_per_1m_input': 0.05,
        'cost_per_1m_output': 0.05,
        'tier': 'premium'
    },

    # Local model
    'llava-local': {
        'provider': 'local',
        'model_name': 'llava:latest',
        'cost_per_1m_input': 0.0,
        'cost_per_1m_output': 0.0,
        'tier': 'free'
    }
}


def test_gemini(image_path: Path, prompt: str, model_name: str) -> Tuple[float, str, int, int]:
    """Test Gemini model"""
    api_key = os.getenv('GEMINI_API_KEY')
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)

    with open(image_path, 'rb') as f:
        image_data = f.read()

    start = time.time()
    try:
        response = model.generate_content([prompt, {'mime_type': 'image/jpeg', 'data': image_data}])
        elapsed = time.time() - start
        text = response.text

        # Estimate tokens (rough: 4 chars = 1 token)
        input_tokens = len(prompt) // 4
        output_tokens = len(text) // 4

        return elapsed, text, input_tokens, output_tokens
    except Exception as e:
        return -1, f"ERROR: {str(e)}", 0, 0


def test_openai(image_path: Path, prompt: str, model_name: str) -> Tuple[float, str, int, int]:
    """Test OpenAI model"""
    api_key = os.getenv('OPENAI_API_KEY')
    client = OpenAI(api_key=api_key)

    base64_image = encode_image_base64(image_path)

    start = time.time()
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]
            }],
            max_tokens=1000
        )
        elapsed = time.time() - start
        text = response.choices[0].message.content

        # Get actual token usage
        input_tokens = response.usage.prompt_tokens
        output_tokens = response.usage.completion_tokens

        return elapsed, text, input_tokens, output_tokens
    except Exception as e:
        return -1, f"ERROR: {str(e)}", 0, 0


def test_glm(image_path: Path, prompt: str, model_name: str) -> Tuple[float, str, int, int]:
    """Test GLM model"""
    from zhipuai import ZhipuAI
    api_key = os.getenv('GLM46_API_KEY')
    client = ZhipuAI(api_key=api_key)

    base64_image = encode_image_base64(image_path)

    start = time.time()
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]
            }]
        )
        elapsed = time.time() - start
        text = response.choices[0].message.content

        # Estimate tokens
        input_tokens = len(prompt) // 4
        output_tokens = len(text) // 4

        return elapsed, text, input_tokens, output_tokens
    except Exception as e:
        return -1, f"ERROR: {str(e)}", 0, 0


def test_llava_local(image_path: Path, prompt: str) -> Tuple[float, str, int, int]:
    """Test local LLaVA via Ollama"""
    start = time.time()
    try:
        result = subprocess.run(
            ['ollama', 'run', 'llava:latest', prompt, str(image_path)],
            capture_output=True,
            text=True,
            check=True,
            timeout=60
        )
        elapsed = time.time() - start
        text = result.stdout.strip()

        # Estimate tokens
        input_tokens = len(prompt) // 4
        output_tokens = len(text) // 4

        return elapsed, text, input_tokens, output_tokens
    except Exception as e:
        return -1, f"ERROR: {str(e)}", 0, 0


def run_model_test(model_key: str, image_path: Path, prompt: str) -> Dict:
    """Run test for a specific model"""
    config = MODELS[model_key]
    provider = config['provider']
    model_name = config['model_name']

    if provider == 'gemini':
        elapsed, text, input_tokens, output_tokens = test_gemini(image_path, prompt, model_name)
    elif provider == 'openai':
        elapsed, text, input_tokens, output_tokens = test_openai(image_path, prompt, model_name)
    elif provider == 'glm':
        elapsed, text, input_tokens, output_tokens = test_glm(image_path, prompt, model_name)
    elif provider == 'local':
        elapsed, text, input_tokens, output_tokens = test_llava_local(image_path, prompt)
    else:
        return None

    # Calculate cost
    cost = 0
    if elapsed > 0:
        cost = (input_tokens / 1_000_000 * config['cost_per_1m_input'] +
                output_tokens / 1_000_000 * config['cost_per_1m_output'])

    return {
        'model_key': model_key,
        'elapsed': elapsed,
        'text': text,
        'length': len(text) if elapsed > 0 else 0,
        'input_tokens': input_tokens,
        'output_tokens': output_tokens,
        'cost': cost,
        'success': elapsed > 0
    }


def extract_keywords(text: str) -> set:
    """Extract meaningful keywords from text for uniqueness scoring"""
    # Convert to lowercase and split
    words = text.lower().split()

    # Filter out common words and keep technical/descriptive terms
    stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                 'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been',
                 'this', 'that', 'these', 'those', 'it', 'its', 'can', 'could', 'would',
                 'should', 'may', 'might', 'will', 'shall', 'i', 'you', 'he', 'she', 'we',
                 'they', 'them', 'their', 'see', 'image', 'shows', 'showing', 'shown'}

    keywords = {word.strip('.,!?;:()[]{}') for word in words
                if len(word) > 3 and word not in stopwords}

    return keywords


def score_model_outputs(results: Dict[str, List[Dict]]) -> Dict:
    """Score all models across multiple dimensions"""
    scores = {}

    for model_key in results:
        model_results = results[model_key]
        successful_results = [r for r in model_results if r['success']]

        if not successful_results:
            scores[model_key] = {
                'cost_score': 0, 'speed_score': 0, 'breadth_score': 0,
                'depth_score': 0, 'uniqueness_score': 0, 'accuracy_score': 0,
                'total_score': 0
            }
            continue

        # Calculate metrics
        avg_time = sum(r['elapsed'] for r in successful_results) / len(successful_results)
        avg_length = sum(r['length'] for r in successful_results) / len(successful_results)
        total_cost = sum(r['cost'] for r in successful_results)

        # Extract all keywords from this model
        all_keywords = set()
        for r in successful_results:
            all_keywords.update(extract_keywords(r['text']))

        scores[model_key] = {
            'avg_time': avg_time,
            'avg_length': avg_length,
            'total_cost': total_cost,
            'success_rate': len(successful_results) / len(model_results),
            'unique_keywords': all_keywords,
            'num_keywords': len(all_keywords)
        }

    # Calculate normalized scores (0-100)
    all_times = [s['avg_time'] for s in scores.values() if 'avg_time' in s]
    all_costs = [s['total_cost'] for s in scores.values() if 'total_cost' in s]
    all_lengths = [s['avg_length'] for s in scores.values() if 'avg_length' in s]
    all_keyword_counts = [s['num_keywords'] for s in scores.values() if 'num_keywords' in s]

    min_time, max_time = min(all_times), max(all_times)
    min_cost, max_cost = min(all_costs), max(all_costs)
    min_length, max_length = min(all_lengths), max(all_lengths)

    for model_key in scores:
        s = scores[model_key]

        if 'avg_time' not in s:
            continue

        # Cost score: lower is better (inverted)
        if max_cost > min_cost:
            s['cost_score'] = 100 - ((s['total_cost'] - min_cost) / (max_cost - min_cost) * 100)
        else:
            s['cost_score'] = 100

        # Speed score: faster is better (inverted)
        if max_time > min_time:
            s['speed_score'] = 100 - ((s['avg_time'] - min_time) / (max_time - min_time) * 100)
        else:
            s['speed_score'] = 100

        # Breadth score: more keywords = more topics covered
        if max(all_keyword_counts) > min(all_keyword_counts):
            s['breadth_score'] = ((s['num_keywords'] - min(all_keyword_counts)) /
                                  (max(all_keyword_counts) - min(all_keyword_counts)) * 100)
        else:
            s['breadth_score'] = 100

        # Depth score: longer responses = more detail
        if max_length > min_length:
            s['depth_score'] = ((s['avg_length'] - min_length) / (max_length - min_length) * 100)
        else:
            s['depth_score'] = 100

        # Accuracy score: based on success rate
        s['accuracy_score'] = s['success_rate'] * 100

    # Calculate uniqueness scores (keywords found by this model but not others)
    for model_key in scores:
        s = scores[model_key]
        if 'unique_keywords' not in s:
            s['uniqueness_score'] = 0
            continue

        # Count keywords unique to this model
        other_keywords = set()
        for other_key in scores:
            if other_key != model_key and 'unique_keywords' in scores[other_key]:
                other_keywords.update(scores[other_key]['unique_keywords'])

        unique_to_this_model = s['unique_keywords'] - other_keywords
        s['truly_unique_count'] = len(unique_to_this_model)
        s['truly_unique'] = unique_to_this_model

        # Uniqueness score: % of keywords that are unique
        if s['num_keywords'] > 0:
            s['uniqueness_score'] = (len(unique_to_this_model) / s['num_keywords']) * 100
        else:
            s['uniqueness_score'] = 0

    # Calculate total weighted score
    # Weights: cost(15%), speed(20%), breadth(15%), depth(20%), uniqueness(15%), accuracy(15%)
    for model_key in scores:
        s = scores[model_key]
        if 'cost_score' in s:
            s['total_score'] = (
                s['cost_score'] * 0.15 +
                s['speed_score'] * 0.20 +
                s['breadth_score'] * 0.15 +
                s['depth_score'] * 0.20 +
                s['uniqueness_score'] * 0.15 +
                s['accuracy_score'] * 0.15
            )
        else:
            s['total_score'] = 0

    return scores


def main():
    """Test all models on 6 representative frames"""

    # Collect all frames
    frames_dir = Path("/tmp/youtube_live_test/frames")
    all_frames = list(frames_dir.glob("*/*.jpg"))

    # Select 6 diverse frames (2 keyword, 2 scene, 2 spacing)
    random.seed(42)
    keyword_frames = [f for f in all_frames if 'keyword' in f.name]
    scene_frames = [f for f in all_frames if 'scene' in f.name]
    spacing_frames = [f for f in all_frames if 'spacing' in f.name or 'coverage' in f.name]

    test_frames = (
        random.sample(keyword_frames, min(2, len(keyword_frames))) +
        random.sample(scene_frames, min(2, len(scene_frames))) +
        random.sample(spacing_frames, min(2, len(spacing_frames)))
    )

    prompt = ("Describe what you see in this image related to lighting or electrical issues. "
              "Be specific about any fixtures, wiring, switches, dimmers, bulbs, or installation methods shown. "
              "Note any problems, solutions, or demonstrations visible.")

    print("=" * 80)
    print("COMPREHENSIVE API VISION MODEL TESTING")
    print("=" * 80)
    print(f"\nTesting {len(test_frames)} frames across {len(MODELS)} models")
    print(f"Prompt: {prompt[:100]}...")

    results = {model_key: [] for model_key in MODELS}

    # Test each model
    for model_key in MODELS:
        config = MODELS[model_key]
        print(f"\n{'=' * 80}")
        print(f"TESTING: {model_key} ({config['model_name']})")
        print(f"Provider: {config['provider']} | Tier: {config['tier']}")
        print("=" * 80)

        for i, frame in enumerate(test_frames, 1):
            print(f"[{i}/{len(test_frames)}] {frame.name}...", end=" ", flush=True)

            result = run_model_test(model_key, frame, prompt)
            results[model_key].append(result)

            if result['success']:
                print(f"✅ {result['elapsed']:.2f}s ({result['length']} chars, ${result['cost']:.6f})")
            else:
                print(f"❌ {result['text'][:80]}")

            # Small delay to avoid rate limits
            time.sleep(0.5)

    # Score all models
    print(f"\n{'=' * 80}")
    print("CALCULATING SCORES...")
    print("=" * 80)

    scores = score_model_outputs(results)

    # Save detailed results
    output_dir = Path("/tmp/youtube_live_test")

    # Save raw results
    with open(output_dir / "comprehensive_test_raw_results.json", 'w') as f:
        # Convert sets to lists for JSON serialization
        scores_serializable = {}
        for k, v in scores.items():
            scores_serializable[k] = {
                key: list(val) if isinstance(val, set) else val
                for key, val in v.items()
            }
        json.dump({
            'results': {k: v for k, v in results.items()},
            'scores': scores_serializable
        }, f, indent=2, default=str)

    # Save sample outputs for manual review
    with open(output_dir / "comprehensive_test_sample_outputs.txt", 'w') as f:
        f.write("SAMPLE OUTPUTS FOR MANUAL QUALITY REVIEW\n")
        f.write("=" * 80 + "\n\n")

        for model_key in MODELS:
            f.write(f"\n{'=' * 80}\n")
            f.write(f"MODEL: {model_key}\n")
            f.write("=" * 80 + "\n\n")

            for i, result in enumerate(results[model_key][:3], 1):  # First 3 samples
                if result['success']:
                    f.write(f"--- Sample {i} ---\n")
                    f.write(f"{result['text']}\n\n")

    print(f"\n✅ Results saved to {output_dir}/")
    print(f"   - comprehensive_test_raw_results.json")
    print(f"   - comprehensive_test_sample_outputs.txt")

    # Print summary table
    print(f"\n{'=' * 80}")
    print("SCORE SUMMARY")
    print("=" * 80)
    print(f"{'Model':<20} {'Cost':>8} {'Speed':>8} {'Breadth':>8} {'Depth':>8} {'Unique':>8} {'Accuracy':>8} {'TOTAL':>8}")
    print("-" * 80)

    sorted_models = sorted(scores.items(), key=lambda x: x[1].get('total_score', 0), reverse=True)
    for model_key, s in sorted_models:
        if 'total_score' in s:
            print(f"{model_key:<20} {s['cost_score']:>7.1f} {s['speed_score']:>7.1f} {s['breadth_score']:>7.1f} "
                  f"{s['depth_score']:>7.1f} {s['uniqueness_score']:>7.1f} {s['accuracy_score']:>7.1f} {s['total_score']:>7.1f}")

    return results, scores


if __name__ == "__main__":
    main()
