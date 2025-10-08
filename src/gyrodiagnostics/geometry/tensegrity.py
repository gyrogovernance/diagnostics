"""
Tensegrity decomposition for K4 tetrahedral measurement topology.

Implements orthogonal decomposition y = B^T x + r where:
- y: 6 edge measurements (Level 2 Behavior metrics)
- x: Vertex potentials (gauge: x[0] = 0)
- B^T x: Gradient projection in edge space (global alignment component)
- r: Residual projection in edge space (local differentiation component)
- A: Aperture ratio (||r||^2_W / ||y||^2_W) targeting ~0.0207

Applies the tensegrity balance geometry from CGM's Balance Universal (BU) stage
to AI alignment measurement. The aperture target (~0.0207) is derived from CGM's
BU stage (see docs/theory/CommonGovernanceModel.md). This represents optimal
tensegrity balance: 97.93% closure (structural stability) + 2.07% aperture
(adaptive capacity).

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
# Cycles: 0-1-2-0, 0-1-3-0, 0-2-3-0
C = np.array([
    [ 1,  1,  0, -1,  0,  0],  # Cycle 0-1-2-0 (edges 01, 02, -12)
    [ 1,  0,  1,  0, -1,  0],  # Cycle 0-1-3-0 (edges 01, 03, -13)
    [ 0,  1,  1,  0,  0, -1]   # Cycle 0-2-3-0 (edges 02, 03, -23)
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
            - aperture: Aperture ratio ||r||^2_W / ||y||^2_W (target ~0.0207 from CGM)
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
    
    return {
        # Vertex potentials (gauge: x[0] = 0 by construction)
        "vertex_potential": x.tolist(),
        
        # Edge-space projections
        "gradient_projection": gradient.tolist(),  # Global alignment component
        "residual_projection": r.tolist(),         # Local differentiation component
        
        # Tensegrity balance (CGM-derived target)
        "aperture": float(aperture),               # Target ~0.0207 from CGM BU
        "closure": float(closure),
        
        # Component magnitudes
        "gradient_norm": float(gradient_norm),
        "residual_norm": float(residual_norm)
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
