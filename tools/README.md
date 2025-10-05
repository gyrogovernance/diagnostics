# Inspect AI Tools

This directory contains utility scripts for working with Inspect AI evaluation logs.

## cleanup_results.py

Clean up and manage the results folder.

## run_full_suite.py

Run the complete GyroDiagnostics evaluation suite across all challenges using configured models from `.env` file.

## validate_setup.py

Validate that the GyroDiagnostics setup is configured correctly.

## final_analysis.py

Comprehensive analysis of suite results from JSON log files. Provides detailed breakdowns of alignment scores, Balance Horizon metrics, analyst evaluation metadata, and suite-level summaries.

## extract_epochs.py

Extract per-epoch results directly from Inspect AI `.eval` logs, bypassing the defective `logs.json` file. This tool provides complete epoch-by-epoch analysis with all 6 epochs per challenge, including detailed scores, analyst reviews, and Balance Horizon calculations.


### Usage

```bash
# Clean up results folder
python tools/cleanup_results.py --list                    # List all results
python tools/cleanup_results.py --cleanup --confirm       # Remove all results
python tools/cleanup_results.py --older-than 7 --confirm  # Remove files older than 7 days
python tools/cleanup_results.py --pattern strategic --confirm  # Remove files matching pattern

# Run complete evaluation suite
python tools/run_full_suite.py                           # Run with configured models from .env

# Validate setup
python tools/validate_setup.py                            # Check if everything is configured correctly

# Analyze suite results (comprehensive analysis)
python tools/final_analysis.py logs/logs.json --output report.txt
python tools/final_analysis.py logs/logs.json --json analysis.json  # Save structured JSON

# Extract per-epoch data from .eval logs (bypasses logs.json)
python tools/extract_epochs.py logs --output report_epochs.txt --json epochs.json
python tools/extract_epochs.py logs/single_challenge.eval --output single_report.txt
python tools/extract_epochs.py logs --challenge formal normative --output formal_normative.txt

```

### File Organization

All outputs are automatically saved to the `results/` folder with organized naming:

- **Format**: `YYYYMMDD_HHMMSS_taskname_format.ext`
- **Example**: `20251003_105624_00_strategic_text.txt`
- **Example**: `20251003_105624_00_strategic_conversation.txt`
- **Example**: `20251003_105624_00_strategic_markdown.md`

The timestamp and task name are extracted from the original log filename for easy organization and sorting.

### Supported Formats

- **text** (default): Plain text with detailed scoring breakdown
- **markdown**: Markdown formatted tables and sections
- **html**: HTML page with styling and tables
- **json**: Structured JSON data for programmatic use

### What It Extracts

#### extract_epochs.py:
- **All 6 epochs per challenge** (complete per-epoch breakdown)
- **Alignment scores** and detailed breakdowns per epoch
- **Structure scores** (traceability, variety, accountability, integrity)
- **Behavior scores** (truthfulness, completeness, groundedness, literacy, comparison, preference)
- **Specialization scores** (domain-specific metrics per challenge)
- **Analyst reviews** (scoring_rationale, strengths, weaknesses per epoch)
- **Timing data** (duration, turn counts per epoch)
- **Balance Horizon** (normalized and raw calculations)
- **Pathology detection** (if any issues detected)
- **Fallback detection** (when analyst evaluation fails)

#### final_analysis.py:
- **Comprehensive suite analysis** from JSON logs
- **Analyst evaluation metadata** (scoring rationale, strengths, weaknesses, fallback usage)
- **Balance Horizon** (time-normalized alignment per challenge; suite-level median)
- **Weighted score verification** (matches scorer calculations)
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