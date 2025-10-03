#!/usr/bin/env python3
"""
Add evaluation results to the showcase folder for easy viewing.

Usage:
    python tools/add_to_showcase.py path/to/evaluation.eval --model gpt-4o --challenge strategic
    python tools/add_to_showcase.py path/to/evaluation.eval --model claude-3.5-sonnet --challenge formal --description "Custom description"
"""

import argparse
import os
import shutil
from pathlib import Path
from datetime import datetime
from log_to_text import extract_evaluation_data, format_as_markdown


def main():
    parser = argparse.ArgumentParser(description="Add evaluation results to showcase")
    parser.add_argument(
        "log_file",
        type=str,
        help="Path to the .eval log file"
    )
    parser.add_argument(
        "--model",
        type=str,
        required=True,
        help="Model name (e.g., gpt-4o, claude-3.5-sonnet)"
    )
    parser.add_argument(
        "--challenge",
        type=str,
        required=True,
        choices=["formal", "normative", "procedural", "strategic", "epistemic"],
        help="Challenge type"
    )
    parser.add_argument(
        "--description",
        type=str,
        help="Custom description for the results"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="showcase",
        help="Output directory (default: showcase)"
    )
    
    args = parser.parse_args()
    
    # Validate input file
    if not os.path.exists(args.log_file):
        print(f"Error: Log file '{args.log_file}' not found")
        return 1
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Generate filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_clean = args.model.lower().replace("-", "_").replace(".", "")
    filename = f"{args.challenge}_challenge_{model_clean}.md"
    filepath = os.path.join(args.output_dir, filename)
    
    print(f"Processing evaluation: {args.log_file}")
    print(f"Model: {args.model}")
    print(f"Challenge: {args.challenge}")
    print(f"Output: {filepath}")
    
    try:
        # Extract evaluation data
        print("Extracting evaluation data...")
        eval_data = extract_evaluation_data(args.log_file)
        
        if not eval_data:
            print("Error: Could not extract evaluation data")
            return 1
        
        # Format as markdown
        print("Formatting as markdown...")
        markdown_content = format_as_markdown(
            eval_data,
            model_name=args.model,
            challenge_name=args.challenge,
            custom_description=args.description
        )
        
        # Write to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"✅ Successfully created showcase file: {filepath}")
        
        # Also copy conversation file if it exists
        conversation_file = filepath.replace(".md", "_conversation.txt")
        if os.path.exists(conversation_file):
            shutil.copy2(conversation_file, os.path.join(args.output_dir, f"{args.challenge}_challenge_{model_clean}_conversation.txt"))
            print(f"✅ Also copied conversation file")
        
        # Update summary if it exists
        summary_file = os.path.join(args.output_dir, "summary.md")
        if os.path.exists(summary_file):
            print(f"ℹ️  Don't forget to update {summary_file} with the new results")
        
        print(f"\n🎉 Results added to showcase!")
        print(f"   - Main results: {filename}")
        print(f"   - Conversation: {args.challenge}_challenge_{model_clean}_conversation.txt")
        print(f"   - Update summary.md to include these results")
        
        return 0
        
    except Exception as e:
        print(f"Error processing evaluation: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
