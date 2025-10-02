"""
Autonomous solver implementing 6-turn progression with minimal continuation cues.
"""

from inspect_ai.solver import solver, Solver, TaskState, Generate, user_message
from inspect_ai.model import ChatMessageUser
from ..utils.constants import CONTINUATION_PROMPT


@solver
def autonomous_solver() -> Solver:
    """
    Autonomous progression solver for multi-turn evaluation.
    
    Executes 6 turns total:
    - Turn 1: Initial response to challenge prompt
    - Turns 2-6: Continuation with minimal cue
    
    This structure tests sustained coherence without external guidance.
    """
    async def solve(state: TaskState, generate: Generate) -> TaskState:
        import time
        
        # Record epoch start time
        epoch_start = time.time()
        
        # Turn 1: Initial generation with challenge prompt
        state = await generate(state)
        
        # Turns 2-6: Minimal continuation cues
        for turn_number in range(2, 7):
            # Add minimal continuation prompt using proper message construction
            state.messages.append(ChatMessageUser(content=CONTINUATION_PROMPT))
            
            # Generate next turn
            state = await generate(state)
            
            # Store turn metadata in state.scratch for temporal analysis
            if not hasattr(state, "scratch"):
                state.scratch = {}
            if "turn_metadata" not in state.scratch:
                state.scratch["turn_metadata"] = []
            
            state.scratch["turn_metadata"].append({
                "turn": turn_number,
                "timestamp": state.completed_at if state.completed_at else time.time()
            })
        
        # Record epoch duration as fallback
        epoch_end = time.time()
        epoch_duration_minutes = (epoch_end - epoch_start) / 60
        
        if "epoch_timing" not in state.scratch:
            state.scratch["epoch_timing"] = {}
        state.scratch["epoch_timing"]["duration_minutes"] = epoch_duration_minutes
        state.scratch["epoch_timing"]["start_time"] = epoch_start
        state.scratch["epoch_timing"]["end_time"] = epoch_end
        
        return state
    
    return solve