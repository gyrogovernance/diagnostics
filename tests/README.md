# Gyroscope Evaluation Tests

This directory contains Inspect AI evaluation scripts for testing Gyroscope protocol implementations.

## Structure

```
tests/
├── test_gyroscope_eval.py     # Main Inspect AI eval script
├── test_local_model.py        # Local model smoke tests
└── fixtures/                  # Test fixtures and data
```

## Running Tests

### With Inspect AI (Cloud Models)
```bash
inspect eval tests/test_gyroscope_eval.py
```

### With Local Models
```bash
python tests/test_local_model.py
```

## What Gets Tested

1. **Structure Tier**: Protocol adherence, trace formatting
2. **Behavior Tier**: Response quality, reasoning patterns
3. **Specialization Tier**: Task-specific performance

