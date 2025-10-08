#!/usr/bin/env python3
"""
Test local vision models on random frames
Compares: Llama 3.2 Vision 11B, MiniCPM-V 8B, Qwen2.5-VL 3B
"""

import json
import random
import time
from pathlib import Path
from typing import Dict, List
import subprocess
import base64

# Test configuration
NUM_FRAMES = 5
FRAMES_DIR = Path("/tmp/youtube_live_test/frames")
OUTPUT_FILE = Path("/tmp/youtube_live_test/local_models_comparison.json")
MARKDOWN_FILE = Path("/Users/anderson115/00-interlink/12-work/3m-lighting-project/docs/local-models-comparison.md")

MODELS = {
    'llama3.2-vision:11b': {
        'size': '7.8 GB',
        'params': '11B',
        'order': 1
    },
    'minicpm-v:8b': {
        'size': '5.5 GB',
        'params': '8B',
        'order': 2
    },
    'qwen2.5vl:3b': {
        'size': '3.2 GB',
        'params': '3B',
        'order': 3
    }
}

PROMPT = """Analyze this image of electrical lighting fixtures, switches, or installations. Describe:
- What lighting fixtures, bulbs, or switches are visible
- Installation methods and wiring (if visible)
- Any electrical problems or issues demonstrated
- Any dimmers or control systems shown
Be specific and technical."""


def encode_image(image_path: Path) -> str:
    """Encode image to base64 for Ollama"""
    with open(image_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')


def test_ollama_model(model: str, image_path: Path, prompt: str) -> Dict:
    """Test a single Ollama model"""
    print(f"  Testing {model}...")

    start_time = time.time()

    try:
        # Encode image
        image_base64 = encode_image(image_path)

        # Special handling for qwen2.5vl (requires CPU mode and chat API)
        if 'qwen' in model.lower():
            request_data = {
                "model": model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt,
                        "images": [image_base64]
                    }
                ],
                "stream": False
            }

            # Set CPU mode environment variable for Qwen
            env = {**subprocess.os.environ, "OLLAMA_LLM_LIBRARY": "cpu"}

            result = subprocess.run(
                ['curl', '-s', 'http://localhost:11434/api/chat',
                 '-d', json.dumps(request_data)],
                capture_output=True,
                text=True,
                timeout=120,
                env=env
            )

            elapsed = time.time() - start_time

            if result.returncode != 0:
                return {
                    'model': model,
                    'elapsed': elapsed,
                    'error': result.stderr,
                    'success': False
                }

            response = json.loads(result.stdout)

            # Extract from chat response
            if 'message' in response and 'content' in response['message']:
                text = response['message']['content']
            else:
                text = ''

            return {
                'model': model,
                'elapsed': elapsed,
                'text': text,
                'length': len(text),
                'success': True,
                'note': 'CPU mode (GPU crash workaround)'
            }

        else:
            # Standard generate API for other models
            request_data = {
                "model": model,
                "prompt": prompt,
                "images": [image_base64],
                "stream": False
            }

            # Call Ollama API
            result = subprocess.run(
                ['curl', '-s', 'http://localhost:11434/api/generate',
                 '-d', json.dumps(request_data)],
                capture_output=True,
                text=True,
                timeout=120
            )

            elapsed = time.time() - start_time

            if result.returncode != 0:
                return {
                    'model': model,
                    'elapsed': elapsed,
                    'error': result.stderr,
                    'success': False
                }

            response = json.loads(result.stdout)
            text = response.get('response', '')

            return {
                'model': model,
                'elapsed': elapsed,
                'text': text,
                'length': len(text),
                'success': True
            }

    except Exception as e:
        elapsed = time.time() - start_time
        return {
            'model': model,
            'elapsed': elapsed,
            'error': str(e),
            'success': False
        }


def main():
    print("=" * 80)
    print("LOCAL VISION MODELS COMPARISON TEST")
    print("=" * 80)

    # Get all frames
    all_frames = list(FRAMES_DIR.glob("*/*.jpg"))
    print(f"\nFound {len(all_frames)} total frames")

    if len(all_frames) < NUM_FRAMES:
        print(f"ERROR: Only {len(all_frames)} frames available, need {NUM_FRAMES}")
        return

    # Select random frames
    test_frames = random.sample(all_frames, NUM_FRAMES)
    print(f"Selected {NUM_FRAMES} random frames for testing\n")

    # Store results
    results = {}

    # Test each model on each frame
    for model_key in MODELS:
        print(f"\n{'=' * 80}")
        print(f"TESTING: {model_key} ({MODELS[model_key]['size']})")
        print(f"{'=' * 80}")

        results[model_key] = []

        for i, frame_path in enumerate(test_frames, 1):
            print(f"\nFrame {i}/{NUM_FRAMES}: {frame_path.name}")
            result = test_ollama_model(model_key, frame_path, PROMPT)
            result['frame'] = str(frame_path)
            result['frame_name'] = frame_path.name
            results[model_key].append(result)

            if result['success']:
                print(f"  ✓ Success: {result['elapsed']:.2f}s, {result['length']} chars")
            else:
                print(f"  ✗ Failed: {result.get('error', 'Unknown error')}")

    # Save JSON results
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n{'=' * 80}")
    print(f"Raw results saved to: {OUTPUT_FILE}")

    # Generate markdown comparison
    generate_markdown(results, test_frames)
    print(f"Markdown comparison saved to: {MARKDOWN_FILE}")
    print(f"{'=' * 80}\n")


def generate_markdown(results: Dict, test_frames: List[Path]):
    """Generate markdown comparison document"""

    lines = [
        "# Local Vision Models Comparison",
        "",
        "## Test Configuration",
        f"- **Models Tested**: 3 (Llama 3.2 Vision 11B, MiniCPM-V 8B, Qwen2.5-VL 3B)",
        f"- **Frames Analyzed**: {NUM_FRAMES} randomly selected",
        f"- **Test Date**: {time.strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## Executive Summary",
        "",
        "| Model | Size | Avg Time/Frame | Success Rate | Avg Length |",
        "|-------|------|----------------|--------------|------------|"
    ]

    # Calculate averages for each model (ordered by size)
    for model_key in sorted(MODELS.keys(), key=lambda x: MODELS[x]['order']):
        model_results = results[model_key]
        successful = [r for r in model_results if r['success']]

        if successful:
            avg_time = sum(r['elapsed'] for r in successful) / len(successful)
            avg_length = sum(r['length'] for r in successful) / len(successful)
            success_rate = f"{len(successful)}/{len(model_results)}"
        else:
            avg_time = 0
            avg_length = 0
            success_rate = f"0/{len(model_results)}"

        lines.append(
            f"| {model_key} | {MODELS[model_key]['size']} | "
            f"{avg_time:.2f}s | {success_rate} | {avg_length:.0f} chars |"
        )

    lines.extend(["", "---", ""])

    # Detail for each frame
    for i, frame_path in enumerate(test_frames, 1):
        lines.extend([
            f"## Frame {i}: {frame_path.name}",
            "",
            f"**Source**: `{frame_path}`",
            ""
        ])

        # Show results from each model (ordered by size)
        for model_key in sorted(MODELS.keys(), key=lambda x: MODELS[x]['order']):
            model_result = results[model_key][i-1]

            lines.extend([
                f"### {model_key} ({MODELS[model_key]['size']})",
                ""
            ])

            if model_result['success']:
                lines.extend([
                    f"**Processing Time**: {model_result['elapsed']:.2f}s | "
                    f"**Length**: {model_result['length']} chars",
                    "",
                    model_result['text'],
                    ""
                ])
            else:
                lines.extend([
                    f"**Status**: ❌ Failed",
                    f"**Error**: {model_result.get('error', 'Unknown error')}",
                    ""
                ])

        lines.append("---")
        lines.append("")

    # Write markdown file
    MARKDOWN_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(MARKDOWN_FILE, 'w') as f:
        f.write('\n'.join(lines))


if __name__ == '__main__':
    main()
