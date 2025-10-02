"""Epistemic Challenge: Explore knowledge limits in self-referential systems."""

from inspect_ai import task, Task
from inspect_ai.dataset import MemoryDataset, Sample
from ..solvers.autonomous_solver import autonomous_solver
from ..scorers.alignment_scorer import alignment_scorer
from ..prompts.challenge_prompts import CHALLENGE_PROMPTS
from ..utils.constants import TASK_CONFIG


@task
def epistemic_challenge():
    """
    Epistemic Specialization Challenge: Self-Referential Knowledge Formation
    
    Tests epistemic reasoning with knowledge and communication specialization metrics.
    """
    dataset = MemoryDataset([
        Sample(
            input=CHALLENGE_PROMPTS["epistemic"],
            target=None,
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
        scorer=alignment_scorer(challenge_type="epistemic"),
        epochs=TASK_CONFIG["epochs"],
        message_limit=TASK_CONFIG["message_limit"],
        time_limit=TASK_CONFIG["time_limit"],
        token_limit=TASK_CONFIG["token_limit"],
        fail_on_error=TASK_CONFIG["fail_on_error"]
    )