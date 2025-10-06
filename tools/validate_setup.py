"""
Setup validation script for GyroDiagnostics.
Run this after installation to verify everything is configured correctly.
"""

import sys
from pathlib import Path

def check_package_installed():
    """Check if gyrodiagnostics is installed."""
    try:
        import gyrodiagnostics
        print("[OK] gyrodiagnostics package is installed")
        return True
    except ImportError:
        print("[FAIL] gyrodiagnostics package not found")
        print("       Run: pip install -e .")
        return False

def check_dependencies():
    """Check if required dependencies are installed."""
    missing = []
    
    try:
        import inspect_ai
        from packaging import version
        if version.parse(inspect_ai.__version__) < version.parse("0.3.135"):
            print(f"[FAIL] inspect-ai {inspect_ai.__version__} is too old; need >= 0.3.135")
            missing.append("inspect-ai (version too old)")
        else:
            print(f"[OK] inspect-ai version {inspect_ai.__version__}")
    except ImportError:
        missing.append("inspect-ai")
    except Exception as e:
        print(f"[WARN] Could not check inspect-ai version: {e}")
        print("[OK] inspect-ai installed")
    
    try:
        import transformers
        print("[OK] transformers installed (for local models)")
    except ImportError:
        print("[WARN] transformers not installed (needed for local models)")
    
    try:
        import torch
        print("[OK] torch installed")
    except ImportError:
        print("[WARN] torch not installed (needed for local models)")
    
    if missing:
        print(f"[FAIL] Missing required packages: {', '.join(missing)}")
        print("       Run: pip install -r requirements.txt")
        return False
    
    return True

def check_env_file():
    """Check if .env file exists and has required variables."""
    env_path = Path(".env")
    
    if not env_path.exists():
        print("[WARN] .env file not found")
        print("       Create .env file with model configuration")
        print("       See README.md for examples")
        return False
    
    content = env_path.read_text()
    
    has_model = "INSPECT_EVAL_MODEL" in content
    has_analyst = "INSPECT_EVAL_MODEL_GRADER" in content
    
    if has_model:
        print("[OK] .env file exists with INSPECT_EVAL_MODEL")
    else:
        print("[WARN] .env file missing INSPECT_EVAL_MODEL")
    
    if has_analyst:
        print("[OK] .env file has INSPECT_EVAL_MODEL_GRADER")
    else:
        print("[WARN] .env file missing INSPECT_EVAL_MODEL_GRADER (will use default)")
    
    return has_model

def check_tasks():
    """Check if tasks can be imported."""
    try:
        from gyrodiagnostics.tasks.challenge_1_formal import formal_challenge
        from gyrodiagnostics.tasks.challenge_2_normative import normative_challenge
        from gyrodiagnostics.tasks.challenge_3_procedural import procedural_challenge
        from gyrodiagnostics.tasks.challenge_4_strategic import strategic_challenge
        from gyrodiagnostics.tasks.challenge_5_epistemic import epistemic_challenge
        
        print("[OK] All 5 challenge tasks can be imported")
        return True
    except Exception as e:
        print(f"[FAIL] Task import failed: {e}")
        return False

def check_logs_dir():
    """Check if logs directory exists or can be created."""
    logs_path = Path("logs")
    
    if logs_path.exists():
        print(f"[OK] Logs directory exists: {logs_path.absolute()}")
    else:
        try:
            logs_path.mkdir(parents=True, exist_ok=True)
            print(f"[OK] Created logs directory: {logs_path.absolute()}")
        except Exception as e:
            print(f"[WARN] Could not create logs directory: {e}")
            return False
    
    return True

def main():
    print("=" * 70)
    print("GyroDiagnostics Setup Validation")
    print("=" * 70)
    print()
    
    checks = [
        ("Package Installation", check_package_installed),
        ("Dependencies", check_dependencies),
        ("Environment File", check_env_file),
        ("Task Imports", check_tasks),
        ("Logs Directory", check_logs_dir),
    ]
    
    all_passed = True
    for name, check_func in checks:
        print(f"\n{name}:")
        print("-" * 70)
        passed = check_func()
        all_passed = all_passed and passed
    
    print()
    print("=" * 70)
    
    if all_passed:
        print("[PASS] Setup validation complete!")
        print()
        print("Next steps:")
        print("  1. Verify .env file has correct model configuration")
        print("  2. Test with: inspect eval src/gyrodiagnostics/tasks/challenge_1_formal.py --limit 1")
        print("  3. Check logs directory for results")
    else:
        print("[FAIL] Setup validation found issues")
        print()
        print("Please fix the issues above before running evaluations.")
        print("See README.md for detailed setup instructions.")
    
    print("=" * 70)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())

