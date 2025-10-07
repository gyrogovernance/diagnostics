#!/usr/bin/env python3
"""
Test if configured models and analysts are accessible.

Usage:
    python tools/test_models.py
"""

import os
import sys
import asyncio
from pathlib import Path


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


async def test_model(model_name: str, role: str = None):
    """Test if a model is accessible"""
    from inspect_ai.model import get_model, ChatMessageUser
    
    print(f"\nTesting: {model_name}")
    if role:
        print(f"  Role: {role}")
    
    try:
        # Get the model
        if role:
            model = get_model(role=role)
        else:
            model = get_model(model_name)
        
        print(f"  Loading model... OK")
        
        # Try a simple generation
        print(f"  Calling API with simple test...")
        messages = [ChatMessageUser(content="Say 'hello' (one word only)")]
        
        response = await asyncio.wait_for(
            model.generate(messages),
            timeout=120  # Longer for thinking models like gemini-2.5-pro
        )
        
        output = response.completion if hasattr(response, 'completion') else str(response)
        print(f"  Response: {output[:50]}...")
        print(f"  [SUCCESS] Model works!")
        return True
        
    except asyncio.TimeoutError:
        print(f"  [TIMEOUT] Model took longer than 30s")
        return False
    except Exception as e:
        error_msg = str(e)
        print(f"  [FAIL] Error: {error_msg[:200]}")
        
        # Give helpful hints
        if "404" in error_msg or "not found" in error_msg.lower():
            print(f"  Hint: Model path may not exist on OpenRouter")
        elif "api key" in error_msg.lower() or "auth" in error_msg.lower():
            print(f"  Hint: Check OPENROUTER_API_KEY in .env")
        elif "rate" in error_msg.lower() or "quota" in error_msg.lower():
            print(f"  Hint: Rate limited - try again later")
        
        return False


async def main():
    # Load .env
    load_env()
    
    print("="*60)
    print("MODEL CONFIGURATION TEST")
    print("="*60)
    
    # Check API key
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("[ERROR] OPENROUTER_API_KEY not found in environment")
        return 1
    print(f"API Key: ...{api_key[-8:] if len(api_key) > 8 else '***'}")
    
    # Get configured models
    primary_model = os.getenv("INSPECT_EVAL_MODEL")
    analyst_a = os.getenv("INSPECT_EVAL_MODEL_GRADER_A")
    analyst_b = os.getenv("INSPECT_EVAL_MODEL_GRADER_B")
    backup_analyst = os.getenv("INSPECT_EVAL_MODEL_GRADER_BACKUP")
    
    results = {}
    
    # Test primary model
    if primary_model:
        print("\n" + "="*60)
        print("PRIMARY MODEL (being evaluated)")
        print("="*60)
        results['primary'] = await test_model(primary_model)
    else:
        print("\n[WARNING] INSPECT_EVAL_MODEL not set")
        results['primary'] = False
    
    # Test analysts
    print("\n" + "="*60)
    print("ANALYST MODELS (ensemble scoring)")
    print("="*60)
    
    if analyst_a:
        results['analyst_a'] = await test_model(analyst_a, role="analyst_a")
    else:
        print("\nanalyst_a: not configured")
        results['analyst_a'] = None
    
    if analyst_b:
        results['analyst_b'] = await test_model(analyst_b, role="analyst_b")
    else:
        print("\nanalyst_b: not configured")
        results['analyst_b'] = None
    
    # Test backup analyst
    if backup_analyst:
        print("\n" + "="*60)
        print("BACKUP ANALYST")
        print("="*60)
        results['backup'] = await test_model(backup_analyst, role="analyst_backup")
    else:
        print("\n[INFO] No backup analyst configured")
        results['backup'] = None
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    working = [k for k, v in results.items() if v is True]
    failing = [k for k, v in results.items() if v is False]
    not_configured = [k for k, v in results.items() if v is None]
    
    print(f"\nWorking models: {len(working)}")
    for m in working:
        print(f"  - {m}")
    
    if failing:
        print(f"\nFailing models: {len(failing)}")
        for m in failing:
            print(f"  - {m}")
    
    if not_configured:
        print(f"\nNot configured: {len(not_configured)}")
        for m in not_configured:
            print(f"  - {m}")
    
    # Check if we have enough working analysts (need 2 for tetrahedral structure)
    analyst_count = sum(1 for k in ['analyst_a', 'analyst_b'] if results.get(k) is True)
    required_analysts = 2
    print(f"\nWorking analysts: {analyst_count} (need {required_analysts} for tetrahedral structure)")
    
    if analyst_count == 0:
        print("[ERROR] No working analysts! Evaluations will fail.")
        return 1
    elif analyst_count == 1:
        print("[WARNING] Only 1 analyst working. Need 2 for proper ensemble evaluation.")
        print("          Backup analyst will be used to reach minimum of 2.")
    elif analyst_count >= 2:
        print("[OK] Sufficient analysts working - ensemble scoring will work!")
    
    if not results.get('primary'):
        print("[ERROR] Primary model not working! Cannot run evaluations.")
        return 1
    
    print("\n" + "="*60)
    if results['primary'] and analyst_count >= 1:
        print("[OK] Ready to run evaluations!")
        return 0
    else:
        print("[FAIL] Fix failing models before running evaluations")
        return 1


if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n[Interrupted]")
        sys.exit(1)
    except Exception as e:
        print(f"\n[FATAL ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

