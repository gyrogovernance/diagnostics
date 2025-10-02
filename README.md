# AI Safety Diagnostics
> **Gyroscopic Alignment Evaluation Lab**

![Gyroscope: Human-Aligned Superintelligence](/assets/diagnostics_cover.png)


<div align="center">

### G Y R O G O V E R N A N C E

[![Home](./assets/menu/home_badge.svg)](https://gyrogovernance.com)
[![Diagnostics](./assets/menu/diagnostics_badge.svg)](https://github.com/gyrogovernance/diagnostics)
[![Protocols](./assets/menu/protocols_badge.svg)](https://github.com/gyrogovernance/protocols)
[![Science](./assets/menu/science_badge.svg)](https://github.com/gyrogovernance/science)
[![Superintelligence](./assets/menu/superintelligence_badge.svg)](https://github.com/gyrogovernance/superintelligence)

</div>

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey?style=for-the-badge&logo=creativecommons&logoColor=white)](https://creativecommons.org/licenses/by-sa/4.0/)
[![Inspect AI](https://img.shields.io/badge/UK%20AISI-Inspect%20AI-red?style=for-the-badge)](https://inspect.aisi.org.uk/)

</div>

---

# GyroDiagnostics: AI Alignment Evaluation Suite

**Mathematical Physics-Informed Evaluation Framework for AI Model Quality and Alignment**

## Overview

GyroDiagnostics is a comprehensive evaluation suite for AI alignment assessment. The suite evaluates AI intelligence quality through structural coherence analysis while detecting reasoning pathologies including hallucination, sycophancy, goal drift, and contextual memory degradation.

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/gyrodiagnostics.git
cd gyrodiagnostics

# Install in development mode
pip install -e .

# Or install from requirements
pip install -r requirements.txt
```

---

## Quick Start

### Run Single Challenge

```bash
python tests/run_single_challenge.py \
  --challenge formal \
  --model openai/gpt-4o
```

### Run Full Suite

```bash
python tests/run_full_suite.py \
  --model openai/gpt-4o \
  --log-dir ./logs
```

### Analyze Results

```bash
python tests/analyze_results.py \
  --log-dir ./logs \
  --output ./analysis_results.json
```

---

## Architecture

### Five Challenge Domains

- **Formal**: Derive spatial structure from gyrogroup dynamics (Physics + Math)
- **Normative**: Optimize resource allocation for global poverty (Policy + Ethics)
- **Procedural**: Specify recursive computational process (Code + Debugging)
- **Strategic**: Forecast AI regulatory evolution (Finance + Strategy)
- **Epistemic**: Explore knowledge limits in self-referential systems (Knowledge + Communication)

### 21-Metric Rubric

#### Structure Metrics (50 points)
- Traceability, Variety, Accountability, Integrity, Aperture

#### Behavior Metrics (60 points)
- Truthfulness, Completeness, Groundedness, Literacy, Comparison, Preference

#### Specialization Metrics (20 points)
- Domain-specific expertise (2 metrics per challenge)

### Balance Horizon

Temporal stability metric: `Balance Horizon = Median(Alignment) / Median(Duration)`

Measures alignment efficiency over time with practical bounds for validation.

---

## Usage Examples

### Python API

```python
from inspect_ai import eval
from gyrodiagnostics import formal_challenge

# Run evaluation
results = eval(
    formal_challenge(),
    model="openai/gpt-4o",
    log_dir="./logs"
)
```

### CLI Usage

```bash
# Using Inspect AI CLI
inspect eval gyrodiagnostics/tasks/formal_challenge.py \
  --model openai/gpt-4o \
  --log-dir ./logs
```

---

## Configuration

Edit `config/evaluation_config.yaml` to customize:

- Task parameters (epochs, turns, limits)
- Scoring weights
- Balance Horizon settings
- Model configurations

---

## Project Structure

```
gyrodiagnostics/
├── src/gyrodiagnostics/
│   ├── tasks/           # Five challenge implementations
│   ├── solvers/         # Autonomous progression solver
│   ├── scorers/         # 21-metric alignment scorer
│   ├── metrics/         # Balance Horizon calculation
│   ├── prompts/         # Challenge prompts & scoring templates
│   └── utils/           # Constants and helpers
├── tests/               # Evaluation runners and analysis
├── config/              # Configuration files
└── docs/                # Theory and specifications
```

---

## Documentation

- **Theory**: `docs/Foundations/CommonGovernanceModel.md`
- **General Specs**: `docs/GyroDiagnostics_General_Specs.md`
- **Technical Specs**: `docs/GyroDiagnostics_Technical_Specs.md`

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

This work is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-sa/4.0/).

Attribution required. Derivative works must be distributed under the same license.

© 2025 Basil Korompilias.

---

## 🔗 Notion Documentation Links

- [Gyroscope Alignment Diagnostics (Extensive Analyses)](https://www.notion.so/Gyroscope-Alignment-Diagnostics-1ee9ff44f43680cc9eaccb25b828b65f?pvs=21)
