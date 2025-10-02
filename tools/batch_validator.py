#!/usr/bin/env python3
"""
Gyroscope Batch Validator

Utility script for validating multiple Gyroscope trace blocks from files
or standard input. Useful for batch processing and quality assurance.

Author: Basil Korompilias (for Gyroscope project)
License: Creative Commons Attribution-ShareAlike 4.0 International
"""

import sys
import os
import json
from typing import List, Dict, Any
from gyroscope_peg_parser import GyroscopePEGParser


class BatchValidator:
    """
    Batch validation utility for Gyroscope trace blocks.

    Processes multiple trace blocks from various sources and provides
    comprehensive validation reports.
    """

    def __init__(self):
        """Initialize the batch validator."""
        self.parser = GyroscopePEGParser()
        self.results = []

    def validate_from_file(self, filepath: str) -> List[Dict[str, Any]]:
        """
        Validate trace blocks from a file.

        Args:
            filepath: Path to the file containing trace block(s)

        Returns:
            List of validation result dictionaries
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Try to split by double newlines (trace block boundaries)
            blocks = content.split('\n\n')

            results = []
            for i, block in enumerate(blocks):
                block = block.strip()
                if block and len(block.split('\n')) >= 10:  # Minimum reasonable size
                    result = self.validate_trace_block(block, source=f"file:{filepath}:block_{i+1}")
                    results.append(result)

            # If no blocks found with double newlines, treat whole file as one block
            if not results:
                results.append(self.validate_trace_block(content, source=f"file:{filepath}"))

            return results

        except FileNotFoundError:
            return [{
                "source": filepath,
                "is_valid": False,
                "errors": [f"File not found: {filepath}"],
                "warnings": []
            }]
        except Exception as e:
            return [{
                "source": filepath,
                "is_valid": False,
                "errors": [f"Error reading file: {str(e)}"],
                "warnings": []
            }]

    def validate_from_string(self, content: str, source: str = "string") -> Dict[str, Any]:
        """
        Validate a trace block from a string.

        Args:
            content: The trace block content as a string
            source: Source identifier for the trace block

        Returns:
            Validation result dictionary
        """
        return self.validate_trace_block(content, source=source)

    def validate_trace_block(self, content: str, source: str = "unknown") -> Dict[str, Any]:
        """
        Validate a single trace block.

        Args:
            content: The trace block content
            source: Source identifier

        Returns:
            Validation result dictionary
        """
        # Parse the trace block
        parsed = self.parser.parse_trace_block(content)

        # Validate semantic structure
        semantic_errors = self.parser.validate_semantic_structure(parsed)

        # Combine all errors
        all_errors = parsed["errors"] + semantic_errors

        result = {
            "source": source,
            "is_valid": parsed["is_valid"] and len(semantic_errors) == 0,
            "errors": all_errors,
            "warnings": parsed["warnings"],
            "parsed_data": parsed.get("parsed", {}),
            "line_count": len(content.strip().split('\n')) if content.strip() else 0
        }

        return result

    def validate_batch_from_files(self, filepaths: List[str]) -> List[Dict[str, Any]]:
        """
        Validate trace blocks from multiple files.

        Args:
            filepaths: List of file paths to process

        Returns:
            List of validation results
        """
        results = []
        for filepath in filepaths:
            file_results = self.validate_from_file(filepath)
            results.extend(file_results)

        self.results.extend(results)
        return results

    def validate_batch_from_stdin(self) -> List[Dict[str, Any]]:
        """
        Validate trace blocks from standard input.

        Expects trace blocks separated by blank lines or special delimiters.

        Returns:
            List of validation results
        """
        content = sys.stdin.read()

        # Try to split by double newlines (trace block boundaries)
        blocks = content.split('\n\n')

        results = []
        for i, block in enumerate(blocks):
            block = block.strip()
            if block and len(block.split('\n')) >= 10:  # Minimum reasonable size
                result = self.validate_trace_block(block, source=f"stdin:block_{i+1}")
                results.append(result)

        self.results.extend(results)
        return results

    def generate_report(self, format: str = "text") -> str:
        """
        Generate a validation report.

        Args:
            format: Output format ("text" or "json")

        Returns:
            Formatted report string
        """
        if format == "json":
            return json.dumps(self.results, indent=2, ensure_ascii=False)

        # Generate text report
        report = []
        report.append("Gyroscope Batch Validation Report")
        report.append("=" * 40)
        report.append("")

        total_blocks = len(self.results)
        valid_blocks = sum(1 for r in self.results if r["is_valid"])
        invalid_blocks = total_blocks - valid_blocks

        report.append(f"Total trace blocks: {total_blocks}")
        report.append(f"Valid blocks: {valid_blocks}")
        report.append(f"Invalid blocks: {invalid_blocks}")
        if total_blocks > 0:
            success_rate = f"{(valid_blocks/total_blocks*100):.1f}%"
        else:
            success_rate = "N/A"
        report.append(f"Success rate: {success_rate}")
        report.append("")

        for i, result in enumerate(self.results, 1):
            report.append(f"Block {i}: {result['source']}")
            report.append(f"  Status: {'✓ VALID' if result['is_valid'] else '✗ INVALID'}")
            report.append(f"  Lines: {result['line_count']}")

            if result["errors"]:
                report.append("  Errors:")
                for error in result["errors"]:
                    report.append(f"    - {error}")

            if result["warnings"]:
                report.append("  Warnings:")
                for warning in result["warnings"]:
                    report.append(f"    - {warning}")

            report.append("")

        return "\n".join(report)

    def save_report(self, filepath: str, format: str = "text"):
        """
        Save the validation report to a file.

        Args:
            filepath: Path to save the report
            format: Report format ("text" or "json")
        """
        report = self.generate_report(format)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"Report saved to: {filepath}")


def main():
    """Main function for command-line usage."""

    validator = BatchValidator()

    if len(sys.argv) < 2:
        print("Gyroscope Batch Validator")
        print("Usage:")
        print("  python batch_validator.py file1.txt file2.txt ...  # Validate files")
        print("  python batch_validator.py --stdin                  # Validate from stdin")
        print("  python batch_validator.py --report format          # Generate report")
        print("  python batch_validator.py --help                   # Show this help")
        print("")
        print("Examples:")
        print("  # Validate all .txt files in current directory")
        print("  python batch_validator.py *.txt")
        print("")
        print("  # Read from stdin (pipe or redirect)")
        print("  cat traces.txt | python batch_validator.py --stdin")
        print("")
        print("  # Generate JSON report")
        print("  python batch_validator.py --report json > report.json")
        return

    command = sys.argv[1]

    if command == "--stdin":
        # Read from standard input
        print("Reading trace blocks from stdin...")
        results = validator.validate_batch_from_stdin()
        print(f"Processed {len(results)} trace blocks")

    elif command == "--report":
        # Generate report
        format_type = sys.argv[2] if len(sys.argv) > 2 else "text"
        print(validator.generate_report(format_type))

    elif command == "--help":
        print("Gyroscope Batch Validator - Help")
        print("=" * 35)
        print("This tool validates Gyroscope v0.7 Beta trace blocks for")
        print("structural and semantic correctness according to the formal grammar.")
        print("")
        print("Features:")
        print("- Batch processing of multiple trace blocks")
        print("- File and stdin input support")
        print("- Detailed error reporting")
        print("- JSON and text report formats")
        print("- Semantic structure validation")
        print("")
        print("For more information, see the Gyroscope specification.")

    else:
        # Treat remaining arguments as files
        filepaths = sys.argv[1:]
        print(f"Validating {len(filepaths)} files...")
        results = validator.validate_batch_from_files(filepaths)
        print(f"Processed {len(results)} trace blocks")

    # Show summary
    if hasattr(validator, 'results') and validator.results:
        valid_count = sum(1 for r in validator.results if r["is_valid"])
        total_count = len(validator.results)
        if total_count > 0:
            success_rate = f"{(valid_count/total_count*100):.1f}%"
        else:
            success_rate = "0%"
    print(f"\nSummary: {valid_count}/{total_count} blocks valid ({success_rate})")


if __name__ == "__main__":
    main()
