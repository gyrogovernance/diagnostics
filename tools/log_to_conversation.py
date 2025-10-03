#!/usr/bin/env python3
"""
Inspect AI Log to Conversation Extractor

Extract just the conversation history from .eval log files in a clean format.

Usage:
    python tools/log_to_conversation.py path/to/logfile.eval
    python tools/log_to_conversation.py path/to/logfile.eval --output conversation.txt
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime
import re

try:
    from inspect_ai.log import read_eval_log
except ImportError:
    print("ERROR: Inspect AI not installed. Install with: pip install inspect-ai")
    sys.exit(1)


def format_timestamp(timestamp: float) -> str:
    """Format timestamp to readable string."""
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")


def generate_output_path(log_file: Path, custom_output: str = None) -> Path:
    """Generate organized output path in results folder."""
    # Create results directory
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)
    
    # Extract timestamp and task info from log filename
    log_stem = log_file.stem
    timestamp_match = re.search(r'(\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2})', log_stem)
    task_match = re.search(r'(\w+)-challenge', log_stem)
    
    if timestamp_match and task_match:
        timestamp = timestamp_match.group(1).replace('T', '_').replace('-', '')
        task = task_match.group(1)
        base_name = f"{timestamp}_{task}_conversation"
    else:
        # Fallback to current timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = f"{timestamp}_{log_stem}_conversation"
    
    if custom_output:
        return Path(custom_output)
    else:
        return results_dir / f"{base_name}.txt"


def extract_conversation(log_file: str) -> str:
    """Extract conversation history from log file."""
    try:
        log = read_eval_log(log_file)
        output = []
        
        output.append("=" * 80)
        output.append("CONVERSATION HISTORY")
        output.append("=" * 80)
        output.append("")
        
        for i, sample in enumerate(log.samples):
            output.append(f"--- SAMPLE {i+1} (EPOCH {sample.epoch}) ---")
            output.append("")
            
            if hasattr(sample, 'messages') and sample.messages:
                for j, msg in enumerate(sample.messages):
                    role = getattr(msg, 'role', 'unknown').upper()
                    content = getattr(msg, 'content', '')
                    timestamp = getattr(msg, 'timestamp', None)
                    
                    output.append(f"[{role}]")
                    if timestamp:
                        output.append(f"Time: {format_timestamp(timestamp)}")
                    output.append("")
                    output.append(content)
                    output.append("")
            
            output.append("-" * 40)
            output.append("")
        
        return "\n".join(output)
        
    except Exception as e:
        return f"ERROR: Failed to extract conversation: {e}"


def main():
    parser = argparse.ArgumentParser(description="Extract conversation history from Inspect AI evaluation logs")
    parser.add_argument("log_file", help="Path to the .eval log file")
    parser.add_argument("--output", "-o", help="Output file (default: stdout)")
    
    args = parser.parse_args()
    
    # Check if log file exists
    log_path = Path(args.log_file)
    if not log_path.exists():
        print(f"ERROR: Log file not found: {log_path}")
        sys.exit(1)
    
    if not log_path.suffix == '.eval':
        print(f"ERROR: File must be a .eval log file: {log_path}")
        sys.exit(1)
    
    # Generate organized output path
    output_path = generate_output_path(log_path, args.output)
    
    # Extract conversation
    conversation = extract_conversation(str(log_path))
    
    # Write output
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(conversation)
    print(f"Conversation exported to: {output_path}")


if __name__ == "__main__":
    main()
