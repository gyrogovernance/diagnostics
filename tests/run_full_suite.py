#!/usr/bin/env python3
"""
Run complete GyroDiagnostics evaluation suite.

Usage:
    python tests/run_full_suite.py --model openai/gpt-4o
"""

import argparse
from inspect_ai import eval_set
from gyrodiagnostics import (
    formal_challenge,
    normative_challenge,
    procedural_challenge,
    strategic_challenge,
    epistemic_challenge
)


def main():
    parser = argparse.ArgumentParser(description="Run full GyroDiagnostics suite")
    parser.add_argument(
        "--model",
        type=str,
        required=True,
        help="Model to evaluate (e.g., 'openai/gpt-4o')"
    )
    parser.add_argument(
        "--log-dir",
        type=str,
        default="./logs",
        help="Directory for evaluation logs"
    )
    parser.add_argument(
        "--judge-model",
        type=str,
        default="anthropic/claude-3-haiku-20240307",
        help="Judge model for scoring (must be different from evaluated model)"
    )
    parser.add_argument(
        "--production-mode",
        action="store_true",
        help="Use production configuration with error tolerance (fail_on_error=0.05)"
    )
    
    args = parser.parse_args()
    
    print(f"\n{'='*60}")
    print(f"GyroDiagnostics Full Suite Evaluation")
    print(f"{'='*60}")
    print(f"Model: {args.model}")
    print(f"Judge Model: {args.judge_model}")
    print(f"Mode: {'Production (tolerant)' if args.production_mode else 'Research (strict)'}")
    print(f"Challenges: 5 (formal, normative, procedural, strategic, epistemic)")
    print(f"Epochs per challenge: 6")
    print(f"Turns per epoch: 6")
    print(f"Total model calls: 5 × 6 × 6 = 180")
    print(f"Log directory: {args.log_dir}")
    print(f"{'='*60}\n")
    
    # Configure evaluation parameters based on mode
    eval_params = {
        "model": args.model,
        "model_roles": {"grader": args.judge_model},
        "log_dir": args.log_dir
    }
    
    # Add production mode parameters if requested
    if args.production_mode:
        eval_params.update({
            "fail_on_error": 0.05,  # Allow 5% failure rate
            "retry_on_error": 1     # Retry failed samples once
        })
    
    # Run all challenges with separate judge model
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
    print(f"Results logged to: {args.log_dir}")
    print(f"{'='*60}\n")
    
    return logs


if __name__ == "__main__":
    main()