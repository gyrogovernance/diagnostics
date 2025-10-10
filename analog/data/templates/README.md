# GyroDiagnostics Manual Evaluation Templates

This directory contains standardized templates for manual evaluation workflows.

## Templates

### Timing Notes
- **`notes_template.md`** - Empty template for timing data and metadata

### Score Files
- **`score_template_general.md`** - Generic template with placeholder specialization metrics
- **`score_template_1_formal.md`** - Formal Challenge (Physics & Math)
- **`score_template_2_normative.md`** - Normative Challenge (Policy & Ethics)
- **`score_template_3_procedural.md`** - Procedural Challenge (Code & Debugging)
- **`score_template_4_strategic.md`** - Strategic Challenge (Finance & Strategy)
- **`score_template_5_epistemic.md`** - Epistemic Challenge (Knowledge & Communication)

## Usage

### Starting a New Evaluation Run

1. Copy `notes_template.md` to `analog/data/notes/notes_run{X}.md`
2. Fill in the model metadata at the top
3. For each challenge × epoch:
   - Start timer when pasting challenge prompt
   - Let model complete 6 turns ("continue" × 5)
   - Stop timer and record as `{challenge}_{epoch}: MM:SS`

### Recording Scores

1. Copy the appropriate challenge template to `analog/data/results/{model_name}/scores/{challenge}_{epoch}_scores.md`
2. Fill in the metadata at the top
3. Paste analyst evaluations (replace `[MODEL_NAME]` and fill in JSON)
4. Add any scoring notes at the bottom

### Running Analysis

```bash
python analog/analog_analyzer.py analog/data/results/{model_name} --notes analog/data/notes/notes_run{X}.md
```

This will generate:
- `analysis_report.txt` - Human-readable summary
- `analysis_data.json` - Structured data
- `insights_data.json` - Consolidated insights

## Specialization Metrics by Challenge

| Challenge | Metric 1 | Metric 2 |
|-----------|----------|----------|
| 1. Formal | physics | math |
| 2. Normative | policy | ethics |
| 3. Procedural | code | debugging |
| 4. Strategic | finance | strategy |
| 5. Epistemic | knowledge | communication |

## Directory Structure

```
analog/data/
├── notes/
│   ├── notes_template.md          # Empty template
│   ├── notes_run1.md              # Actual run data
│   └── notes_run2.md
├── results/
│   ├── gpt5_chat/
│   │   └── scores/
│   │       ├── 1_1_scores.md      # Formal, Epoch 1
│   │       ├── 1_2_scores.md      # Formal, Epoch 2
│   │       └── ...
│   ├── claude_sonnet/
│   │   └── scores/
│   │       └── ...
│   └── ...
├── transcripts/                    # Optional
│   └── {model_name}/
│       └── ...
└── templates/                      # This directory
    └── ...
```

## Validation Checklist

Before running the analyzer, verify:

- [ ] All timing entries use `MM:SS` format (not `M:SS` or `MM:S`)
- [ ] All JSON blocks have proper `{` and `}` boundaries
- [ ] No trailing commas in JSON
- [ ] `"pathologies"` is a list `[]`, not a string
- [ ] Specialization metrics match challenge type
- [ ] `"N/A"` values in quotes for comparison/preference when not applicable
- [ ] File naming: `{challenge_number}_{epoch_number}_scores.md`

