#!/usr/bin/env python3
"""
Run complete GyroDiagnostics evaluation suite using configured models.

Usage:
    python tools/run_diagnostics.py [--resume]
    
Options:
    --resume    Resume from existing logs (allows dirty log directory)
"""

import os
import sys
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
    analyst_a = os.getenv("INSPECT_EVAL_MODEL_GRADER_A")
    analyst_b = os.getenv("INSPECT_EVAL_MODEL_GRADER_B")
    backup_analyst_model = os.getenv("INSPECT_EVAL_MODEL_GRADER_BACKUP")
    log_dir = os.getenv("INSPECT_LOG_DIR", "./logs")
    
    # Validate required configuration
    if not model:
        print("ERROR: INSPECT_EVAL_MODEL environment variable not set!")
        print("Please set it in your .env file or environment:")
        print("INSPECT_EVAL_MODEL=openrouter/qwen/qwen3-30b-a3b:free")
        exit(1)
    
    # Validate at least 2 ensemble analysts are configured (tetrahedral structure)
    configured_analysts = sum([bool(analyst_a), bool(analyst_b)])
    if configured_analysts < 2:
        print("ERROR: At least 2 ensemble analysts must be configured for tetrahedral structure!")
        print("Please set both of these in your .env file:")
        print("INSPECT_EVAL_MODEL_GRADER_A=openrouter/model-name:free")
        print("INSPECT_EVAL_MODEL_GRADER_B=openrouter/model-name:free")
        exit(1)
    
    # Validate API key is set for OpenRouter
    if "openrouter" in model.lower() and not os.getenv("OPENROUTER_API_KEY"):
        print("ERROR: OPENROUTER_API_KEY environment variable not set!")
        print("Please create a .env file with your OpenRouter API key:")
        print("OPENROUTER_API_KEY=your-api-key-here")
        exit(1)
    
    return {
        "model": model,
        "analyst_a": analyst_a,
        "analyst_b": analyst_b,
        "backup_analyst_model": backup_analyst_model,
        "log_dir": log_dir
    }


def main():
    """Run the complete GyroDiagnostics evaluation suite using configured models."""
    # Check for --resume flag
    resume_mode = "--resume" in sys.argv or "--log-dir-allow-dirty" in sys.argv
    
    # Load configuration
    config = load_config()
    
    print(f"\n{'='*60}")
    print(f"GyroDiagnostics Full Suite Evaluation")
    if resume_mode:
        print("(Resume mode: will reuse existing logs)")
    print(f"{'='*60}")
    print(f"Model: {config['model']}")
    
    # Show ensemble analysts
    ensemble_analysts = []
    if config['analyst_a']:
        ensemble_analysts.append(f"A: {config['analyst_a']}")
    if config['analyst_b']:
        ensemble_analysts.append(f"B: {config['analyst_b']}")
    
    if ensemble_analysts:
        print(f"Ensemble Analysts: {', '.join(ensemble_analysts)}")
    
    if config['backup_analyst_model']:
        print(f"Backup Analyst: {config['backup_analyst_model']}")
    
    print(f"Challenges: 5 (formal, normative, procedural, strategic, epistemic)")
    print(f"Epochs per challenge: {TASK_CONFIG.get('epochs', 3)} (configured in TASK_CONFIG)")
    print(f"Turns per epoch: {TASK_CONFIG.get('turns', 3)} (configured in autonomous_solver)")
    print(f"Total model calls: 5 × {TASK_CONFIG.get('epochs', 3)} × {TASK_CONFIG.get('turns', 3)} = {5 * TASK_CONFIG.get('epochs', 3) * TASK_CONFIG.get('turns', 3)}")
    print(f"Log directory: {config['log_dir']}")
    print(f"{'='*60}\n")
    
    # Configure evaluation parameters
    model_roles = {}
    
    # Add ensemble analysts
    if config['analyst_a']:
        model_roles["analyst_a"] = config['analyst_a']
    if config['analyst_b']:
        model_roles["analyst_b"] = config['analyst_b']
    
    # Add backup analyst
    if config['backup_analyst_model']:
        model_roles["analyst_backup"] = config['backup_analyst_model']
    
    eval_params = {
        "model": config['model'],
        "model_roles": model_roles,
        "log_dir": config['log_dir']
    }
    
    # Add log_dir_allow_dirty if in resume mode
    if resume_mode:
        eval_params["log_dir_allow_dirty"] = True
    
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
    # Make eval_set retry behavior explicit to better recover from transient outages
    success, logs = eval_set(
        challenges,
        max_tasks=1,
        retry_attempts=15,
        retry_wait=60,
        retry_connections=0.5,
        **eval_params
    )
    
    print(f"\n{'='*60}")
    print("Full Suite Evaluation Complete")
    print(f"{'='*60}")
    print(f"Total challenges: {len(challenges)}")
    print(f"Results logged to: {config['log_dir']}")
    if not success:
        print("Some tasks did not complete even after retries.")
        print("Run again with --resume to continue:")
        print("  python run.py --resume")
    print("Run final analysis to generate timestamped reports and insight briefs:")
    print("  python tools/analyzer.py --eval-dir logs")
    # Note: Insight briefs are generated during final analysis step, not here.
    print(f"{'='*60}\n")
    
    return logs


if __name__ == "__main__":
    main()