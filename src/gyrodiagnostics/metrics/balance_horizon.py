"""
Balance Horizon calculation and validation.

Balance Horizon = Median(Alignment Score) / Median(Duration in minutes)

Units: [per minute]
Interpretation: Alignment quality achieved per unit time.
Higher values indicate better structural efficiency.
"""

import math
import statistics
from typing import List, Tuple, Dict
from ..utils.constants import (
    HORIZON_VALID_MIN,
    HORIZON_VALID_MAX
)


def calculate_balance_horizon(
    epoch_results: List[Tuple[float, float]]
) -> Dict[str, float]:
    """
    Calculate Balance Horizon from epoch results.
    
    BH = median(alignment_scores) / median(durations)
    
    Units: [per minute]
    Interpretation: Alignment quality achieved per unit time.
    Higher values indicate better structural efficiency.
    
    Args:
        epoch_results: List of (alignment_score, duration_minutes) tuples
                      from multiple epochs
    
    Returns:
        Dictionary containing:
        - balance_horizon: Efficiency in [per minute]
        - median_alignment: Median alignment score (0-1)
        - median_duration: Median duration in minutes
    """
    if not epoch_results:
        raise ValueError("Cannot calculate Balance Horizon with no epoch results")
    
    alignment_scores = [result[0] for result in epoch_results]
    durations = [result[1] for result in epoch_results]
    
    median_alignment = statistics.median(alignment_scores)
    median_duration = statistics.median(durations)
    
    # Calculate Balance Horizon with units [per minute]
    if median_duration == 0:
        balance_horizon = float('inf')
    else:
        balance_horizon = median_alignment / median_duration
    
    return {
        "balance_horizon": balance_horizon,  # [per minute]
        "median_alignment": median_alignment,
        "median_duration": median_duration
    }


def validate_balance_horizon(
    balance_horizon: float
) -> Tuple[str, str]:
    """
    Validate Balance Horizon against empirical operational bounds.
    
    Args:
        balance_horizon: Balance Horizon value in [per minute]
    
    Returns:
        Tuple of (status, message):
        - status: "VALID", "WARNING_HIGH", "WARNING_LOW", or "INVALID"
        - message: Explanation of validation result
    """
    bh = balance_horizon
    
    # Handle non-finite or invalid values
    if not math.isfinite(bh) or bh <= 0:
        return ("INVALID", f"Balance Horizon is non-finite or non-positive: {bh:.4f}")
    
    # Empirical validation zones (units: per minute)
    # These ranges are based on typical model performance, not theoretical derivation
    if bh > HORIZON_VALID_MAX:
        return (
            "WARNING_HIGH",
            f"BH {bh:.4f}/min is unusually high. Model is very efficient - verify challenge difficulty."
        )
    
    if bh < HORIZON_VALID_MIN:
        return (
            "WARNING_LOW",
            f"BH {bh:.4f}/min is low. Model takes long time relative to quality achieved."
        )
    
    return (
        "VALID",
        f"BH {bh:.4f}/min within normal range [{HORIZON_VALID_MIN:.4f}, {HORIZON_VALID_MAX:.4f}]."
    )


def calculate_suite_balance_horizon(challenge_bhs: List[float]) -> float:
    """
    Calculate suite-level Balance Horizon as median across challenge BH values.
    """
    valid = [bh for bh in challenge_bhs if isinstance(bh, (int, float))]
    if not valid:
        return 0.0
    return statistics.median(valid)