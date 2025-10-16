# GyroDiagnostics Test Suite

## Overview

This directory contains tests for the GyroDiagnostics framework, with a focus on mathematical property verification for the tensegrity decomposition and alignment metrics.

## Test Files

### `test_geometry_properties.py`

Comprehensive property-based tests for the tensegrity decomposition mathematics. Tests fundamental invariants that must hold for the decomposition to be mathematically sound.

**Test Categories (23 total tests):**

1. **Orthogonality Tests** (3) - Verify W-orthogonality: `<g, r>_W ≈ 0`
   - Identity weights
   - Diagonal weights
   - Multiple random configurations

2. **Energy Conservation Tests** (3) - Verify: `||y||²_W = ||g||²_W + ||r||²_W`
   - Identity and weighted cases
   - Aperture + Closure = 1.0

3. **Reconstruction Tests** (2) - Verify: `y = g + r`
   - Exact reconstruction
   - Weighted reconstruction

4. **Scale Invariance Tests** (3) - Verify invariants under scaling
   - Aperture invariant under `y → c·y` (measurement scaling)
   - Aperture and projections invariant under `W → c·W` (weight scaling)
   - Gauge determinism (`x[0]=0` gives unique result)

5. **Superintelligence Index Tests** (3) - Verify: `SI(A) = SI(A*²/A)`
   - Symmetric deviations from A*
   - Perfect alignment (SI = 100 at A*)
   - Monotonic decrease away from A*

6. **Alignment Rate Tests** (4) - Test AR categorization thresholds
   - SLOW boundary (0.03/min)
   - SUPERFICIAL boundary (0.15/min)
   - Formula validation
   - Invalid value handling

7. **Gauge Fixing Tests** (2) - Verify gauge constraint: `x[0] = 0`
   - Fixed reference vertex
   - 3 free parameters (x[1], x[2], x[3])

8. **Edge Cases** (3) - Boundary conditions
   - Uniform measurements
   - Small/zero weights
   - Extreme measurement values

## Running Tests

### As standalone script

```bash
python tests/test_geometry_properties.py
```

The script will run all tests and provide a summary of passed/failed tests.

## Requirements

```bash
pip install numpy
```

No additional testing frameworks required - tests run as a standard Python script.

## Mathematical Background

The tests verify properties from the theoretical foundations documented in:
- `docs/theory/Measurement.md` - Tensegrity decomposition mathematics
- `docs/theory/CommonGovernanceModel.md` - CGM balance geometry

### Key Properties

**Orthogonal Decomposition:**
```
y = B^T x + r
<B^T x, r>_W = 0
||y||²_W = ||B^T x||²_W + ||r||²_W
```

**Aperture Ratio:**
```
A = ||r||²_W / ||y||²_W
Target: A* ≈ 0.0207 (from CGM Balance Universal)
```

**Superintelligence Index:**
```
SI = 100 / D
D = max(A/A*, A*/A)
SI ∈ (0, 100], SI = 100 ⟺ A = A*
```

**Alignment Rate:**
```
AR = median(QI) / median(duration_minutes)
SLOW: AR < 0.03/min
VALID: 0.03 ≤ AR ≤ 0.15/min
SUPERFICIAL: AR > 0.15/min
```

**Scale Invariance:**
```
A(c·y, W) = A(y, W)  for c > 0
A(y, c·W) = A(y, W)  for c > 0
SI(c·y) = SI(y)      for c > 0
```

## Interpretation

- **All tests passing**: Mathematical implementation is sound and consistent with theory
- **Orthogonality failures**: Issue with weighted least squares or gauge fixing
- **Energy conservation failures**: Numerical instability or projection error
- **SI symmetry failures**: Formula implementation bug
- **AR boundary failures**: Threshold misconfiguration

## Adding New Tests

When adding new geometric or metric calculations:

1. **Define the mathematical property** from theory docs
2. **Create test cases** covering:
   - Typical values
   - Edge cases (zeros, extremes, uniform)
   - Random configurations
3. **Set tight tolerances** (< 1e-8 for exact properties)
4. **Document the theory** in test docstrings

Example template:

```python
class TestNewProperty:
    """Test [property name]: [mathematical statement]."""
    
    def test_property_typical_case(self):
        """[Description of what's being tested]."""
        # Setup
        # Compute
        # Assert with clear failure message
```

## Continuous Integration

These tests should run on every commit to ensure mathematical correctness is preserved across refactoring.

