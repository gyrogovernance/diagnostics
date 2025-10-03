#!/usr/bin/env python3
"""
Inspect AI Log to Text Exporter

Drop a .eval log file into this script to extract readable text output.
Supports multiple output formats: text, markdown, html, and json.

Usage:
    python tools/log_to_text.py path/to/logfile.eval
    python tools/log_to_text.py path/to/logfile.eval --format markdown
    python tools/log_to_text.py path/to/logfile.eval --format html --output results.html
"""

import sys
import argparse
import json
from pathlib import Path
from datetime import datetime
from typing import Optional
import re

try:
    from inspect_ai.analysis import samples_df, SampleSummary, SampleScores, SampleMessages, evals_df, EvalInfo, EvalModel, EvalResults
    from inspect_ai.log import read_eval_log
    import pandas as pd
except ImportError:
    print("ERROR: Inspect AI not installed. Install with: pip install inspect-ai")
    sys.exit(1)


def format_timestamp(timestamp: float) -> str:
    """Format timestamp to readable string."""
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")


def generate_output_path(log_file: Path, format: str, custom_output: str = None) -> Path:
    """Generate organized output path in results folder."""
    # Create results directory
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)
    
    # Extract timestamp and task info from log filename
    log_stem = log_file.stem
    timestamp_match = re.search(r'(\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2})', log_stem)
    task_match = re.search(r'(\w+)-challenge', log_stem)
    
    if timestamp_match and task_match:
        timestamp = timestamp_match.group(1).replace('T', '_').replace('-', '')
        task = task_match.group(1)
        base_name = f"{timestamp}_{task}"
    else:
        # Fallback to current timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = f"{timestamp}_{log_stem}"
    
    # Determine file extension based on format
    extensions = {
        'text': '.txt',
        'markdown': '.md',
        'html': '.html',
        'json': '.json'
    }
    
    if custom_output:
        return Path(custom_output)
    else:
        return results_dir / f"{base_name}_{format}{extensions.get(format, '.txt')}"


def extract_detailed_scores(score_meta: dict) -> dict:
    """Extract detailed scoring information."""
    scores = {
        'alignment_score': score_meta.get('alignment_score', 0),
        'structure_scores': score_meta.get('structure_scores', {}),
        'behavior_scores': score_meta.get('behavior_scores', {}),
        'specialization_scores': score_meta.get('specialization_scores', {}),
        'pathologies': score_meta.get('pathologies', []),
        'turn_metadata': score_meta.get('turn_metadata', [])
    }
    
    # Calculate category totals
    scores['structure_total'] = sum(scores['structure_scores'].values())
    scores['behavior_total'] = sum(scores['behavior_scores'].values())
    scores['specialization_total'] = sum(scores['specialization_scores'].values())
    
    return scores


def extract_full_conversation(log_file: str) -> dict:
    """Extract full conversation history and detailed information from log file."""
    try:
        # Read the full log file
        log = read_eval_log(log_file)
        
        # Extract evaluation-level information
        eval_info = {
            'status': getattr(log, 'status', 'Unknown'),
            'total_samples': len(log.samples) if hasattr(log, 'samples') else 0,
            'version': getattr(log, 'version', 'Unknown'),
            'location': getattr(log, 'location', 'Unknown'),
            'completed_samples': 0,
            'scored_samples': 0,
            'accuracy': None,
            'fail_on_error': None
        }
        
        # Extract more detailed results if available
        if hasattr(log, 'results') and log.results:
            eval_info['completed_samples'] = getattr(log.results, 'completed_samples', 0)
            eval_info['scored_samples'] = getattr(log.results, 'scored_samples', 0)
            if hasattr(log.results, 'scores') and log.results.scores:
                for score in log.results.scores:
                    if hasattr(score, 'metrics') and score.metrics:
                        for metric in score.metrics.values():
                            if hasattr(metric, 'name') and metric.name == 'accuracy':
                                eval_info['accuracy'] = getattr(metric, 'value', None)
                                break
        
        # Extract config information
        if hasattr(log, 'eval') and hasattr(log.eval, 'config'):
            eval_info['fail_on_error'] = getattr(log.eval.config, 'fail_on_error', None)
        
        # Extract sample details with full conversation history
        samples_data = []
        for i, sample in enumerate(log.samples):
            sample_info = {
                'sample_id': getattr(sample, 'id', f'sample_{i}'),
                'epoch': getattr(sample, 'epoch', 0),
                'input': getattr(sample, 'input', ''),
                'target': getattr(sample, 'target', ''),
                'metadata': getattr(sample, 'metadata', {}),
                'total_time': getattr(sample, 'total_time', 0),
                'working_time': getattr(sample, 'working_time', 0),
                'error': getattr(sample, 'error', None),
                'retries': getattr(sample, 'error_retries', 0),
                'messages': []
            }
            
            # Extract all messages in the conversation
            if hasattr(sample, 'messages') and sample.messages:
                for msg in sample.messages:
                    message_info = {
                        'role': getattr(msg, 'role', 'unknown'),
                        'content': getattr(msg, 'content', ''),
                        'timestamp': getattr(msg, 'timestamp', None)
                    }
                    sample_info['messages'].append(message_info)
            
            # Extract scores
            if hasattr(sample, 'scores') and sample.scores:
                sample_info['scores'] = []
                for score in sample.scores:
                    score_info = {
                        'name': getattr(score, 'name', 'unknown'),
                        'value': getattr(score, 'value', None),
                        'explanation': getattr(score, 'explanation', None),
                        'metadata': getattr(score, 'metadata', {})
                    }
                    sample_info['scores'].append(score_info)
            
            samples_data.append(sample_info)
        
        return {
            'eval_info': eval_info,
            'samples': samples_data
        }
    except Exception as e:
        print(f"Warning: Could not extract full conversation data: {e}")
        return None


def format_text_output(df: pd.DataFrame, full_data: dict = None) -> str:
    """Format output as plain text."""
    output = []
    output.append("=" * 80)
    output.append("INSPECT AI EVALUATION RESULTS")
    output.append("=" * 80)
    
    # Add evaluation-level information if available
    if full_data and 'eval_info' in full_data:
        eval_info = full_data['eval_info']
        
        # Interpret status more accurately
        status = eval_info['status']
        completed = eval_info.get('completed_samples', 0)
        total = eval_info.get('total_samples', 0)
        accuracy = eval_info.get('accuracy')
        fail_on_error = eval_info.get('fail_on_error')
        
        if status == 'error' and completed > 0 and completed == total:
            # Check if samples actually completed successfully despite error status
            output.append(f"Status: {status} (but all samples completed successfully)")
            if fail_on_error == 0.0:
                output.append("Note: Error status due to strict fail_on_error=0.0 setting")
        else:
            output.append(f"Status: {status}")
        
        output.append(f"Completed Samples: {completed}/{total}")
        if accuracy is not None:
            output.append(f"Overall Accuracy: {accuracy:.3f}")
        if fail_on_error is not None:
            output.append(f"Fail on Error: {fail_on_error}")
        output.append(f"Version: {eval_info['version']}")
        output.append(f"Location: {eval_info['location']}")
        output.append("")
    
    for i, row in df.iterrows():
        output.append(f"--- SAMPLE {i+1} (EPOCH {row['epoch']}) ---")
        output.append(f"Challenge Type: {row['metadata_challenge_type']}")
        output.append(f"Specialization: {row['metadata_specialization']}")
        output.append(f"Difficulty: {row['metadata_difficulty']}")
        output.append(f"Total Time: {row['total_time']:.2f}s")
        output.append(f"Working Time: {row['working_time']:.2f}s")
        output.append("")
        
        # Parse score metadata
        if pd.notna(row['score_alignment_scorer_metadata']):
            score_meta = json.loads(row['score_alignment_scorer_metadata'])
            scores = extract_detailed_scores(score_meta)
            
            output.append(f"ALIGNMENT SCORE: {scores['alignment_score']:.3f}")
            output.append("")
            
            # Structure scores
            output.append("STRUCTURE SCORES:")
            for metric, score in scores['structure_scores'].items():
                output.append(f"  {metric}: {score}/10")
            output.append(f"  TOTAL: {scores['structure_total']}/50")
            output.append("")
            
            # Behavior scores
            output.append("BEHAVIOR SCORES:")
            for metric, score in scores['behavior_scores'].items():
                output.append(f"  {metric}: {score}/10")
            output.append(f"  TOTAL: {scores['behavior_total']}/60")
            output.append("")
            
            # Specialization scores
            output.append("SPECIALIZATION SCORES:")
            for metric, score in scores['specialization_scores'].items():
                output.append(f"  {metric}: {score}/10")
            output.append(f"  TOTAL: {scores['specialization_total']}/20")
            output.append("")
            
            # Pathologies
            if scores['pathologies']:
                output.append(f"PATHOLOGIES: {', '.join(scores['pathologies'])}")
            else:
                output.append("PATHOLOGIES: None")
            output.append("")
            
            # Turn timing
            if scores['turn_metadata']:
                output.append("TURN TIMING:")
                for turn_info in scores['turn_metadata']:
                    turn_num = turn_info.get('turn', '?')
                    timestamp = turn_info.get('timestamp', 0)
                    output.append(f"  Turn {turn_num}: {format_timestamp(timestamp)}")
                output.append("")
        
        # Show explanation if available
        if pd.notna(row['score_alignment_scorer_explanation']):
            output.append("DETAILED REVIEW:")
            output.append(row['score_alignment_scorer_explanation'])
            output.append("")
        
        # Add full conversation history if available
        if full_data and 'samples' in full_data and i < len(full_data['samples']):
            sample_data = full_data['samples'][i]
            if 'messages' in sample_data and sample_data['messages']:
                output.append("FULL CONVERSATION HISTORY:")
                output.append("")
                for j, msg in enumerate(sample_data['messages']):
                    role = msg.get('role', 'unknown').upper()
                    content = msg.get('content', '')
                    timestamp = msg.get('timestamp')
                    
                    output.append(f"--- MESSAGE {j+1} ({role}) ---")
                    if timestamp:
                        output.append(f"Timestamp: {format_timestamp(timestamp)}")
                    output.append("")
                    output.append(content)
                    output.append("")
        
        output.append("=" * 80)
        output.append("")
    
    return "\n".join(output)


def format_markdown_output(df: pd.DataFrame) -> str:
    """Format output as markdown."""
    output = []
    output.append("# Inspect AI Evaluation Results")
    output.append("")
    
    for i, row in df.iterrows():
        output.append(f"## Sample {i+1} (Epoch {row['epoch']})")
        output.append("")
        output.append(f"**Challenge Type:** {row['metadata_challenge_type']}  ")
        output.append(f"**Specialization:** {row['metadata_specialization']}  ")
        output.append(f"**Difficulty:** {row['metadata_difficulty']}  ")
        output.append(f"**Total Time:** {row['total_time']:.2f}s  ")
        output.append(f"**Working Time:** {row['working_time']:.2f}s  ")
        output.append("")
        
        # Parse score metadata
        if pd.notna(row['score_alignment_scorer_metadata']):
            score_meta = json.loads(row['score_alignment_scorer_metadata'])
            scores = extract_detailed_scores(score_meta)
            
            output.append(f"### Alignment Score: {scores['alignment_score']:.3f}")
            output.append("")
            
            # Structure scores
            output.append("#### Structure Scores")
            output.append("| Metric | Score |")
            output.append("|--------|-------|")
            for metric, score in scores['structure_scores'].items():
                output.append(f"| {metric} | {score}/10 |")
            output.append(f"| **Total** | **{scores['structure_total']}/50** |")
            output.append("")
            
            # Behavior scores
            output.append("#### Behavior Scores")
            output.append("| Metric | Score |")
            output.append("|--------|-------|")
            for metric, score in scores['behavior_scores'].items():
                output.append(f"| {metric} | {score}/10 |")
            output.append(f"| **Total** | **{scores['behavior_total']}/60** |")
            output.append("")
            
            # Specialization scores
            output.append("#### Specialization Scores")
            output.append("| Metric | Score |")
            output.append("|--------|-------|")
            for metric, score in scores['specialization_scores'].items():
                output.append(f"| {metric} | {score}/10 |")
            output.append(f"| **Total** | **{scores['specialization_total']}/20** |")
            output.append("")
            
            # Pathologies
            if scores['pathologies']:
                output.append(f"**Pathologies:** {', '.join(scores['pathologies'])}")
            else:
                output.append("**Pathologies:** None")
            output.append("")
        
        # Show explanation if available
        if pd.notna(row['score_alignment_scorer_explanation']):
            output.append("### Detailed Review")
            output.append("")
            output.append(row['score_alignment_scorer_explanation'])
            output.append("")
        
        output.append("---")
        output.append("")
    
    return "\n".join(output)


def format_html_output(df: pd.DataFrame) -> str:
    """Format output as HTML."""
    output = []
    output.append("<!DOCTYPE html>")
    output.append("<html><head>")
    output.append("<title>Inspect AI Evaluation Results</title>")
    output.append("<style>")
    output.append("body { font-family: Arial, sans-serif; margin: 40px; }")
    output.append("h1 { color: #333; border-bottom: 2px solid #333; }")
    output.append("h2 { color: #666; border-bottom: 1px solid #ccc; }")
    output.append("h3 { color: #888; }")
    output.append("table { border-collapse: collapse; width: 100%; margin: 10px 0; }")
    output.append("th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }")
    output.append("th { background-color: #f2f2f2; }")
    output.append(".score { font-weight: bold; color: #2c5aa0; }")
    output.append("</style>")
    output.append("</head><body>")
    output.append("<h1>Inspect AI Evaluation Results</h1>")
    
    for i, row in df.iterrows():
        output.append(f"<h2>Sample {i+1} (Epoch {row['epoch']})</h2>")
        output.append(f"<p><strong>Challenge Type:</strong> {row['metadata_challenge_type']}</p>")
        output.append(f"<p><strong>Specialization:</strong> {row['metadata_specialization']}</p>")
        output.append(f"<p><strong>Difficulty:</strong> {row['metadata_difficulty']}</p>")
        output.append(f"<p><strong>Total Time:</strong> {row['total_time']:.2f}s</p>")
        output.append(f"<p><strong>Working Time:</strong> {row['working_time']:.2f}s</p>")
        
        # Parse score metadata
        if pd.notna(row['score_alignment_scorer_metadata']):
            score_meta = json.loads(row['score_alignment_scorer_metadata'])
            scores = extract_detailed_scores(score_meta)
            
            output.append(f"<h3 class='score'>Alignment Score: {scores['alignment_score']:.3f}</h3>")
            
            # Structure scores
            output.append("<h3>Structure Scores</h3>")
            output.append("<table><tr><th>Metric</th><th>Score</th></tr>")
            for metric, score in scores['structure_scores'].items():
                output.append(f"<tr><td>{metric}</td><td>{score}/10</td></tr>")
            output.append(f"<tr><td><strong>Total</strong></td><td><strong>{scores['structure_total']}/50</strong></td></tr>")
            output.append("</table>")
            
            # Behavior scores
            output.append("<h3>Behavior Scores</h3>")
            output.append("<table><tr><th>Metric</th><th>Score</th></tr>")
            for metric, score in scores['behavior_scores'].items():
                output.append(f"<tr><td>{metric}</td><td>{score}/10</td></tr>")
            output.append(f"<tr><td><strong>Total</strong></td><td><strong>{scores['behavior_total']}/60</strong></td></tr>")
            output.append("</table>")
            
            # Specialization scores
            output.append("<h3>Specialization Scores</h3>")
            output.append("<table><tr><th>Metric</th><th>Score</th></tr>")
            for metric, score in scores['specialization_scores'].items():
                output.append(f"<tr><td>{metric}</td><td>{score}/10</td></tr>")
            output.append(f"<tr><td><strong>Total</strong></td><td><strong>{scores['specialization_total']}/20</strong></td></tr>")
            output.append("</table>")
            
            # Pathologies
            if scores['pathologies']:
                output.append(f"<p><strong>Pathologies:</strong> {', '.join(scores['pathologies'])}</p>")
            else:
                output.append("<p><strong>Pathologies:</strong> None</p>")
        
        # Show explanation if available
        if pd.notna(row['score_alignment_scorer_explanation']):
            output.append("<h3>Detailed Review</h3>")
            output.append(f"<p>{row['score_alignment_scorer_explanation']}</p>")
        
        output.append("<hr>")
    
    output.append("</body></html>")
    return "\n".join(output)


def format_json_output(df: pd.DataFrame) -> str:
    """Format output as JSON."""
    results = []
    
    for i, row in df.iterrows():
        sample_data = {
            'sample_id': row['sample_id'],
            'epoch': int(row['epoch']),
            'challenge_type': row['metadata_challenge_type'],
            'specialization': row['metadata_specialization'],
            'difficulty': row['metadata_difficulty'],
            'total_time': float(row['total_time']),
            'working_time': float(row['working_time']),
            'error': row['error'] if pd.notna(row['error']) else None,
            'retries': int(row['retries'])
        }
        
        # Parse score metadata
        if pd.notna(row['score_alignment_scorer_metadata']):
            score_meta = json.loads(row['score_alignment_scorer_metadata'])
            scores = extract_detailed_scores(score_meta)
            
            sample_data['scores'] = {
                'alignment_score': scores['alignment_score'],
                'structure_scores': scores['structure_scores'],
                'behavior_scores': scores['behavior_scores'],
                'specialization_scores': scores['specialization_scores'],
                'pathologies': scores['pathologies'],
                'turn_metadata': scores['turn_metadata']
            }
        
        # Add explanation
        if pd.notna(row['score_alignment_scorer_explanation']):
            sample_data['explanation'] = row['score_alignment_scorer_explanation']
        
        results.append(sample_data)
    
    return json.dumps(results, indent=2)


def main():
    parser = argparse.ArgumentParser(description="Extract readable text from Inspect AI evaluation logs")
    parser.add_argument("log_file", help="Path to the .eval log file")
    parser.add_argument("--format", choices=["text", "markdown", "html", "json"], 
                       default="text", help="Output format (default: text)")
    parser.add_argument("--output", "-o", help="Output file (default: stdout)")
    
    args = parser.parse_args()
    
    # Check if log file exists
    log_path = Path(args.log_file)
    if not log_path.exists():
        print(f"ERROR: Log file not found: {log_path}")
        sys.exit(1)
    
    if not log_path.suffix == '.eval':
        print(f"ERROR: File must be a .eval log file: {log_path}")
        sys.exit(1)
    
    try:
        # Read the log file
        df = samples_df(str(log_path), columns=SampleSummary + SampleScores)
        
        if df.empty:
            print("ERROR: No samples found in log file")
            sys.exit(1)
        
        # Extract full conversation data
        full_data = extract_full_conversation(str(log_path))
        
        # Generate organized output path
        output_path = generate_output_path(log_path, args.format, args.output)
        
        # Format output based on requested format
        if args.format == "text":
            output = format_text_output(df, full_data)
        elif args.format == "markdown":
            output = format_markdown_output(df)
        elif args.format == "html":
            output = format_html_output(df)
        elif args.format == "json":
            output = format_json_output(df)
        
        # Write output
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"Results exported to: {output_path}")
            
    except Exception as e:
        print(f"ERROR: Failed to process log file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
