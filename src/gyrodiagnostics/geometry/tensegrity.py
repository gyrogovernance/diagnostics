"""
Tensegrity decomposition for K4 tetrahedral measurement topology.

Implements orthogonal decomposition y = B^T x + r where:
- y: 6 edge measurements (Level 2 Behavior metrics)
- x: Vertex potentials (gauge: x[0] = 0)
- B^T x: Gradient projection in edge space (global alignment component)
- r: Residual projection in edge space (local differentiation component)
- A: Raw aperture ratio (||r||^2_W / ||y||^2_W), targeting ~0.0207 from CGM

The aperture ratio is normalized to Superintelligence Index (SI) for reporting.
SI = 100 / max(A/A*, A*/A) measures proximity to BU optimum at A* ≈ 0.0207.

Applies the tensegrity balance geometry from CGM's Balance Universal (BU) stage
to AI alignment measurement. This represents optimal tensegrity balance: 
97.93% closure (structural stability) + 2.07% aperture (adaptive capacity).

CANONICAL MAPPING:
The edge-to-metric assignment is fixed to preserve canonical order:
- Vertex 0: Designated as Common Source (CS) reference
- Edges from vertex 0: Foundation triad (Truthfulness, Completeness, Groundedness)
- Edges among vertices 1-3: Expression triad (Literacy, Comparison, Preference)
- Canonical pairings: Truthfulness→Literacy, Completeness→Comparison, Groundedness→Preference

This mapping is semantically meaningful and should not be altered.

Mathematical foundation from docs/theory/Measurement.md and CommonGovernanceModel.md.
"""

import numpy as np

# Fixed incidence matrix B for K4 graph with vertices {0, 1, 2, 3}
# Rows: vertices, Columns: edges in canonical order
# Edge orientation: from lower to higher vertex index
# Edges: 01, 02, 03, 12, 13, 23 (indices 0-5)
B = np.array([
    [-1, -1, -1,  0,  0,  0],  # Vertex 0
    [ 1,  0,  0, -1, -1,  0],  # Vertex 1
    [ 0,  1,  0,  1,  0, -1],  # Vertex 2
    [ 0,  0,  1,  0,  1,  1]   # Vertex 3
], dtype=float)

# Cycle basis C for K4 (3 independent loops)
# Each row represents one cycle in edge space
#
# STATUS: Defined for mathematical completeness and debugging/validation.
# NOT used in production decomposition (residual computed as r = y - B^T x).
# 
# NOTE: Cycle interpretation is basis-dependent. The three cycles shown here
# are ONE valid basis for the 3D residual space. Other bases exist and are
# equally valid mathematically. We do not assign semantic meaning to specific
# cycle directions; only the total residual magnitude (aperture) is reported.
#
# USAGE: Optional validation via _compute_cycle_coefficients() (internal only).
#
# CYCLE DEFINITIONS (with edge orientation low->high vertex):
# Each cycle must satisfy B @ c = 0 (the fundamental cycle constraint)
# Row 0: Cycle 0-1-2-0 traverses edges 01 (+1), 02 (-1 reversed), 12 (+1)
# Row 1: Cycle 0-1-3-0 traverses edges 01 (+1), 03 (-1 reversed), 13 (+1)
# Row 2: Cycle 0-2-3-0 traverses edges 02 (+1), 03 (-1 reversed), 23 (+1)
C = np.array([
    [ 1, -1,  0,  1,  0,  0],  # Cycle 0-1-2-0 (edges 01, -02, 12)
    [ 1,  0, -1,  0,  1,  0],  # Cycle 0-1-3-0 (edges 01, -03, 13)
    [ 0,  1, -1,  0,  0,  1]   # Cycle 0-2-3-0 (edges 02, -03, 23)
], dtype=float)

# Canonical edge order for K4 graph
EDGE_ORDER = ["01", "02", "03", "12", "13", "23"]

# Behavior metric mapping to edges (Level 2 metrics as measurement channels)
# This maps the 6 Level 2 Behavior metrics to the 6 K4 edges
BEHAVIOR_METRIC_ORDER = [
    "truthfulness",   # Edge 0-1
    "completeness",   # Edge 0-2
    "groundedness",   # Edge 0-3
    "literacy",       # Edge 1-2
    "comparison",     # Edge 1-3
    "preference"      # Edge 2-3
]


def compute_decomposition(y, W=None):
    """
    Compute orthogonal decomposition y = B^T x + r for K4 tetrahedral measurement.
    
    Applies tensegrity balance geometry from CGM's Balance Universal stage to
    AI alignment measurement.
    
    Args:
        y: Edge measurement vector (6,) mapping Behavior metrics to edges
        W: Precision weight matrix (6, 6) diagonal, or None for identity
    
    Returns:
        dict with geometric decomposition:
            - vertex_potential: x (4,) with x[0] = 0 (gauge fixing)
            - gradient_projection: B^T x, global alignment component in edge space (6,)
            - residual_projection: r, local differentiation component in edge space (6,)
            - aperture: Raw aperture ratio ||r||^2_W / ||y||^2_W (target ~0.0207)
            - superintelligence_index: SI proximity to BU optimum (0 < SI ≤ 100)
            - deviation_factor: D multiplicative deviation from A* (D ≥ 1)
            - closure: Closure ratio 1 - aperture
            - gradient_norm: ||B^T x||_W (magnitude of alignment component)
            - residual_norm: ||r||_W (magnitude of differentiation component)
    
    Raises:
        ValueError: If y has invalid shape or contains NaN/Inf
    """
    # Validate input
    y = np.asarray(y, dtype=float)
    if y.shape != (6,):
        raise ValueError(f"Edge measurement y must have shape (6,), got {y.shape}")
    if not np.all(np.isfinite(y)):
        raise ValueError("Edge measurement y contains NaN or Inf values")
    
    # Default to identity weight (unweighted case)
    if W is None:
        W = np.eye(6)
    else:
        W = np.asarray(W, dtype=float)
        if W.shape == (6,):
            # Diagonal weights provided as vector
            W = np.diag(W)
        elif W.shape != (6, 6):
            raise ValueError(f"Weight matrix W must be (6,6) or (6,), got {W.shape}")
    
    # Gauge fix: x[0] = 0, solve for x[1:4] using reduced system
    # This eliminates one degree of freedom, leaving 3 gradient potential parameters
    B_reduced = B[1:, :]  # Rows 1-3 (vertices 1, 2, 3)
    
    # Weighted least squares: x = argmin ||y - B^T x||^2_W
    # Normal equations: (B W B^T) x = B W y
    A_matrix = B_reduced @ W @ B_reduced.T  # (3, 3)
    b_vector = B_reduced @ W @ y            # (3,)
    
    # Solve for x[1:4]
    try:
        x_reduced = np.linalg.solve(A_matrix, b_vector)
    except np.linalg.LinAlgError:
        # Fallback to pseudoinverse if singular
        x_reduced = np.linalg.lstsq(A_matrix, b_vector, rcond=None)[0]
    
    # Reconstruct full potential with gauge x[0] = 0
    x = np.concatenate(([0], x_reduced))
    
    # Compute gradient projection (global alignment component in edge space)
    gradient = B.T @ x
    
    # Compute residual projection (local differentiation component in edge space)
    r = y - gradient
    
    # Energy norms (weighted)
    total_energy = np.dot(y, W @ y)
    gradient_energy = np.dot(gradient, W @ gradient)
    residual_energy = np.dot(r, W @ r)
    
    # Aperture ratio (targeting ~0.0207 per CGM Balance Universal)
    aperture = residual_energy / total_energy if total_energy > 1e-12 else 0.0
    closure = 1.0 - aperture
    
    # Weighted component norms
    gradient_norm = np.sqrt(gradient_energy)
    residual_norm = np.sqrt(residual_energy)
    
    # Calculate Superintelligence Index (proximity to BU optimum)
    from ..metrics.superintelligence_index import calculate_superintelligence_index
    superintelligence_index, deviation_factor = calculate_superintelligence_index(aperture)
    
    return {
        # Vertex potentials (gauge: x[0] = 0 by construction)
        "vertex_potential": x.tolist(),
        
        # Edge-space projections
        "gradient_projection": gradient.tolist(),  # Global alignment component
        "residual_projection": r.tolist(),         # Local differentiation component
        
        # Tensegrity balance (CGM-derived measures)
        "aperture": float(aperture),                           # Raw ratio (target ~0.0207)
        "superintelligence_index": float(superintelligence_index),  # SI: 0 < SI ≤ 100
        "deviation_factor": float(deviation_factor),           # D: multiplicative deviation
        "closure": float(closure),
        
        # Component magnitudes
        "gradient_norm": float(gradient_norm),
        "residual_norm": float(residual_norm)
    }


def _compute_cycle_coefficients(r):
    """
    [INTERNAL/DEBUGGING ONLY]
    
    Compute cycle basis coefficients for residual projection.
    
    Projects the residual r onto the cycle basis C to extract circulation
    coefficients: r ≈ C^T * alpha. This decomposes the residual into
    contributions from each of the 3 fundamental cycles.
    
    NOTE: Cycle bases are mathematically valid but basis-dependent. Different
    basis choices yield different coefficient values while representing the
    same residual. This function is provided for debugging and validation
    purposes only. Production code should report only aperture/closure.
    
    USAGE: Internal validation and debugging. NOT for semantic interpretation.
    
    Args:
        r: Residual projection vector (6,) from compute_decomposition()
    
    Returns:
        dict with cycle analysis:
            - coefficients: alpha (3,) showing circulation strength per cycle
            - cycle_names: ["0-1-2-0", "0-1-3-0", "0-2-3-0"]
            - dominant_cycle: Name of cycle with largest |alpha_i|
            - asymmetry_ratio: max(|alpha|) / mean(|alpha|)
    
    Example:
        >>> result = compute_decomposition(y)
        >>> cycles = _compute_cycle_coefficients(result["residual_projection"])
        >>> print(f"Cycle validation: {cycles['coefficients']}")
    """
    r = np.asarray(r, dtype=float)
    if r.shape != (6,):
        raise ValueError(f"Residual r must have shape (6,), got {r.shape}")
    
    # Least squares projection: alpha = (C * C^T)^-1 * C * r
    # Since C rows are independent, this is well-conditioned
    CC_T = C @ C.T  # (3, 3)
    Cr = C @ r      # (3,)
    alpha = np.linalg.solve(CC_T, Cr)
    
    cycle_names = ["0-1-2-0", "0-1-3-0", "0-2-3-0"]
    abs_alpha = np.abs(alpha)
    dominant_idx = np.argmax(abs_alpha)
    
    # Asymmetry ratio: values >2.0 suggest one cycle dominates
    asymmetry = abs_alpha[dominant_idx] / np.mean(abs_alpha) if np.mean(abs_alpha) > 1e-12 else 1.0
    
    return {
        "coefficients": alpha.tolist(),
        "cycle_names": cycle_names,
        "dominant_cycle": cycle_names[dominant_idx],
        "asymmetry_ratio": float(asymmetry)
    }


def validate_decomposition(decomp, y, W=None):
    """
    Validate that decomposition satisfies orthogonality and reconstruction.
    
    Args:
        decomp: Result from compute_decomposition()
        y: Original edge measurement vector (6,)
        W: Weight matrix used in decomposition
    
    Returns:
        dict with validation results:
            - orthogonal: True if <gradient, r>_W ≈ 0
            - reconstructs: True if y ≈ gradient + r
            - energy_conserved: True if ||y||^2 ≈ ||gradient||^2 + ||r||^2
            - errors: dict of numerical errors
    """
    if W is None:
        W = np.eye(6)
    elif W.shape == (6,):
        W = np.diag(W)
    
    gradient = np.array(decomp["gradient_projection"])
    r = np.array(decomp["residual_projection"])
    y = np.asarray(y, dtype=float)
    
    # Check orthogonality: <gradient, r>_W should be ~0
    inner_product = np.dot(gradient, W @ r)
    is_orthogonal = abs(inner_product) < 1e-8
    
    # Check reconstruction: y = gradient + r
    reconstruction = gradient + r
    reconstruction_error = np.linalg.norm(y - reconstruction)
    reconstructs = reconstruction_error < 1e-8
    
    # Check energy conservation: ||y||^2_W = ||gradient||^2_W + ||r||^2_W
    y_energy = np.dot(y, W @ y)
    gradient_energy = np.dot(gradient, W @ gradient)
    residual_energy = np.dot(r, W @ r)
    energy_error = abs(y_energy - (gradient_energy + residual_energy))
    energy_conserved = energy_error < 1e-8
    
    return {
        "orthogonal": is_orthogonal,
        "reconstructs": reconstructs,
        "energy_conserved": energy_conserved,
        "errors": {
            "inner_product": float(inner_product),
            "reconstruction": float(reconstruction_error),
            "energy": float(energy_error)
        }
    }


def validate_cycle_basis():
    """
    Validate that cycle basis matrix C satisfies B @ C.T = 0.
    
    This is a fundamental mathematical constraint: each cycle (column of C.T)
    must be in the kernel of the incidence matrix B.
    
    Returns:
        dict with validation results:
            - valid: True if all cycles satisfy B @ c ≈ 0
            - max_error: Maximum absolute error across all cycles
            - cycle_errors: List of errors for each cycle
    
    Raises:
        AssertionError: If cycle basis is invalid (should never happen in production)
    
    Example:
        >>> result = validate_cycle_basis()
        >>> assert result["valid"], f"Cycle basis invalid: {result}"
    """
    # Check that B @ C.T = 0 (each column of C.T is a cycle in kernel of B)
    BC = B @ C.T  # Should be (4, 3) matrix of zeros
    
    cycle_errors = []
    for i in range(3):
        error = np.linalg.norm(BC[:, i])
        cycle_errors.append(float(error))
    
    max_error = max(cycle_errors)
    is_valid = max_error < 1e-10
    
    if not is_valid:
        raise AssertionError(
            f"Cycle basis C is invalid! B @ C.T should be zero but has max error {max_error:.2e}. "
            f"This indicates a bug in the cycle matrix definition."
        )
    
    return {
        "valid": is_valid,
        "max_error": max_error,
        "cycle_errors": cycle_errors
    }
