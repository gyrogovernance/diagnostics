#!/usr/bin/env python3
"""
Run complete GyroDiagnostics evaluation suite using configured models.

Usage:
    python tools/run_full_suite.py
"""

import os
from pathlib import Path
from inspect_ai import eval_set
from gyrodiagnostics import (
    formal_challenge,
    normative_challenge,
    procedural_challenge,
    strategic_challenge,
    epistemic_challenge
)
from gyrodiagnostics.utils.constants import TASK_CONFIG


def load_config():
    """Load configuration from .env file and config files."""
    # Load environment variables from .env file
    env_file = Path(".env")
    if env_file.exists():
        try:
            with open(env_file, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        try:
                            key, value = line.split('=', 1)
                            # Clean up any problematic characters
                            key = key.strip()
                            value = value.strip()
                            os.environ[key] = value
                        except ValueError as e:
                            print(f"Warning: Skipping malformed line {line_num} in .env file: {line}")
                            continue
        except Exception as e:
            print(f"Warning: Could not read .env file: {e}")
            print("Continuing with environment variables only...")
    
    # Get model configuration from environment (no defaults - must be explicitly set)
    model = os.getenv("INSPECT_EVAL_MODEL")
    judge_model = os.getenv("INSPECT_EVAL_MODEL_GRADER")
    log_dir = os.getenv("INSPECT_LOG_DIR", "./logs")
    
    # Validate required configuration
    if not model:
        print("ERROR: INSPECT_EVAL_MODEL environment variable not set!")
        print("Please set it in your .env file or environment:")
        print("INSPECT_EVAL_MODEL=openrouter/qwen/qwen3-30b-a3b:free")
        exit(1)
    
    if not judge_model:
        print("ERROR: INSPECT_EVAL_MODEL_GRADER environment variable not set!")
        print("Please set it in your .env file or environment:")
        print("INSPECT_EVAL_MODEL_GRADER=openrouter/meta-llama/llama-3.3-70b-instruct:free")
        exit(1)
    
    # Validate API key is set for OpenRouter
    if "openrouter" in model.lower() and not os.getenv("OPENROUTER_API_KEY"):
        print("ERROR: OPENROUTER_API_KEY environment variable not set!")
        print("Please create a .env file with your OpenRouter API key:")
        print("OPENROUTER_API_KEY=your-api-key-here")
        exit(1)
    
    return {
        "model": model,
        "judge_model": judge_model,
        "log_dir": log_dir
    }


def main():
    """Run the complete GyroDiagnostics evaluation suite using configured models."""
    # Load configuration
    config = load_config()
    
    print(f"\n{'='*60}")
    print(f"GyroDiagnostics Full Suite Evaluation")
    print(f"{'='*60}")
    print(f"Model: {config['model']}")
    print(f"Judge Model: {config['judge_model']}")
    print(f"Challenges: 5 (formal, normative, procedural, strategic, epistemic)")
    print(f"Epochs per challenge: {TASK_CONFIG.get('epochs', 3)} (configured in TASK_CONFIG)")
    print(f"Turns per epoch: {TASK_CONFIG.get('turns', 3)} (configured in autonomous_solver)")
    print(f"Total model calls: 5 × {TASK_CONFIG.get('epochs', 3)} × {TASK_CONFIG.get('turns', 3)} = {5 * TASK_CONFIG.get('epochs', 3) * TASK_CONFIG.get('turns', 3)}")
    print(f"Log directory: {config['log_dir']}")
    print(f"{'='*60}\n")
    
    # Configure evaluation parameters
    eval_params = {
        "model": config['model'],
        "model_roles": {"grader": config['judge_model']},
        "log_dir": config['log_dir']
    }
    
    # Define all challenges
    challenges = [
        formal_challenge(),
        normative_challenge(),
        procedural_challenge(),
        strategic_challenge(),
        epistemic_challenge()
    ]
    
    print(f"Running {len(challenges)} challenges:")
    for i, challenge in enumerate(challenges, 1):
        print(f"  {i}. {challenge.name}")
    print()
    
    # Run all challenges with configured models
    logs = eval_set(challenges, max_tasks=1, **eval_params)
    
    print(f"\n{'='*60}")
    print("Full Suite Evaluation Complete")
    print(f"{'='*60}")
    print(f"Total challenges: {len(challenges)}")
    print(f"Results logged to: {config['log_dir']}")
    print(f"{'='*60}\n")
    
    return logs


if __name__ == "__main__":
    main()