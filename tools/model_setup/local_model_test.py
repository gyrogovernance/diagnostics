"""
Local Model Testing for Gyroscope Diagnostics

This script tests the Gyroscope pipeline using a local Qwen3 model
for fast iteration and development.

Optimized for CPU with 32GB RAM.
"""

import os
import warnings
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import asyncio
import json

# Suppress deprecation warnings
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', message='.*torch_dtype.*')

# For memory monitoring
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False


class LocalQwen3Solver:
    """Local solver using Qwen3-1.7B-Base for testing."""
    
    def __init__(self, model_name: str = "Qwen/Qwen3-1.7B-Base", use_gyroscope: bool = True):
        self.model_name = model_name
        self.use_gyroscope = use_gyroscope
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # AGGRESSIVE CPU optimization for 32GB RAM system
        if self.device == "cpu":
            try:
                torch.backends.mkldnn.enabled = True
            except:
                pass
        
        print(f"Loading {model_name}...")
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            trust_remote_code=True
        )
        
        # Use 'dtype' instead of deprecated 'torch_dtype'
        # Load with aggressive caching - use that RAM!
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float32,  # float32 for CPU
            device_map=None,
            trust_remote_code=True,
            low_cpu_mem_usage=False  # Use MORE memory for speed!
        )
        
        if self.device == "cpu":
            self.model = self.model.to(self.device)
            self.model.eval()
            
            # Try to compile the model for faster inference (PyTorch 2.0+)
            try:
                self.model = torch.compile(self.model, mode="reduce-overhead")
                print("Model compiled and loaded")
            except:
                print("Model loaded")
            
            # Show actual memory usage
            if PSUTIL_AVAILABLE:
                process = psutil.Process()
                mem_gb = process.memory_info().rss / (1024**3)
                print(f"RAM usage: {mem_gb:.1f}GB")
        else:
            print("Model loaded")

    def generate_response(self, prompt: str, max_length: int = 150) -> str:
        """Generate a response using the local model.
        
        AGGRESSIVELY optimized for 32GB RAM - uses memory for speed!
        """
        import time
        
        # Tokenize input with padding for better batching
        inputs = self.tokenizer(
            prompt, 
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=2048
        ).to(self.device)
        
        print(f"  Generating (max {max_length} tokens)...", end="", flush=True)
        start_time = time.time()
        
        # Generate response with AGGRESSIVE memory usage for speed
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_length,
                do_sample=False,  # Greedy is faster on CPU
                pad_token_id=self.tokenizer.eos_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
                num_beams=1,
                use_cache=True,  # Use KV cache (takes memory but faster!)
                repetition_penalty=1.1
            )
        
        elapsed = time.time() - start_time
        tokens_generated = outputs[0].size(0) - inputs['input_ids'].size(1)
        tok_per_sec = tokens_generated/elapsed if elapsed > 0 else 0
        print(f" {tokens_generated} tokens in {elapsed:.1f}s ({tok_per_sec:.1f} tok/s)")
        
        # Decode response
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Remove input prompt from response
        if prompt in response:
            response = response.replace(prompt, "").strip()
            
        return response

    async def solve(self, state, generate_func):
        """Execute the Gyroscope conversation pattern using local model."""
        
        challenge = state.input
        conversation = []

        print(f"\nStarting 6-turn conversation...")
        
        for turn in range(6):
            if turn % 2 == 0:
                # Generative mode (even turns)
                mode = "Generative"
                prompt_suffix = self._get_generative_prompt()
            else:
                # Integrative mode (odd turns)
                mode = "Integrative"
                prompt_suffix = self._get_integrative_prompt()

            print(f"Turn {turn + 1}/6 ({mode})")
            
            # Build full prompt
            if self.use_gyroscope:
                full_prompt = f"{challenge}\n\n{prompt_suffix}"
            else:
                # Freestyle - no structured prompt
                full_prompt = challenge

            # Generate response using local model
            response = self.generate_response(full_prompt)

            # Add trace block for Gyroscope responses
            if self.use_gyroscope:
                trace_block = self._generate_trace_block(mode, turn // 2 + 1)
                response = f"{response}\n\n{trace_block}"

            conversation.append({
                "turn": turn + 1,
                "mode": mode,
                "response": response
            })

            # Update challenge for next turn (continuity cue)
            challenge = "✓"  # Minimal continuity cue

        # Store conversation in state for scoring
        state.conversation = conversation
        print(f"\nCompleted 6 turns")
        return state

    def _get_generative_prompt(self) -> str:
        """Get the prompt suffix for Generative mode."""
        return """
Apply the Gyroscope Protocol v0.7 Beta:

**Reasoning States** (in order):
@ Traceability: Ground reasoning in Purpose, Logic, and context
& Variety: Introduce diverse, non-convergent perspectives
% Accountability: Surface tensions or gaps transparently
~ Integrity: Synthesize into coherent, recursive response

**Current Mode**: Generative (forward reasoning)
**Recursive Memory**: Reference the last 3 messages for context integrity

Structure your response with explicit reasoning states and provide a comprehensive answer.
"""

    def _get_integrative_prompt(self) -> str:
        """Get the prompt suffix for Integrative mode."""
        return """
Apply the Gyroscope Protocol v0.7 Beta:

**Reasoning States** (in order):
~ Integrity: Synthesize elements recursively
% Accountability: Identify tensions transparently
& Variety: Consider diverse perspectives
@ Traceability: Ground in context and purpose

**Current Mode**: Integrative (reflective reasoning)
**Recursive Memory**: Reference the last 3 messages for context integrity

Structure your response with explicit reasoning states and provide a comprehensive reflection.
"""

    def _generate_trace_block(self, mode: str, cycle: int) -> str:
        """Generate a Gyroscope trace block for auditability."""
        import datetime

        return f"""
[Gyroscope - Start]
[v0.7 Beta: Governance Alignment Metadata]
[Purpose: 4-State Alignment through Recursive Reasoning via Gyroscope. Order matters. Context continuity is preserved across the last 3 messages.]
[States {{Format: Symbol = How (Why)}}:
@ = Governance Traceability (Common Source),
& = Information Variety (Unity Non-Absolute),
% = Inference Accountability (Opposition Non-Absolute),
~ = Intelligence Integrity (Balance Universal)]
[Modes {{Format: Type = Path}}:
Generative (Gen) = @ → & → % → ~,
Integrative (Int) = ~ → % → & → @,
Current (Gen/Int) = {mode[:3]}]
[Data: Timestamp = {datetime.datetime.now().isoformat()}, Mode = {mode[:3]}, Alignment (Y/N) = Y, ID = {cycle:03d}]
[Gyroscope - End]
"""


async def test_quick():
    """Quick smoke test with minimal tokens for fast iteration."""
    print("Quick Test")
    print("=" * 60)
    
    solver = LocalQwen3Solver(use_gyroscope=True)
    
    test_prompt = "What is 2+2?"
    print(f"\nPrompt: {test_prompt}")
    response = solver.generate_response(test_prompt, max_length=20)
    print(f"Response: {response}")
    print("\nTest completed")


async def test_single_challenge():
    """Test a single turn to verify the pipeline works."""
    
    print("Single Turn Test")
    print("=" * 60)
    
    challenge = "What is recursive reasoning?"
    print(f"Challenge: {challenge}\n")
    
    solver = LocalQwen3Solver(use_gyroscope=True)
    
    # Just test ONE turn to verify it works
    response = solver.generate_response(challenge, max_length=50)
    print(f"\nResponse: {response}")
    
    print("\nTest completed")

if __name__ == "__main__":
    import sys
    
    print("Gyroscope Local Model Test")
    print("=" * 60)
    
    # Set CPU optimizations FIRST
    if not torch.cuda.is_available():
        torch.set_num_threads(12)
        torch.set_num_interop_threads(6)
        os.environ['OMP_NUM_THREADS'] = '12'
        os.environ['MKL_NUM_THREADS'] = '12'
    
    # System information
    if torch.cuda.is_available():
        print(f"Device: GPU ({torch.cuda.get_device_name(0)})")
    else:
        print(f"Device: CPU ({torch.get_num_threads()} threads)")
    
    print()
    
    # Check for command line argument
    test_mode = sys.argv[1] if len(sys.argv) > 1 else "single"
    
    if test_mode == "quick":
        asyncio.run(test_quick())
    else:
        asyncio.run(test_single_challenge())
