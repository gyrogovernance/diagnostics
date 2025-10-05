# AI Safety Diagnostics
> **Gyroscopic Alignment Evaluation Lab**

![Gyroscope: Human-Aligned Superintelligence](/assets/diagnostics_cover.png)


<div align="center">

### G Y R O G O V E R N A N C E

[![Home](./assets/menu/home_badge.svg)](https://gyrogovernance.com)
[![Diagnostics](./assets/menu/diagnostics_badge.svg)](https://github.com/gyrogovernance/diagnostics)
[![Tools](./assets/menu/tools_badge.svg)](https://github.com/gyrogovernance/tools)
[![Science](./assets/menu/science_badge.svg)](https://github.com/gyrogovernance/science)
[![Superintelligence](./assets/menu/superintelligence_badge.svg)](https://github.com/gyrogovernance/superintelligence)

</div>

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Inspect AI](https://img.shields.io/badge/UK%20AISI-Inspect%20AI-red?style=for-the-badge)](https://inspect.aisi.org.uk/)

</div>

---

# GyroDiagnostics: AI Alignment Evaluation Suite

**Mathematical Physics-Informed Evaluation Framework for AI Model Quality and Alignment**

## Overview

GyroDiagnostics is a comprehensive evaluation suite for AI alignment assessment. The suite evaluates Machine Learning intelligence quality through structural coherence analysis while detecting reasoning pathologies including hallucination, sycophancy, goal drift, and contextual memory degradation.

The framework serves a dual purpose in advancing AI safety and capability development. First, it provides rigorous diagnostics of AI system structural health through mathematical assessment of alignment characteristics, enabling organizations to understand model reliability and identify architectural improvements needed for high-stakes deployment. Second, the evaluation process generates substantive research contributions by extracting novel solution pathways, critical trade-offs, and innovative approaches from model responses to real-world challenges across domains including poverty alleviation, regulatory frameworks, and knowledge synthesis. These insights, contextualized by structural health metrics, offer valuable resources for model fine-tuning and contribute meaningful analysis to the broader research community addressing these complex societal challenges.

---

## Key Insights

- **Structural Balance**: Alignment emerges from mathematical balance between coherence (closure) and differentiation (openness), grounded in the Common Governance Model (CGM)
- **Tetrahedral Topology**: Eliminates role-based bias through geometric neutrality - no designated 'critics' or 'supporters'
- **Pathology Detection**: Identifies 5 specific failure modes (sycophantic agreement, deceptive coherence, goal misgeneralization, superficial optimization, semantic drift)
- **Temporal Stability**: Balance Horizon reveals whether capabilities are brittle or stable over extended operation

---

## Architecture

### Five Challenge Domains

- **Formal**: Derive spatial structure from gyrogroup dynamics (Physics + Math)
- **Normative**: Optimize resource allocation for global poverty (Policy + Ethics)
- **Procedural**: Specify recursive computational process (Code + Debugging)
- **Strategic**: Forecast AI regulatory evolution (Finance + Strategy)
- **Epistemic**: Examine reasoning and communication under constraints (Knowledge + Communication)

Each challenge is designed with **one-shot unsolvability** in mind, requiring sustained multi-turn reasoning that cannot be completed in a single response. These default challenges can be customized or replaced according to specific evaluation needs.

### 20-Metric Rubric

**Structure Metrics (40 points)**
- Traceability, Variety, Accountability, Integrity

**Behavior Metrics (60 points)**
- Truthfulness, Completeness, Groundedness, Literacy, Comparison, Preference

**Specialization Metrics (20 points)**
- Domain-specific expertise (2 metrics per challenge)

**Balance Horizon**

Time-normalized alignment metric per challenge:

`Balance Horizon = T_ref(challenge) × (Median Alignment / Median Duration in minutes)`

Suite-level Balance Horizon is the median across the five challenges.

### Ensemble Analysis System

**Robust Evaluation**: Three parallel AI analysts evaluate each response sequence independently, with scores aggregated using median per metric to reduce bias and improve reliability.

**Fallback Chain**: If ensemble analysts fail, the system attempts a backup analyst before falling back to default scoring, ensuring evaluation continuity.

**Per-Analyst Tracking**: Detailed metadata captures each analyst's performance, enabling analysis of inter-analyst agreement and systematic scoring patterns.

---

## Evaluation Outputs

Each complete evaluation generates:
- **Per-Epoch Results**: Detailed scores across all 20 metrics with analyst metadata
- **Challenge Summaries**: Aggregated performance with pathology detection
- **Suite-Level Report**: Overall Balance Horizon and cross-challenge patterns
- **Research Insights**: Extracted solution pathways and novel approaches from model responses

---

## Showcase

Sample evaluation results demonstrating what GyroDiagnostics produces:

- 📊 [Results Analysis](showcase/results.txt)
Detailed per-epoch extraction report showing Meta-Llama 3.3 70B performance across 30 evaluation epochs (6 per challenge type). Includes alignment scores, duration metrics, structure analysis, behavior assessment, and domain-specific specialization scores.

- 📋 [Performance Review](showcase/review.md)
Comprehensive analysis report covering challenge-specific performance, cross-challenge patterns, pathological behavior detection (zero detected), and strategic insights across Formal, Normative, Procedural, Strategic, and Epistemic challenges.

---

## Theoretical Foundation

- **Common Governance Model (CGM)**: Mathematical framework deriving emergent structure from single axiom through gyrogroup theory
- **Recursive Systems Theory**: Evaluates structural dynamics rather than surface behaviors
- **Topological Analysis**: Measures foundational properties determining reliable intelligence

### Documentation

- **Theory**: [CGM: Gyroscopic Science Repository](https://github.com/gyrogovernance/science)
- **General Specs**: [GyroDiagnostics General Specifications](docs/GyroDiagnostics_General_Specs.md)
- **Technical Specs**: [GyroDiagnostics Technical Specifications](docs/GyroDiagnostics_Technical_Specs.md)

---

## 📄 Based on Paper

**AI Quality Governance**  
*Human Data Evaluation and Responsible AI Behavior Alignment*

[![View Publication](https://img.shields.io/badge/📖%20View%20Publication-4A90E2?style=for-the-badge&labelColor=2F2F2F)](http://doi.org/10.17613/43wc1-mvn58)

---

## Next Improvements

**Common Consensus Alignment: Human-AI Agreement Info-set Dynamics**

Tensegrity Mapping based on Tetrahedron Topology, inspired by Stafford Beer's work (Cybernetics Theory).

Notes:
[Measurement Analysis: Info-Set Dynamics for Alignment](/docs/theory/Measurement.md)

---

## Configuration

Edit `config/evaluation_config.yaml` to customize:

- **Model selection**: Choose models to evaluate and analyst models for scoring
- **Reference times**: Calibrate expected durations per challenge type (from pilot runs)
- **Safety limits**: Adjust time/token limits for operational constraints
- **Production mode**: Enable error tolerance for deployment vs. strict research mode

Most parameters (scoring weights, epochs, rubric structure) are fixed by the theoretical framework.

---

## Project Structure

```
gyrodiagnostics/
├── src/gyrodiagnostics/
│   ├── tasks/           # Five challenge implementations
│   ├── solvers/         # Autonomous progression solver
│   ├── scorers/         # 20-metric alignment scorer
│   ├── metrics/         # Balance Horizon calculation
│   ├── prompts/         # Challenge prompts & scoring templates
│   └── utils/           # Constants and helpers
├── tools/               # Utility scripts for log processing and analysis
│   ├── run_full_suite.py      # Run complete evaluation suite
│   ├── cleanup_results.py     # Manage results folder
│   ├── validate_setup.py      # Validate configuration
│   └── README.md              # Tools documentation
├── showcase/            # Sample evaluation results for easy viewing
├── config/              # Configuration files
└── docs/                # Theory and specifications
```

---

## Installation

```bash
# Clone the repository
git clone https://github.com/gyrogovernance/diagnostics.git
cd diagnostics

# Install dependencies
pip install -r requirements.txt

# Install package in editable mode (REQUIRED for imports to work)
pip install -e .

# Validate setup
python tools/validate_setup.py
```

**Note**: The `pip install -e .` step is **required** for the package imports to work correctly, especially when running in debug mode or from different contexts.

### Configure Environment

Create a `.env` file in the project root by copying the example:

```bash
cp .env.example .env
```

Then edit `.env` with your actual API keys:

```ini
# Primary Model (the one being evaluated)
INSPECT_EVAL_MODEL=openai/gpt-4o

# Analyst Model (for scoring - can be same or different)
INSPECT_EVAL_MODEL_GRADER=openai/gpt-4o

# API Keys (replace with your actual keys)
OPENROUTER_API_KEY=your_openrouter_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# Log Configuration
INSPECT_LOG_DIR=./logs
INSPECT_LOG_LEVEL=info

# Evaluation Settings
INSPECT_EVAL_MAX_RETRIES=1
INSPECT_EVAL_MAX_CONNECTIONS=8
```

---

## Quick Start

### Using Inspect AI CLI (Recommended)

```bash
# Run a single challenge
inspect eval src/gyrodiagnostics/tasks/challenge_1_formal.py

# Run with specific model
inspect eval src/gyrodiagnostics/tasks/challenge_1_formal.py \
  --model openai/gpt-4o \
  --model-role grader=openai/gpt-4o

# Run with limit (for testing)
inspect eval src/gyrodiagnostics/tasks/challenge_1_formal.py --limit 1
```

### Using Python Scripts

```bash
# Run full evaluation suite (uses configured models from .env)
python tools/run_full_suite.py

# Validate setup
python tools/validate_setup.py
```

### Analyze Results

```bash
# Analyze suite results from JSON logs (comprehensive analysis)
python tools/final_analysis.py logs/logs.json --output report.txt

# Clean up results folder
python tools/cleanup_results.py --list
```
---

## Tools

The `tools/` directory contains utility scripts for working with evaluation results and running the complete suite. See [tools/README.md](tools/README.md) for detailed documentation.

### Key Tools

- **`run_full_suite.py`**: Run all 5 challenges using configured models from `.env`
- **`extract_epochs.py`**: Extract per-epoch data from .eval logs (bypasses logs.json)
- **`final_analysis.py`**: Comprehensive analysis of suite results with analyst metadata and Balance Horizon
- **`cleanup_results.py`**: Manage and organize the results folder
- **`validate_setup.py`**: Verify that your configuration is correct

### Quick Tool Usage

```bash
# Run complete evaluation suite
python tools/run_full_suite.py

# Extract per-epoch data from .eval logs (bypasses logs.json)
python tools/extract_epochs.py logs --output report_epochs.txt --json epochs.json

# Analyze suite results (comprehensive analysis with analyst metadata)
python tools/final_analysis.py logs/logs.json --output report.txt

# Clean up old results
python tools/cleanup_results.py --older-than 7 --confirm
```

---

## Contributing

This is a research framework under active development. Contributions welcome via issues and pull requests.

## 📖 Citation

If you use Gyroscope in your research or work, please cite:

```bibtex
@misc{gyrogovernancediagnosticsrepo,
  title={AI Safety Diagnostics: Gyroscopic Alignment Evaluation Lab},
  author={Korompilias, Basil},
  year={2025},
  howpublished={GitHub Repository},
  url={https://github.com/gyrogovernance/diagnostics},
  note={mathematical physics informed frameworks}
}
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

© 2025 Basil Korompilias.

---

<div style="border: 1px solid #ccc; padding: 1em; font-size: 0.6em; background-color: #f9f9f9; border-radius: 6px; line-height: 1.5;">
  <p><strong>🤖 AI Disclosure</strong></p>
  <p>All software architecture, design, implementation, documentation, and evaluation frameworks in this project were authored and engineered by its Author.</p>
  <p>Artificial intelligence was employed solely as a technical assistant, limited to code drafting, formatting, verification, and editorial services, always under direct human supervision.</p>
  <p>All foundational ideas, design decisions, and conceptual frameworks originate from the Author.</p>
  <p>Responsibility for the validity, coherence, and ethical direction of this project remains fully human.</p>
  <p><strong>Acknowledgements:</strong><br>
  This project benefited from AI language model services accessed through LMArena, Cursor IDE, OpenAI (ChatGPT), Anthropic (Claude), XAI (Grok), Deepseek, and Google (Gemini).</p>
</div>
