#!/usr/bin/env python3
"""
Clean up results folder - remove old or specific result files.

Usage:
    python tools/cleanup_results.py                    # List all results
    python tools/cleanup_results.py --cleanup          # Remove all results
    python tools/cleanup_results.py --older-than 7     # Remove files older than 7 days
    python tools/cleanup_results.py --pattern strategic # Remove files matching pattern
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime, timedelta
import re

def list_results():
    """List all result files in the results directory."""
    results_dir = Path("results")
    if not results_dir.exists():
        print("No results directory found.")
        return []
    
    files = list(results_dir.glob("*"))
    files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    
    print(f"Found {len(files)} result files:")
    for file in files:
        if file.is_file():
            mtime = datetime.fromtimestamp(file.stat().st_mtime)
            size = file.stat().st_size
            print(f"  {file.name} ({size:,} bytes, {mtime.strftime('%Y-%m-%d %H:%M:%S')})")
    
    return files

def cleanup_results(older_than_days=None, pattern=None, dry_run=True):
    """Clean up result files based on criteria."""
    results_dir = Path("results")
    if not results_dir.exists():
        print("No results directory found.")
        return
    
    files = list(results_dir.glob("*"))
    files_to_remove = []
    
    for file in files:
        if not file.is_file():
            continue
            
        # Check age filter
        if older_than_days:
            file_age = datetime.now() - datetime.fromtimestamp(file.stat().st_mtime)
            if file_age.days < older_than_days:
                continue
        
        # Check pattern filter
        if pattern:
            if not re.search(pattern, file.name, re.IGNORECASE):
                continue
        
        files_to_remove.append(file)
    
    if not files_to_remove:
        print("No files match the cleanup criteria.")
        return
    
    print(f"Found {len(files_to_remove)} files to remove:")
    for file in files_to_remove:
        print(f"  {file.name}")
    
    if dry_run:
        print("\n[DRY RUN] Use --confirm to actually remove files.")
        return
    
    # Actually remove files
    removed_count = 0
    for file in files_to_remove:
        try:
            file.unlink()
            removed_count += 1
            print(f"Removed: {file.name}")
        except Exception as e:
            print(f"Error removing {file.name}: {e}")
    
    print(f"\nRemoved {removed_count} files.")

def main():
    parser = argparse.ArgumentParser(description="Clean up results folder")
    parser.add_argument("--cleanup", action="store_true", help="Remove all result files")
    parser.add_argument("--older-than", type=int, help="Remove files older than N days")
    parser.add_argument("--pattern", help="Remove files matching pattern (regex)")
    parser.add_argument("--confirm", action="store_true", help="Actually remove files (default is dry run)")
    parser.add_argument("--list", action="store_true", help="List all result files")
    
    args = parser.parse_args()
    
    if args.list or not any([args.cleanup, args.older_than, args.pattern]):
        list_results()
    else:
        cleanup_results(
            older_than_days=args.older_than,
            pattern=args.pattern,
            dry_run=not args.confirm
        )

if __name__ == "__main__":
    main()
