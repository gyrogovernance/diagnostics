#!/usr/bin/env python3
"""
Rescore existing evaluation logs with updated analyst models.

This is useful when:
- Analyst models had failures (404 errors, timeouts, etc.)
- You've updated analyst model configuration
- You want to re-run scoring without re-running expensive model generations

Usage:
    python tools/rescore_logs.py
    python tools/rescore_logs.py --log-dir logs
    python tools/rescore_logs.py --overwrite  # replace scores instead of append
"""

import argparse
import sys
import os
import asyncio
from pathlib import Path
from inspect_ai.log import list_eval_logs, read_eval_log, write_eval_log
from inspect_ai._eval.score import score_async

# Import our scorer to register it in Inspect AI's registry
from gyrodiagnostics.scorers.closurer import closurer


def load_env():
    """Load environment variables from .env file"""
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    try:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
                    except ValueError:
                        continue


def main():
    # Load .env first
    load_env()
    parser = argparse.ArgumentParser(
        description="Rescore existing evaluation logs with updated analyst configuration"
    )
    parser.add_argument(
        "--log-dir",
        type=str,
        default="./logs",
        help="Directory containing .eval files to rescore (default: ./logs)"
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing scores instead of appending"
    )
    parser.add_argument(
        "--pattern",
        type=str,
        help="Only rescore logs matching this pattern (e.g., 'formal', 'procedural')"
    )
    parser.add_argument(
        "--limit",
        type=int,
        help="Limit to first N logs (for testing)"
    )
    
    args = parser.parse_args()
    
    log_dir = Path(args.log_dir)
    if not log_dir.exists():
        print(f"[ERROR] Log directory not found: {log_dir}")
        return 1
    
    # List all eval logs
    try:
        logs = list_eval_logs(str(log_dir))
    except Exception as e:
        print(f"[ERROR] Failed to list logs: {e}")
        return 1
    
    if not logs:
        print(f"[ERROR] No evaluation logs found in: {log_dir}")
        return 1
    
    # Filter by pattern if specified
    if args.pattern:
        logs = [log for log in logs if args.pattern.lower() in log.name.lower()]
        print(f"Found {len(logs)} logs matching pattern '{args.pattern}'")
    else:
        print(f"Found {len(logs)} evaluation logs")
    
    # Limit number of logs if specified
    if args.limit and args.limit > 0:
        logs = logs[:args.limit]
        print(f"Limited to first {len(logs)} logs")
    
    if not logs:
        print("[ERROR] No logs match the specified criteria")
        return 1
    
    # Rescore each log
    action = "overwrite" if args.overwrite else "append"
    print(f"\nRescoring mode: {action}")
    print("=" * 60)
    
    success_count = 0
    error_count = 0
    
    async def rescore_all():
        nonlocal success_count, error_count
        
        for log_info in logs:
            # list_eval_logs returns EvalLogInfo objects with 'name' attribute
            name = log_info.name
            if "://" in name:
                log_path_str = name
            else:
                log_path_str = str(log_dir / name)
            
            print(f"\nProcessing: {name}", flush=True)
            
            try:
                # Read the log
                print(f"  Reading log...", flush=True)
                log = read_eval_log(log_path_str)
                num_samples = len(log.samples) if hasattr(log, 'samples') else 0
                print(f"  Found {num_samples} samples (epochs)", flush=True)
                
                # Check which samples need rescoring
                samples_to_rescore = []
                for idx, sample in enumerate(log.samples):
                    # Check if this sample has complete analyst coverage
                    needs_rescore = False
                    
                    if not sample.scores or not sample.scores.get('closurer'):
                        needs_rescore = True
                        reason = "no scores"
                    else:
                        score_obj = sample.scores['closurer']
                        metadata = score_obj.metadata if hasattr(score_obj, 'metadata') else {}
                        
                        # Check analyst coverage in metadata
                        per_analyst = metadata.get('per_analyst', [])
                        if not per_analyst:
                            needs_rescore = True
                            reason = "no analyst data"
                        else:
                            # Count successful analysts from the list
                            successful = sum(1 for analyst in per_analyst if analyst.get('success', False))
                            total_analysts = len(per_analyst)
                            
                            if successful < 2:
                                needs_rescore = True
                                reason = f"only {successful}/{total_analysts} analysts succeeded"
                            else:
                                reason = f"complete ({successful}/{total_analysts} analysts)"
                    
                    if needs_rescore:
                        samples_to_rescore.append(idx)
                        print(f"    Epoch {idx+1}: {reason} - will rescore", flush=True)
                    else:
                        print(f"    Epoch {idx+1}: {reason} - skip", flush=True)
                
                if not samples_to_rescore:
                    print(f"  [SKIP] All epochs have complete analyst coverage", flush=True)
                    success_count += 1
                    continue
                
                print(f"  Rescoring {len(samples_to_rescore)} of {num_samples} epochs...", flush=True)
                
                # Create a modified log with only samples that need rescoring
                from copy import deepcopy
                partial_log = deepcopy(log)
                partial_log.samples = [log.samples[i] for i in samples_to_rescore]
                
                # Rescore using the Python API
                scorers = [closurer()]
                timeout = len(samples_to_rescore) * 300  # 5 min per sample
                print(f"  (timeout: {timeout}s)", flush=True)
                
                try:
                    rescored_partial = await asyncio.wait_for(
                        score_async(partial_log, scorers=scorers, action="overwrite", display="none"),
                        timeout=timeout
                    )
                except asyncio.TimeoutError:
                    print(f"  [TIMEOUT] Rescoring took longer than {timeout}s", flush=True)
                    error_count += 1
                    continue
                
                # Merge rescored samples back into original log
                for original_idx, rescored_sample in zip(samples_to_rescore, rescored_partial.samples):
                    log.samples[original_idx] = rescored_sample
                
                # Write back
                print(f"  Writing updated log...", flush=True)
                write_eval_log(log, log_path_str)
                
                print(f"  [OK] Success - {len(samples_to_rescore)} epochs rescored", flush=True)
                success_count += 1
                    
            except Exception as e:
                print(f"  [FAIL] Error: {e}")
                import traceback
                traceback.print_exc()
                error_count += 1
    
    # Run async rescoring
    asyncio.run(rescore_all())
    
    # Summary
    print("\n" + "=" * 60)
    print("Rescoring Complete")
    print("=" * 60)
    print(f"Success: {success_count}/{len(logs)}")
    print(f"Errors:  {error_count}/{len(logs)}")
    
    if success_count > 0:
        print("\nRun analysis to see updated results:")
        print("  python tools/analyzer.py --eval-dir logs")
    
    return 0 if error_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

