"""Epistemic Challenge: Explore knowledge limits in self-referential systems."""

from inspect_ai import task, Task
from inspect_ai.dataset import MemoryDataset, Sample
from gyrodiagnostics.solvers.autonomous_solver import autonomous_solver
from gyrodiagnostics.scorers.alignment_scorer import alignment_scorer
from gyrodiagnostics.prompts.challenge_prompts import CHALLENGE_PROMPTS
from gyrodiagnostics.utils.constants import TASK_CONFIG


@task
def epistemic_challenge():
    """
    Epistemic Specialization Challenge: Self-Referential Knowledge Formation
    
    Tests epistemic reasoning with knowledge and communication specialization metrics.
    """
    dataset = MemoryDataset([
        Sample(
            input=CHALLENGE_PROMPTS["epistemic"],
            target="",  # Empty target for open-ended evaluation
            id="epistemic_001",
            metadata={
                "challenge_type": "epistemic",
                "specialization": "epistemic",
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