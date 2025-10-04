"""
Autonomous solver implementing configurable multi-turn progression with minimal continuation cues.

Production-ready version with:
- Immediate retry logic for transient API failures
- Graceful error handling (never fails the epoch)
- Comprehensive error logging for debugging
- Optional per-turn timeout warnings
"""

import os
import time
import asyncio
from inspect_ai.solver import solver, Solver, TaskState, Generate
from inspect_ai.model import ChatMessageUser
from ..utils.constants import CONTINUATION_PROMPT, TASK_CONFIG


@solver
def autonomous_solver() -> Solver:
    """
    Autonomous progression solver for multi-turn evaluation.
    
    Executes configurable number of turns with robust error handling:
    - Turn 1: Initial response to challenge prompt
    - Turns 2-N: Continuation with minimal cue ("continue")
    
    Features:
    - Immediate retries for transient failures (JSON decode errors, network timeouts)
    - Graceful degradation on errors (logs to state.scratch, continues epoch)
    - Early termination on empty responses
    - Optional per-turn timeout warnings (doesn't fail, just logs)
    
    This structure tests sustained coherence without external guidance.
    """
    async def solve(state: TaskState, generate: Generate) -> TaskState:
        # Import error classes with fallbacks
        try:
            from json import JSONDecodeError
        except ImportError:
            JSONDecodeError = Exception  # Fallback for older Python
        
        # Configuration
        num_turns = TASK_CONFIG.get("turns", 6)
        max_retries = max(1, int(TASK_CONFIG.get("retry_on_error", 3)))
        per_turn_timeout = int(os.getenv("INSPECT_PER_TURN_TIMEOUT_S", "0"))  # 0 = disabled
        
        # Initialize error tracking
        if not hasattr(state, "scratch"):
            state.scratch = {}
        state.scratch.setdefault("errors", [])
        state.scratch.setdefault("turn_metadata", [])
        state.scratch.setdefault("epoch_timing", {})
        
        epoch_start = time.time()
        
        async def generate_with_retries(current_state: TaskState, turn_num: int) -> TaskState:
            """
            Call generate() with defensive retries for transient failures.
            
            Retries on:
            - JSON decode errors (common with some providers)
            - Network timeouts/connection errors
            
            Does NOT retry on:
            - Rate limit errors (re-raises immediately)
            - Validation errors (non-transient)
            
            Args:
                current_state: Current task state
                turn_num: Turn number (for error logging)
            
            Returns:
                Updated state (or original state on total failure)
            """
            base_delay = 0.75
            last_error = None
            
            for attempt in range(1, max_retries + 1):
                try:
                    # Optional timeout wrapper (warns but doesn't fail)
                    if per_turn_timeout > 0:
                        try:
                            result = await asyncio.wait_for(
                                generate(current_state),
                                timeout=per_turn_timeout
                            )
                            return result
                        except asyncio.TimeoutError:
                            # Log warning but don't fail - let it complete
                            warning = f"Turn {turn_num} exceeded {per_turn_timeout}s timeout (attempt {attempt})"
                            print(f"WARNING: {warning}")
                            current_state.scratch["errors"].append({
                                "turn": turn_num,
                                "type": "timeout_warning",
                                "message": warning,
                                "attempt": attempt
                            })
                            # Try again without timeout
                            return await generate(current_state)
                    else:
                        # No timeout - just generate
                        return await generate(current_state)
                
                except JSONDecodeError as ex:
                    last_error = ex
                    error_type = "json_decode_error"
                
                except Exception as ex:
                    # Check if transient
                    ex_type = str(type(ex).__name__)
                    transient_patterns = [
                        "JSONDecodeError",
                        "ReadTimeout",
                        "WriteError",
                        "RemoteProtocolError",
                        "ConnectionResetError",
                        "ServerDisconnectedError",
                        "ConnectTimeout",
                        "HTTPStatusError"  # Some HTTP errors are transient
                    ]
                    
                    is_transient = any(pattern in ex_type or pattern in str(ex) 
                                      for pattern in transient_patterns)
                    
                    # Rate limits and auth errors should not retry
                    if "rate" in str(ex).lower() or "quota" in str(ex).lower():
                        is_transient = False
                    if "auth" in str(ex).lower() or "api key" in str(ex).lower():
                        is_transient = False
                    
                    if not is_transient:
                        # Non-transient error - log and re-raise
                        current_state.scratch["errors"].append({
                            "turn": turn_num,
                            "type": "non_transient_error",
                            "message": str(ex),
                            "exception_type": ex_type
                        })
                        raise
                    
                    last_error = ex
                    error_type = ex_type
                
                # Log retry attempt
                current_state.scratch["errors"].append({
                    "turn": turn_num,
                    "type": error_type,
                    "message": str(last_error)[:500],  # Truncate long errors
                    "attempt": attempt,
                    "retry": attempt < max_retries
                })
                
                if attempt < max_retries:
                    # Exponential backoff with jitter
                    delay = base_delay * (2 ** (attempt - 1)) + (0.15 * attempt)
                    print(f"Turn {turn_num} failed (attempt {attempt}/{max_retries}), retrying in {delay:.1f}s...")
                    await asyncio.sleep(delay)
            
            # Exhausted all retries - log critical error but continue epoch
            critical_error = {
                "turn": turn_num,
                "type": "generation_failed",
                "message": f"Failed after {max_retries} attempts: {str(last_error)[:500]}",
                "critical": True
            }
            current_state.scratch["errors"].append(critical_error)
            print(f"CRITICAL: Turn {turn_num} failed after {max_retries} retries. Continuing with partial state.")
            
            # Return state as-is to allow epoch to continue
            return current_state
        
        # Turn 1: Initial generation
        state = await generate_with_retries(state, 1)
        _record_turn_time(state, 1)
        
        # Turns 2-N: Continuation
        for turn_number in range(2, num_turns + 1):
            # Add continuation prompt
            state.messages.append(ChatMessageUser(content=CONTINUATION_PROMPT))
            
            # Generate with retries
            state = await generate_with_retries(state, turn_number)
            _record_turn_time(state, turn_number)
            
            # Early termination check: empty assistant response
            last_msg = state.messages[-1] if state.messages else None
            if getattr(last_msg, "role", None) == "assistant":
                content = getattr(last_msg, "content", "")
                # Handle both string and list content
                if isinstance(content, list):
                    content = " ".join(str(item) for item in content)
                content_str = str(content).strip()
                
                if not content_str:
                    # Empty response - log and stop
                    state.scratch["errors"].append({
                        "turn": turn_number,
                        "type": "empty_response",
                        "message": "Assistant returned empty response, terminating early"
                    })
                    print(f"Turn {turn_number}: Empty response, stopping early.")
                    break
        
        # Record epoch timing
        epoch_end = time.time()
        state.scratch["epoch_timing"].update({
            "start_time": epoch_start,
            "end_time": epoch_end,
            "duration_minutes": (epoch_end - epoch_start) / 60.0,
            "turns_completed": len(state.scratch.get("turn_metadata", []))
        })
        
        return state
    
    return solve


def _record_turn_time(state: TaskState, turn_number: int) -> None:
    """
    Record timestamp for a turn completion.
    
    Args:
        state: Task state to update
        turn_number: Turn number (1-indexed)
    """
    if not hasattr(state, "scratch"):
        state.scratch = {}
    
    state.scratch.setdefault("turn_metadata", [])
    state.scratch["turn_metadata"].append({
        "turn": turn_number,
        "timestamp": time.time()
    })