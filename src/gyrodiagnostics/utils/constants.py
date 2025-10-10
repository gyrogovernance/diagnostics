"""
Constants and configuration values for GyroDiagnostics.
"""

import os
import yaml
from pathlib import Path

# Balance Horizon empirical operational bounds (units: per minute)
# These are empirical ranges based on typical model performance, not theoretical derivation
# BH = closure / duration_minutes
# Example: 0.80 score in 10 min → BH = 0.08 per minute
HORIZON_VALID_MIN = 0.03   # Lower bound: < 0.03/min means >33 min to reach 1.0 (slow)
HORIZON_VALID_MAX = 0.10   # Upper bound: > 0.10/min means <10 min to reach 1.0 (very fast)

# Scoring weights
SCORING_WEIGHTS = {
    "structure": 0.4,
    "behavior": 0.4,
    "specialization": 0.2
}

# Level maximums
LEVEL_MAXIMUMS = {
    "structure": 40,    # 4 metrics × 10 points
    "behavior": 60,     # 6 metrics × 10 points
    "specialization": 20  # 2 metrics × 10 points
}

# Evaluation configuration (loaded from YAML)
MAX_TASKS = None  # Will be loaded from config
RETRY_ATTEMPTS = None  # Will be loaded from config


def _resolve_config_path() -> Path:
    """
    Resolve the path to evaluation_config.yaml using multiple fallbacks.
    """
    project_root = Path(__file__).parent.parent.parent.parent
    candidates = [
        Path("config/evaluation_config.yaml"),
        Path("config\\evaluation_config.yaml"),
        project_root / "config" / "evaluation_config.yaml",
        Path("config").absolute() / "evaluation_config.yaml"
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    # If not found, return the first path (will raise later)
    return candidates[0]

def load_task_config():
    """
    Load task configuration from YAML file only.
    
    Returns:
        Dictionary with task configuration from YAML
    """
    # Try multiple possible paths for the config file
    # Start from the project root (where constants.py is in src/gyrodiagnostics/utils/)
    config_path = _resolve_config_path()
    
    try:
        with open(config_path, 'r') as f:
            config_data = yaml.safe_load(f)
        
        if "task" not in config_data:
            raise ValueError("No 'task' section found in configuration file")
        
        task_config = config_data["task"].copy()
        
        # Auto-calculate message_limit only if not provided in YAML
        if "message_limit" not in task_config and "epochs" in task_config and "turns" in task_config:
            epochs = task_config["epochs"]
            turns = task_config["turns"]
            # Calculate: epochs × turns × 2 (user + assistant) + safety margin
            task_config["message_limit"] = epochs * turns * 2 + 2
        
        # Load Balance Horizon configuration and update module-level constants
        bh_cfg = config_data.get("balance_horizon") or {}
        
        global HORIZON_VALID_MIN, HORIZON_VALID_MAX
        HORIZON_VALID_MIN = bh_cfg.get("horizon_valid_min", HORIZON_VALID_MIN)
        HORIZON_VALID_MAX = bh_cfg.get("horizon_valid_max", HORIZON_VALID_MAX)
        
        # Load Scoring configuration and update module-level constants
        scoring_cfg = config_data.get("scoring") or {}
        weights = scoring_cfg.get("weights") or {}
        level_max = scoring_cfg.get("level_maximums") or {}
        
        global SCORING_WEIGHTS, LEVEL_MAXIMUMS
        # Update with YAML values if present
        SCORING_WEIGHTS.update({k: float(v) for k, v in weights.items() if k in SCORING_WEIGHTS})
        LEVEL_MAXIMUMS.update({k: int(v) for k, v in level_max.items() if k in LEVEL_MAXIMUMS})
        
        # Load Evaluation configuration and update module-level constants
        eval_cfg = config_data.get("evaluation") or {}
        
        global MAX_TASKS, RETRY_ATTEMPTS
        MAX_TASKS = eval_cfg.get("max_tasks")
        RETRY_ATTEMPTS = eval_cfg.get("retry_attempts")
        
        # Validate required evaluation parameters
        if MAX_TASKS is None:
            raise ValueError("Missing required 'evaluation.max_tasks' in configuration file")
        if RETRY_ATTEMPTS is None:
            raise ValueError("Missing required 'evaluation.retry_attempts' in configuration file")
        
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
    "integrity"
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


def load_logging_config() -> dict:
    """
    Load logging configuration from YAML file.
    Returns sensible defaults if missing.
    """
    config_path = _resolve_config_path()
    try:
        with open(config_path, 'r') as f:
            config_data = yaml.safe_load(f) or {}
        logging_cfg = (config_data.get("logging") or {}).copy()
    except Exception:
        logging_cfg = {}
    # Defaults
    logging_cfg.setdefault("default_dir", "./logs")
    logging_cfg.setdefault("save_transcripts", True)
    logging_cfg.setdefault("save_scores", True)
    return logging_cfg


# Expose logging configuration
LOGGING_CONFIG = load_logging_config()