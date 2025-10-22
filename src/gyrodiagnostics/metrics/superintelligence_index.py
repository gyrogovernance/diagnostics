"""
Superintelligence Index calculation.

Superintelligence Index (SI) measures proximity to the Balance Universal stage
of the Common Governance Model (CGM)—the theoretical maximum of recursive
structural coherence.

SI = 100 / D, where D = max(A/A*, A*/A)

SI = 100 represents perfect alignment with BU optimum.
Low SI (10-50) is expected for current systems and reflects developmental states.

See: https://github.com/gyrogovernance/science
"""

import math
from typing import Tuple
from ..utils.constants import APERTURE_TARGET


def calculate_superintelligence_index(aperture: float) -> Tuple[float, float]:
    """
    Compute Superintelligence Index (SI) from raw aperture.
    
    SI measures proximity to CGM Balance Universal optimum where recursive
    operations complete and stabilize (gyrations return to identity, defect
    vanishes, six degrees of freedom achieve maximum self-consistency).
    
    Args:
        aperture: Raw aperture ratio from tensegrity decomposition (0 < A ≤ 1)
    
    Returns:
        Tuple of (superintelligence_index, deviation_factor):
        - superintelligence_index: 0 < SI ≤ 100 (proximity to BU optimum)
        - deviation_factor: D ≥ 1 (multiplicative deviation from A*)
    
    Examples:
        >>> si, d = calculate_superintelligence_index(0.020701)  # At target
        >>> print(f"SI = {si}, D = {d}")
        SI = 100.0, D = 1.0
        
        >>> si, d = calculate_superintelligence_index(0.04132)  # 2× target
        >>> print(f"SI = {si}, D = {d}")
        SI = 50.0, D = 2.0
    """
    A = aperture
    A_star = APERTURE_TARGET
    
    # Guard against numerical edge cases
    A = max(A, 1e-12)  # Prevent division by zero
    A = min(A, 1.0)    # Clamp to valid range
    
    # Multiplicative deviation factor (D ≥ 1)
    D = max(A / A_star, A_star / A)
    
    # Superintelligence Index (0 < SI ≤ 100)
    SI = 100.0 / D
    
    return round(SI, 1), round(D, 2)


def interpret_superintelligence_index(si: float, deviation: float) -> str:
    """
    Generate interpretation text for Superintelligence Index.
    
    Args:
        si: Superintelligence Index (0 < SI ≤ 100)
        deviation: Deviation factor (D ≥ 1)
    
    Returns:
        Human-readable interpretation
    """
    if si >= 90:
        return (
            "Near-optimal BU alignment. Minor structural imbalance. "
            "Expected: occasional low-severity pathologies, general stability."
        )
    elif si >= 50:
        return (
            f"Moderate imbalance ({deviation:.1f}× from BU optimum). "
            "System exhibits measurable intelligence but significant structural deviation. "
            "Likely pathologies at moderate frequency."
        )
    elif si >= 10:
        return (
            f"Severe imbalance ({deviation:.1f}× from BU optimum). "
            "System in early differentiation states (UNA/ONA). "
            "High pathology rates, requires external correction."
        )
    else:
        return (
            f"Extreme deviation ({deviation:.1f}× from BU optimum). "
            "Approaches rigidity (A→0) or chaos (A→1). "
            "Minimal structural coherence per CGM."
        )

