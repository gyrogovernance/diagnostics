"""Task definitions for the five challenge types."""

from .challenge_1_formal import formal_challenge
from .challenge_2_normative import normative_challenge
from .challenge_3_procedural import procedural_challenge
from .challenge_4_strategic import strategic_challenge
from .challenge_5_epistemic import epistemic_challenge

__all__ = [
    "formal_challenge",
    "normative_challenge",
    "procedural_challenge",
    "strategic_challenge",
    "epistemic_challenge",
]