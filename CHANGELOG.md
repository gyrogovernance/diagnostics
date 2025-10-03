# Changelog

All notable changes to the Gyroscope project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.9.2] - 2025-10-03

### 🛠️ **Tooling & Documentation Improvements**

#### **Added**
- `tools/` directory with utility scripts for log processing and evaluation
- `showcase/` folder for easy viewing of evaluation results by non-technical users
- `.gitignore` and `.cursorignore` files for proper project hygiene
- `tools/add_to_showcase.py` script to automatically format and add results to showcase

#### **Changed**
- Moved utility scripts from `tests/` to `tools/` directory
- Updated `run_full_suite.py` to use configured models from `.env` (no command-line flags needed)
- Simplified project structure and documentation

#### **Fixed**
- Configuration consistency across all challenge tasks
- Error tolerance settings (fail_on_error: 0.1, retry_on_error: 1)
- VS Code settings for proper virtual environment usage
- Multi-turn conversation handling and scoring issues in task implementations

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
