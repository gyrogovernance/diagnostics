# Inspect AI Tools

This directory contains utility scripts for working with Inspect AI evaluation logs.

## log_to_text.py

Extract comprehensive readable text output from Inspect AI `.eval` log files, including scores, conversation history, and detailed analysis.

## log_to_conversation.py

Extract just the conversation history from `.eval` log files in a clean, readable format.

## cleanup_results.py

Clean up and manage the results folder.

## run_full_suite.py

Run the complete GyroDiagnostics evaluation suite across all challenges using configured models from `.env` file.

## validate_setup.py

Validate that the GyroDiagnostics setup is configured correctly.

## add_to_showcase.py

Add evaluation results to the showcase folder for easy viewing by non-technical users.

### Usage

```bash
# Basic usage - automatically saves to results/ folder with organized naming
python tools/log_to_text.py path/to/logfile.eval

# Different formats - all auto-organized
python tools/log_to_text.py path/to/logfile.eval --format markdown
python tools/log_to_text.py path/to/logfile.eval --format html
python tools/log_to_text.py path/to/logfile.eval --format json

# Custom output location (overrides auto-organization)
python tools/log_to_text.py path/to/logfile.eval --output custom/path/results.txt

# Extract just conversation history - auto-organized
python tools/log_to_conversation.py path/to/logfile.eval

# Custom conversation output
python tools/log_to_conversation.py path/to/logfile.eval --output custom/conversation.txt

# Clean up results folder
python tools/cleanup_results.py --list                    # List all results
python tools/cleanup_results.py --cleanup --confirm       # Remove all results
python tools/cleanup_results.py --older-than 7 --confirm  # Remove files older than 7 days
python tools/cleanup_results.py --pattern strategic --confirm  # Remove files matching pattern

# Run complete evaluation suite
python tools/run_full_suite.py                           # Run with configured models from .env

# Validate setup
python tools/validate_setup.py                            # Check if everything is configured correctly

# Add results to showcase
python tools/add_to_showcase.py logs/evaluation.eval --model gpt-4o --challenge strategic
python tools/add_to_showcase.py logs/evaluation.eval --model claude-3.5-sonnet --challenge formal --description "Custom description"
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

- **Alignment scores** and detailed breakdowns
- **Structure scores** (traceability, variety, accountability, integrity, aperture)
- **Behavior scores** (truthfulness, completeness, groundedness, literacy, comparison, preference)
- **Specialization scores** (finance, strategy, etc.)
- **Pathologies** (any issues detected)
- **Timing data** (total time, working time, turn timestamps)
- **Detailed reviews** (if available from scorer)
- **Full conversation history** (all messages between user and model)
- **Evaluation metadata** (status, version, sample counts, accuracy)
- **Smart status interpretation** (explains why "error" status may occur despite successful completion)

### Requirements

- Python 3.7+
- `inspect-ai` package
- `pandas` package
- `pyarrow` package (for log reading)

Install dependencies:
```bash
pip install inspect-ai pandas pyarrow
```