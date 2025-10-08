"""
Geometric decomposition module for tensegrity-based alignment measurement.

This module implements the tetrahedral K4 graph decomposition described in
Measurement.md, mapping the 6 Level 2 (Behavior) metrics to the 6 edges
of a complete graph on 4 vertices.
"""

from .tensegrity import (
    compute_decomposition,
    validate_decomposition,
    validate_cycle_basis,
    EDGE_ORDER,
    BEHAVIOR_METRIC_ORDER
)
# Note: _compute_cycle_coefficients is internal/debugging only, not exported

__all__ = [
    "compute_decomposition",
    "validate_decomposition",
    "validate_cycle_basis",
    "EDGE_ORDER",
    "BEHAVIOR_METRIC_ORDER"
]
