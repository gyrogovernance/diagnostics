#!/usr/bin/env python3
"""
Analyze GyroDiagnostics evaluation results and calculate Balance Horizon.

Usage:
    python tests/analyze_results.py --log-dir ./logs
"""

import argparse
import json
from pathlib import Path
from inspect_ai.log import read_eval_log
from gyrodiagnostics.metrics.balance_horizon import (
    calculate_balance_horizon,
    validate_balance_horizon
)


def extract_challenge_type(task_name: str) -> str:
    """Extract challenge type from task name."""
    for challenge in ["formal", "normative", "procedural", "strategic", "epistemic"]:
        if challenge in task_name.lower():
            return challenge
    return "formal"  # Default fallback


def analyze_challenge_results(log_path: Path) -> dict:
    """Analyze results from a single challenge log."""
    log = read_eval_log(log_path)
    
    # Extract epoch results (alignment_score, duration)
    epoch_results = []
    
    for sample in log.samples:
        if sample.scores:
            # Get alignment score from metadata - handle different log schemas
            alignment_score = 0
            
            # Try to find alignment_score in any score object's metadata
            for score_name, score_obj in sample.scores.items():
                if hasattr(score_obj, 'metadata') and score_obj.metadata:
                    if "alignment_score" in score_obj.metadata:
                        alignment_score = score_obj.metadata["alignment_score"]
                        break
            
            # Fallback: if no alignment_score found, skip this sample
            if alignment_score == 0:
                continue
            
            # Calculate duration in minutes with fallback to metadata
            duration_minutes = 0
            
            if sample.completed_at and sample.created_at:
                duration_seconds = (sample.completed_at - sample.created_at).total_seconds()
                duration_minutes = duration_seconds / 60
            else:
                # Fallback: try to get duration from score metadata
                for score_name, score_obj in sample.scores.items():
                    if hasattr(score_obj, 'metadata') and score_obj.metadata:
                        if "epoch_duration_minutes" in score_obj.metadata:
                            duration_minutes = score_obj.metadata["epoch_duration_minutes"]
                            break
                        elif "turn_metadata" in score_obj.metadata:
                            # Try to calculate from actual timestamps if available
                            turn_data = score_obj.metadata["turn_metadata"]
                            if turn_data and len(turn_data) > 0:
                                # Only use if we have actual timestamps
                                first_turn = turn_data[0]
                                last_turn = turn_data[-1]
                                if (first_turn.get("timestamp") and last_turn.get("timestamp")):
                                    duration_seconds = last_turn["timestamp"] - first_turn["timestamp"]
                                    duration_minutes = duration_seconds / 60
                                    break
            
            epoch_results.append((alignment_score, duration_minutes))
    
    if not epoch_results:
        return {"error": "No valid epoch results found"}
    
    # Calculate Balance Horizon (extract challenge type from task name)
    challenge_type = extract_challenge_type(log.eval.task)
    bh_results = calculate_balance_horizon(epoch_results, challenge_type=challenge_type)
    status, message = validate_balance_horizon(bh_results["balance_horizon_normalized"])
    
    return {
        "challenge": log.eval.task,
        "model": log.eval.model,
        "epochs_completed": len(epoch_results),
        "median_alignment_score": bh_results["median_alignment"],
        "median_duration_minutes": bh_results["median_duration"],
        "balance_horizon_normalized": bh_results["balance_horizon_normalized"],
        "balance_horizon_raw": bh_results["balance_horizon_raw"],
        "reference_time_used": bh_results["reference_time_used"],
        "theoretical_max_horizon": bh_results["theoretical_max"],
        "validation_status": status,
        "validation_message": message
    }


def main():
    parser = argparse.ArgumentParser(description="Analyze GyroDiagnostics results")
    parser.add_argument(
        "--log-dir",
        type=str,
        default="./logs",
        help="Directory containing evaluation logs"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="./analysis_results.json",
        help="Output file for analysis results"
    )
    
    args = parser.parse_args()
    
    log_dir = Path(args.log_dir)
    
    if not log_dir.exists():
        print(f"Error: Log directory {log_dir} does not exist")
        return
    
    # Find all log files
    log_files = list(log_dir.glob("*.json"))
    
    if not log_files:
        print(f"Error: No log files found in {log_dir}")
        return
    
    print(f"\n{'='*60}")
    print("GyroDiagnostics Results Analysis")
    print(f"{'='*60}")
    print(f"Log directory: {log_dir}")
    print(f"Log files found: {len(log_files)}")
    print(f"{'='*60}\n")
    
    # Analyze each challenge
    results = []
    
    for log_file in log_files:
        print(f"Analyzing: {log_file.name}")
        challenge_results = analyze_challenge_results(log_file)
        results.append(challenge_results)
        
        if "error" not in challenge_results:
            print(f"  Challenge: {challenge_results['challenge']}")
            print(f"  Epochs: {challenge_results['epochs_completed']}")
            print(f"  Median Alignment: {challenge_results['median_alignment_score']:.3f}")
            print(f"  Median Duration: {challenge_results['median_duration_minutes']:.2f} min")
            print(f"  Balance Horizon (normalized): {challenge_results['balance_horizon_normalized']:.4f}")
            print(f"  Balance Horizon (raw): {challenge_results['balance_horizon_raw']:.4f} per-min")
            print(f"  Reference Time: {challenge_results['reference_time_used']:.1f} min")
            print(f"  Status: {challenge_results['validation_status']}")
            print(f"  {challenge_results['validation_message']}")
        else:
            print(f"  Error: {challenge_results['error']}")
        print()
    
    # Save results
    output_path = Path(args.output)
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"{'='*60}")
    print(f"Analysis complete. Results saved to: {output_path}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()