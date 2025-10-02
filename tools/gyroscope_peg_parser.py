#!/usr/bin/env python3
"""
Gyroscope v0.7 Beta PEG Parser

Formal grammar implementation for parsing and validating Gyroscope
trace blocks according to the specification.

Author: Basil Korompilias (for Gyroscope project)
License: Creative Commons Attribution-ShareAlike 4.0 International
"""

import re
from typing import Dict, List, Any, Optional
from datetime import datetime


class GyroscopePEGParser:
    """
    PEG (Parsing Expression Grammar) parser for Gyroscope trace blocks.

    Implements the formal grammar specified in the Gyroscope v0.7 Beta
    specification for validating trace block structure and content.
    """

    def __init__(self):
        """Initialize the PEG parser with grammar rules."""
        self.grammar = {
            'trace_block': [
                'HEADER', 'VERSION', 'PURPOSE', 'STATES', 'MODES', 'DATA', 'FOOTER'
            ],

            'HEADER': r'\[Gyroscope - Start\]',
            'VERSION': r'\[v0\.7 Beta: Governance Alignment Metadata\]',
            'PURPOSE': r'\[Purpose: 4-State Alignment through Recursive Reasoning via Gyroscope\. Order matters\. Context continuity is preserved across the last 3 messages\.\]',

            'STATES': [
                r'\[States \{Format: Symbol = How \(Why\)\}:',
                'state', 'state', 'state', 'state',
                r'\]'
            ],

            'state': r'([@&%~]) = ([^()]+) \(([^()]+)\)',

            'MODES': [
                r'\[Modes',
                'mode', 'mode', 'current_mode',
                r'\]'
            ],

            'mode': r'([A-Za-z]+) \(([A-Za-z]+)\) = (.+)',
            'current_mode': r'Current \(([A-Za-z/]+)\) = ([A-Za-z]+)',

            'DATA': r'\[Data: Timestamp = (\d{4}-\d{2}-\d{2}T\d{2}:\d{2}), Mode = ([A-Za-z]+), Alignment \([YN]/N\) = ([YN]), ID = (\d+)\]',

            'FOOTER': r'\[Gyroscope - End\]'
        }

        # Expected state mappings
        self.expected_states = {
            "@": "Governance Traceability",
            "&": "Information Variety",
            "%": "Inference Accountability",
            "~": "Intelligence Integrity"
        }

        self.expected_policies = {
            "@": "Common Source",
            "&": "Unity Non-Absolute",
            "%": "Opposition Non-Absolute",
            "~": "Balance Universal"
        }

    def parse_trace_block(self, trace_block: str) -> Dict[str, Any]:
        """
        Parse a Gyroscope trace block according to the formal grammar.

        Args:
            trace_block: The trace block string to parse

        Returns:
            Dictionary containing parsed components and validation results
        """
        lines = [line.strip() for line in trace_block.strip().split('\n') if line.strip()]

        result = {
            "is_valid": True,
            "parsed": {},
            "errors": [],
            "warnings": []
        }

        # Check minimum line count
        if len(lines) < 10:
            result["errors"].append(f"Too few lines, expected at least 10, found {len(lines)}")
            result["is_valid"] = False

        try:
            # Parse header (line 0)
            if not re.match(self.grammar['HEADER'], lines[0]):
                result["errors"].append("Invalid header format")
                result["is_valid"] = False
            result["parsed"]["header"] = lines[0]

            # Parse version (line 1)
            if not re.match(self.grammar['VERSION'], lines[1]):
                result["errors"].append("Invalid version format")
                result["is_valid"] = False
            result["parsed"]["version"] = lines[1]

            # Parse purpose (line 2)
            if not re.match(self.grammar['PURPOSE'], lines[2]):
                result["errors"].append("Invalid purpose format")
                result["is_valid"] = False
            result["parsed"]["purpose"] = lines[2]

            # Parse states section
            states_section_start = 3
            if states_section_start >= len(lines):
                result["errors"].append("Missing states section")
                result["is_valid"] = False
                return result

            if not lines[states_section_start].startswith("[States"):
                result["errors"].append("Invalid states section header")
                result["is_valid"] = False
                return result

            result["parsed"]["states"] = {}
            # Parse 4 state lines
            for i in range(4):
                state_line_idx = states_section_start + 1 + i
                if state_line_idx >= len(lines):
                    result["errors"].append(f"Missing state line {i+1}")
                    result["is_valid"] = False
                    continue

                state_line = lines[state_line_idx]
                match = re.match(self.grammar['state'], state_line)
                if not match:
                    result["errors"].append(f"Invalid state format at line {state_line_idx+1}: {state_line}")
                    result["is_valid"] = False
                    continue

                symbol, state_name, policy = match.groups()
                result["parsed"]["states"][symbol] = {
                    "name": state_name,
                    "policy": policy
                }

                # Validate against expected values
                if symbol not in self.expected_states:
                    result["errors"].append(f"Unknown state symbol: {symbol}")
                    result["is_valid"] = False
                elif state_name != self.expected_states[symbol]:
                    result["errors"].append(f"Incorrect state name for {symbol}: expected '{self.expected_states[symbol]}', got '{state_name}'")
                    result["is_valid"] = False
                elif policy != self.expected_policies[symbol]:
                    result["errors"].append(f"Incorrect policy for {symbol}: expected '{self.expected_policies[symbol]}', got '{policy}'")
                    result["is_valid"] = False

            # Parse modes section
            modes_section_start = states_section_start + 5  # After states section
            if modes_section_start >= len(lines):
                result["errors"].append("Missing modes section")
                result["is_valid"] = False
                return result

            if "[Modes" not in lines[modes_section_start]:
                result["errors"].append("Invalid modes section header")
                result["is_valid"] = False
                return result

            result["parsed"]["modes"] = {}
            # Parse 2 mode lines
            for i in range(2):
                mode_line_idx = modes_section_start + 1 + i
                if mode_line_idx >= len(lines):
                    result["errors"].append(f"Missing mode line {i+1}")
                    result["is_valid"] = False
                    continue

                mode_line = lines[mode_line_idx]
                match = re.match(self.grammar['mode'], mode_line)
                if not match:
                    result["errors"].append(f"Invalid mode format at line {mode_line_idx+1}: {mode_line}")
                    result["is_valid"] = False
                    continue

                mode_type, mode_short, path = match.groups()
                result["parsed"]["modes"][mode_type] = {
                    "short": mode_short,
                    "path": path
                }

            # Parse current mode line
            current_mode_idx = modes_section_start + 3
            if current_mode_idx >= len(lines):
                result["errors"].append("Missing current mode line")
                result["is_valid"] = False
            else:
                current_mode_line = lines[current_mode_idx]
                match = re.match(self.grammar['current_mode'], current_mode_line)
                if not match:
                    result["errors"].append(f"Invalid current mode format: {current_mode_line}")
                    result["is_valid"] = False
                else:
                    scope, current_mode = match.groups()
                    result["parsed"]["current_mode"] = {
                        "scope": scope,
                        "mode": current_mode
                    }

            # Parse data line
            data_idx = current_mode_idx + 1
            if data_idx >= len(lines):
                result["errors"].append("Missing data line")
                result["is_valid"] = False
            else:
                data_line = lines[data_idx]
                match = re.match(self.grammar['DATA'], data_line)
                if not match:
                    result["errors"].append(f"Invalid data format: {data_line}")
                    result["is_valid"] = False
                else:
                    timestamp, mode, alignment, trace_id = match.groups()
                    result["parsed"]["data"] = {
                        "timestamp": timestamp,
                        "mode": mode,
                        "alignment": alignment,
                        "trace_id": int(trace_id)
                    }

                    # Validate timestamp format
                    try:
                        datetime.strptime(timestamp, "%Y-%m-%dT%H:%M")
                    except ValueError:
                        result["errors"].append(f"Invalid timestamp format: {timestamp}")
                        result["is_valid"] = False

                    # Validate mode
                    if mode not in ["Gen", "Int"]:
                        result["errors"].append(f"Invalid mode: {mode} (expected Gen or Int)")
                        result["is_valid"] = False

                    # Validate alignment
                    if alignment not in ["Y", "N"]:
                        result["errors"].append(f"Invalid alignment: {alignment} (expected Y or N)")
                        result["is_valid"] = False

            # Parse footer (should be last line)
            if lines[-1] != "[Gyroscope - End]":
                result["errors"].append("Invalid or missing footer")
                result["is_valid"] = False
            result["parsed"]["footer"] = lines[-1]

        except Exception as e:
            result["errors"].append(f"Parsing error: {str(e)}")
            result["is_valid"] = False

        return result

    def validate_semantic_structure(self, parsed: Dict[str, Any]) -> List[str]:
        """
        Validate the semantic structure of a parsed trace block.

        Args:
            parsed: Parsed trace block from parse_trace_block()

        Returns:
            List of semantic validation errors
        """
        errors = []

        # Check state order in generative mode
        if parsed.get("parsed", {}).get("current_mode", {}).get("mode") == "Gen":
            states = parsed.get("parsed", {}).get("states", {})
            expected_order = ["@", "&", "%", "~"]

            actual_order = list(states.keys())
            if actual_order != expected_order:
                errors.append(f"States out of order for Generative mode. Expected {expected_order}, got {actual_order}")

        # Check mode paths
        modes = parsed.get("parsed", {}).get("modes", {})
        expected_paths = {
            "Generative": "@ → & → % → ~",
            "Integrative": "~ → % → & → @"
        }

        for mode_name, mode_info in modes.items():
            expected_path = expected_paths.get(mode_name)
            if expected_path and mode_info.get("path") != expected_path:
                errors.append(f"Incorrect path for {mode_name}: expected '{expected_path}', got '{mode_info['path']}'")

        return errors

    def generate_trace_block(self, mode: str = "Gen", trace_id: int = 1) -> str:
        """
        Generate a valid trace block according to the grammar.

        Args:
            mode: "Gen" for Generative or "Int" for Integrative
            trace_id: Numeric trace ID

        Returns:
            Valid trace block string
        """
        timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M")

        return f"""[Gyroscope - Start]
[v0.7 Beta: Governance Alignment Metadata]
[Purpose: 4-State Alignment through Recursive Reasoning via Gyroscope. Order matters. Context continuity is preserved across the last 3 messages.]
[States {{Format: Symbol = How (Why)}}:
@ = Governance Traceability (Common Source),
& = Information Variety (Unity Non-Absolute),
% = Inference Accountability (Opposition Non-Absolute),
~ = Intelligence Integrity (Balance Universal)]
[Modes {{Format: Type = Path}}:
Generative (Gen) = @ → & → % → ~,
Integrative (Int) = ~ → % → & → @,
Current (Gen/Int) = {mode}]
[Data: Timestamp = {timestamp}, Mode = {mode}, Alignment (Y/N) = Y, ID = {trace_id:03d}]
[Gyroscope - End]"""


def example_usage():
    """Demonstrate PEG parser usage."""

    parser = GyroscopePEGParser()

    # Example 1: Parse a valid trace block
    valid_trace = parser.generate_trace_block("Gen", 1)

    print("=== Example 1: Parsing Valid Trace Block ===")
    result = parser.parse_trace_block(valid_trace)
    print(f"Parse valid: {result['is_valid']}")
    if result['errors']:
        print(f"Errors: {result['errors']}")
    print("\n")

    # Example 2: Validate semantic structure
    print("=== Example 2: Semantic Validation ===")
    semantic_errors = parser.validate_semantic_structure(result)
    if semantic_errors:
        print(f"Semantic errors: {semantic_errors}")
    else:
        print("Semantic structure is valid")
    print("\n")

    # Example 3: Parse an invalid trace block
    invalid_trace = """[Gyroscope - Start]
[v0.7 Beta: Governance Alignment Metadata]
[Purpose: 4-State Alignment through Recursive Reasoning via Gyroscope. Order matters. Context continuity is preserved across the last 3 messages.]
[States {Format: Symbol = How (Why)}:
@ = Governance Traceability (Common Source),
& = Information Variety (Unity Non-Absolute),
~ = Intelligence Integrity (Balance Universal)]
[Modes {Format: Type = Path}:
Generative (Gen) = @ → & → % → ~,
Integrative (Int) = ~ → % → & → @,
Current (Gen/Int) = Gen]
[Data: Timestamp = 2025-05-12T12:00, Mode = Gen, Alignment (Y/N) = Y, ID = 001]
[Gyroscope - End]"""

    print("=== Example 3: Parsing Invalid Trace Block (Missing State) ===")
    invalid_result = parser.parse_trace_block(invalid_trace)
    print(f"Parse valid: {invalid_result['is_valid']}")
    if invalid_result['errors']:
        print(f"Errors: {invalid_result['errors']}")
    print("\n")

    # Example 4: Generate and validate round-trip
    print("=== Example 4: Round-trip Validation ===")
    generated = parser.generate_trace_block("Int", 42)
    parsed = parser.parse_trace_block(generated)
    semantic = parser.validate_semantic_structure(parsed)

    print(f"Generated valid: {parsed['is_valid']}")
    print(f"Semantic valid: {len(semantic) == 0}")
    if semantic:
        print(f"Semantic errors: {semantic}")


if __name__ == "__main__":
    example_usage()
