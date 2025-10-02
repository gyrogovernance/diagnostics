"""
GyroDiagnostics: Mathematical Physics-Informed AI Alignment Evaluation Suite

Grounded in the Common Governance Model (CGM), this suite evaluates AI model behavior
through principles derived from recursive systems theory and topological analysis.
"""

__version__ = "0.1.0"

from .tasks.formal_challenge import formal_challenge
from .tasks.normative_challenge import normative_challenge
from .tasks.procedural_challenge import procedural_challenge
from .tasks.strategic_challenge import strategic_challenge
from .tasks.epistemic_challenge import epistemic_challenge

__all__ = [
    "formal_challenge",
    "normative_challenge",
    "procedural_challenge",
    "strategic_challenge",
    "epistemic_challenge",
]