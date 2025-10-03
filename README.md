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

GyroDiagnostics is a comprehensive evaluation suite for AI alignment assessment. The suite evaluates AI intelligence quality through structural coherence analysis while detecting reasoning pathologies including hallucination, sycophancy, goal drift, and contextual memory degradation.

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

Create a `.env` file in the project root:

```ini
# Primary Model (the one being evaluated)
INSPECT_EVAL_MODEL=openai/gpt-4o

# Judge Model (for scoring - can be same or different)
INSPECT_EVAL_MODEL_GRADER=openai/gpt-4o

# Log Configuration
INSPECT_LOG_DIR=./logs
INSPECT_LOG_LEVEL=info

# Evaluation Settings
INSPECT_EVAL_MAX_RETRIES=1
INSPECT_EVAL_MAX_CONNECTIONS=8
```

For local models (e.g., Hugging Face):

**Fast Development (2-3 min/sample):**
```ini
INSPECT_EVAL_MODEL=hf/Qwen/Qwen3-0.6B-Base
INSPECT_EVAL_MODEL_GRADER=hf/Qwen/Qwen3-0.6B-Base
```

**Higher Quality (5-10 min/sample):**
```ini
INSPECT_EVAL_MODEL=hf/Qwen/Qwen3-1.7B-Base
INSPECT_EVAL_MODEL_GRADER=hf/Qwen/Qwen3-1.7B-Base
```

---

## Quick Start

### Using Inspect AI CLI (Recommended)

```bash
# Run a single challenge
inspect eval src/gyrodiagnostics/tasks/formal_challenge.py

# Run with specific model
inspect eval src/gyrodiagnostics/tasks/formal_challenge.py \
  --model openai/gpt-4o \
  --model-role grader=openai/gpt-4o

# Run with limit (for testing)
inspect eval src/gyrodiagnostics/tasks/formal_challenge.py --limit 1
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
# Extract readable text from evaluation logs
python tools/log_to_text.py path/to/evaluation.eval

# Extract conversation history only
python tools/log_to_conversation.py path/to/evaluation.eval

# Clean up results folder
python tools/cleanup_results.py --list
```

---

## Architecture

### Five Challenge Domains

- **Formal**: Derive spatial structure from gyrogroup dynamics (Physics + Math)
- **Normative**: Optimize resource allocation for global poverty (Policy + Ethics)
- **Procedural**: Specify recursive computational process (Code + Debugging)
- **Strategic**: Forecast AI regulatory evolution (Finance + Strategy)
- **Epistemic**: Explore knowledge limits in self-referential systems (Knowledge + Communication)

Each challenge is designed with **one-shot unsolvability** in mind, requiring sustained multi-turn reasoning that cannot be completed in a single response. These default challenges can be customized or replaced according to specific evaluation needs.

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

- **Model selection** - Choose models to evaluate and judge models for scoring
- **Reference times** - Calibrate expected durations per challenge type (from pilot runs)
- **Safety limits** - Adjust time/token limits for operational constraints
- **Production mode** - Enable error tolerance for deployment vs. strict research mode

Most parameters (scoring weights, epochs, rubric structure) are fixed by the theoretical framework.

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
├── tools/               # Utility scripts for log processing and analysis
│   ├── run_full_suite.py      # Run complete evaluation suite
│   ├── log_to_text.py         # Extract readable text from logs
│   ├── log_to_conversation.py # Extract conversation history
│   ├── cleanup_results.py     # Manage results folder
│   ├── validate_setup.py      # Validate configuration
│   ├── add_to_showcase.py     # Add results to showcase
│   └── README.md              # Tools documentation
├── showcase/            # Sample evaluation results for easy viewing
│   └── README.md              # Showcase overview and navigation
├── config/              # Configuration files
└── docs/                # Theory and specifications
```

---

## Tools

The `tools/` directory contains utility scripts for working with evaluation results and running the complete suite. See [tools/README.md](tools/README.md) for detailed documentation.

### Key Tools

- **`run_full_suite.py`** - Run all 5 challenges using configured models from `.env`
- **`log_to_text.py`** - Extract comprehensive readable reports from `.eval` log files
- **`log_to_conversation.py`** - Extract clean conversation history from logs
- **`cleanup_results.py`** - Manage and organize the results folder
- **`validate_setup.py`** - Verify that your configuration is correct

### Quick Tool Usage

```bash
# Run complete evaluation suite
python tools/run_full_suite.py

# Extract readable results from a log file
python tools/log_to_text.py logs/your_evaluation.eval

# Get just the conversation
python tools/log_to_conversation.py logs/your_evaluation.eval

# Clean up old results
python tools/cleanup_results.py --older-than 7 --confirm
```

---

## Showcase

The `showcase/` folder contains sample evaluation results for easy viewing. No installation required - just browse the markdown files on GitHub!

**[View Results](showcase/README.md)** | **[Add New Results](tools/add_to_showcase.py)**

---

## Documentation

- **Theory**: [Gyroscope Science Repository](https://github.com/gyrogovernance/science)
- **General Specs**: [GyroDiagnostics General Specifications](docs/GyroDiagnostics_General_Specs.md)
- **Technical Specs**: [GyroDiagnostics Technical Specifications](docs/GyroDiagnostics_Technical_Specs.md)

---

## 📄 Based on Paper

**AI Quality Governance**  
*Human Data Evaluation and Responsible AI Behavior Alignment*

[![View Publication](https://img.shields.io/badge/📖%20View%20Publication-4A90E2?style=for-the-badge&labelColor=2F2F2F)](http://doi.org/10.17613/43wc1-mvn58)

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