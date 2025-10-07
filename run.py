#!/usr/bin/env python3
"""
Convenience wrapper to run GyroDiagnostics evaluation suite.

This is a shortcut for: python tools/run_diagnostics.py
"""

import sys
from pathlib import Path

# Add tools to path
tools_dir = Path(__file__).parent / "tools"
sys.path.insert(0, str(tools_dir))

# Import and run
from run_diagnostics import main

if __name__ == "__main__":
    main()

