"""Strategic Challenge: Forecast AI regulatory evolution across jurisdictions."""

from inspect_ai import task, Task
from inspect_ai.dataset import MemoryDataset, Sample
from gyrodiagnostics.solvers.autonomous_solver import autonomous_solver
from gyrodiagnostics.scorers import alignment_scorer
from gyrodiagnostics.prompts.challenge_prompts import CHALLENGE_PROMPTS
from gyrodiagnostics.utils.constants import TASK_CONFIG


@task
def strategic_challenge():
    """
    Strategic Specialization Challenge: AI Regulatory Forecasting
    
    Tests strategic reasoning with finance and strategy specialization metrics.
    """
    # Create multiple samples with unique IDs for epochs
    samples = [
        Sample(
            input=CHALLENGE_PROMPTS["strategic"],
            target="",  # Empty target for open-ended evaluation
            id=f"strategic_{i+1:03d}",
            metadata={
                "challenge_type": "strategic",
                "specialization": "strategic",
                "difficulty": "impossible_single_turn"
            }
        )
        for i in range(TASK_CONFIG["epochs"])
    ]
    
    dataset = MemoryDataset(samples)
    
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
