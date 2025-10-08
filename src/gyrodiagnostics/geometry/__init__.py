"""
Geometric decomposition module for tensegrity-based alignment measurement.

This module implements the tetrahedral K4 graph decomposition described in
Measurement.md, mapping the 6 Level 2 (Behavior) metrics to the 6 edges
of a complete graph on 4 vertices.
"""

from .tensegrity import compute_decomposition, EDGE_ORDER, BEHAVIOR_METRIC_ORDER

__all__ = ["compute_decomposition", "EDGE_ORDER", "BEHAVIOR_METRIC_ORDER"]
