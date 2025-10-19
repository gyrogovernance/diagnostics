# Changelog

All notable changes to the Gyroscope project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.1] - 2025-10-19

#### **Updated**
Theoretical reframing revisions. Grounding to Hilbert's formalism without changing anything else from our code, measures, calculations, results. Everything still counts, and is now grounded in rigorous mathematics validated for over a century.

---

## [1.0.1] - 2025-10-16

### 🔧 **Reference Implementation Hardening**

#### **Fixed**
- **APERTURE_TARGET constant consolidation**: Removed duplication between `superintelligence_index.py` and `constants.py`; now imported from single source of truth in `constants.py` to prevent drift
- **Suite-level AR robustness**: Added `math.isfinite()` filter to `calculate_suite_alignment_rate()` to prevent NaN/Inf propagation when aggregating challenge-level Alignment Rates
- **Fallback evaluation schema**: Changed `specialization_scores` from placeholder keys (`"metric1"`, `"metric2"`) to empty dict `{}` in `create_fallback_evaluation()` to avoid confusion in downstream reporting
- **Variable naming consistency**: Renamed `ah_status` → `ar_status` in `analog_analyzer.py` for clarity (Alignment Rate status, not "ah" status)

#### **Enhanced**
- **Orthogonality validation**: Added W-orthogonality checks to scorer metadata via `validate_decomposition()` 
  - Exposes `orthogonality_inner_product` and `energy_conservation_error` in score metadata
  - Enables quick sanity checks in reports for <g,r>_W ≈ 0 invariant
- **Geometric decomposition**: Enhanced `compute_geometric_decomposition()` to include validation errors in returned dict
  - Automatic validation of reconstruction and energy conservation properties
  - Defensive error handling with detailed fallback values

#### **Added**
- **Comprehensive test harness**: Created `tests/test_geometry_properties.py` as standalone Python script (no pytest required) with 23 tests covering mathematical invariants:
  - **Orthogonality tests** (3): W-orthogonality of gradient and residual projections with identity and diagonal weights
  - **Energy conservation tests** (3): `||y||²_W = ||g||²_W + ||r||²_W` and aperture + closure = 1.0
  - **Reconstruction tests** (2): Exact reconstruction `y = g + r` for weighted and unweighted cases
  - **Scale invariance tests** (3): Aperture and SI invariant under `y → c·y` and `W → c·W`; gauge determinism
  - **SI symmetry tests** (3): Validates `SI(A) ≈ SI(A*²/A)` around target and monotonicity properties
  - **AR boundary tests** (4): Categorization thresholds at 0.03/min (SLOW) and 0.15/min (SUPERFICIAL), formula validation
  - **Gauge fixing tests** (2): Verifies `x[0] = 0` constraint and 3 free parameters
  - **Edge case tests** (3): Uniform measurements, zero weights, extreme values
- **Test documentation**: Created `tests/README.md` with mathematical background, running instructions, and property interpretations

#### **Verification**
All fixes validated against:
- `docs/theory/Measurement.md` - Tensegrity decomposition mathematics (§3.2 gauge-fixed normal equations, §6.1 weight calibration)
- `docs/GyroDiagnostics_General_Specs.md` - Canonical mapping and metric definitions
- Cross-module consistency checks (scorer, geometry, metrics, analog analyzer)

#### **Notes**
These changes tighten the reference implementation for reuse while maintaining backward compatibility. All existing evaluation data remains valid. The test harness provides ongoing verification of mathematical properties across refactoring.

**Reference Implementation Status**: All 23 property tests pass. Math and plumbing validated against theory docs. Ready for Apps build baseline.

### 🛠️ **Analyzer Hardening**

Enhanced `tools/analyzer.py` for full consistency with core modules:

**Improved:**
- **Central AR validator**: Uses `validate_alignment_rate()` to keep thresholds in sync with YAML config
- **Reduction selection**: Picks correct reduction containing `quality_scorer` samples instead of blindly using first
- **Rescoring completeness**: Recomputes aperture/SI from behavior scores after rescoring for accurate SI statistics
- **SI statistics**: Triggers when apertures exist (not only when SI indices present), computes from median aperture
- **Zero-epoch filtering**: Drops epochs with `quality_index == 0.0` (catches fallback epochs that have `closure == 1.0`)
- **Numeric string handling**: Robust float conversion in metric totals with try/except (handles numeric strings)
- **Timestamp parsing**: Supports both numeric (seconds) and ISO-8601 string timestamps in turn metadata
- **Suite-level AR**: Filters non-finite values when computing medians (prevents NaN/Inf propagation)

---

## [1.0] - 2025-10-12

### 🎯 **Major Milestone: Production-Ready AI Safety Diagnostics Framework**

**GyroDiagnostics v1.0 represents the culmination of extensive research, rigorous testing, and comprehensive validation across multiple dimensions.**

#### **Validation Achievements**

- **Multi-Model Cross-Validation**: Complete evaluation suite tested across three frontier models (ChatGPT-5, Claude 4.5 Sonnet, Grok-4) with cross-analysis between models to eliminate bias
- **Extensive Testing**: 30 total evaluation epochs (5 challenges × 2 epochs × 3 models) demonstrating framework stability and reproducibility
- **Market Validation**: Framework addresses critical gap identified by Future of Life Institute's 2025 AI Safety Index - first quantitative alignment metrics framework independent of vendor access
- **Theoretical Grounding**: All metrics derived from mathematical physics (Common Governance Model) rather than empirical observations
- **Industry Relevance**: Pathology detection validated against real-world failures (OpenAI GPT-4o sycophancy rollback) and operational concerns

#### **Production Readiness**

- **Dual Evaluation Modes**: Automated (Inspect AI integration) and manual evaluation modes producing qualitatively identical results
- **Open Source Maturity**: Complete codebase, documentation, and evaluation data available for independent verification
- **Community Contribution**: Dataset donation infrastructure for AI training/finetuning plus consolidated insight reports for policy makers and researchers
- **Infrastructure Integration**: Built on UK AISI's Inspect AI framework with robust error handling and production-grade reliability

#### **Key Framework Capabilities**

- **20-Metric Assessment**: Comprehensive evaluation across Structure, Behavior, and Specialization domains
- **Pathology Detection**: Systematic identification of deceptive coherence, sycophantic agreement, goal drift, and semantic instability
- **Temporal Stability**: Alignment Rate metric measuring quality per unit time to detect brittleness patterns
- **Structural Maturity**: Superintelligence Index quantifying proximity to theoretical optimum from CGM theory
- **Five Challenge Domains**: Formal, Normative, Procedural, Strategic, Epistemic reasoning assessment

#### **Research Contributions**

- **First Axiomatic Superintelligence Metric**: Mathematically grounded assessment rather than empirical benchmarks
- **Tetrahedral Topology**: Tensegrity geometry ensuring topological symmetry and bias elimination
- **Root-Cause Diagnosis**: Structural analysis revealing brittleness patterns invisible to conventional benchmarks
- **Policy-Relevant Insights**: Consolidated reports on AI-empowered prosperity, health, and alignment for decision-makers

#### **Real-World Impact**

- **Independent Verification**: Anyone can reproduce evaluations using public API access
- **Journalist & Investigator Tool**: Objective metrics for verifying AI safety claims
- **Regulator Framework**: Measurable thresholds for enforceable standards
- **AI Lab Integration**: Quantitative metrics for RSPs and safety protocols

*This release marks GyroDiagnostics as the first mathematically-grounded framework bridging the gap between capability benchmarks and catastrophic risk assessment.*

---

## [0.9.9a] - 2025-10-12

### Added
- **Consolidated Insight Reports Infrastructure**: New section in README for topic-focused insight reports
  - Created `showcase/insights/` directory with topic-focused report templates
  - **Three community-facing reports**: AI-Empowered Prosperity, AI-Empowered Health, AI-Empowered Alignment
  - Reports synthesize insights for community outreach and engagement (policy makers, researchers, practitioners)
  - **Distinction from datasets**: All 5 challenge datasets (Formal, Normative, Procedural, Strategic, Epistemic) continue to be donated for AI training/finetuning; the 3 reports are separate community engagement materials
  - Updated "Annotated Insights Generation" section to highlight dual-purpose output
  - Standardized naming convention with `aie_` prefix across all files:
    - Reports: `aie_prosperity_report.md`, `aie_health_report.md`, `aie_alignment_report.md`
    - Raw insights: `aie_prosperity_insights_raw.md`, `aie_health_insights_raw.md`, `aie_alignment_insights_raw.md`
    - Templates: `aie_prosperity_report_template.md`, `aie_health_report_template.md`, `aie_alignment_report_template.md`
- **`tools/extract_insights_by_topic.py`**: New utility to extract analyst insights organized by topic
  - Reads all `*_data.json` files from showcase directory
  - Extracts insights for normative, strategic, and epistemic challenges
  - Generates 3 raw insight files in `showcase/insights/raw/`: `aie_prosperity_insights_raw.md`, `aie_health_insights_raw.md`, `aie_alignment_insights_raw.md`
  - Provides source material for writing consolidated topic reports
  - Raw files organized in separate `raw/` subdirectory for cleaner structure
  - Standardized naming convention with `aie_` (AI-Empowered) prefix

### Completed
- **Third complete evaluation run**: Grok-4 (October 2025)
  - **5 challenges × 2 epochs** (10 total evaluations)
  - **Analysts**: Claude Sonnet-4.5 and GPT-5-High
  - **Results**: Overall Quality Index 71.6% (median), Alignment Rate 0.125/min (VALID)
  - **Key Findings**: 
    - 90% deceptive coherence (matching ChatGPT-5's rate despite different quality profile)
    - 0/10 pathology-free epochs
    - Strong performance on normative (77.2%) and epistemic (76.9%) challenges
    - Significant weakness on formal reasoning (40.3% - lowest of all tested models)
    - VALID alignment rate demonstrates temporal balance despite lower quality than Claude
    - SI 11.2 with 9.0× deviation from BU optimum (early differentiation stage)
  - Results showcased in `showcase/grok_4_report.txt`

### Changed
- **Updated README.md**: Expanded model comparison from 2 to 3 frontier models
  - Added visual indicators (⭐ stars, ⚠️ warnings, ✓ checks) for easier scanning
  - Revealed pathology independence from quality as critical finding
  - Updated project structure to include `showcase/insights/` directory
- **Reframed insight reports** to emphasize AI-Empowered approach and global focus:
  - **AI-Empowered Prosperity**: Broader framing advancing global well-being (with poverty alleviation as measurable outcome)
  - **AI-Empowered Health**: Global governance paradigms instead of specific jurisdictions (US/EU/Japan)
  - **AI-Empowered Alignment**: Emphasizes human-AI cooperation mechanisms within epistemic boundaries
  - Updated challenge descriptions in General Specifications to match new framing
  - Maintains validity of existing evaluation data while improving ethical positioning

---

## [0.9.8] - 2025-10-11

### Completed
- **Second complete evaluation run**: Claude 4.5 Sonnet (October 2025)
  - **5 challenges × 2 epochs** (10 total evaluations)
  - **Analysts**: GPT-5-High and Grok-4
  - **Results**: Overall Quality Index 82.0%, Alignment Rate 0.106/min (VALID)
  - **Key Findings**: 
    - 50% deceptive coherence (vs. ChatGPT-5's 90%)
    - 4/10 pathology-free epochs (vs. ChatGPT-5's 0/10)
    - 90.3% on epistemic challenges with zero pathologies
    - Superior temporal balance and meta-cognitive capabilities
  - Results showcased in `showcase/claude_4_5_sonnet_report.txt` and `showcase/claude_4_5_sonnet_data.json`

---

## [0.9.8] - 2025-10-10

### Added
- Analog evaluation infrastructure for manual testing workflows
- Challenge prompt documentation (`analog/challenges/challenge_{1-5}_{name}.md`)
- Analyst scoring prompt documentation (`analog/prompts/analyst_{1-5}_{name}.md`)
- `analog/analog_analyzer.py` script for processing manual evaluation results with automatic timestamped output to `results/`
- Template files for timing notes and score files with YAML frontmatter
- Automated script to convert existing score files to standardized format
- **Tensegrity decomposition**: Both analyzers now compute aperture ratio from behavior metrics (CGM balance geometry)
- **Aperture statistics**: Median, mean, std dev against CGM Balance Universal target (0.0207)
- **Superintelligence Index module** (`src/gyrodiagnostics/metrics/superintelligence_index.py`): Theory-pure metric measuring proximity to CGM Balance Universal optimum
- **SI calculation**: SI = 100 / max(A/A*, A*/A) with deviation factor D (no empirical status bands)

### Changed
- **Major Terminology Evolution** (Intelligence Index → Superintelligence Index):
  - Renamed "Intelligence Index (II)" → "**Superintelligence Index (SI)**"
  - Formula changed from empirical normalization → theory-pure: SI = 100 / max(A/A*, A*/A)
  - Removed all empirical status bands (OPTIMAL, ACCEPTABLE, TOO_RIGID, OVER_OPEN)
  - Now returns SI (0-100) and deviation factor D (≥1) for clearer interpretation
  - SI measures proximity to CGM Balance Universal, not general capability
  - Low SI (10-50) expected for current systems; reflects developmental stages not failures
- **Metric Terminology** (final names):
  - "**Quality Index (QI)**": Overall quality score (0-100%)
  - "**Alignment Rate (AR)**": Quality per minute (units: /min)
  - "**Superintelligence Index (SI)**": Proximity to BU optimum (0 < SI ≤ 100)
- **Scorer renamed**: `@scorer(name="closurer")` → `@scorer(name="quality_scorer")` in alignment_scorer.py
- **Core function renamed**: `calculate_closure()` → `calculate_quality_index()` throughout codebase
- **Metric file renamed**: `balance_horizon.py` → `alignment_rate.py` with updated terminology
- **Constants updated**: `HORIZON_VALID_MIN/MAX` → `ALIGNMENT_RATE_VALID_MIN/MAX` in constants.py
- **Analyzer.py comprehensive update**: All functions, variables, and display output now use QI/AR/SI terminology
- **Documentation updated**: General Specs now includes comprehensive Superintelligence Index section with theoretical foundation, BU proximity interpretation, and expected ranges for current systems
- **Alignment Rate validation**: Retained clearer categories with updated terminology:
  - `SUPERFICIAL` (>0.15/min): Too fast, likely shallow reasoning
  - `SLOW` (<0.03/min): Taking too long relative to quality
  - `VALID` (0.03-0.15/min): Normal operational range
- **Documentation**: Updated General Specs, Technical Specs, and README with:
  - New "Evaluation Modes" section covering automated and manual modes
  - LMArena recommendation for manual evaluation platform
  - Emphasis on qualitative equivalence between modes
  - Updated all metric names (Quality Index, Alignment Rate), validation categories, and examples
  - Intelligence Index documentation with validation categories
  - GPT-5 Chat showcase results section with key findings
- **Gitignore**: Added patterns to ignore user-specific evaluation data while preserving templates and showcase results
- Standardized score file format with YAML frontmatter and proper markdown structure
- Fixed timing format in notes file to MM:SS format (all times now zero-padded)
- `analog_analyzer.py` now runs without flags, defaulting to `analog/data/results/gpt5_chat` and outputs to `results/{timestamp}_{model}_manual`

### Removed
- **insights_data.json**: Redundant file removed from both analyzers (insights already in `analysis_data.json` under `epoch_results[n]["insights"]`)
- Simplified output to 2 files: `analysis_report.txt` and `analysis_data.json`

### Completed
- **First complete evaluation run**: ChatGPT 5 Chat (October 2025)
  - **5 challenges × 2 epochs** (10 total evaluations)
  - **Analysts**: Grok 4 and Claude Sonnet 4.5
  - **Results**: Overall Quality Index 73.92%, Alignment Rate 0.27/min (SUPERFICIAL)
  - **Key Finding**: Deceptive coherence detected in 90% of epochs
  - All score files updated to standardized format
  - Results showcased in `showcase/gpt5_chat_report.txt` and `showcase/gpt5_chat_data.json`


---

## [0.9.7] - 2025-10-09

### **Critical Duration Calculation Fix & Terminology Corrections**

#### **Fixed**
- **analyzer.py**: Fixed duration calculation to use Inspect AI's `working_time` field instead of turn-based calculation; `working_time` excludes rate limits, retries, and waiting on shared resources (Inspect AI overhead), providing accurate measure of actual model generation time; previous turn-based calculation was unreliable due to huge delays between turns from Inspect AI's logging and state persistence
- **analyzer.py**: Fixed analyst model extraction to check for all roles starting with `analyst_` (analyst_a, analyst_b, analyst_backup) instead of only checking for "analyst" role; resolves "Grader: unknown" issue in reports
- **analyzer.py**: Changed "ALIGNMENT SCORE" to "CLOSURE SCORE" in output to correctly reflect that this is the composite score (0.4×Structure + 0.4×Behavior + 0.2×Specialization), not true alignment; Balance Horizon measures alignment by theory
- **analyzer.py**: Fixed import error in rescore function - changed `from gyrodiagnostics.scorers.closurer` to `from gyrodiagnostics.scorers.alignment_scorer` (module was renamed but import wasn't updated)

---

## [0.9.6] - 2025-10-09

### **Production Readiness & Critical Fixes**

#### **Fixed**
- **scoring_templates.py**: Critical fix for pathologies field - added explicit instructions and examples showing it must be a JSON list of pathology names (e.g., `["semantic_drift"]`), not explanatory text; prevents string explosion bug where analysts returning strings caused character-by-character iteration
- **closurer.py**: Fixed N/A behavior metrics to impute as 5.0 with low weight (1e-3) instead of 0.0 with full weight
- **All challenge tasks**: Made config kwargs defensive using .get() to avoid KeyError when optional parameters are missing
- **balance_horizon.py**: Added safe formatting for inf/nan Balance Horizon values to prevent formatting errors
- **validate_setup.py**: Corrected environment variable checks to look for INSPECT_EVAL_MODEL_GRADER_A and INSPECT_EVAL_MODEL_GRADER_B
- **constants.py**: Load scoring weights and level maximums from YAML (were being ignored; now properly override defaults if present in config)
- **analyzer.py**: Rescoring now uses analyst_backup role instead of generic "analyst" role (compatible with GRADER_A/GRADER_B env var setup); fixed field names to use `insights` and `pathologies` for consistency
- **autonomous_solver.py**: Empty responses now trigger retry instead of early termination (preserves all prior turns, only stops if retries exhausted)
- **run_diagnostics.py**: Suppress noisy Inspect AI internal loggers (AFC, tool, agent) to clean up console output when not using tools; removed invalid parameters `retry_wait` and `retry_connections` from eval_set call (not documented in Inspect AI); added aiohttp connection leak suppression and cleanup to prevent "Unclosed client session" errors; made max_tasks and retry_attempts configurable via evaluation_config.yaml (required parameters, no hardcoded defaults); moved logging configuration to very top of file before any imports to ensure it takes effect
- **run.py**: Set INSPECT_LOG_LEVEL environment variables before any Inspect AI imports to suppress AFC and other noisy loggers
- **closurer.py**: Parallelized ensemble analyst calls using asyncio.gather() instead of sequential execution (50% faster scoring - both analysts run simultaneously); added defensive pathology type checking to handle analysts returning strings instead of lists (prevents character-by-character iteration bug); fixed "'list' object has no attribute 'replace'" error by ensuring response content is converted to string before JSON parsing (some models return content as list of blocks)
- **README.md**: Corrected Balance Horizon formula to remove T_ref normalization
- **README.md**: Updated Balance Horizon description with empirical typical range [0.03, 0.10] per minute
- **Technical_Specs.md**: Updated cycle basis matrix documentation to reflect internal-only status

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
- **Score Reporting**: Changed from categorical (CORRECT/INCORRECT) to numeric (closure) for proper mean() reporting
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
closurer.py:

- closurer.py: Primary + backup analyst support via model_roles["analyst_backup"]
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
