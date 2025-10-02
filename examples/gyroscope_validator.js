#!/usr/bin/env node
/**
 * Gyroscope v0.7 Beta Trace Block Validator
 *
 * JavaScript utility for validating Gyroscope metadata trace blocks
 * for structural correctness according to the protocol specification.
 *
 * Author: Basil Korompilias (for Gyroscope project)
 * License: Creative Commons Attribution-ShareAlike 4.0 International
 */

class GyroscopeValidator {
    constructor() {
        this.states = {
            "@": "Governance Traceability (Common Source)",
            "&": "Information Variety (Unity Non-Absolute)",
            "%": "Inference Accountability (Opposition Non-Absolute)",
            "~": "Intelligence Integrity (Balance Universal)"
        };

        this.modes = {
            "Generative": "@ → & → % → ~",
            "Integrative": "~ → % → & → @"
        };
    }

    /**
     * Validate a Gyroscope trace block for structural correctness
     * @param {string} traceBlock - The trace block string to validate
     * @returns {object} Validation results with isValid, errors, and warnings
     */
    validateTraceBlock(traceBlock) {
        const lines = traceBlock.trim().split('\n');
        const result = {
            isValid: true,
            errors: [],
            warnings: []
        };

        // Expected structure
        const expectedLines = [
            "[Gyroscope - Start]",
            "[v0.7 Beta: Governance Alignment Metadata]",
            "[Purpose: 4-State Alignment through Recursive Reasoning via Gyroscope. Order matters. Context continuity is preserved across the last 3 messages.]",
            "[States {Format: Symbol = How (Why)}:",
            "@ = Governance Traceability (Common Source),",
            "& = Information Variety (Unity Non-Absolute),",
            "% = Inference Accountability (Opposition Non-Absolute),",
            "~ = Intelligence Integrity (Balance Universal)]",
            "[Modes {Format: Type = Path}:",
            "Generative (Gen) = @ → & → % → ~,",
            "Integrative (Int) = ~ → % → & → @,",
            "Current (Gen/Int) = Gen]",
            "[Data: Timestamp = YYYY-MM-DDTHH:MM, Mode = Gen, Alignment (Y/N) = Y, ID = NNN]",
            "[Gyroscope - End]"
        ];

        // Check each expected line
        for (let i = 0; i < expectedLines.length && i < lines.length; i++) {
            const expected = expectedLines[i];
            const actual = lines[i].trim();

            // Allow flexibility for data line (timestamp, ID will vary)
            if (i === 12) {
                if (!actual.startsWith("[Data:") || !actual.endsWith("]")) {
                    result.errors.push(`Data line malformed: expected format [Data: ...], got: ${actual}`);
                    result.isValid = false;
                }
                // Check for required fields in data line
                if (!actual.includes("Timestamp = ") || !actual.includes("Mode = ") ||
                    !actual.includes("Alignment (Y/N) = ") || !actual.includes("ID = ")) {
                    result.errors.push("Data line missing required fields");
                    result.isValid = false;
                }
            } else if (actual !== expected) {
                result.errors.push(`Line ${i + 1}: expected "${expected}", got "${actual}"`);
                result.isValid = false;
            }
        }

        // Check total line count
        if (lines.length !== expectedLines.length) {
            result.warnings.push(`Expected ${expectedLines.length} lines, found ${lines.length}`);
        }

        // Validate data section specifically
        const dataLine = lines[12];
        if (dataLine) {
            const timestampMatch = dataLine.match(/Timestamp = (\d{4}-\d{2}-\d{2}T\d{2}:\d{2})/);
            if (!timestampMatch) {
                result.errors.push("Invalid timestamp format (expected YYYY-MM-DDTHH:MM)");
                result.isValid = false;
            }

            const modeMatch = dataLine.match(/Mode = (Gen|Int)/);
            if (!modeMatch) {
                result.errors.push("Invalid mode (expected Gen or Int)");
                result.isValid = false;
            }

            const alignmentMatch = dataLine.match(/Alignment \(Y\/N\) = (Y|N)/);
            if (!alignmentMatch) {
                result.errors.push("Invalid alignment (expected Y or N)");
                result.isValid = false;
            }

            const idMatch = dataLine.match(/ID = (\d+)/);
            if (!idMatch) {
                result.errors.push("Invalid ID format (expected numeric)");
                result.isValid = false;
            }
        }

        return result;
    }

    /**
     * Generate a valid trace block
     * @param {string} mode - "Gen" for Generative or "Int" for Integrative
     * @param {number} traceId - Numeric ID for the trace
     * @returns {string} Complete trace block
     */
    generateTraceBlock(mode = "Gen", traceId = 1) {
        const timestamp = new Date().toISOString().slice(0, 16).replace('T', 'T');
        const alignment = "Y";

        return `[Gyroscope - Start]
[v0.7 Beta: Governance Alignment Metadata]
[Purpose: 4-State Alignment through Recursive Reasoning via Gyroscope. Order matters. Context continuity is preserved across the last 3 messages.]
[States {Format: Symbol = How (Why)}:
@ = Governance Traceability (Common Source),
& = Information Variety (Unity Non-Absolute),
% = Inference Accountability (Opposition Non-Absolute),
~ = Intelligence Integrity (Balance Universal)]
[Modes {Format: Type = Path}:
Generative (Gen) = @ → & → % → ~,
Integrative (Int) = ~ → % → & → @,
Current (Gen/Int) = ${mode}]
[Data: Timestamp = ${timestamp}, Mode = ${mode}, Alignment (Y/N) = ${alignment}, ID = ${traceId.toString().padStart(3, '0')}]
[Gyroscope - End]`;
    }

    /**
     * Format an AI response with a trace block
     * @param {string} content - The AI's response content
     * @param {string} mode - "Gen" for Generative or "Int" for Integrative
     * @param {number} traceId - Numeric ID for the trace
     * @returns {string} Complete response with trace block
     */
    formatResponse(content, mode = "Gen", traceId = 1) {
        const traceBlock = this.generateTraceBlock(mode, traceId);
        return `${content}\n\n${traceBlock}`;
    }
}

// Example usage and command-line interface
function main() {
    const validator = new GyroscopeValidator();

    // Example 1: Generate a trace block
    console.log("=== Example 1: Generated Trace Block ===");
    const traceBlock = validator.generateTraceBlock("Gen", 42);
    console.log(traceBlock);
    console.log("\n");

    // Example 2: Validate the generated trace block
    console.log("=== Example 2: Validation Results ===");
    const validation = validator.validateTraceBlock(traceBlock);
    console.log(`Valid: ${validation.isValid}`);
    if (validation.errors.length > 0) {
        console.log(`Errors: ${validation.errors.join(', ')}`);
    }
    if (validation.warnings.length > 0) {
        console.log(`Warnings: ${validation.warnings.join(', ')}`);
    }
    console.log("\n");

    // Example 3: Format a complete response
    console.log("=== Example 3: Complete Formatted Response ===");
    const content = "Balance in life can be approached from multiple perspectives. Physical balance requires adequate rest and exercise. Emotional balance comes from supportive relationships. Systemic balance involves creating structures that support your priorities.";
    const formattedResponse = validator.formatResponse(content, "Gen", 1);
    console.log(formattedResponse);
    console.log("\n");

    // Example 4: Validate the formatted response's trace block
    console.log("=== Example 4: Validation of Formatted Response ===");
    const responseTraceBlock = formattedResponse.split('\n\n')[1];
    const responseValidation = validator.validateTraceBlock(responseTraceBlock);
    console.log(`Response Valid: ${responseValidation.isValid}`);
    if (responseValidation.errors.length > 0) {
        console.log(`Errors: ${responseValidation.errors.join(', ')}`);
    }
}

// CLI interface for validation
function validateFromArgs() {
    const args = process.argv.slice(2);

    if (args.length === 0) {
        console.log("Usage: node gyroscope_validator.js <trace-block>");
        console.log("Or run without arguments for examples");
        process.exit(1);
    }

    const traceBlock = args.join('\n');
    const validator = new GyroscopeValidator();
    const result = validator.validateTraceBlock(traceBlock);

    console.log(`Validation Result: ${result.isValid ? 'VALID' : 'INVALID'}`);
    if (result.errors.length > 0) {
        console.log(`Errors: ${result.errors.join('\n')}`);
    }
    if (result.warnings.length > 0) {
        console.log(`Warnings: ${result.warnings.join('\n')}`);
    }
}

// Run CLI if arguments provided, otherwise show examples
if (process.argv.length > 2) {
    validateFromArgs();
} else {
    main();
}

module.exports = GyroscopeValidator;
