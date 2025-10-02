#!/usr/bin/env python3
"""
Run a single challenge evaluation.

Usage:
    python tests/run_single_challenge.py --challenge formal --model openai/gpt-4o
"""

import argparse
from inspect_ai import eval
from gyrodiagnostics import (
    formal_challenge,
    normative_challenge,
    procedural_challenge,
    strategic_challenge,
    epistemic_challenge
)


CHALLENGES = {
    "formal": formal_challenge,
    "normative": normative_challenge,
    "procedural": procedural_challenge,
    "strategic": strategic_challenge,
    "epistemic": epistemic_challenge
}


def main():
    parser = argparse.ArgumentParser(description="Run single GyroDiagnostics challenge")
    parser.add_argument(
        "--challenge",
        type=str,
        required=True,
        choices=list(CHALLENGES.keys()),
        help="Challenge type to run"
    )
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
    
    # Get challenge task
    challenge_task = CHALLENGES[args.challenge]()
    
    print(f"\n{'='*60}")
    print(f"GyroDiagnostics Evaluation")
    print(f"{'='*60}")
    print(f"Challenge: {args.challenge}")
    print(f"Model: {args.model}")
    print(f"Judge Model: {args.judge_model}")
    print(f"Mode: {'Production (tolerant)' if args.production_mode else 'Research (strict)'}")
    print(f"Epochs: 6 (per configuration)")
    print(f"Turns per epoch: 6")
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
    
    # Run evaluation with separate judge model
    results = eval(challenge_task, **eval_params)
    
    print(f"\n{'='*60}")
    print("Evaluation Complete")
    print(f"{'='*60}")
    print(f"Results logged to: {args.log_dir}")
    print(f"{'='*60}\n")
    
    return results


if __name__ == "__main__":
    main()