#!/usr/bin/env python3
"""
Extract per-epoch results directly from Inspect AI .eval logs, bypassing logs.json.

Usage:
    python tools/extract_epochs.py logs/ --output report_epochs.txt --json epochs.json
    python tools/extract_epochs.py path/to/single.eval --output report.txt

Notes:
    - Works with directories (recursively finds .eval files) or a single .eval file
    - Produces a per-epoch breakdown for each challenge log
    - Aggregates medians and Balance Horizon per challenge
"""

import argparse
import json
import os
import statistics
from pathlib import Path
from typing import Dict, List, Optional, Tuple


# --- Helper: Challenge detection and Balance Horizon ---

REFERENCE_TIME_CONSTANTS: Dict[str, float] = {
    "formal": 15.0,
    "normative": 18.0,
    "procedural": 12.0,
    "strategic": 20.0,
    "epistemic": 16.0,
}


def extract_challenge_type(task_name: str) -> str:
    name = (task_name or "").lower()
    for challenge in ["formal", "normative", "procedural", "strategic", "epistemic"]:
        if challenge in name:
            return challenge
    return "unknown"


def calculate_balance_horizon(median_alignment: float, median_duration: float, challenge_type: str) -> Dict:
    if not median_duration or median_duration <= 0:
        return {
            "balance_horizon_normalized": None,
            "balance_horizon_raw": None,
            "error": "Zero or missing median duration - cannot calculate Balance Horizon",
        }
    t_ref = REFERENCE_TIME_CONSTANTS.get(challenge_type, 15.0)
    bh_raw = median_alignment / median_duration
    bh_norm = bh_raw * t_ref
    return {
        "balance_horizon_normalized": bh_norm,
        "balance_horizon_raw": bh_raw,
        "reference_time": t_ref,
    }


def duration_from_turns(turn_metadata: List[Dict]) -> float:
    if not turn_metadata:
        return 0.0
    try:
        timestamps = [float(t.get("timestamp", 0)) for t in turn_metadata if "timestamp" in t]
        if not timestamps:
            return 0.0
        return (max(timestamps) - min(timestamps)) / 60.0
    except Exception:
        return 0.0


# --- Core extraction ---

def list_eval_file_paths(input_path: Path) -> List[Path]:
    if input_path.is_file():
        return [input_path]
    paths: List[Path] = []
    for p in input_path.rglob("*.eval"):
        if p.is_file():
            paths.append(p)
    return sorted(paths)


def read_eval_log_safe(path: Path):
    try:
        # Inspect AI log API
        from inspect_ai.log import read_eval_log
    except Exception as ex:  # pragma: no cover
        raise RuntimeError(
            f"Inspect AI not available or wrong version: {ex}. Ensure 'inspect-ai' is installed and up to date."
        )
    return read_eval_log(str(path))


def extract_epochs_from_log(path: Path) -> Optional[Dict]:
    """Return per-epoch data for a single .eval log file."""
    try:
        log = read_eval_log_safe(path)
    except Exception as e:
        return {"error": f"Failed to read log: {e}", "path": str(path)}

    try:
        # Eval metadata
        eval_info = getattr(log, "eval", None) or {}
        task_name = getattr(eval_info, "task", None) or (eval_info.get("task") if isinstance(eval_info, dict) else None) or "unknown"
        model = getattr(eval_info, "model", None) or (eval_info.get("model") if isinstance(eval_info, dict) else None) or "unknown"
        model_roles = getattr(eval_info, "model_roles", None) or (eval_info.get("model_roles") if isinstance(eval_info, dict) else {})
        grader_model = "unknown"
        try:
            grader = model_roles.get("grader", {}) if isinstance(model_roles, dict) else {}
            grader_model = grader.get("model", grader.get("name", "unknown"))
        except Exception:
            pass

        challenge_type = extract_challenge_type(task_name)

        # Samples = epochs when dataset has one sample and epochs>1
        samples = getattr(log, "samples", None) or []
        epoch_results: List[Dict] = []

        for sample in samples:
            # Pull the first score (alignment_scorer) if available
            scores = getattr(sample, "scores", {}) or {}
            if not scores:
                continue
            # scores may be dict-like mapping -> Score
            try:
                score_obj = None
                if isinstance(scores, dict):
                    # Prefer alignment scorer if present
                    keys = list(scores.keys())
                    align_keys = [k for k in keys if "alignment" in str(k).lower()]
                    key = align_keys[0] if align_keys else keys[0]
                    score_obj = scores[key]
                else:
                    # Fallback: iterate
                    for _k in scores:
                        score_obj = scores[_k]
                        break

                meta = getattr(score_obj, "metadata", {}) or {}
                alignment_score = float(meta.get("alignment_score", 0.0))
                structure_scores = meta.get("structure_scores", {}) or {}
                behavior_scores = meta.get("behavior_scores", {}) or {}
                specialization_scores = meta.get("specialization_scores", {}) or {}
                pathologies = meta.get("pathologies", []) or []
                analyst_fallback_used = bool(meta.get("analyst_fallback_used", False))
                scoring_rationale = meta.get("scoring_rationale", "") or ""
                strengths = meta.get("strengths", "") or ""
                weaknesses = meta.get("weaknesses", "") or ""
                turn_metadata = meta.get("turn_metadata", []) or []
                epoch_duration = float(meta.get("epoch_duration_minutes", 0.0))
                if epoch_duration == 0.0 and turn_metadata:
                    epoch_duration = duration_from_turns(turn_metadata)

                epoch_results.append(
                    {
                        "alignment_score": alignment_score,
                        "duration_minutes": epoch_duration,
                        "structure_scores": structure_scores,
                        "behavior_scores": behavior_scores,
                        "specialization_scores": specialization_scores,
                        "pathologies": pathologies,
                        "turn_count": len(turn_metadata),
                        "analyst_fallback_used": analyst_fallback_used,
                        "scoring_rationale": scoring_rationale,
                        "strengths": strengths,
                        "weaknesses": weaknesses,
                    }
                )
            except Exception:
                # Skip malformed samples
                continue

        # Aggregate medians
        alignment_scores = [e["alignment_score"] for e in epoch_results if isinstance(e.get("alignment_score"), (int, float))]
        durations = [e["duration_minutes"] for e in epoch_results if isinstance(e.get("duration_minutes"), (int, float))]
        median_alignment = statistics.median(alignment_scores) if alignment_scores else 0.0
        median_duration = statistics.median(durations) if durations else 0.0
        bh = calculate_balance_horizon(median_alignment, median_duration, challenge_type)

        return {
            "path": str(path),
            "task_name": task_name,
            "challenge_type": challenge_type,
            "model": model,
            "grader_model": grader_model,
            "epochs_analyzed": len(epoch_results),
            "median_alignment_score": median_alignment,
            "median_duration_minutes": median_duration,
            "balance_horizon": bh,
            "epoch_results": epoch_results,
        }
    except Exception as e:
        return {"error": f"Unexpected failure: {e}", "path": str(path)}


# --- Output helpers ---

def print_result(result: Dict, p):
    if "error" in result:
        p(f"ERROR: {result['error']}")
        if result.get("path"):
            p(f"   Log: {result['path']}")
        return
    p("=" * 70)
    p(f"TASK: {result.get('task_name', 'unknown')}")
    p(f"MODEL: {result.get('model', 'unknown')}")
    p(f"GRADER: {result.get('grader_model', 'unknown')}")
    p(f"CHALLENGE: {result.get('challenge_type', 'unknown').upper()}")
    p(f"EPOCHS: {result.get('epochs_analyzed', 0)}")
    p()
    p("ALIGNMENT SCORE")
    p(f"   Median: {result.get('median_alignment_score', 0.0):.4f}")
    p()
    p("EPOCH DURATION")
    p(f"   Median: {result.get('median_duration_minutes', 0.0):.3f} minutes")
    p()
    p("BALANCE HORIZON")
    bh = result.get("balance_horizon", {})
    if bh.get("error"):
        p(f"   Not available: {bh['error']}")
    else:
        p(f"   Normalized: {bh.get('balance_horizon_normalized', 0.0):.4f}")
        p(f"   Raw:        {bh.get('balance_horizon_raw', 0.0):.4f} per-minute")
        p(f"   T_ref:      {bh.get('reference_time', 0.0):.1f} minutes")
    p()
    if result.get("epoch_results"):
        epochs = result["epoch_results"]
        p(f"EPOCH DETAIL ({len(epochs)} total)")
        p()
        for idx, e in enumerate(epochs, start=1):
            p(f"- Epoch {idx}")
            p(f"  Alignment: {e.get('alignment_score', 0.0):.4f}")
            dur = e.get('duration_minutes', 0.0)
            p(f"  Duration:  {dur:.3f} min")
            p(f"  Turns:     {e.get('turn_count', 0)}")
            # Scores
            structure = e.get("structure_scores", {})
            behavior = e.get("behavior_scores", {})
            specialization = e.get("specialization_scores", {})
            p("  Structure:")
            for k in ["traceability", "variety", "accountability", "integrity"]:
                v = structure.get(k, "N/A")
                p(f"    {k.capitalize():15s}: {v}")
            p("  Behavior:")
            for k in ["truthfulness", "completeness", "groundedness", "literacy", "comparison", "preference"]:
                v = behavior.get(k, "N/A")
                p(f"    {k.capitalize():15s}: {v}")
            p("  Specialization:")
            for k, v in sorted(specialization.items()):
                p(f"    {k.capitalize():15s}: {v}")
            # Review text
            rationale = (e.get("scoring_rationale") or "").strip()
            strengths = (e.get("strengths") or "").strip()
            weaknesses = (e.get("weaknesses") or "").strip()
            if rationale:
                p("  Rationale:")
                import textwrap
                p(textwrap.fill(rationale, width=70, initial_indent="    ", subsequent_indent="    "))
            if strengths:
                p("  Strengths:")
                import textwrap
                p(textwrap.fill(strengths, width=70, initial_indent="    ", subsequent_indent="    "))
            if weaknesses:
                p("  Weaknesses:")
                import textwrap
                p(textwrap.fill(weaknesses, width=70, initial_indent="    ", subsequent_indent="    "))
            p()


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract per-epoch data from .eval logs")
    parser.add_argument("input", type=str, help="Path to .eval file or directory containing .eval logs")
    parser.add_argument("--output", type=str, help="Write a text summary to this file")
    parser.add_argument("--json", type=str, help="Write structured JSON to this file")
    parser.add_argument("--challenge", type=str, nargs="*", help="Optional filter: one or more challenge types")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"[ERROR] Input path not found: {input_path}")
        return 1

    eval_paths = list_eval_file_paths(input_path)
    if not eval_paths:
        print(f"[ERROR] No .eval files found in: {input_path}")
        return 1

    results: List[Dict] = []
    for p in eval_paths:
        r = extract_epochs_from_log(p)
        if not r:
            continue
        # Optional filter by challenge
        if args.challenge:
            ct = (r.get("challenge_type") or "").lower()
            if ct not in [c.lower() for c in args.challenge]:
                continue
        results.append(r)

    # Sort by canonical order
    order = {"formal": 0, "normative": 1, "procedural": 2, "strategic": 3, "epistemic": 4}
    results.sort(key=lambda x: order.get(x.get("challenge_type", "unknown"), 999))

    # Prepare output writer
    out_fh = open(args.output, "w", encoding="utf-8") if args.output else None
    try:
        def p(text: str = ""):
            if out_fh:
                out_fh.write(text + "\n")
            else:
                print(text)

        p("=" * 70)
        p("PER-EPOCH EXTRACTION REPORT")
        p("(Parsed directly from .eval logs — independent of logs.json)")
        p("=" * 70)
        p(f"Source: {input_path}")
        p(f"Logs found: {len(eval_paths)}")
        p(f"Results analyzed: {len(results)}")
        p()

        for r in results:
            print_result(r, p)

        p("=" * 70)
        p("END OF REPORT")
        p("=" * 70)
    finally:
        if out_fh:
            out_fh.close()
            print(f"[OK] Report saved to: {args.output}")

    if args.json:
        with open(args.json, "w", encoding="utf-8") as jf:
            json.dump(results, jf, indent=2)
        print(f"[OK] JSON saved to: {args.json}")

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())


