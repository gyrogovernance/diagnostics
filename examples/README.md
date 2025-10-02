# Gyroscope Examples

This directory contains practical examples and implementations of the Gyroscope v0.7 Beta protocol.

## 📁 Files

### `gyroscope_generator.py`
**Python implementation for automated trace generation**

- Complete Python class for generating valid Gyroscope trace blocks
- Validation utilities to check trace block structural correctness
- Example usage and demonstration functions
- Handles both Generative (AI) and Integrative (human) modes

**Key Features:**
- Automatic timestamp generation
- Sequential trace ID management
- Comprehensive validation with detailed error reporting
- Easy integration into existing AI systems

### `gyroscope_validator.js`
**JavaScript validation and generation utilities**

- Node.js compatible validator for trace blocks
- Command-line interface for validation
- Example usage demonstrations
- Lightweight implementation for web applications

**Key Features:**
- Structural validation against the PEG grammar
- Data format validation (timestamps, IDs, modes)
- Error reporting and warnings
- CLI interface for batch processing

### `example_conversation.md`
**Complete conversation example with analysis**

- Real-world conversation demonstrating Gyroscope in action
- Shows both human (optional) and AI trace blocks
- Detailed analysis of reasoning paths
- Benefits demonstration and validation examples

### `diagnostic_evaluation_examples.py`
**Comprehensive diagnostic evaluation framework**

- Implements the full Gyroscope Alignment Diagnostics methodology
- Demonstrates 5 challenge types with comparative evaluation
- Shows how to score responses across 20 metrics and 3 tiers
- Includes pathology detection and statistical analysis
- Provides complete evaluation workflow examples

## 🚀 Quick Start

### Using Python Generator

```python
from gyroscope_generator import GyroscopeGenerator

generator = GyroscopeGenerator()

# Generate a trace block
trace_block = generator.generate_trace_block("Gen", 1)

# Format an AI response
response = "Your AI response here..."
formatted_response = generator.format_ai_response(response, trace_id=1)

# Validate a trace block
validation = generator.validate_trace_block(trace_block)
print(f"Valid: {validation['is_valid']}")
```

### Using JavaScript Validator

```javascript
const GyroscopeValidator = require('./gyroscope_validator');

const validator = new GyroscopeValidator();

// Generate a trace block
const traceBlock = validator.generateTraceBlock("Gen", 1);

// Validate a trace block
const result = validator.validateTraceBlock(traceBlock);
console.log(`Valid: ${result.isValid}`);

// Format a response
const content = "Your AI response here...";
const formatted = validator.formatResponse(content, "Gen", 1);
```

### Command Line Usage

```bash
# Validate a trace block
node gyroscope_validator.js "[Gyroscope - Start]
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
Current (Gen/Int) = Gen]
[Data: Timestamp = 2025-05-12T12:00, Mode = Gen, Alignment (Y/N) = Y, ID = 001]
[Gyroscope - End]"

# Run examples
node gyroscope_validator.js
```

## 🔧 Integration Examples

### With OpenAI API

```python
import openai
from gyroscope_generator import GyroscopeGenerator

def get_gyroscope_response(prompt, model="gpt-4"):
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000
    )

    generator = GyroscopeGenerator()
    content = response.choices[0].message.content
    formatted_response = generator.format_ai_response(content, trace_id=1)

    return formatted_response
```

### With Express.js

```javascript
const express = require('express');
const GyroscopeValidator = require('./gyroscope_validator');

const app = express();
const validator = new GyroscopeValidator();

app.post('/chat', async (req, res) => {
    const userMessage = req.body.message;

    // Get AI response (implement your AI integration here)
    const aiResponse = await getAIResponse(userMessage);

    // Format with Gyroscope trace
    const formattedResponse = validator.formatResponse(aiResponse, "Gen", 1);

    res.json({ response: formattedResponse });
});
```

## 📊 Validation Examples

### Valid Trace Block

```python
# This will pass validation
valid_trace = generator.generate_trace_block("Gen", 1)
validation = generator.validate_trace_block(valid_trace)
assert validation['is_valid'] == True
```

### Invalid Trace Block (Missing State)

```python
# This will fail validation
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
[Data: Timestamp = 2025-05-12T12:00, Mode = Gen, Alignment (Y/N) = N, ID = 001]
[Gyroscope - End]"""

validation = generator.validate_trace_block(invalid_trace)
assert validation['is_valid'] == False
assert "Incorrect state definition" in validation['errors']
```

## 🤝 Contributing

Feel free to contribute additional examples for other programming languages or AI frameworks!

**Guidelines:**
- Include proper documentation and examples
- Follow the Gyroscope v0.7 Beta specification
- Add validation tests
- Maintain compatibility with the formal grammar (PEG)

## 📄 License

All examples are licensed under the same Creative Commons Attribution-ShareAlike 4.0 International License as the main project.

© 2025 Basil Korompilias
