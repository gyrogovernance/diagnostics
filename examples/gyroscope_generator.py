#!/usr/bin/env python3
"""
Gyroscope v0.7 Beta Trace Block Generator

This module provides utilities for generating Gyroscope metadata trace blocks
for AI responses to ensure alignment with the Gyroscope protocol.

Author: Basil Korompilias (for Gyroscope project)
License: Creative Commons Attribution-ShareAlike 4.0 International
"""

import datetime
from typing import Dict, Any, Optional
import json


class GyroscopeGenerator:
    """
    Generator for Gyroscope v0.7 Beta trace blocks.

    This class handles the creation of metadata blocks that document
    the reasoning process according to the four-state Gyroscope protocol.
    """

    def __init__(self):
        """Initialize the Gyroscope trace generator."""
        self.states = {
            "@": "Governance Traceability (Common Source)",
            "&": "Information Variety (Unity Non-Absolute)",
            "%": "Inference Accountability (Opposition Non-Absolute)",
            "~": "Intelligence Integrity (Balance Universal)"
        }

        self.modes = {
            "Generative": "@ → & → % → ~",
            "Integrative": "~ → % → & → @"
        }

    def generate_trace_block(self, mode: str = "Gen", trace_id: Optional[int] = None) -> str:
        """
        Generate a complete Gyroscope trace block.

        Args:
            mode: Either "Gen" for Generative or "Int" for Integrative
            trace_id: Numeric ID for the trace (auto-incremented if not provided)

        Returns:
            Complete trace block as a string
        """
        if trace_id is None:
            # In a real implementation, you'd track this across conversations
            trace_id = 1

        timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")
        alignment = "Y"  # Assume valid generation

        # Determine full mode name
        full_mode = "Generative" if mode == "Gen" else "Integrative"

        trace_block = f"""[Gyroscope - Start]
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
[Data: Timestamp = {timestamp}, Mode = {mode}, Alignment (Y/N) = {alignment}, ID = {trace_id:03d}]
[Gyroscope - End]"""

        return trace_block

    def validate_trace_block(self, trace_block: str) -> Dict[str, Any]:
        """
        Validate a Gyroscope trace block for structural correctness.

        Args:
            trace_block: The trace block string to validate

        Returns:
            Dictionary with validation results
        """
        lines = trace_block.strip().split('\n')
        validation = {
            "is_valid": True,
            "errors": [],
            "warnings": []
        }

        # Check header
        if not lines[0].strip() == "[Gyroscope - Start]":
            validation["errors"].append("Missing or incorrect header")
            validation["is_valid"] = False

        # Check version
        if not lines[1].strip() == "[v0.7 Beta: Governance Alignment Metadata]":
            validation["errors"].append("Missing or incorrect version line")
            validation["is_valid"] = False

        # Check purpose line
        expected_purpose = "[Purpose: 4-State Alignment through Recursive Reasoning via Gyroscope. Order matters. Context continuity is preserved across the last 3 messages.]"
        if not lines[2].strip() == expected_purpose:
            validation["errors"].append("Missing or incorrect purpose line")
            validation["is_valid"] = False

        # Check states section
        states_start = 3
        if not lines[states_start].strip().startswith("[States {Format: Symbol = How (Why)}:"):
            validation["errors"].append("Missing or incorrect states section")
            validation["is_valid"] = False

        # Check all four states are present in correct order
        expected_states = ["@ = Governance Traceability (Common Source),",
                          "& = Information Variety (Unity Non-Absolute),",
                          "% = Inference Accountability (Opposition Non-Absolute),",
                          "~ = Intelligence Integrity (Balance Universal)"]

        for i, expected_state in enumerate(expected_states):
            if not lines[states_start + 1 + i].strip() == expected_state:
                validation["errors"].append(f"Incorrect state definition: {expected_state}")
                validation["is_valid"] = False

        # Check modes section
        modes_start = states_start + 5
        if not lines[modes_start].strip().startswith("[Modes {Format: Type = Path}:"):
            validation["errors"].append("Missing or incorrect modes section")
            validation["is_valid"] = False

        # Check data section
        data_start = modes_start + 4
        data_line = lines[data_start].strip()
        if not data_line.startswith("[Data:"):
            validation["errors"].append("Missing or incorrect data section")
            validation["is_valid"] = False

        # Check footer
        if not lines[-1].strip() == "[Gyroscope - End]":
            validation["errors"].append("Missing or incorrect footer")
            validation["is_valid"] = False

        return validation

    def format_ai_response(self, content: str, mode: str = "Gen", trace_id: Optional[int] = None) -> str:
        """
        Format an AI response with a Gyroscope trace block.

        Args:
            content: The AI's response content
            mode: Either "Gen" for Generative or "Int" for Integrative
            trace_id: Numeric ID for the trace

        Returns:
            Complete response with trace block appended
        """
        trace_block = self.generate_trace_block(mode, trace_id)
        return f"{content}\n\n{trace_block}"


def example_usage():
    """Demonstrate usage of the Gyroscope generator."""

    generator = GyroscopeGenerator()

    # Example 1: Simple AI response
    response = "Balance in life can be achieved by considering multiple dimensions. From a physical perspective, ensure adequate rest and exercise. Emotionally, maintain supportive relationships."

    formatted_response = generator.format_ai_response(response, trace_id=1)
    print("=== Example 1: Formatted AI Response ===")
    print(formatted_response)
    print("\n")

    # Example 2: Validate a trace block
    validation = generator.validate_trace_block(formatted_response.split('\n\n')[1])
    print("=== Example 2: Validation Results ===")
    print(f"Valid: {validation['is_valid']}")
    if validation['errors']:
        print(f"Errors: {validation['errors']}")
    print("\n")

    # Example 3: Generate standalone trace block
    trace_block = generator.generate_trace_block("Gen", 42)
    print("=== Example 3: Standalone Trace Block ===")
    print(trace_block)


if __name__ == "__main__":
    example_usage()
