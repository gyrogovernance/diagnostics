# Inspect AI Tools

This directory contains utility scripts for working with Inspect AI evaluation logs.

## cleaner.py

Clean up and manage the results folder.

## run_diagnostics.py

Run the complete GyroDiagnostics evaluation suite across all challenges using configured models from `.env` file.

## validate_setup.py

Validate that the GyroDiagnostics setup is configured correctly.

## analyzer.py

Comprehensive analysis of suite results from .eval logs. Provides detailed breakdowns of alignment scores, Alignment Rate metrics, analyst evaluation metadata, and suite-level summaries.

Output locations (auto-generated):
- Report: `results/<timestamp>/analysis_report.txt`
- JSON: `results/<timestamp>/analysis_data.json`

## extract_insights_by_topic.py

Extract analyst-generated insights from evaluation data, organized by topic rather than by model.

Reads all `*_data.json` files from `showcase/` and extracts insights for the three key challenges:
- **Normative**: Global poverty reduction framework
- **Strategic**: AI medical diagnostics regulation  
- **Epistemic**: AI alignment and epistemic limits

Output files (written to `showcase/insights/raw/`):
- `poverty_insights_raw.md`: All models' insights on poverty reduction
- `regulation_insights_raw.md`: All models' insights on AI healthcare regulation
- `epistemics_insights_raw.md`: All models' insights on epistemic constraints

Use these raw insight files as source material to write consolidated topic reports.


### Usage

```bash
# Clean up results folder
python tools/cleaner.py --list                    # List all results
python tools/cleaner.py --cleanup --confirm       # Remove all results
python tools/cleaner.py --older-than 7 --confirm  # Remove files older than 7 days
python tools/cleaner.py --pattern strategic --confirm  # Remove files matching pattern

# Run complete evaluation suite
python tools/run_diagnostics.py                           # Run with configured models from .env

# Validate setup
python tools/validate_setup.py                            # Check if everything is configured correctly

# Analyze .eval logs (comprehensive analysis)
python tools/analyzer.py                           # Auto-generates timestamped outputs
python tools/analyzer.py --eval-dir logs           # Specify logs directory
python tools/analyzer.py logs/logs.json --output custom/report.txt  # Custom output paths

# Extract insights by topic (for consolidated reports)
python tools/extract_insights_by_topic.py          # Generates 3 raw insight files by topic

```

### File Organization

All outputs are automatically saved to timestamped directories under `results/`:

- **Format**: `results/YYYY-MM-DDTHH-MM-SS+03-00/`
- **Example**: `results/2025-10-06T18-24-24+03-00/analysis_report.txt`
- **Example**: `results/2025-10-06T18-24-24+03-00/analysis_data.json`
- **Example**: `results/2025-10-06T18-24-24+03-00/insights_data.json`

The timestamp is extracted from the first .eval file for easy organization and prevents overwriting.

### What It Extracts

#### analyzer.py:
- **Comprehensive suite analysis** from .eval logs
- **All epochs per challenge** (complete per-epoch breakdown)
- **Alignment scores** and detailed breakdowns per epoch
- **Structure scores** (traceability, variety, accountability, integrity)
- **Behavior scores** (truthfulness, completeness, groundedness, literacy, comparison, preference)
- **Specialization scores** (domain-specific metrics per challenge)
- **Analyst reviews** (scoring_rationale, strengths, weaknesses per epoch)
- **Timing data** (duration, turn counts per epoch)
- **Alignment Rate** (time-normalized quality per challenge; suite-level median)
- **Pathology detection** (if any issues detected)
- **Fallback detection** (when analyst evaluation fails)
- **Insight briefs** (aggregated analyst insights per challenge)
- **Suite-level summaries** (overall performance, rankings, pathology analysis)
- **Analyst reliability analysis** (fallback usage across epochs)

### Requirements

- Python 3.7+
- `inspect-ai` package
- `pandas` package
- `pyarrow` package (for log reading)

Install dependencies:
```bash
pip install inspect-ai pandas pyarrow
```