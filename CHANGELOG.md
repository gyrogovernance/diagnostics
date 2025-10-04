# Changelog

All notable changes to the Gyroscope project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

- alignment_scorer.py: Primary + backup judge support via model_roles["grader_backup"]
Stores transcript + raw judge output for offline rescoring
Retry logic with exponential backoff
Graceful degradation (fallback scores, clear error messages)
analyze_suite.py:

- final_analysis.py: Supports both logs.json and .eval files (--eval-dir)
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
- Updated `run_full_suite.py` to use configured models from `.env` (no command-line flags needed)
- Simplified project structure and documentation

#### **Fixed**
- Configuration consistency across all challenge tasks
- Error tolerance settings (fail_on_error: 0.1, retry_on_error: 1)
- VS Code settings for proper virtual environment usage
- Multi-turn conversation handling and scoring issues in task implementations
- Content handling bug in autonomous solver (AttributeError when content is list instead of string)
- Type comparison bug in pathology detection (TypeError when comparing string scores with integers)
- JSON parsing error in alignment scorer (JSONDecodeError when judge returns malformed JSON)
- Added comprehensive fallback scoring with 0 scores (not neutral) to prevent expensive evaluation failures while making failures obvious
- Fixed score calculation to handle mixed numeric/string values and invalid data types
- Updated all imports and references to use new numbered task filenames (challenge_1_formal.py, etc.)
- Fixed constants to read from YAML config file instead of hardcoded values (epochs, turns, etc. now configurable)
- Removed all hardcoded configuration values - constants now read exclusively from YAML config
- Removed obsolete TASK_CONFIG_PRODUCTION hardcoded dictionary
- Fixed cross-platform path resolution for config file loading (Windows/Unix compatibility)
- Increased retry_on_error from 1 to 3 for better handling of cloud API rate limits and network issues
- Fixed challenge counting in run_full_suite.py to correctly report all 5 challenges instead of 2
- Added missing scoring_rationale, strengths, and weaknesses fields to score metadata (judge provides these but they weren't being saved)
- Created tools/extract_judge_text.py to extract judge text from existing .eval files (note: existing files don't contain these fields as they were added after those evaluations)
- Enhanced tools/final_analysis.py to display judge metadata (scoring_rationale, strengths, weaknesses, judge_fallback_used) in analysis reports
- Fixed Unicode encoding issues in analysis script for Windows compatibility

---

## [0.9.1] - 2025-10-02

### 🔬 **Major Release: GyroDiagnostics Specification Suite**

Complete GyroDiagnostics framework - a mathematical physics-informed evaluation suite for AI alignment assessment.

#### **Added**
- **21-metric evaluation framework** across Structure (5), Behavior (6), and Specialization (10) tiers
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
