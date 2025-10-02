# Gyroscope Protocol Core

This directory will contain the core Gyroscope protocol implementation when refactored from tools/.

## Planned Structure

```
src/
└── gyroscope/
    ├── __init__.py
    ├── protocol.py        # Core protocol logic
    ├── solver.py          # Inspect AI solver
    ├── scorers.py         # Evaluation scorers
    └── utils.py           # Utilities
```

Currently, implementation lives in `tools/gyroscope_inspect_integration.py`.

