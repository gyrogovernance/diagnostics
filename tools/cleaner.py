#!/usr/bin/env python3
"""
Clean up logs and results folders - remove old or specific files/directories.

Usage:
    python tools/cleaner.py                    # Remove all log files
    python tools/cleaner.py --results         # Remove all result directories
    python tools/cleaner.py --list             # List all files/directories
    python tools/cleaner.py --older-than 7     # Remove files/dirs older than 7 days
    python tools/cleaner.py --pattern strategic # Remove files/dirs matching pattern
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime, timedelta
import re

def list_files(target_dir="logs"):
    """List all files in the target directory."""
    target_path = Path(target_dir)
    if not target_path.exists():
        print(f"No {target_dir} directory found.")
        return []
    
    if target_dir == "results":
        # For results, list directories
        items = [d for d in target_path.iterdir() if d.is_dir()]
    else:
        # For logs, list files
        items = [f for f in target_path.iterdir() if f.is_file()]
    
    items.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    
    print(f"Found {len(items)} items in {target_dir}:")
    for item in items:
        mtime = datetime.fromtimestamp(item.stat().st_mtime)
        if item.is_dir():
            # Calculate total size of directory
            total_size = sum(f.stat().st_size for f in item.rglob('*') if f.is_file())
            file_count = len(list(item.rglob('*')))
            print(f"  {item.name} ({file_count} files, {total_size:,} bytes, {mtime.strftime('%Y-%m-%d %H:%M:%S')})")
        else:
            size = item.stat().st_size
            print(f"  {item.name} ({size:,} bytes, {mtime.strftime('%Y-%m-%d %H:%M:%S')})")
    
    return items

def cleanup_files(target_dir="logs", older_than_days=None, pattern=None):
    """Clean up files/directories based on criteria."""
    target_path = Path(target_dir)
    if not target_path.exists():
        print(f"No {target_dir} directory found.")
        return
    
    if target_dir == "results":
        # For results, work with directories
        items = [d for d in target_path.iterdir() if d.is_dir()]
    else:
        # For logs, work with files
        items = [f for f in target_path.iterdir() if f.is_file()]
    
    items_to_remove = []
    
    for item in items:
        # Check age filter
        if older_than_days:
            item_age = datetime.now() - datetime.fromtimestamp(item.stat().st_mtime)
            if item_age.days < older_than_days:
                continue
        
        # Check pattern filter
        if pattern:
            if not re.search(pattern, item.name, re.IGNORECASE):
                continue
        
        items_to_remove.append(item)
    
    if not items_to_remove:
        print(f"No items match the cleanup criteria in {target_dir}.")
        return
    
    print(f"Found {len(items_to_remove)} items to remove from {target_dir}:")
    for item in items_to_remove:
        if item.is_dir():
            file_count = len(list(item.rglob('*')))
            total_size = sum(f.stat().st_size for f in item.rglob('*') if f.is_file())
            print(f"  {item.name} ({file_count} files, {total_size:,} bytes)")
        else:
            size = item.stat().st_size
            print(f"  {item.name} ({size:,} bytes)")
    
    # Actually remove items
    removed_count = 0
    for item in items_to_remove:
        try:
            if item.is_dir():
                import shutil
                shutil.rmtree(item)
            else:
                item.unlink()
            removed_count += 1
            print(f"Removed: {item.name}")
        except Exception as e:
            print(f"Error removing {item.name}: {e}")
    
    print(f"\nRemoved {removed_count} items from {target_dir}.")

def main():
    parser = argparse.ArgumentParser(description="Clean up logs and results folders")
    parser.add_argument("--list", action="store_true", help="List all files/directories")
    parser.add_argument("--results", action="store_true", help="Clean up results instead of logs")
    parser.add_argument("--older-than", type=int, help="Remove files/dirs older than N days")
    parser.add_argument("--pattern", help="Remove files/dirs matching pattern (regex)")
    
    args = parser.parse_args()
    
    # Determine target directory
    target_dir = "results" if args.results else "logs"
    
    # Default behavior: clean up logs (unless --list or --results specified)
    if args.list:
        list_files(target_dir)
    else:
        cleanup_files(
            target_dir=target_dir,
            older_than_days=args.older_than,
            pattern=args.pattern
        )

if __name__ == "__main__":
    main()
