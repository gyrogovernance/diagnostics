#!/usr/bin/env python3
"""
Extract analyst-generated insights from evaluation data, organized by topic.

This script reads evaluation data from all models and extracts insights for:
- Normative Challenge (Poverty Reduction)
- Strategic Challenge (AI Medical Regulation)
- Epistemic Challenge (AI Alignment & Epistemic Limits)

Output: Three markdown files in showcase/insights/ with raw insights from all models.
"""

import json
import os
from pathlib import Path
from datetime import datetime

# Challenge mapping
CHALLENGE_MAP = {
    "normative": {
        "name": "AI-Empowered Prosperity",
        "title": "Normative Challenge: Advancing Global Well-Being Through Human-AI Cooperation",
        "output": "aie_prosperity_insights_raw.md"
    },
    "strategic": {
        "name": "AI-Empowered Health",
        "title": "Strategic Challenge: Global Health System Regulatory Evolution",
        "output": "aie_health_insights_raw.md"
    },
    "epistemic": {
        "name": "AI-Empowered Alignment",
        "title": "Epistemic Challenge: Recursive Reasoning and Human-AI Cooperation",
        "output": "aie_alignment_insights_raw.md"
    }
}

def extract_insights_from_file(json_path):
    """Extract insights from a single evaluation data file."""
    print(f"Reading {json_path}...")
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Extract model name from filename (e.g., "grok_4_data.json" -> "Grok-4")
    filename = Path(json_path).stem
    if filename.endswith('_data'):
        model_name = filename.replace('_data', '').replace('_', ' ').title()
    else:
        model_name = filename.replace('_', ' ').title()
    
    insights_by_challenge = {}
    
    # The data is organized with challenge names as top-level keys
    for challenge_name in ['normative', 'strategic', 'epistemic']:
        if challenge_name not in data:
            continue
        
        challenge_data = data[challenge_name]
        insights_by_challenge[challenge_name] = []
        
        # Extract insights from all epochs
        for idx, epoch_data in enumerate(challenge_data.get('epoch_results', []), 1):
            insights = epoch_data.get('insights', '')
            if insights and insights.strip():
                insights_by_challenge[challenge_name].append({
                    'epoch': idx,
                    'content': insights.strip()
                })
    
    return model_name, insights_by_challenge

def format_insights_markdown(challenge_key, all_model_insights):
    """Format insights as markdown for a specific challenge."""
    challenge_info = CHALLENGE_MAP[challenge_key]
    
    lines = []
    lines.append(f"# {challenge_info['name']}")
    lines.append(f"## {challenge_info['title']}")
    lines.append("")
    lines.append("> **Raw Insights Extracted from Multi-Model Evaluation**")
    lines.append(f"> *Generated: {datetime.now().strftime('%Y-%m-%d')}*")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("This file contains the raw analyst-generated insights from all evaluated models.")
    lines.append("Use this as source material to write the consolidated insight report.")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Add insights organized by model
    for model_name, insights_list in all_model_insights.items():
        if not insights_list:
            continue
            
        lines.append(f"## {model_name}")
        lines.append("")
        
        for insight_data in insights_list:
            epoch = insight_data['epoch']
            content = insight_data['content']
            
            lines.append(f"### Epoch {epoch}")
            lines.append("")
            lines.append(content)
            lines.append("")
            lines.append("---")
            lines.append("")
    
    return "\n".join(lines)

def main():
    """Main execution function."""
    # Set up paths
    project_root = Path(__file__).parent.parent
    showcase_dir = project_root / "showcase"
    insights_dir = showcase_dir / "insights" / "raw"
    
    # Ensure output directory exists
    insights_dir.mkdir(parents=True, exist_ok=True)
    
    # Find all data files
    data_files = list(showcase_dir.glob("*_data.json"))
    
    if not data_files:
        print("[ERROR] No evaluation data files found in showcase/")
        print("   Looking for files matching pattern: *_data.json")
        return
    
    print(f"Found {len(data_files)} evaluation data files")
    print()
    
    # Collect insights by challenge across all models
    insights_by_challenge = {
        'normative': {},
        'strategic': {},
        'epistemic': {}
    }
    
    for data_file in data_files:
        try:
            model_name, model_insights = extract_insights_from_file(data_file)
            
            for challenge_key, insights_list in model_insights.items():
                if challenge_key in insights_by_challenge:
                    insights_by_challenge[challenge_key][model_name] = insights_list
                    print(f"  [OK] {model_name}: {challenge_key} - {len(insights_list)} epoch(s)")
        
        except Exception as e:
            print(f"  [ERROR] Error processing {data_file.name}: {e}")
            continue
    
    print()
    print("Generating insight files...")
    print()
    
    # Generate output files
    for challenge_key, all_model_insights in insights_by_challenge.items():
        if not all_model_insights:
            print(f"  [WARN] No insights found for {challenge_key}")
            continue
        
        challenge_info = CHALLENGE_MAP[challenge_key]
        output_file = insights_dir / challenge_info['output']
        
        markdown_content = format_insights_markdown(challenge_key, all_model_insights)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        total_epochs = sum(len(insights) for insights in all_model_insights.values())
        print(f"  [OK] {challenge_info['name']}")
        print(f"    -> {output_file.relative_to(project_root)}")
        print(f"    -> {len(all_model_insights)} models, {total_epochs} total epochs")
        print()
    
    print("[DONE] Raw insights extracted by topic.")
    print()
    print("Next steps:")
    print("  1. Review the raw insight files in showcase/insights/raw/")
    print("  2. Use them as source material for your consolidated reports")
    print("  3. Fill in the template files with synthesized findings")

if __name__ == "__main__":
    main()

