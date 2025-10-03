"""
Autonomous solver implementing configurable multi-turn progression with minimal continuation cues.
"""

from inspect_ai.solver import solver, Solver, TaskState, Generate
from inspect_ai.model import ChatMessageUser
from ..utils.constants import CONTINUATION_PROMPT, TASK_CONFIG


@solver
def autonomous_solver() -> Solver:
    """
    Autonomous progression solver for multi-turn evaluation.
    
    Executes configurable number of turns:
    - Turn 1: Initial response to challenge prompt
    - Turns 2-N: Continuation with minimal cue
    
    This structure tests sustained coherence without external guidance.
    """
    async def solve(state: TaskState, generate: Generate) -> TaskState:
        import time
        import asyncio
        try:
            # Prefer specific error classes if available
            from json import JSONDecodeError  # type: ignore
        except Exception:  # pragma: no cover
            JSONDecodeError = Exception  # fallback if not present

        async def generate_with_retries(current_state: TaskState) -> TaskState:
            """
            Call generate() with defensive retries for intermittent provider
            response parsing/network issues that surface as JSON decode errors
            or transient HTTP client errors.
            """
            max_attempts = max(1, int(TASK_CONFIG.get("retry_on_error", 3)))
            base_delay = 0.75

            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return await generate(current_state)
                except JSONDecodeError as ex:  # type: ignore
                    last_exc = ex
                except Exception as ex:
                    # Retry only clearly transient categories; otherwise re-raise
                    transient = (
                        "JSONDecodeError" in str(type(ex))
                        or "ReadTimeout" in str(type(ex))
                        or "WriteError" in str(type(ex))
                        or "RemoteProtocolError" in str(type(ex))
                        or "ConnectionResetError" in str(type(ex))
                        or "ServerDisconnectedError" in str(type(ex))
                    )
                    if not transient:
                        raise
                    last_exc = ex

                if attempt < max_attempts:
                    # Exponential backoff with jitter
                    delay = base_delay * (2 ** (attempt - 1))
                    delay += 0.15 * attempt
                    await asyncio.sleep(delay)

            # Exhausted retries — re-raise last exception
            if last_exc:
                raise last_exc
            return current_state
        start = time.time()
        
        # Get configured number of turns
        num_turns = TASK_CONFIG.get("turns", 3)

        # Turn 1
        state = await generate_with_retries(state)
        _record_turn_time(state, 1)

        # Turns 2-N
        for turn_number in range(2, num_turns + 1):
            state.messages.append(ChatMessageUser(content=CONTINUATION_PROMPT))
            state = await generate_with_retries(state)
            _record_turn_time(state, turn_number)

            # Guard: if assistant replied with empty text, stop early
            last = state.messages[-1] if state.messages else None
            if getattr(last, "role", None) == "assistant":
                content = getattr(last, "content", "")
                # Handle both string and list content
                if isinstance(content, list):
                    content = " ".join(str(item) for item in content)
                if not content or not str(content).strip():
                    break

        end = time.time()
        state.scratch.setdefault("epoch_timing", {})
        state.scratch["epoch_timing"]["duration_minutes"] = (end - start) / 60
        state.scratch["epoch_timing"]["start_time"] = start
        state.scratch["epoch_timing"]["end_time"] = end
        return state
    
    return solve


def _record_turn_time(state: TaskState, turn_number: int):
    import time
    if not hasattr(state, "scratch"):
        state.scratch = {}
    state.scratch.setdefault("turn_metadata", [])
    state.scratch["turn_metadata"].append({
        "turn": turn_number,
        "timestamp": time.time()
    })