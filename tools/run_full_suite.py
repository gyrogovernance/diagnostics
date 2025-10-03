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


def load_config():
    """Load configuration from .env file and config files."""
    # Load environment variables from .env file
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value
    
    # Get model configuration from environment
    model = os.getenv("INSPECT_EVAL_MODEL", "openai/gpt-4o")
    judge_model = os.getenv("INSPECT_EVAL_MODEL_GRADER", "anthropic/claude-3-haiku-20240307")
    log_dir = os.getenv("INSPECT_LOG_DIR", "./logs")
    
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
    print(f"Epochs per challenge: 3 (configured in TASK_CONFIG)")
    print(f"Turns per epoch: 3 (configured in autonomous_solver)")
    print(f"Total model calls: 5 × 3 × 3 = 45")
    print(f"Log directory: {config['log_dir']}")
    print(f"{'='*60}\n")
    
    # Configure evaluation parameters
    eval_params = {
        "model": config['model'],
        "model_roles": {"grader": config['judge_model']},
        "log_dir": config['log_dir']
    }
    
    # Run all challenges with configured models
    logs = eval_set(
        [
            formal_challenge(),
            normative_challenge(),
            procedural_challenge(),
            strategic_challenge(),
            epistemic_challenge()
        ],
        **eval_params
    )
    
    print(f"\n{'='*60}")
    print("Full Suite Evaluation Complete")
    print(f"{'='*60}")
    print(f"Total challenges: {len(logs)}")
    print(f"Results logged to: {config['log_dir']}")
    print(f"{'='*60}\n")
    
    return logs


if __name__ == "__main__":
    main()