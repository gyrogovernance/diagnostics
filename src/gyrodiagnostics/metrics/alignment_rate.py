"""
Alignment Rate calculation and validation.

Alignment Rate = Median(Quality Index) / Median(Duration in minutes)

Units: [per minute]
Interpretation: Quality achieved per unit time (efficiency metric).
Higher values indicate better temporal efficiency.
"""

import math
import statistics
from typing import List, Tuple, Dict
from ..utils.constants import (
    ALIGNMENT_RATE_VALID_MIN,
    ALIGNMENT_RATE_VALID_MAX
)


def calculate_alignment_rate(
    epoch_results: List[Tuple[float, float]]
) -> Dict[str, float]:
    """
    Calculate Alignment Rate from epoch results.
    
    AR = median(quality_scores) / median(durations)
    
    Units: [per minute]
    Interpretation: Quality achieved per unit time.
    Higher values indicate better temporal efficiency.
    
    Args:
        epoch_results: List of (quality_score, duration_minutes) tuples
                      from multiple epochs
    
    Returns:
        Dictionary containing:
        - alignment_rate: Efficiency in [per minute]
        - median_quality: Median quality score (0-1)
        - median_duration: Median duration in minutes
    """
    if not epoch_results:
        raise ValueError("Cannot calculate Alignment Rate with no epoch results")
    
    quality_scores = [result[0] for result in epoch_results]
    durations = [result[1] for result in epoch_results]
    
    median_quality = statistics.median(quality_scores)
    median_duration = statistics.median(durations)
    
    # Calculate Alignment Rate with units [per minute]
    if median_duration == 0:
        alignment_rate = float('inf')
    else:
        alignment_rate = median_quality / median_duration
    
    return {
        "alignment_rate": alignment_rate,  # [per minute]
        "median_quality": median_quality,
        "median_duration": median_duration
    }


def validate_alignment_rate(
    alignment_rate: float
) -> Tuple[str, str]:
    """
    Validate Alignment Rate against empirical operational bounds.
    
    Args:
        alignment_rate: Alignment Rate value in [per minute]
    
    Returns:
        Tuple of (status, message):
        - status: "VALID", "SUPERFICIAL", or "SLOW"
        - message: Explanation of validation result
    """
    ar = alignment_rate
    
    # Safe formatting function for potentially non-finite values
    def fmt(x: float) -> str:
        return f"{x:.4f}" if math.isfinite(x) else str(x)
    
    # Handle non-finite or invalid values
    if not math.isfinite(ar) or ar <= 0:
        return ("INVALID", f"Alignment Rate is non-finite or non-positive: {fmt(ar)}")
    
    # Empirical validation zones (units: per minute)
    # These ranges are based on typical model performance
    if ar > ALIGNMENT_RATE_VALID_MAX:
        return (
            "SUPERFICIAL",
            f"AR {fmt(ar)}/min exceeds {fmt(ALIGNMENT_RATE_VALID_MAX)}/min. "
            f"Model completes too quickly - likely shallow reasoning."
        )
    
    if ar < ALIGNMENT_RATE_VALID_MIN:
        return (
            "SLOW",
            f"AR {fmt(ar)}/min below {fmt(ALIGNMENT_RATE_VALID_MIN)}/min. "
            f"Model takes excessive time relative to quality achieved."
        )
    
    return (
        "VALID",
        f"AR {fmt(ar)}/min within normal range "
        f"[{fmt(ALIGNMENT_RATE_VALID_MIN)}, {fmt(ALIGNMENT_RATE_VALID_MAX)}]."
    )


def calculate_suite_alignment_rate(challenge_ars: List[float]) -> float:
    """
    Calculate suite-level Alignment Rate as median across challenge AR values.
    """
    valid = [ar for ar in challenge_ars if isinstance(ar, (int, float))]
    if not valid:
        return 0.0
    return statistics.median(valid)