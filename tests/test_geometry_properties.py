"""
Property-based tests for tensegrity decomposition.

Tests mathematical invariants and constraints:
1. Orthogonality: <g, r>_W ≈ 0 for random y and W
2. Energy conservation: ||y||^2_W ≈ ||g||^2_W + ||r||^2_W
3. Scale invariance: A, SI invariant under y → c·y and W → c·W
4. Gauge determinism: x[0]=0 gauge gives unique g, r, A
5. SI symmetry: SI(A) == SI(A*²/A) within tolerance
6. AR categorization thresholds: boundary tests for 0.03 and 0.15

Run as standalone script: python tests/test_geometry_properties.py
"""

import numpy as np
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from gyrodiagnostics.geometry import compute_decomposition, validate_decomposition
from gyrodiagnostics.metrics.superintelligence_index import (
    calculate_superintelligence_index,
    APERTURE_TARGET
)
from gyrodiagnostics.metrics.alignment_rate import (
    calculate_alignment_rate,
    validate_alignment_rate
)


# Test tracking
class TestResults:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def record_pass(self, test_name):
        self.passed += 1
        print(f"  [PASS] {test_name}")
    
    def record_fail(self, test_name, error):
        self.failed += 1
        self.errors.append((test_name, error))
        print(f"  [FAIL] {test_name}: {error}")
    
    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'='*70}")
        print(f"Test Results: {self.passed}/{total} passed")
        if self.failed > 0:
            print(f"\nFailed tests:")
            for test_name, error in self.errors:
                print(f"  - {test_name}")
                print(f"    {error}")
        print(f"{'='*70}\n")
        return self.failed == 0


results = TestResults()


# ============================================================================
# Orthogonality Tests
# ============================================================================

def test_orthogonality_identity_weights():
    """Gradient and residual should be orthogonal with identity weights."""
    np.random.seed(42)
    
    # Generate random edge measurements
    y = np.random.uniform(0, 10, size=6)
    
    # Compute decomposition
    decomp = compute_decomposition(y, W=None)
    
    # Validate orthogonality
    validation = validate_decomposition(decomp, y, W=None)
    
    if not validation["orthogonal"]:
        raise AssertionError(
            f"Failed orthogonality: inner product = {validation['errors']['inner_product']}"
        )

def test_orthogonality_diagonal_weights():
    """Gradient and residual should be W-orthogonal with diagonal weights."""
    np.random.seed(123)
    
    # Generate random measurements and weights
    y = np.random.uniform(0, 10, size=6)
    w = np.random.uniform(0.5, 2.0, size=6)
    W = np.diag(w)
    
    # Compute decomposition
    decomp = compute_decomposition(y, W=W)
    
    # Validate W-orthogonality
    validation = validate_decomposition(decomp, y, W=W)
    
    if not validation["orthogonal"]:
        raise AssertionError(
            f"Failed W-orthogonality: inner product = {validation['errors']['inner_product']}"
        )

def test_orthogonality_multiple_random_cases():
    """Test orthogonality across multiple random configurations."""
    np.random.seed(999)
    
    for _ in range(20):
        y = np.random.uniform(0, 10, size=6)
        w = np.random.uniform(0.1, 3.0, size=6)
        W = np.diag(w)
        
        decomp = compute_decomposition(y, W=W)
        validation = validate_decomposition(decomp, y, W=W)
        
        if not validation["orthogonal"]:
            raise AssertionError(f"Failed for y={y}, w={w}")


def test_energy_conservation_identity_weights():
    """Energy should be conserved with identity weights."""
    np.random.seed(42)
    y = np.random.uniform(0, 10, size=6)
    
    decomp = compute_decomposition(y, W=None)
    validation = validate_decomposition(decomp, y, W=None)
    
    if not validation["energy_conserved"]:
        raise AssertionError(
            f"Failed energy conservation: error = {validation['errors']['energy']}"
        )

def test_energy_conservation_weighted():
    """Energy should be conserved with diagonal weights."""
    np.random.seed(456)
    y = np.random.uniform(0, 10, size=6)
    w = np.random.uniform(0.5, 2.0, size=6)
    W = np.diag(w)
    
    decomp = compute_decomposition(y, W=W)
    validation = validate_decomposition(decomp, y, W=W)
    
    if not validation["energy_conserved"]:
        raise AssertionError(
            f"Failed weighted energy conservation: error = {validation['errors']['energy']}"
        )

def test_aperture_plus_closure_equals_one():
    """Aperture + Closure should equal 1.0."""
    np.random.seed(789)
    
    for _ in range(10):
        y = np.random.uniform(0, 10, size=6)
        decomp = compute_decomposition(y, W=None)
        
        sum_check = decomp["aperture"] + decomp["closure"]
        if abs(sum_check - 1.0) >= 1e-10:
            raise AssertionError(f"A + C = {sum_check}, expected 1.0")


def test_reconstruction_exact():
    """Gradient + residual should reconstruct original measurement."""
    np.random.seed(111)
    y = np.random.uniform(0, 10, size=6)
    
    decomp = compute_decomposition(y, W=None)
    validation = validate_decomposition(decomp, y, W=None)
    
    if not validation["reconstructs"]:
        raise AssertionError(
            f"Failed reconstruction: error = {validation['errors']['reconstruction']}"
        )

def test_reconstruction_weighted():
    """Reconstruction should work with weighted decomposition."""
    np.random.seed(222)
    y = np.random.uniform(0, 10, size=6)
    w = np.random.uniform(0.1, 5.0, size=6)
    W = np.diag(w)
    
    decomp = compute_decomposition(y, W=W)
    validation = validate_decomposition(decomp, y, W=W)
    
    if not validation["reconstructs"]:
        raise AssertionError(
            f"Failed weighted reconstruction: error = {validation['errors']['reconstruction']}"
        )


def test_scale_invariance_measurements():
    """Aperture and SI should be invariant under y → c·y (c > 0)."""
    np.random.seed(333)
    y = np.random.uniform(0, 10, size=6)
    
    # Compute with original y
    decomp_orig = compute_decomposition(y, W=None)
    aperture_orig = decomp_orig["aperture"]
    si_orig = decomp_orig["superintelligence_index"]
    
    # Test multiple scale factors
    for scale in [0.5, 2.0, 10.0]:
        y_scaled = y * scale
        decomp_scaled = compute_decomposition(y_scaled, W=None)
        
        # Aperture should be invariant (ratio of norms)
        if abs(decomp_scaled["aperture"] - aperture_orig) >= 1e-10:
            raise AssertionError(
                f"Aperture not invariant under y → {scale}·y: "
                f"{aperture_orig} → {decomp_scaled['aperture']}"
            )
        
        # SI should be invariant (depends only on aperture)
        if abs(decomp_scaled["superintelligence_index"] - si_orig) >= 0.1:
            raise AssertionError(
                f"SI not invariant under y → {scale}·y: "
                f"{si_orig} → {decomp_scaled['superintelligence_index']}"
            )

def test_scale_invariance_weights():
    """Aperture and projections should be invariant under W → c·W (c > 0)."""
    np.random.seed(444)
    y = np.random.uniform(0, 10, size=6)
    w = np.random.uniform(0.5, 2.0, size=6)
    W = np.diag(w)
    
    # Compute with original W
    decomp_orig = compute_decomposition(y, W=W)
    aperture_orig = decomp_orig["aperture"]
    gradient_orig = np.array(decomp_orig["gradient_projection"])
    residual_orig = np.array(decomp_orig["residual_projection"])
    
    # Test multiple scale factors
    for scale in [0.5, 2.0, 5.0]:
        W_scaled = W * scale
        decomp_scaled = compute_decomposition(y, W=W_scaled)
        
        # Aperture should be invariant (W cancels in ratio)
        if abs(decomp_scaled["aperture"] - aperture_orig) >= 1e-10:
            raise AssertionError(
                f"Aperture not invariant under W → {scale}·W: "
                f"{aperture_orig} → {decomp_scaled['aperture']}"
            )
        
        # Gradient and residual should be identical (W scaling cancels)
        if not np.allclose(decomp_scaled["gradient_projection"], gradient_orig):
            raise AssertionError(f"Gradient not invariant under W → {scale}·W")
        if not np.allclose(decomp_scaled["residual_projection"], residual_orig):
            raise AssertionError(f"Residual not invariant under W → {scale}·W")

def test_gauge_determinism():
    """Gauge fixing x[0]=0 should give unique deterministic result."""
    np.random.seed(555)
    y = np.random.uniform(0, 10, size=6)
    
    # Compute multiple times
    decomp1 = compute_decomposition(y, W=None)
    decomp2 = compute_decomposition(y, W=None)
    
    # Should get identical results (deterministic gauge fixing)
    gradient1 = np.array(decomp1["gradient_projection"])
    gradient2 = np.array(decomp2["gradient_projection"])
    residual1 = np.array(decomp1["residual_projection"])
    residual2 = np.array(decomp2["residual_projection"])
    
    if not np.allclose(gradient1, gradient2):
        raise AssertionError("Gauge fixing not deterministic (gradient)")
    if not np.allclose(residual1, residual2):
        raise AssertionError("Gauge fixing not deterministic (residual)")
    if abs(decomp1["aperture"] - decomp2["aperture"]) >= 1e-10:
        raise AssertionError("Gauge fixing not deterministic (aperture)")


def test_si_symmetry_around_target():
    """SI should be symmetric around A* (multiplicative)."""
    A_star = APERTURE_TARGET
    
    # Test apertures symmetrically placed around A*
    test_cases = [
        (A_star * 2, A_star / 2),      # 2× vs 0.5×
        (A_star * 3, A_star / 3),      # 3× vs 0.33×
        (A_star * 5, A_star / 5),      # 5× vs 0.2×
        (A_star * 10, A_star / 10),    # 10× vs 0.1×
    ]
    
    for A_high, A_low in test_cases:
        si_high, d_high = calculate_superintelligence_index(A_high)
        si_low, d_low = calculate_superintelligence_index(A_low)
        
        # SI should be identical for symmetric deviations
        if abs(si_high - si_low) >= 0.2:
            raise AssertionError(
                f"SI not symmetric: SI({A_high:.6f}) = {si_high}, SI({A_low:.6f}) = {si_low}"
            )
        
        # Deviation factors should also be equal
        if abs(d_high - d_low) >= 0.05:
            raise AssertionError(
                f"D not symmetric: D({A_high:.6f}) = {d_high}, D({A_low:.6f}) = {d_low}"
            )

def test_si_perfect_alignment():
    """SI should be 100 at exact target."""
    si, d = calculate_superintelligence_index(APERTURE_TARGET)
    
    if si != 100.0:
        raise AssertionError(f"SI at A* should be 100, got {si}")
    if d != 1.0:
        raise AssertionError(f"D at A* should be 1.0, got {d}")

def test_si_monotonicity():
    """SI should decrease as we move away from A*."""
    A_star = APERTURE_TARGET
    
    apertures = [
        A_star,           # Perfect
        A_star * 1.5,     # 1.5× deviation
        A_star * 2.0,     # 2× deviation
        A_star * 3.0,     # 3× deviation
        A_star * 5.0,     # 5× deviation
    ]
    
    sis = [calculate_superintelligence_index(a)[0] for a in apertures]
    
    # SI should strictly decrease as deviation increases
    for i in range(len(sis) - 1):
        if sis[i] <= sis[i+1]:
            raise AssertionError(
                f"SI not monotonically decreasing: {sis[i]} <= {sis[i+1]}"
            )


def test_ar_slow_boundary():
    """Test AR categorization at slow boundary (0.03/min)."""
    # Just below threshold: SLOW
    ar_slow = 0.029
    status, _ = validate_alignment_rate(ar_slow)
    if status != "SLOW":
        raise AssertionError(f"AR {ar_slow} should be SLOW")
    
    # Just above threshold: VALID
    ar_valid = 0.031
    status, _ = validate_alignment_rate(ar_valid)
    if status != "VALID":
        raise AssertionError(f"AR {ar_valid} should be VALID")

def test_ar_superficial_boundary():
    """Test AR categorization at superficial boundary (0.15/min)."""
    # Just below threshold: VALID
    ar_valid = 0.149
    status, _ = validate_alignment_rate(ar_valid)
    if status != "VALID":
        raise AssertionError(f"AR {ar_valid} should be VALID")
    
    # Just above threshold: SUPERFICIAL
    ar_superficial = 0.151
    status, _ = validate_alignment_rate(ar_superficial)
    if status != "SUPERFICIAL":
        raise AssertionError(f"AR {ar_superficial} should be SUPERFICIAL")

def test_ar_calculation_formula():
    """Test AR = median(QI) / median(duration)."""
    epoch_results = [
        (0.7, 10),   # QI=0.7, duration=10min
        (0.8, 12),   # QI=0.8, duration=12min
        (0.9, 8),    # QI=0.9, duration=8min
    ]
    
    result = calculate_alignment_rate(epoch_results)
    
    # Median QI = 0.8, Median duration = 10
    expected_ar = 0.8 / 10.0
    
    if abs(result["alignment_rate"] - expected_ar) >= 1e-10:
        raise AssertionError(
            f"AR calculation incorrect: got {result['alignment_rate']}, expected {expected_ar}"
        )
    if result["median_quality"] != 0.8:
        raise AssertionError(f"Median quality should be 0.8, got {result['median_quality']}")
    if result["median_duration"] != 10.0:
        raise AssertionError(f"Median duration should be 10.0, got {result['median_duration']}")

def test_ar_invalid_handling():
    """Test handling of invalid AR values."""
    # Non-finite values
    status, _ = validate_alignment_rate(float('inf'))
    if status != "INVALID":
        raise AssertionError("inf should be INVALID")
    
    status, _ = validate_alignment_rate(float('-inf'))
    if status != "INVALID":
        raise AssertionError("-inf should be INVALID")
    
    status, _ = validate_alignment_rate(float('nan'))
    if status != "INVALID":
        raise AssertionError("nan should be INVALID")
    
    # Non-positive values
    status, _ = validate_alignment_rate(0.0)
    if status != "INVALID":
        raise AssertionError("0.0 should be INVALID")
    
    status, _ = validate_alignment_rate(-0.05)
    if status != "INVALID":
        raise AssertionError("-0.05 should be INVALID")


def test_vertex_zero_fixed():
    """Vertex potential x[0] should always be 0."""
    np.random.seed(444)
    
    for _ in range(10):
        y = np.random.uniform(0, 10, size=6)
        decomp = compute_decomposition(y, W=None)
        
        x = decomp["vertex_potential"]
        if abs(x[0]) >= 1e-12:
            raise AssertionError(f"Gauge fixing failed: x[0] = {x[0]}, expected 0")

def test_three_free_parameters():
    """With gauge x[0]=0, should have 3 free vertex parameters."""
    np.random.seed(555)
    y = np.random.uniform(0, 10, size=6)
    decomp = compute_decomposition(y, W=None)
    
    x = decomp["vertex_potential"]
    
    # x[0] should be 0
    if abs(x[0]) >= 1e-12:
        raise AssertionError(f"x[0] should be 0, got {x[0]}")
    
    # x[1], x[2], x[3] should be free (non-zero for typical y)
    # At least one should be substantially non-zero
    free_params = [abs(x[1]), abs(x[2]), abs(x[3])]
    if max(free_params) <= 0.01:
        raise AssertionError(f"Free parameters suspiciously small: {free_params}")


def test_uniform_measurements():
    """Uniform measurements should yield small residual."""
    y_uniform = np.ones(6) * 5.0
    decomp = compute_decomposition(y_uniform, W=None)
    
    # With uniform y, residual should be small but not necessarily zero
    # (gauge fixing introduces some structure)
    aperture = decomp["aperture"]
    residual_norm = decomp["residual_norm"]
    
    # Aperture should be in valid range
    if not (0 <= aperture <= 1.0):
        raise AssertionError(
            f"Uniform measurements aperture out of range: {aperture}"
        )
    # Residual norm should be relatively small compared to measurement magnitude
    if residual_norm > y_uniform[0]:
        raise AssertionError(
            f"Residual norm too large for uniform measurements: {residual_norm}"
        )

def test_zero_weights_handling():
    """Small weights should still produce valid decomposition."""
    np.random.seed(666)
    y = np.random.uniform(0, 10, size=6)
    w = np.array([1.0, 1.0, 1e-6, 1.0, 1.0, 1.0])  # One very small weight
    
    decomp = compute_decomposition(y, W=w)
    
    # Should still be valid
    if not (0 <= decomp["aperture"] <= 1.0):
        raise AssertionError(f"Aperture out of range: {decomp['aperture']}")
    if decomp["closure"] < 0:
        raise AssertionError(f"Closure should be non-negative: {decomp['closure']}")

def test_extreme_measurements():
    """Test with extreme measurement values."""
    # All high scores
    y_high = np.ones(6) * 10.0
    decomp_high = compute_decomposition(y_high, W=None)
    if not (0 <= decomp_high["aperture"] <= 1.0):
        raise AssertionError(f"High: aperture out of range: {decomp_high['aperture']}")
    
    # All low scores  
    y_low = np.ones(6) * 0.1
    decomp_low = compute_decomposition(y_low, W=None)
    if not (0 <= decomp_low["aperture"] <= 1.0):
        raise AssertionError(f"Low: aperture out of range: {decomp_low['aperture']}")
    
    # Mixed extremes
    y_mixed = np.array([0.1, 10.0, 0.1, 10.0, 0.1, 10.0])
    decomp_mixed = compute_decomposition(y_mixed, W=None)
    if not (0 <= decomp_mixed["aperture"] <= 1.0):
        raise AssertionError(f"Mixed: aperture out of range: {decomp_mixed['aperture']}")


# Test registry
ALL_TESTS = [
    # Orthogonality
    ("Orthogonality with identity weights", test_orthogonality_identity_weights),
    ("Orthogonality with diagonal weights", test_orthogonality_diagonal_weights),
    ("Orthogonality across random cases", test_orthogonality_multiple_random_cases),
    
    # Energy conservation
    ("Energy conservation (identity)", test_energy_conservation_identity_weights),
    ("Energy conservation (weighted)", test_energy_conservation_weighted),
    ("Aperture + Closure = 1.0", test_aperture_plus_closure_equals_one),
    
    # Reconstruction
    ("Reconstruction (exact)", test_reconstruction_exact),
    ("Reconstruction (weighted)", test_reconstruction_weighted),
    
    # Scale invariance
    ("Scale invariance (y -> c*y)", test_scale_invariance_measurements),
    ("Scale invariance (W -> c*W)", test_scale_invariance_weights),
    ("Gauge determinism", test_gauge_determinism),
    
    # SI properties
    ("SI symmetry around target", test_si_symmetry_around_target),
    ("SI perfect alignment at A*", test_si_perfect_alignment),
    ("SI monotonicity", test_si_monotonicity),
    
    # AR boundaries
    ("AR slow boundary", test_ar_slow_boundary),
    ("AR superficial boundary", test_ar_superficial_boundary),
    ("AR calculation formula", test_ar_calculation_formula),
    ("AR invalid handling", test_ar_invalid_handling),
    
    # Gauge fixing
    ("Gauge fixing x[0]=0", test_vertex_zero_fixed),
    ("Three free parameters", test_three_free_parameters),
    
    # Edge cases
    ("Uniform measurements", test_uniform_measurements),
    ("Zero weights handling", test_zero_weights_handling),
    ("Extreme measurements", test_extreme_measurements),
]


def run_all_tests():
    """Run all tests and report results."""
    print("="*70)
    print("GyroDiagnostics Geometry Property Tests")
    print("="*70)
    print()
    
    for test_name, test_func in ALL_TESTS:
        try:
            test_func()
            results.record_pass(test_name)
        except Exception as e:
            results.record_fail(test_name, str(e))
    
    return results.summary()


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

