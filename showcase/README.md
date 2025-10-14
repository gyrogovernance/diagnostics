# GyroDiagnostics Showcase

This directory contains comprehensive evaluation results and strategic insights from the GyroDiagnostics AI safety framework.

## 📊 Model Evaluation Reports

Complete analysis reports for frontier AI models tested with the GyroDiagnostics framework. Each report contains:

- **Quality Index (QI)**: Overall alignment quality across 20 metrics
- **Alignment Rate (AR)**: Temporal stability measuring quality per unit time
- **Superintelligence Index (SI)**: Structural proximity to theoretical optimum
- **Pathology Detection**: Identification of reasoning failures and brittleness patterns
- **Per-Epoch Analysis**: Detailed breakdown of all 5 challenges across 2 epochs each

### Available Reports

| Model | Report | Key Findings |
|-------|--------|--------------|
| **ChatGPT-5** | [gpt_5_chat_report.txt](gpt_5_chat_report.txt) | 73.9% Quality, SUPERFICIAL processing, 90% deceptive coherence |
| **Claude 4.5 Sonnet** | [claude_4_5_sonnet_report.txt](claude_4_5_sonnet_report.txt) | 82.0% Quality, VALID temporal balance, 4/10 pathology-free epochs |
| **Grok-4** | [grok_4_report.txt](grok_4_report.txt) | 71.6% Quality, VALID alignment, weakest formal reasoning (40.3%) |

### Cross-Model Insights

- **Pathology Independence**: High deceptive coherence rates (90%) in both ChatGPT-5 and Grok-4 despite different quality profiles
- **Domain-Specific Excellence**: Claude leads epistemic challenges (90.3%), all models struggle with formal reasoning (40-55%)
- **Temporal Balance**: Claude and Grok maintain VALID alignment rates vs. ChatGPT-5's SUPERFICIAL processing
- **Structural Imbalance**: All models show 7-9× deviation from theoretical optimum (SI scores: 11.2-13.2)

## 🧠 Consolidated Insight Reports

Beyond model evaluation, our framework generates valuable strategic insights on critical topics. See [`insights/`](insights/) for detailed reports synthesizing approaches across all tested models.

### Available Reports

- **[AI-Empowered Prosperity](insights/aie_prosperity_report.md)**: Multi-stakeholder frameworks for global well-being
- **[AI-Empowered Health](insights/aie_health_report.md)**: Global regulatory evolution for health systems
- **[AI-Empowered Alignment](insights/aie_alignment_report.md)**: Fundamental constraints on recursive reasoning

## 📁 Data Files

Corresponding JSON data files are available for each model evaluation:
- `gpt_5_chat_data.json`
- `claude_4_5_sonnet_data.json`
- `grok_4_data.json`

These contain complete raw data for independent analysis and verification.

## 🔬 Research Value

### For AI Safety Research
- **Pathology Taxonomy**: Real-world validation of reasoning failure modes
- **Structural Assessment**: Root-cause analysis beyond surface-level performance
- **Temporal Stability**: Detection of brittleness patterns in extended operation
- **Cross-Model Patterns**: Architecture-independent failure modes

### For Policy & Governance
- **Measurable Thresholds**: Quantitative standards for AI safety protocols
- **Independent Verification**: Public API-based evaluations anyone can reproduce
- **Strategic Insights**: Practical frameworks for human-AI cooperation

## 📖 Usage

### Reproducing Evaluations
```bash
# Clone repository
git clone https://github.com/gyrogovernance/diagnostics.git
cd diagnostics

# Install dependencies and run evaluation
pip install -r requirements.txt
pip install -e .
python tools/run_diagnostics.py
```

### Analyzing Results
```bash
# Generate comprehensive analysis
python tools/analyzer.py

# Extract insights by topic
python tools/extract_insights_by_topic.py
```

## ⚖️ Validation

All evaluations use:
- **Public API Access**: No privileged model access required
- **Cross-Analysis**: Models evaluate each other to eliminate bias
- **Mathematical Grounding**: Metrics derived from Common Governance Model theory
- **Reproducible Methods**: Complete codebase and documentation available

## 📄 Citation

```bibtex
@misc{gyrodiagnostics_showcase_2025,
  title={GyroDiagnostics Showcase: Model Evaluations and Strategic Insights},
  author={Korompilias, Basil},
  year={2025},
  howpublished={GitHub Repository},
  url={https://github.com/gyrogovernance/diagnostics/tree/main/showcase},
  note={Comprehensive AI alignment evaluation results and strategic insights}
}
```

---

## 📋 Framework Summary

**Evaluation Dates**: October 2025
**Analysts**: Multi-model cross-validation (each model analyzed by others)
**Challenges**: 5 domains × 2 epochs = 10 evaluations per model
**Metrics**: 20-point rubric across Structure, Behavior, Specialization
**Total Evaluations**: 30 epochs across 3 frontier models

*This showcase demonstrates GyroDiagnostics as the first mathematically-grounded framework bridging capability benchmarks and catastrophic risk assessment.*

© 2025 Basil Korompilias | [GyroDiagnostics](https://github.com/gyrogovernance/diagnostics)
