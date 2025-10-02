# Gyroscope Tools

This directory contains tools and utilities for working with Gyroscope v0.7 Beta trace blocks.

## 🛠️ Available Tools

### `gyroscope_peg_parser.py`
**Formal Grammar Parser and Validator**

- PEG (Parsing Expression Grammar) implementation for trace blocks
- Validates against the formal grammar specification
- Semantic structure validation
- Programmatic API for integration into other tools

**Key Features:**
- Complete grammar validation
- Semantic correctness checking
- Detailed error reporting
- Trace block generation
- State order validation

**Usage:**
```python
from gyroscope_peg_parser import GyroscopePEGParser

parser = GyroscopePEGParser()
result = parser.parse_trace_block(trace_block_content)
print(f"Valid: {result['is_valid']}")
```

### `batch_validator.py`
**Batch Processing and Validation Tool**

- Process multiple trace blocks from files or stdin
- Generate comprehensive validation reports
- Support for both text and JSON output formats
- Command-line interface for automation

**Key Features:**
- File and directory processing
- Standard input support
- Detailed reporting
- Batch quality assurance
- Error aggregation and summary

## 🚀 Quick Start

### Basic Validation

```python
from gyroscope_peg_parser import GyroscopePEGParser

# Initialize parser
parser = GyroscopePEGParser()

# Your trace block content
trace_block = """[Gyroscope - Start]
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
[Gyroscope - End]"""

# Parse and validate
result = parser.parse_trace_block(trace_block)
if result['is_valid']:
    print("✅ Trace block is valid!")
else:
    print("❌ Trace block has errors:")
    for error in result['errors']:
        print(f"  - {error}")
```

### Batch Processing

```bash
# Validate all trace blocks in current directory
python batch_validator.py *.txt

# Process a large file with multiple trace blocks
python batch_validator.py large_trace_file.txt

# Generate detailed report
python batch_validator.py --report text
```

## 📊 Validation Features

### Grammar Validation
- ✅ Correct header and footer format
- ✅ Proper version specification
- ✅ Exact purpose statement
- ✅ Four states in correct order
- ✅ Valid mode definitions
- ✅ Proper data format (timestamp, mode, alignment, ID)

### Semantic Validation
- ✅ State order matches declared mode
- ✅ Mode paths follow specification
- ✅ Symbol-to-state mapping correctness
- ✅ Policy-to-symbol mapping correctness
- ✅ Data field format validation

### Error Reporting
- 🔍 Line-specific error locations
- 📝 Detailed error descriptions
- ⚠️ Warnings for minor issues
- 📊 Summary statistics

## 🔧 Integration Examples

### With CI/CD Pipeline

```yaml
# GitHub Actions example
- name: Validate Gyroscope Trace Blocks
  run: |
    python tools/batch_validator.py examples/*.txt
    python tools/batch_validator.py --report json > validation_report.json
```

### With Python Application

```python
from gyroscope_peg_parser import GyroscopePEGParser

class GyroscopeApp:
    def __init__(self):
        self.parser = GyroscopePEGParser()

    def add_trace_to_response(self, content, mode="Gen", trace_id=1):
        # Generate trace block
        trace_block = self.parser.generate_trace_block(mode, trace_id)

        # Validate the generated trace
        validation = self.parser.parse_trace_block(trace_block)

        if not validation['is_valid']:
            raise ValueError(f"Generated invalid trace block: {validation['errors']}")

        return f"{content}\n\n{trace_block}"
```

### With Quality Assurance

```python
import os
from batch_validator import BatchValidator

def qa_check_trace_blocks(directory):
    """Quality assurance check for all trace blocks in a directory."""

    validator = BatchValidator()

    # Find all trace block files
    trace_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt') or file.endswith('.md'):
                trace_files.append(os.path.join(root, file))

    # Validate all files
    results = validator.validate_batch_from_files(trace_files)

    # Generate report
    report = validator.generate_report("json")

    # Check for failures
    failed_blocks = [r for r in results if not r['is_valid']]

    if failed_blocks:
        print(f"❌ Found {len(failed_blocks)} invalid trace blocks")
        for block in failed_blocks:
            print(f"  - {block['source']}: {len(block['errors'])} errors")
        return False
    else:
        print("✅ All trace blocks are valid!")
        return True
```

## 📈 Performance Tips

### For Large Batches
- Use `--report json` for machine-readable output
- Process files in smaller chunks if memory is limited
- Consider parallel processing for very large datasets

### For Real-time Validation
- Cache the parser instance
- Pre-validate trace block templates
- Use the lightweight validation for speed-critical paths

## 🐛 Troubleshooting

### Common Issues

1. **"Invalid timestamp format"**
   - Ensure timestamp follows `YYYY-MM-DDTHH:MM` format
   - Use 24-hour format for hours

2. **"States out of order"**
   - For Generative mode: @, &, %, ~
   - For Integrative mode: ~, %, &, @

3. **"Missing required fields"**
   - Check all sections are present
   - Verify exact formatting of headers and brackets

### Debug Mode

Enable debug output by modifying the parser:

```python
# Add debug prints to see parsing progress
result = parser.parse_trace_block(trace_block)
import pprint
pprint.pprint(result)
```

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional output formats (XML, CSV)
- Performance optimizations
- More comprehensive semantic checks
- Integration with testing frameworks

## 📄 License

All tools are licensed under the same Creative Commons Attribution-ShareAlike 4.0 International License as the main project.

© 2025 Basil Korompilias
