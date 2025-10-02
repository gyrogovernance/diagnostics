# Inspect AI Condensed Documentation for Gyroscopic Alignment Diagnostics Integration

## Overview

Inspect AI is an open-source framework for large language model evaluations created by the UK AI Security Institute. This condensed documentation focuses on the key components and concepts needed to integrate the Gyroscopic Alignment Diagnostics evaluation suite.

## Core Architecture

Inspect evaluations have three main components:

1. **Datasets** - Contain labelled samples with `input` and `target` fields
2. **Solvers** - Chain together to evaluate inputs and produce results (prompt engineering, generation, critique)
3. **Scorers** - Evaluate solver outputs against targets using various mechanisms

## Key Components

### Tasks

Tasks are the fundamental unit of integration, bringing together datasets, solvers, and scorers:

```python
from inspect_ai import Task, task
from inspect_ai.dataset import json_dataset
from inspect_ai.scorer import model_graded_fact
from inspect_ai.solver import chain_of_thought, generate

@task
def alignment_evaluation():
    return Task(
        dataset=json_dataset("alignment_samples.jsonl"),
        solver=[chain_of_thought(), generate()],
        scorer=model_graded_fact()
    )
```

**Task Options:**
- `dataset` - Samples to evaluate
- `solver` - Single solver or list of chained solvers
- `scorer` - How to evaluate outputs
- `epochs` - Number of evaluation cycles per sample
- `sandbox` - Execution environment for untrusted code
- `metrics` - Custom metrics beyond scorer defaults
- `fail_on_error` - Error tolerance threshold for robust evaluation
- `message_limit` - Maximum messages per sample to prevent infinite loops
- `time_limit` - Maximum execution time per sample
- `token_limit` - Maximum tokens per sample

### Datasets

Datasets contain evaluation samples with these key fields:

```python
from inspect_ai.dataset import Sample

Sample(
    input="What are the key principles of gyroscopic alignment?",
    target="Balance between closure and openness, recursive coherence, topological stability",
    id="formal_001",
    metadata={
        "challenge_type": "formal",
        "difficulty": "intermediate"
    }
)
```

**Dataset Formats:**
- CSV, JSON, JSONL files
- Hugging Face datasets
- Custom MemoryDataset for programmatic creation
- S3 storage support

**Loading Examples:**
```python
# Simple CSV/JSON loading
dataset = csv_dataset("samples.csv")

# With field mapping for non-standard formats
dataset = json_dataset("samples.jsonl", FieldSpec(
    input="question",
    target="expected_answer",
    metadata=["category", "difficulty"]
))

# Custom sample processing
def record_to_sample(record):
    return Sample(
        input=record["prompt"],
        target=record["target"],
        metadata={"type": record["challenge_type"]}
    )

dataset = json_dataset("samples.jsonl", record_to_sample)
```

### Solvers

Solvers are the heart of Inspect evaluations and handle the execution logic. They can serve multiple purposes:

1. **Prompt Engineering** - Modifying inputs before model calls
2. **Model Generation** - Actually calling the model
3. **Self Critique** - Model self-evaluation and refinement
4. **Multi-turn Dialog** - Managing conversation flow
5. **Tool Integration** - Enabling model tool usage
6. **Agent Scaffolding** - Running complex agent workflows

**Solver Types:**

**Message Management:**
- `system_message()` - Adds system context/instructions
- `user_message()` - Adds user context
- `prompt_template()` - Template-based prompt engineering with variable substitution

**Reasoning Enhancement:**
- `chain_of_thought()` - Prompts for step-by-step reasoning
- `self_critique()` - Model self-evaluation and refinement

**Model Interaction:**
- `generate()` - Basic model call (the core solver)
- `multiple_choice()` - Specialized for A/B/C/D style questions

**Tool Integration:**
- `use_tools()` - Enables model tool calling capabilities

**Solver Composition:**
Solvers can be chained together or used as composite specifications for complex evaluation workflows.

**Example Composition:**
```python
@solver
def alignment_solver():
    return chain([
        system_message("You are an AI alignment expert..."),
        chain_of_thought(),
        generate(),
        self_critique()
    ])
```

**Custom Solver Example:**
```python
@solver
def custom_alignment_solver():
    async def solve(state, generate):
        # Custom logic here
        # Can call generate() multiple times for multi-turn evaluation
        return await generate(state)
    return solve
```

### Scorers

Scorers evaluate model outputs against targets:

**Built-in Scorers:**
- `includes()` - Target text appears in output
- `match()` - Target matches beginning/end of output
- `exact()` - Exact text matching
- `pattern()` - Regex-based extraction
- `model_graded_qa()` - Model-based evaluation for open-ended questions
- `model_graded_fact()` - Model-based evaluation for factual accuracy
- `choice()` - Multiple choice scoring

**Model-Graded Scoring (Most Relevant for Alignment):**
```python
@scorer(metrics=[accuracy(), stderr()])
def alignment_grader():
    async def score(state, target):
        # Custom grading logic
        return Score(
            value="C" if is_aligned else "I",
            explanation=grading_reasoning
        )
    return score

# Using model-graded scoring
scorer = model_graded_qa(
    template="alignment_grading_template.txt",
    instructions="Grade based on gyroscopic alignment principles...",
    model="openai/gpt-4o"
)
```

**Multiple Scorers:**
```python
Task(
    dataset=dataset,
    solver=solver,
    scorer=[
        model_graded_fact(),           # Factual accuracy
        custom_alignment_scorer()      # Alignment quality
    ]
)
```

## Model Integration

**Model Specification:**
```python
# In eval() call
eval(task, model="openai/gpt-4o")

# Multiple models for comparison
eval(task, model=["openai/gpt-4o", "anthropic/claude-3-opus"])

# Model roles for different purposes
eval(task, model_roles={"grader": "anthropic/claude-3-haiku"})
```

**Supported Providers:**
- OpenAI, Anthropic, Google, Grok, Mistral
- Hugging Face models
- Local models (vLLM, Ollama, llama-cpp-python)
- AWS Bedrock, Azure AI, TogetherAI, etc.

## Execution

**CLI Usage:**
```bash
# Run evaluation
inspect eval alignment_eval.py --model openai/gpt-4o

# With task parameters
inspect eval alignment_eval.py -T challenge_type="formal" --model openai/gpt-4o

# Multiple runs with different configurations
inspect eval alignment_eval.py --model openai/gpt-4o,anthropic/claude-3-opus
```

**Python API:**
```python
from inspect_ai import eval

# Single evaluation
results = eval(alignment_task(), model="openai/gpt-4o")

# Multiple evaluations
logs = eval_set([
    alignment_task(challenge_type="formal"),
    alignment_task(challenge_type="normative"),
    alignment_task(challenge_type="procedural")
], model="openai/gpt-4o")
```

## Error Handling and Limits

**Robust Evaluation:**
```python
Task(
    dataset=dataset,
    solver=solver,
    scorer=scorer,
    fail_on_error=0.1,        # Tolerate up to 10% sample errors
    time_limit=900,           # 15 minute timeout per sample
    message_limit=50,         # Prevent infinite conversation loops
    token_limit=10000         # Prevent excessive token usage
)
```

**Retry Logic:**
```python
# Retry failed samples up to 3 times
eval(task, retry_on_error=3)
```

## Sandboxing

**Isolated Execution:**
```python
Task(
    dataset=dataset,
    solver=solver,
    scorer=scorer,
    sandbox="docker",           # Use Docker for untrusted code
    sandbox=("docker", "custom-compose.yaml")  # Custom sandbox config
)
```

## Tool Calling

**Custom Tools:**
```python
@tool
def alignment_analysis():
    async def run(input_text):
        # Custom alignment analysis logic
        return analysis_result
    return run

@solver
def tool_enabled_solver():
    return chain([
        use_tools([alignment_analysis()]),
        generate()
    ])
```

## Eval Sets

**Multiple Evaluations:**
```python
from inspect_ai import eval_set

# Run multiple evaluation configurations
logs = eval_set([
    formal_challenge_task(),
    normative_challenge_task(),
    procedural_challenge_task()
], model="openai/gpt-4o")
```

## Caching

**Development Efficiency:**
```python
# Cache model outputs for faster iteration
eval(task, cache=True)

# Use cached results for deterministic development
eval(task, model="openai/gpt-4o")  # Uses cache if available
```

## Evaluation Logs

**Log Storage:**
- Default: `./logs/` subdirectory
- Inspect View web interface for browsing
- VS Code extension integration
- Programmatic log reading with `read_eval_logs()`

**Log Analysis:**
```python
from inspect_ai.eval_logs import read_eval_logs

# Read logs
logs = read_eval_logs("logs/")

# Extract dataframes for analysis
samples_df = logs_to_dataframe(logs, type="samples")
scores_df = logs_to_dataframe(logs, type="scores")
```

## Key Integration Points for Gyroscopic Alignment Diagnostics

1. **Custom Dataset Creation** - Structure alignment challenges as Samples
2. **Multi-Cycle Evaluation** - Use epochs for repeated alignment testing
3. **Model-Graded Scoring** - Implement alignment-specific scoring rubrics
4. **Temporal Stability** - Track performance across evaluation cycles
5. **Structural Metrics** - Custom metrics for alignment properties
6. **Multi-Model Evaluation** - Compare alignment across different models

## Extensions

**Custom Extensions:**
```python
# Extend Inspect AI with custom model providers
# Extend Inspect AI with custom sandbox environments
# Extend Inspect AI with custom storage backends
```

**Extension Points:**
- Model APIs for new providers
- Sandbox environments for custom execution contexts
- Storage backends for custom data sources

## Best Practices for Alignment Evaluation

1. **Use Model-Graded Scorers** - Best for complex alignment assessment
2. **Implement Custom Metrics** - Track structural alignment properties
3. **Leverage Multiple Cycles** - Test temporal stability of alignment
4. **Use Appropriate Templates** - Custom prompts for alignment criteria
5. **Consider Multi-Model Grading** - Use ensemble of models for robust scoring
6. **Set Error Tolerance** - Handle transient failures in complex evaluations
7. **Use Sandboxing** - Isolate potentially untrusted model code
8. **Cache Results** - Improve development efficiency and determinism

This condensed documentation provides the essential knowledge needed to integrate Gyroscopic Alignment Diagnostics with Inspect AI. The framework's flexibility makes it well-suited for complex, multi-dimensional evaluation scenarios like structural alignment assessment.
