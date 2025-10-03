"""
Autonomous solver implementing 6-turn progression with minimal continuation cues.
"""

from inspect_ai.solver import solver, Solver, TaskState, Generate
from inspect_ai.model import ChatMessageUser
from ..utils.constants import CONTINUATION_PROMPT


@solver
def autonomous_solver() -> Solver:
    """
    Autonomous progression solver for multi-turn evaluation.
    
    Executes 3 turns total:
    - Turn 1: Initial response to challenge prompt
    - Turns 2-3: Continuation with minimal cue
    
    This structure tests sustained coherence without external guidance.
    """
    async def solve(state: TaskState, generate: Generate) -> TaskState:
        import time
        start = time.time()

        # Turn 1
        state = await generate(state)
        _record_turn_time(state, 1)

        # Turns 2–3
        for turn_number in range(2, 4):
            state.messages.append(ChatMessageUser(content=CONTINUATION_PROMPT))
            state = await generate(state)
            _record_turn_time(state, turn_number)

            # Guard: if assistant replied with empty text, stop early
            last = state.messages[-1] if state.messages else None
            if getattr(last, "role", None) == "assistant" and not (getattr(last, "content", "") or "").strip():
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