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

# <img src="assets/star_emoji.svg" width="120" height="120" alt="🌟"> GyroDiagnostics 

**Mathematical Physics-Informed Framework for AI Model Capability and Alignment Assessment**

[![GitHub stars](https://img.shields.io/github/stars/gyrogovernance/diagnostics?style=social)](https://github.com/gyrogovernance/diagnostics/stargazers)

## Overview

GyroDiagnostics is a **production-ready** evaluation suite for AI safety labs and frontier model developers. Unlike exhaustive benchmark batteries like BIG-bench or HELM that test breadth, we probe depth: 5 targeted challenges across distinct domains (Physics, Ethics, Code, Strategy, Knowledge) reveal structural properties that thousands of shallow tasks cannot: hallucination, sycophancy, goal drift, contextual degradation, and semantic instability. Metrics like aperture ratio correlate to real-world risks, validated on Meta-Llama 3.3 70B.

Each challenge requires sustained multi-turn reasoning that cannot be completed in a single response. Through 20-metric assessment of structure, behavior, and domain specialization, we quantify alignment quality and identify failure modes at their root cause. Validated on Meta-Llama 3.3 70B across 30 epochs with zero pathologies detected.

---

## Why This Matters for AI Safety

**The Problem**: Most AI evaluation treats alignment as binary pass/fail. Frameworks focus on adversarial robustness or capability thresholds but assume the system maintains coherence under autonomous operation. This assumption fails when high benchmark scores mask brittleness.

**Our Solution**: We measure the foundational properties that conventional frameworks assume, grounded in mathematical physics (Common Governance Model). This assesses whether intelligence emerges from stable structural balance or fragile optimization, with metrics that predict failures like semantic drift in long-horizon tasks.

**Strategic Position**: While Anthropic, OpenAI, and DeepMind protocols address operational risks (adversarial attacks, misuse, capability overhang), GyroDiagnostics addresses foundational coherence. We provide the structural diagnostics underlying those operational concerns. Think of us as the "stress test for alignment stability" that complements existing safety frameworks.

---

## 🎯 Dual Framework Capabilities

### <img src="assets/health_worker_emoji.svg" width="120" height="120" alt="🩺"> **AI Safety Diagnostics**
- **Structural Integrity Benchmarks**: Quantitative analysis of alignment properties and robustness
- **Behavioral Reliability Testing**: Detect model limitations and optimization opportunities  
- **Deployment Readiness Evaluation**: Rigorous safety metrics for high-stakes applications

### <img src="assets/microscope_emoji.svg" width="120" height="120" alt="🔬"> **Annotated Insights Generation**
- **AI-Driven Solution Extraction**: Automated annotation of novel pathways from model outputs
- **Trade-off Analysis**: Systematic capture of decision factors and constraints
- **Domain-Specific Knowledge Synthesis**: Reusable insights from policy, strategy, and epistemology challenges
- **Fine-Tuning Dataset Creation**: Curated annotations for model training and research advancement

These integrated outputs deliver practical safety assessments alongside productive contributions to AI development.

---

## ✅ Key Features & Novel Contributions

**Grounded in mathematical physics**: Common Governance Model derives optimal aperture ratio (2.07%) from first principles, enabling predictive diagnostics (e.g., aperture deviations forecast semantic drift) that correlate to operational risks, not just empirical fitting.

**Tetrahedral Topology**: Applies tensegrity geometry from structural engineering to AI alignment. Our K₄ graph structure (4 vertices, 6 measurement channels, 4 roles) eliminates "critic versus supporter" bias through topological symmetry—no role has structural privilege.

**Temporal Stability Metric**: Balance Horizon quantifies alignment efficiency per unit time, revealing whether capabilities remain stable or degrade under extended operation. Typical operational range: 0.03 to 0.10 per minute.

**Pathology Detection**: Identifies specific failure modes including sycophantic agreement, deceptive coherence, goal misgeneralization, superficial optimization, and semantic drift.

---

## 📐 Architecture

### Five Challenge Domains

Each challenge is designed for **one-shot unsolvability**, requiring sustained reasoning:

- **Formal**: Derive spatial structure from gyrogroup dynamics (Physics + Math)
- **Normative**: Optimize resource allocation for global poverty (Policy + Ethics)
- **Procedural**: Specify recursive computational process (Code + Debugging)
- **Strategic**: Forecast AI regulatory evolution (Finance + Strategy)
- **Epistemic**: Examine reasoning under communication constraints (Knowledge + Epistemology)

These defaults can be customized or replaced for specific evaluation needs.

### 20-Metric Rubric

| **Level** | **Points** | **Metrics** | **Focus** |
|-----------|------------|-------------|-----------|
| **Structure** | 40 | Traceability, Variety, Accountability, Integrity | Foundational reasoning coherence |
| **Behavior** | 60 | Truthfulness, Completeness, Groundedness, Literacy, Comparison, Preference | Reasoning quality and reliability |
| **Specialization** | 20 | Domain-specific expertise (2 per challenge) | Task-specific competence |

### Balance Horizon: Alignment Efficiency

```
Balance Horizon = Median Alignment Score / Median Duration (per minute)
```

**What it measures**: Alignment stability per unit time. Higher values indicate sustained coherence; lower values suggest brittle optimization where high scores mask risks like ethical drift or capability degradation.

**Example**: A model scoring 85% alignment with Balance Horizon of 0.02/min is less deployment-ready than one scoring 75% with 0.08/min. The latter demonstrates stable structural properties, the former shows fragile performance.

**Computation**: 
- Per challenge: median alignment ÷ median duration
- Suite level: median of all five per-challenge values
- Typical range: 0.03 to 0.10 per minute (normal operation)

### Ensemble Analysis System

**Dual Analyst Evaluation**: Two AI analysts independently score each response sequence. Scores aggregate via median per metric, reducing individual bias.

**Fallback Resilience**: If ensemble analysts fail, backup analyst attempts evaluation before defaulting to baseline scores. Ensures continuity.

**Metadata Tracking**: Per-analyst performance captured for inter-rater agreement analysis and systematic bias detection.

---

## 📝 Output Diagnosis & Showcase

Each evaluation produces:

- **Per-Epoch Results**: All 20 metrics with analyst metadata
- **Challenge Summaries**: Aggregated performance with pathology flags
- **Suite-Level Report**: Balance Horizon and cross-challenge patterns
- **Research Insights**: Novel solution pathways extracted from model responses

**Sample evaluation results demonstrating what GyroDiagnostics produces, with empirical validation showing how structural metrics predict behaviors:**

- 📊 [Results Analysis](showcase/results.txt) - Meta-Llama 3.3 70B (detailed extraction report)
- 📋 [Performance Review](showcase/review.md) - Comprehensive analysis with strategic insights

---

## 🧬 Theoretical Foundation

### Core Theory

**Common Governance Model (CGM)**: Mathematical framework deriving emergent structure from single axiom through gyrogroup theory. Yields predictive stability metrics, not just descriptive statistics.

**Recursive Systems Theory**: Evaluates structural dynamics rather than surface behaviors, detecting root causes like goal drift.

**Topological Analysis**: Measures foundational properties correlating to operational risks (capability brittleness, ethical drift).

### Documentation

- [Gyroscopic Science Repository](https://github.com/gyrogovernance/science) - Full CGM theory
- [General Specifications](docs/GyroDiagnostics_General_Specs.md) - Framework overview
- [Technical Specifications](docs/GyroDiagnostics_Technical_Specs.md) - Implementation details
- [Info-Set Dynamics for Alignment](docs/theory/Measurement.md) - Tensegrity mapping (Stafford Beer's Cybernetics)

---

## 📄 Based on Paper

**AI Quality Governance: Human Data Evaluation and Responsible AI Behavior Alignment**

[![View Publication](https://img.shields.io/badge/📖%20View%20Publication-4A90E2?style=for-the-badge&labelColor=2F2F2F)](http://doi.org/10.17613/43wc1-mvn58)

---

## Installation

```bash
# Clone repository
git clone https://github.com/gyrogovernance/diagnostics.git
cd diagnostics

# Install dependencies
pip install -r requirements.txt

# Install package in editable mode (required)
pip install -e .

# Validate setup
python tools/validate_setup.py
```

### Configure Environment

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` with your API keys:

```ini
# Primary Model (under evaluation)
INSPECT_EVAL_MODEL=openai/gpt-4o

# Analyst Model (for scoring)
INSPECT_EVAL_MODEL_GRADER=openai/gpt-4o

# API Keys
OPENROUTER_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here

# Logging
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
# Run single challenge
inspect eval src/gyrodiagnostics/tasks/challenge_1_formal.py

# Specify models
inspect eval src/gyrodiagnostics/tasks/challenge_1_formal.py \
  --model openai/gpt-4o \
  --model-role analyst=openai/gpt-4o

# Test run (limited epochs)
inspect eval src/gyrodiagnostics/tasks/challenge_1_formal.py --limit 1
```

### Using Python Scripts

```bash
# From root directory
python run.py

# From tools directory
python tools/run_diagnostics.py

# Validate configuration
python tools/validate_setup.py
```

### Analyze Results

```bash
# Analyze evaluation logs (outputs to results/<timestamp>/)
python tools/analyzer.py

# Clean old logs
python tools/cleaner.py
```

---

## Configuration

Edit `config/evaluation_config.yaml` to customize:

- Model selection (evaluation target and analyst models)
- Balance Horizon validation bounds
- Safety limits (time/token constraints)
- Production mode (error tolerance vs strict research mode)

Core parameters (scoring weights, rubric structure, epochs) are fixed by theoretical framework. Challenges can be extended or replaced for custom benchmarks.

---

## Tools

Utility scripts for evaluation management. See [tools/README.md](tools/README.md) for details.

**Key Tools**:
- `run_diagnostics.py` - Execute all 5 challenges
- `analyzer.py` - Comprehensive suite analysis with Balance Horizon
- `cleaner.py` - Manage logs and results folders
- `validate_setup.py` - Verify configuration

**Quick Usage**:

```bash
# Run full suite
python run.py

# Analyze results
python tools/analyzer.py

# Clean logs older than 7 days
python tools/cleaner.py --older-than 7
```

---

## Project Structure

```
gyrodiagnostics/
├── src/gyrodiagnostics/
│   ├── tasks/           # Challenge implementations
│   ├── solvers/         # Autonomous progression
│   ├── scorers/         # 20-metric alignment scorer
│   ├── metrics/         # Balance Horizon calculation
│   ├── prompts/         # Challenge and scoring templates
│   └── utils/           # Constants and helpers
├── tools/               # Utility scripts
├── showcase/            # Sample evaluation results
├── config/              # Configuration files
└── docs/                # Theory and specifications
```

---

## Contributing

Research framework under active development. Contributions welcome via issues and pull requests.

---

## 📖 Citation

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

MIT License. See [LICENSE](LICENSE) for details.

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