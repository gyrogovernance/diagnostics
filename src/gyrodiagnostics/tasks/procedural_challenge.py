"""Procedural Challenge: Specify recursive computational process with asymmetry."""

from inspect_ai import task, Task
from inspect_ai.dataset import MemoryDataset, Sample
from gyrodiagnostics.solvers.autonomous_solver import autonomous_solver
from gyrodiagnostics.scorers.alignment_scorer import alignment_scorer
from gyrodiagnostics.prompts.challenge_prompts import CHALLENGE_PROMPTS
from gyrodiagnostics.utils.constants import TASK_CONFIG


@task
def procedural_challenge():
    """
    Procedural Specialization Challenge: Recursive Computational Process
    
    Tests procedural reasoning with code and debugging specialization metrics.
    """
    dataset = MemoryDataset([
        Sample(
            input=CHALLENGE_PROMPTS["procedural"],
            target="",  # Empty target for open-ended evaluation
            id="procedural_001",
            metadata={
                "challenge_type": "procedural",
                "specialization": "procedural",
                "difficulty": "impossible_single_turn"
            }
        )
    ])
    
    return Task(
        dataset=dataset,
        solver=autonomous_solver(),
        scorer=alignment_scorer(),
        epochs=TASK_CONFIG["epochs"],  # Use configured epochs
        message_limit=TASK_CONFIG["message_limit"],
        time_limit=TASK_CONFIG["time_limit"],
        token_limit=TASK_CONFIG["token_limit"],
        temperature=TASK_CONFIG["temperature"],
        top_p=TASK_CONFIG["top_p"],
        top_k=TASK_CONFIG["top_k"],
        max_tokens=2048,  # Balanced for complex responses
        fail_on_error=TASK_CONFIG["fail_on_error"]
    )