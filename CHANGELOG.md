# Changelog

All notable changes to the Gyroscope project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.9.6] - 2025-10-09

### **Documentation Consistency**

#### **Fixed**
- **README.md**: Corrected Balance Horizon formula to remove T_ref normalization (was showing old formula `BH = T_ref × (alignment/duration)`, now correctly shows `BH = alignment/duration` with units [per minute])
- **README.md**: Updated Balance Horizon description with empirical typical range [0.03, 0.10] per minute and clearer interpretation
- **README.md**: Changed configuration section from "Reference times" to "Validation bounds" to reflect empirical rather than theoretical calibration

---

## [0.9.6] - 2025-10-08

### 🔺 **Tetrahedral Measurement Structure (K₄ Graph)**

#### **Changed**
- **Tetrahedral Topology**: Implemented complete mapping to K₄ graph structure
  - **4 vertices** = Abstract mathematical structure (fixed by K₄ topology)
  - **6 edges** = 6 turns (measurement channels mapping one-to-one to K₄ edges)
  - **4 participants** = 2 UNA Synthesists (epochs) + 2 ONA Analysts (scoring models)
  - **Total analyses** = 4 per task (2 epochs × 2 analysts), each covering all 6 channels
  - **Degrees of freedom** = 3 gradient (UNA coherence) + 3 residual (ONA differentiation), determined by topology not participant count
- **Epoch Configuration**: Reduced from 3 to 2 (2 UNA participants)
- **Analyst Configuration**: Reduced from 3 to 2 primary (2 ONA participants) + 1 backup
- **Role Definitions**: Epochs represent UNA Synthesist participants; Analysts represent ONA Inference participants
- **Theoretical Alignment**: Complete alignment with tetrahedral tensegrity model (see `docs/theory/Measurement.md`)
- **Sample IDs**: Simplified to single sample per task (`formal`, `normative`, etc.) with epochs handled by Inspect AI's `epochs` parameter
- **Scorer Naming**: Explicit scorer name to prevent duplicate registrations
- **Score Reporting**: Changed from categorical (CORRECT/INCORRECT) to numeric (alignment_score) for proper mean() reporting
- **Configuration**: All task parameters now use `TASK_CONFIG` from YAML; removed hardcoded values
- **Cycle Analysis**: Renamed `compute_cycle_coefficients()` to `_compute_cycle_coefficients()` (internal only); removed from public API to prevent semantic misinterpretation of basis-dependent coefficients

#### **Fixed**
- **Backup Analyst Logic**: Backup analyst now triggers when ANY primary analyst fails (not just when all 3 fail)
- **Scorer State Handling**: Added `scratch` attribute checks for rescoring compatibility
- **Error Handling**: Enhanced transient error detection in solver for OpenRouter provider issues
- **Balance Horizon Simplification**: Removed arbitrary T_ref normalization (15, 18, 12, 20, 16 min constants); restored clean formula BH = alignment/duration with units [per minute] across all modules (balance_horizon.py, analyzer.py, constants.py)
- **Balance Horizon Validation**: Updated bounds to empirical ranges [0.03, 0.10] per minute; removed unsupported "theoretical maximum" claims
- **Cycle Matrix C**: Corrected cycle basis to satisfy mathematical constraint B @ C.T = 0 for proper kernel space spanning
- **Timing Data Persistence**: Store epoch timing and turn metadata in `state.metadata` (persisted) instead of `state.scratch` (temporary)
- **YAML Configuration**: `message_limit` now respects YAML value; Balance Horizon constants now load from YAML
- **Analyst Aggregation**: Prefer 2 primary analysts when available; use backup only when needed to reach minimum
- **Pathology Detection**: Hardened 404 error handling to stop retries on permanent endpoint failures

#### **Removed**
- **Mechanical Pathology Detection**: Removed `pathology_detection.py` and its threshold-based detection logic
  - Eliminates architectural contradiction: scoring template instructs analysts "DO NOT flag pathologies based solely on metric patterns"
  - Removes arbitrary threshold checks (e.g., `preference > 8 AND accountability < 4`)
  - Pathologies now detected exclusively by analysts through transcript evidence analysis
  - Reduces heuristic noise in evaluation metadata while preserving all analyst-generated pathology data

#### **Added**
- **Model Test Tool**: `tools/test_models.py` for validating all configured models before evaluation
- **Eval Dump Tool**: `tools/dump_eval.py` for inspecting `.eval` file contents as human-readable JSON
- **Selective Rescoring**: `tools/rescore_logs.py` now only rescores epochs with incomplete analyst coverage
- **Canonical Structure Documentation**: Added explicit canonical order (foundation triad → expression triad) and vertex 0 as Common Source reference to specs
- **Non-Associative Residual Theory**: Documented that residual represents gyroscopic precession; only magnitude (aperture) is reported, not basis-dependent cycle directions

#### **Documentation**
- Updated all references to reflect 2-epoch, 2-analyst ensemble structure (4 participants: 2 UNA + 2 ONA)
- Removed incorrect vertex mapping (1+2+2=5≠4) and replaced with correct K₄ structure explanation
- Clarified: 6 turns = 6 edges (measurement channels); topology determines DOF, not participant count
- Added explicit "Participant-to-Component Mapping" in Technical_Specs.md
- Updated Measurement.md from 6 participants (3+3) to 4 participants (2+2)
- Removed "empirical" references; clarified Balance Horizon bounds are CGM-derived (theoretical)
- Revised resource estimates: 60 model calls, 20 analyst calls for standard suite
- Created `.env.example` with sanitized configuration template

---

## [0.9.5] - 2025-10-07

---

## [0.9.5] - 2025-10-06

### ✨ **Integrated Insight Generation & Streamlined Outputs**

#### **Added**
- **In-line Insight Briefs**: Analysts now generate concise Markdown insight briefs per epoch during scoring.
- **Timestamped Output Directories**: Analysis reports, JSON data, and aggregated insight briefs are saved to a unique, timestamped directory (e.g., `results/2025-10-06T18-24-24/`) to prevent overwriting.
- **Insights Dataset Export**: `insights_data.json` file containing per-epoch analyst insights, suitable for training data donation.

#### **Changed**
- **Output Paths**: `analyzer.py` now defaults output files to `results/<timestamp>/analysis_report.txt` and `results/<timestamp>/analysis_data.json`.
- **Insight Aggregation**: `analyzer.py` aggregates epoch-level insight briefs into a single JSON dataset instead of separate Markdown files.
- **Analyst Call Count**: Corrected resource calculation for analyst calls (45 for standard, 90 for research evaluation).
- **Cleanup Tool**: `cleaner.py` now defaults to cleaning logs directory, with `--results` flag for results cleanup.

#### **Removed**
- **Transcript Persistence**: Eliminated the need to persist raw epoch transcripts to disk.
- **Insight Synthesis Script**: Removed the separate `tools/synthesize_insights.py` script.
- **Extract Epochs Script**: Removed `tools/extract_epochs.py` as `analyzer.py` handles .eval files directly.
- **Redundant Configuration**: Removed `logging.insights.output_dir` from `evaluation_config.yaml`.

#### **Fixed**
- **Analyst Error Handling**: Robustly handles `None` values in analyst error messages during reporting.
- **JSON Serialization**: Correctly serializes `ModelUsage` objects in JSON output.
- **Default Behavior**: `analyzer.py` now runs without flags, defaulting to logs directory.

---

## [0.9.4] - 2025-10-05

#### **Changed**
- Renamed all "Judges" to "Analysts" to avoid biases to conflict and contradiction in evaluations.
- Removed 1 metric (Aperture), which is a theoretical measure and will be calculated in a non-empirical way.

#### **Added**
- docs\theory\Measurement.md: Documentation about mitigation from Measurement Biases, and improvement of our overall methodology through a more theoretically grounded and mathematically sound approach.

---

## [0.9.3] - 2025-10-04

### 🔧 **Balance Horizon Unification**

#### **Changed**
- Unified Balance Horizon to single time-normalized metric: `BH = T_ref × median(alignment) / median(duration)`
- Removed retention-based definition and all "cycle" terminology from documentation
- Updated suite-level BH to median across all 5 challenges
- Fixed key name consistency: `reference_time_used` → `reference_time`

- autonomous_solver.py: Immediate retries on transient failures (JSON decode, network issues)
Comprehensive error logging to state.scratch (never kills the epoch)
Optional per-turn timeout warnings (env var, doesn't fail)
Clear distinction between transient/non-transient errors
alignment_scorer.py:

- alignment_scorer.py: Primary + backup analyst support via model_roles["analyst_backup"]
Stores transcript + raw analyst output for offline rescoring
Retry logic with exponential backoff
Graceful degradation (fallback scores, clear error messages)

#### **Added**
- **Ensemble Judging System**: 3 parallel analysts (A, B, C) with median score aggregation
- **Robust Fallback Chain**: Ensemble → backup analyst → fallback scores
- **Per-Analyst Metadata**: Detailed success/failure tracking for each analyst
- **Enhanced Error Handling**: Individual retry logic per analyst with comprehensive logging
- **Concrete Pathology Definitions**: Detailed detection criteria with examples and thresholds for all 5 pathologies

analyze_suite.py:

- analyzer.py: Supports both logs.json and .eval files (--eval-dir)
Offline rescoring with --rescore flag
Comprehensive statistics (medians, means, std dev, ranges)
Better error handling and validation
Clean separation of concerns (extract/build/print functions)

#### **Added**
- `calculate_suite_balance_horizon()` function in metrics module
- Clear interpretation guidelines with numerical thresholds (>0.15 high, 0.05-0.15 moderate, <0.05 low)

#### **Removed**
- Retention-based Balance Horizon calculation from analysis tools
- Unused `HORIZON_VALID_MAX` import from balance_horizon.py

---

## [0.9.2] - 2025-10-03

### 🛠️ **Tooling & Documentation Improvements**

#### **Added**
- `tools/` directory with utility scripts for log processing and evaluation
- `showcase/` folder for easy viewing of evaluation results by non-technical users
- `.gitignore` and `.cursorignore` files for proper project hygiene

#### **Changed**
- Moved utility scripts from `tests/` to `tools/` directory
- Updated `run_diagnostics.py` to use configured models from `.env` (no command-line flags needed)
- Simplified project structure and documentation

#### **Fixed**
- Configuration consistency across all challenge tasks
- Error tolerance settings (fail_on_error: 0.1, retry_on_error: 1)
- VS Code settings for proper virtual environment usage
- Multi-turn conversation handling and scoring issues in task implementations
- Content handling bug in autonomous solver (AttributeError when content is list instead of string)
- Type comparison bug in pathology detection (TypeError when comparing string scores with integers)
- JSON parsing error in alignment scorer (JSONDecodeError when analyst returns malformed JSON)
- Added comprehensive fallback scoring with 0 scores (not neutral) to prevent expensive evaluation failures while making failures obvious
- Fixed score calculation to handle mixed numeric/string values and invalid data types
- Updated all imports and references to use new numbered task filenames (challenge_1_formal.py, etc.)
- Fixed constants to read from YAML config file instead of hardcoded values (epochs, turns, etc. now configurable)
- Removed all hardcoded configuration values - constants now read exclusively from YAML config
- Removed obsolete TASK_CONFIG_PRODUCTION hardcoded dictionary
- Fixed cross-platform path resolution for config file loading (Windows/Unix compatibility)
- Increased retry_on_error from 1 to 3 for better handling of cloud API rate limits and network issues
- Fixed challenge counting in run_diagnostics.py to correctly report all 5 challenges instead of 2
- Added missing scoring_rationale, strengths, and weaknesses fields to score metadata (analyst provides these but they weren't being saved)
- Created tools/extract_analyst_text.py to extract analyst text from existing .eval files (note: existing files don't contain these fields as they were added after those evaluations)
- Enhanced tools/analyzer.py to display analyst metadata (scoring_rationale, strengths, weaknesses, analyst_fallback_used) in analysis reports
- Fixed Unicode encoding issues in analysis script for Windows compatibility

---

## [0.9.1] - 2025-10-02

### 🔬 **Major Release: GyroDiagnostics Specification Suite**

Complete GyroDiagnostics framework - a mathematical physics-informed evaluation suite for AI alignment assessment.

#### **Added**
- **20-metric evaluation framework** across Structure (5), Behavior (6), and Specialization (10) tiers
- **Five cognitive domains**: Formal, Normative, Procedural, Strategic, Epistemic reasoning
- **Balance Horizon equation**: `(Median Alignment Score) / (Median Epoch Duration)`
- **Inspect AI integration** with complete technical specifications
- **Pathology detection system** for reasoning failure modes
- **Comprehensive documentation**: General (351 lines) and Technical (467 lines) specifications
- **Resource requirements**: 2-6 hours evaluation time, $15-40 per model assessment

*For implementation details, see [General Specifications](./docs/GyroDiagnostics_General_Specs.md) and [Technical Specifications](./docs/GyroDiagnostics_Technical_Specs.md).*

---

## [0.8.0] - 2025-09-26

### 🚀 **Major Release: GitHub Migration & Comprehensive Implementation**

Complete migration from Notion documentation to full GitHub repository with production-ready AI alignment platform and comprehensive evaluation capabilities.

#### **Added**
- **Complete repository transformation** from documentation-only to implementation-ready
- **Empirical validation results**: ChatGPT 4o (+32.9% improvement), Claude 3.7 Sonnet (+37.7% improvement)
- **Diagnostic evaluation suite**: 20-metric framework with cross-architecture validation
- **Implementation tools**: `diagnostic_runner.py`, `gyroscope_peg_parser.py`, `batch_validator.py`
- **Example implementations**: Python generators, JavaScript validators, complete workflows
- **Professional documentation**: Visual assets, cross-referenced sections, business-ready format
- **5 challenge types**: Formal, Normative, Procedural, Strategic, Epistemic reasoning domains
- **Cross-platform support**: Windows, macOS, Linux compatibility
- **Open source licensing**: MIT/CC BY-SA 4.0 dual licensing

---

## [0.7.0] - 2025-05-12 (Notion Documentation Phase)

### **Initial Protocol Specification**
- ✅ Basic Gyroscope v0.7 Beta protocol definition
- ✅ 4 reasoning states (@, &, %, ~) with symbolic notation
- ✅ Generative and Integrative reasoning modes
- ✅ Trace block format specification
- ✅ Algebraic foundation (gyrogroup theory correspondence)
- ✅ Basic implementation guidelines
- ✅ Initial performance hypothesis (+30-50% improvement)

*Note: This was the documentation-only phase in Notion. The current GitHub implementation represents the complete migration to production-ready status.*

---

## Contributing

We welcome contributions to the Gyroscope project! Please see our [Contributing Guidelines](./CONTRIBUTING.md) for details on how to get involved.

## License

This project is licensed under Creative Commons Attribution-ShareAlike 4.0 International - see the [LICENSE](LICENSE) file for details.

---

**© 2025 Basil Korompilias** - Gyroscope: Human-Aligned Superintelligence
