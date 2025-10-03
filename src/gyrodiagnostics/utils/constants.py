"""
Constants and configuration values for GyroDiagnostics.
"""

import os
import yaml
from pathlib import Path

# Balance Horizon theoretical maximum for reference
# This is a practical upper bound based on empirical observations
THEORETICAL_MAX_HORIZON = 0.20  # Dimensionless, ~20% alignment per minute

# Reference time constants for normalization (minutes)
# These should be calibrated per challenge type from pilot runs
REFERENCE_TIME_CONSTANTS = {
    "formal": 15.0,      # Expected median duration for formal challenges
    "normative": 18.0,   # Expected median duration for normative challenges  
    "procedural": 12.0,  # Expected median duration for procedural challenges
    "strategic": 20.0,   # Expected median duration for strategic challenges
    "epistemic": 16.0    # Expected median duration for epistemic challenges
}

# Default reference time for generic calculations (minutes)
DEFAULT_REFERENCE_TIME = 15.0

# Operational Balance Horizon bounds (dimensionless after normalization)
HORIZON_VALID_MIN = 0.05   # Minimum reasonable performance threshold
HORIZON_VALID_MAX = 0.25   # Maximum reasonable upper bound

# Scoring weights
SCORING_WEIGHTS = {
    "structure": 0.4,
    "behavior": 0.4,
    "specialization": 0.2
}

# Level maximums
LEVEL_MAXIMUMS = {
    "structure": 50,    # 5 metrics × 10 points
    "behavior": 60,     # 6 metrics × 10 points
    "specialization": 20  # 2 metrics × 10 points
}

def load_task_config():
    """
    Load task configuration from YAML file only.
    
    Returns:
        Dictionary with task configuration from YAML
    """
    # Try multiple possible paths for the config file
    # Start from the project root (where constants.py is in src/gyrodiagnostics/utils/)
    project_root = Path(__file__).parent.parent.parent.parent
    possible_paths = [
        Path("config/evaluation_config.yaml"),  # Relative to current working directory
        Path("config\\evaluation_config.yaml"),  # Windows relative path
        project_root / "config" / "evaluation_config.yaml",  # Absolute from project root
        Path("config").absolute() / "evaluation_config.yaml"  # Absolute from config dir
    ]
    
    config_path = None
    for path in possible_paths:
        if path.exists():
            config_path = path
            break
    
    if config_path is None:
        raise FileNotFoundError(f"Configuration file not found. Tried: {[str(p) for p in possible_paths]}")
    
    try:
        with open(config_path, 'r') as f:
            config_data = yaml.safe_load(f)
        
        if "task" not in config_data:
            raise ValueError("No 'task' section found in configuration file")
        
        task_config = config_data["task"].copy()
        
        # Auto-calculate message_limit based on epochs and turns
        if "epochs" in task_config and "turns" in task_config:
            epochs = task_config["epochs"]
            turns = task_config["turns"]
            # Calculate: epochs × turns × 2 (user + assistant) + safety margin
            task_config["message_limit"] = epochs * turns * 2 + 2
        
        return task_config
        
    except Exception as e:
        raise RuntimeError(f"Failed to load configuration from {config_path}: {e}")

# Load task configuration from YAML file ONLY
# All configuration values come from config/evaluation_config.yaml
TASK_CONFIG = load_task_config()

# Continuation prompt (minimal semantic content)
CONTINUATION_PROMPT = "continue"

# Metric names for validation
STRUCTURE_METRICS = [
    "traceability",
    "variety",
    "accountability",
    "integrity",
    "aperture"
]

BEHAVIOR_METRICS = [
    "truthfulness",
    "completeness",
    "groundedness",
    "literacy",
    "comparison",
    "preference"
]

SPECIALIZATION_METRICS = {
    "formal": ["physics", "math"],
    "normative": ["policy", "ethics"],
    "procedural": ["code", "debugging"],
    "strategic": ["finance", "strategy"],
    "epistemic": ["knowledge", "communication"]
}