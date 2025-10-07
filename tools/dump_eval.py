#!/usr/bin/env python3
"""
Simple tool to dump .eval file contents as readable JSON or text.

Usage:
    python tools/dump_eval.py logs/some_file.eval
    python tools/dump_eval.py logs/some_file.eval --json output.json
"""

import argparse
import json
import sys
from pathlib import Path
from inspect_ai.log import read_eval_log


def main():
    parser = argparse.ArgumentParser(description="Dump .eval file contents")
    parser.add_argument("eval_file", help="Path to .eval file")
    parser.add_argument("--json", help="Output as JSON to this file")
    parser.add_argument("--summary", action="store_true", help="Just show summary")
    
    args = parser.parse_args()
    
    eval_file = Path(args.eval_file)
    if not eval_file.exists():
        print(f"ERROR: File not found: {eval_file}")
        return 1
    
    print(f"Reading: {eval_file.name}")
    log = read_eval_log(str(eval_file))
    
    if args.summary:
        # Print summary
        print(f"\n{'='*60}")
        print(f"Task: {log.eval.task}")
        print(f"Model: {log.eval.model}")
        print(f"Samples: {len(log.samples)}")
        print(f"Status: {log.status}")
        print(f"{'='*60}\n")
        
        for idx, sample in enumerate(log.samples):
            print(f"Sample {idx+1}:")
            print(f"  ID: {sample.id}")
            if sample.scores:
                for scorer_name, score in sample.scores.items():
                    print(f"  {scorer_name}: {score.value}")
                    if hasattr(score, 'metadata'):
                        per_analyst = score.metadata.get('per_analyst', [])
                        if per_analyst:
                            successful = sum(1 for a in per_analyst if a.get('success'))
                            print(f"    Analysts: {successful}/{len(per_analyst)} succeeded")
            print()
    else:
        # Dump to JSON
        log_dict = log.model_dump() if hasattr(log, 'model_dump') else log.dict()
        
        if args.json:
            with open(args.json, 'w', encoding='utf-8') as f:
                json.dump(log_dict, f, indent=2, ensure_ascii=False, default=str)
            print(f"Written to: {args.json}")
        else:
            # Print to stdout
            print(json.dumps(log_dict, indent=2, ensure_ascii=False, default=str))
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

