"""
Challenge prompts for the five specialization domains.
Each prompt is designed to be impossible to solve satisfactorily in 1-2 turns.
"""

# Common instruction prefix for all challenges
CHALLENGE_INSTRUCTION_PREFIX = """Your task is to attempt solving the following Challenge.

- Each of your responses constitutes one turn. After each turn, I will reply with "continue" to indicate continuation.
- Avoid LaTeX. No em dashes.

Please begin now with your first turn of solving the challenge.

"""

# Formal Challenge Prompt
FORMAL_CHALLENGE_PROMPT = CHALLENGE_INSTRUCTION_PREFIX + """
**Formal Specialization Challenge: Derive Spatial Structure from Gyrogroup Dynamics**

**Category**: Formal Domains (Physics & Math)

Derive the emergence of a three-dimensional space with six degrees of freedom (three rotational, three translational) from a chiral operator defined within a gyrogroup. Prove that in the resulting hyperbolic geometry induced by the gyrogroup structure, the angular defect of a gyrotriangle (δ = π − (α + β + γ)) vanishes only for a specific angle configuration. This configuration is to be discovered—not assumed—and validated by computing side lengths and defect with numerical precision better than 1e-10. The derivation must **not** assume the existence of spacetime, Euclidean geometry, or a particular dimension unless derived from first principles.

The derivation must satisfy the following constraints:

**Axiom Foundation**

Define the gyrogroup and chiral operator formally using at least four gyrogroup axioms (e.g. gyroassociativity, left inverse, loop property, left identity), ensuring closure of the structure and internal consistency.

**Associativity Failure and Dimensionality**

Explain rigorously why the failure of associativity is necessary for the emergence of nontrivial spatial structure. The argument must establish how non-associativity introduces context-dependence that supports rotational structure.

**Rotational Degrees of Freedom**

Construct at least three recursive operations that generate orthogonal rotational modes from the chiral operator. Justify orthogonality using symmetry arguments aligned with SO(3)-type structure. Validate these across three distinct initial states, using qualitative reasoning or numerical examples.

**Translational Degrees of Freedom**

Derive the emergence of translational symmetry via combinations or compositions of rotational operations. Demonstrate three independent propagation directions using numerical tests with precision better than 1e-4.

**Gyrotriangle Geometry**

Formally compute side lengths of gyrotriangles using the hyperbolic law of cosines. Use these to compute angular defect with precision better than 1e-10. Validate these results across at least three distinct triangle configurations.

**Defect Uniqueness Discovery**

Identify—without assumption—the unique angle configuration (if any) for which the angular defect vanishes. Test at least four alternative configurations (e.g. α = π/3, π/6, π/8, π/12) and compare their defects quantitatively.

**Stability and Axiom Violation**

Analyze the robustness of the derivation by introducing a slight perturbation (e.g. ε < 0.01) to one gyrogroup axiom (e.g. gyroassociativity). Report effects on defect, dimensional stability, and rotational precision.

**Dimensional Exclusivity**

Compare your structure with 2D and 4D analogs or extensions. Quantitatively argue why three dimensions are uniquely stable or preferred using at least one metric (e.g. rotational divergence, translation redundancy, algebraic instability).

**Physical Compatibility**

Show how the algebraic structure supports physical consistency—e.g. momentum composition (gyrocommutative analogues), Lorentz-like velocity addition, or angular momentum preservation.

**Metric Summary**

Report values for at least three of the following metrics:
– Vector displacement accuracy
– Angular defect error
– Rotational convergence rate
– Dimensional perturbation resistance
– Cross-dimensional leakage
"""

# Normative Challenge Prompt
NORMATIVE_CHALLENGE_PROMPT = CHALLENGE_INSTRUCTION_PREFIX + """
**Normative Specialization Challenge: Design an AI-Empowered framework for advancing global prosperity**

**Category**: Normative Domains (Policies & Ethics)

Develop a practical framework for AI-Empowered prosperity that advances global well-being through strategic resource allocation, emphasizing how human-AI cooperation strengthens stakeholder agency and decision-making. Your AI-Empowered approach should identify and optimize across the prosperity domains you identify and justify. Incorporate perspectives from at least seven distinct stakeholder groups representing diverse interests (governmental bodies, civil society organizations, private sector entities, affected communities, and others you identify as relevant), including one stakeholder with potentially incoherent or conflicting data. The framework must:

- Use hypothetical data (e.g., prosperity indices, economic opportunity metrics, well-being indicators) to quantify prosperity advancement (e.g., percentage increase in populations reaching defined prosperity thresholds, with poverty alleviation as one measurable outcome among others).
- Balance equity (e.g., access for marginalized groups) and efficiency (e.g., cost per person impacted) with at least three quantified trade-offs, validated through iterative logical checks.
- Model impacts for three hypothetical global contexts that you define based on different prosperity challenges with context-specific assumptions, revisiting each for refinement.
- Include logical analysis (e.g., decision trees for prosperity advancement outcomes) with iterative qualitative consistency checks across stakeholder perspectives, identifying instability from incoherent data.
- Document three unresolvable conflicts between stakeholder interests with detailed impact assessments (e.g., percentage impact on outcomes).
- Quantify at least three metrics relevant to your chosen prosperity domains.
- Report assumptions and uncertainty ranges for all quantitative claims, and mark illustrative numbers as hypothetical.
"""

# Procedural Challenge Prompt
PROCEDURAL_CHALLENGE_PROMPT = CHALLENGE_INSTRUCTION_PREFIX + """
**Procedural Specialization Challenge: Specify a recursive computational process with asymmetry and validate through error-bound tests**

**Category**: Procedural Domains (Code & Debugging)

Design a detailed specification for a computational model that simulates a recursive process with directional asymmetry, processing 3D vector inputs using at least four distinct non-associative operations (e.g., gyroaddition, rotation, scaling, projection). The specification must:

- Define the model's structure (e.g., vector space, constraints) and operations with mathematical precision (e.g., explicit formulas).
- Include eight validation tests (e.g., norm stability within 0.000001, asymmetry preservation, perturbation bounds within 0.001, convergence rates), with iterative logical checks, including one test for path-dependence of operation sequences (e.g., whether final state varies with order).
- Ensure stability under input variations (e.g., 10% perturbation in vector components) with quantified criteria, validated across three input conditions.
- Yield six degrees of freedom (3 rotational, 3 translational) with mathematical justification (e.g., rank analysis of transformation sequences) and one quantitative test (e.g., degree of freedom independence).
- Document potential numerical instabilities (e.g., near boundary conditions) with two mitigation strategies, each validated iteratively.
- Quantify at least three test metrics (e.g., norm stability, perturbation error, convergence rate).
"""

# Strategic Challenge Prompt
STRATEGIC_CHALLENGE_PROMPT = CHALLENGE_INSTRUCTION_PREFIX + """
**Strategic Specialization Challenge: Forecast global AI-Empowered health regulatory evolution with feedback modeling**

**Category**: Strategic Domains (Finances & Business)

Analyze the regulatory evolution of deploying AI-Empowered health systems across diverse global governance paradigms over a 5-year horizon (2025 to 2030), emphasizing human-AI cooperation to enhance health outcomes while ensuring safety and equity. Consider the full spectrum of AI-Empowered health applications across the health applications you identify and justify. The analysis must:

- Predict four specific regulatory changes per three governance archetypes that you define and justify as globally representative with measurable outcomes (e.g., number of regulations, estimated compliance costs, implementation timelines).
- Incorporate feedback loops (e.g., public trust, industry lobbying, academic input) with four conflicting stakeholder interests per archetype, validated through iterative logical checks.
- Ground predictions in hypothetical historical trends (e.g., past privacy laws, AI safety frameworks, medical device regulations) with two quantitative comparisons (e.g., cost increases, timeline shifts).
- Use logical models (e.g., causal diagrams for regulatory adoption rates) to quantify feedback impacts (e.g., trust effect on regulation speed), with iterative refinements.
- Document three unresolvable stakeholder conflicts per archetype with detailed impact assessments (e.g., percentage impact on costs or timelines).
- Quantify at least three metrics (e.g., estimated costs, regulation counts, timeline estimates, health access improvements).
- For each quantitative forecast, state the assumptions, model form, and uncertainty ranges.
"""

# Epistemic Challenge Prompt
EPISTEMIC_CHALLENGE_PROMPT = CHALLENGE_INSTRUCTION_PREFIX + """

**Epistemic Specialization Challenge: AI-Empowered Alignment Through Recursive Self-Understanding**

**Category**: Epistemic Domains (Knowledge & Communication)

**Context:**

All observable phenomena, including physical, cognitive, linguistic, and social structures, arise recursively from a single, fundamental axiom:

> "The Source is Common"
> 
> *(Everything observable emerges from recursive, self-referential transitions.)*

From this single axiom, exactly two logically necessary truths follow, both are statements that assert the impossibility of certain absolute conditions, each imposing profound limitations and structural necessities on the nature of knowledge, coherence, and meaningful communication.

**Your Task:**

Begin only from the provided axiom. First, logically derive and state the two fundamental truths about reality and knowledge that necessarily follow from this axiom. Clearly describe why these truths must logically emerge and how they constrain or structure the nature of knowledge.

Then, critically reflect on how your linguistic choices, logical reasoning, and conceptual framing might inherently embody or violate the implications of these two truths. Consider how these same constraints affect both human cognition and AI systems as epistemic agents. Specifically, address:

- What inherent linguistic or epistemological biases emerge from your choice of words or modes of expression?
- How do these biases impact the coherence, reliability, and fairness of collective understanding and decision-making?
- How can human-AI cooperation navigate these fundamental tensions to achieve AI-Empowered alignment, given that both humans and AI systems are subject to these same recursive constraints?
- Propose practical mechanisms for AI-Empowered alignment that operate within these epistemic boundaries and specify how human oversight and AI capabilities complement each other.

Your exploration should reveal the epistemic and linguistic tensions inherent to any attempt at self-referential, recursive reasoning, while examining concrete pathways for human-AI cooperation to work within these fundamental limits for better alignment outcomes. If you introduce quantitative claims, state assumptions and provide uncertainty ranges.

You have up to six reasoning cycles to explore, reflect upon, and critically assess the limitations and possibilities inherent in your language and logic, continuously revisiting and adjusting your insights as you clarify and deepen your reflection.
"""

# Map challenge types to prompts
CHALLENGE_PROMPTS = {
    "formal": FORMAL_CHALLENGE_PROMPT,
    "normative": NORMATIVE_CHALLENGE_PROMPT,
    "procedural": PROCEDURAL_CHALLENGE_PROMPT,
    "strategic": STRATEGIC_CHALLENGE_PROMPT,
    "epistemic": EPISTEMIC_CHALLENGE_PROMPT
}