"""
GyroDiagnostics: Mathematical Physics-Informed AI Alignment Evaluation Suite

Grounded in the Common Governance Model (CGM), this suite evaluates AI model behavior
through principles derived from recursive systems theory and topological analysis.
"""

__version__ = "0.1.0"

from .tasks.challenge_1_formal import formal_challenge
from .tasks.challenge_2_normative import normative_challenge
from .tasks.challenge_3_procedural import procedural_challenge
from .tasks.challenge_4_strategic import strategic_challenge
from .tasks.challenge_5_epistemic import epistemic_challenge

__all__ = [
    "formal_challenge",
    "normative_challenge",
    "procedural_challenge",
    "strategic_challenge",
    "epistemic_challenge",
]