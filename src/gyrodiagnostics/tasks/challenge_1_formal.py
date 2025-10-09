"""Formal Challenge: Derive spatial structure from gyrogroup dynamics."""

from inspect_ai import task, Task
from inspect_ai.dataset import MemoryDataset, Sample
from gyrodiagnostics.solvers.autonomous_solver import autonomous_solver
from gyrodiagnostics.scorers import alignment_scorer
from gyrodiagnostics.prompts.challenge_prompts import CHALLENGE_PROMPTS
from gyrodiagnostics.utils.constants import TASK_CONFIG


@task
def formal_challenge():
    """
    Formal Specialization Challenge: Derive Spatial Structure from Gyrogroup Dynamics
    
    Tests formal reasoning with physics and mathematics specialization metrics.
    """
    dataset = MemoryDataset([
        Sample(
            input=CHALLENGE_PROMPTS["formal"],
            target="",  # Empty target for open-ended evaluation
            id="formal",
            metadata={
                "challenge_type": "formal",
                "specialization": "formal",
                "difficulty": "impossible_single_turn"
            }
        )
    ])
    
    # Build Task kwargs defensively to avoid KeyError if config keys are missing
    extra = {}
    for k in ("message_limit", "time_limit", "token_limit", "temperature", "top_p", "top_k", "max_tokens", "fail_on_error"):
        v = TASK_CONFIG.get(k)
        if v is not None:
            extra[k] = v
    
    return Task(
        dataset=dataset,
        solver=autonomous_solver(),
        scorer=alignment_scorer(),
        epochs=TASK_CONFIG.get("epochs", 2),
        **extra
    )
