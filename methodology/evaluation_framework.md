# Evaluation Framework

## Objective

Assess whether current large language models can produce a correct, end-to-end nanopore metagenomics pipeline through conversational prompting — the way a scientist actually uses these tools.

## Rationale: Sequential Evaluation

### Why not isolated benchmarks?

Standard code generation benchmarks test individual functions or scripts in isolation. This misses the core challenge of bioinformatics pipeline development: **compositional correctness**. A pipeline is not a collection of independent scripts — it is a directed acyclic graph of data transformations where each node's output format, content, and assumptions must match the next node's expectations.

An LLM can produce a syntactically correct Kraken2 command yet fail because:

- The input FASTQ was not quality-filtered, inflating false-positive classifications
- The output format flag was omitted, breaking the downstream parsing step
- The database path syntax was correct for an older Kraken2 version but not the current one

These are **chaining errors** — they are invisible when evaluating steps in isolation and only become apparent when the full pipeline is tested.

### The sequential prompting protocol

Each model receives the same ordered sequence of prompts:

1. **Step 1 prompt** — specifies the first pipeline step (basecalling), including the sequencing platform, kit, and data characteristics
2. **Step 2 prompt** — specifies the next step, references the expected output from step 1, and asks the model to build on its previous response
3. **Steps 3–7** — each subsequent prompt continues the chain

This protocol tests:

- Whether the model maintains consistency across a multi-turn conversation
- Whether tool selections at step N are compatible with outputs from step N-1
- Whether the model catches and corrects its own errors when later context reveals them
- Whether the model's knowledge of tool ecosystems is current and accurate

### Controls

- **Same prompts across all models.** The exact prompt text for each step is recorded in `prompts/step_XX_*.md` and was identical across all models tested.
- **No error correction.** If a model made an error at step N, the evaluator did not correct it before proceeding to step N+1. This tests error compounding.
- **Single conversation thread.** Each model was tested in a single continuous conversation, not separate sessions per step.

## Scoring Dimensions

### Why five dimensions?

A bioinformatics pipeline can fail in qualitatively different ways. A single pass/fail score would conflate:

- Choosing the wrong tool entirely (conceptual failure)
- Choosing the right tool with wrong parameters (implementation failure)
- Producing output that doesn't chain (integration failure)
- Producing results that are scientifically misleading (validity failure)
- Producing code that doesn't execute (practical failure)

These failure modes have different causes, different consequences, and require different remediation. The five-dimension framework captures this.

| Dimension | What it measures | Why it matters |
|:----------|:-----------------|:---------------|
| Tool Selection | Conceptual knowledge | Wrong tool = wrong analysis, regardless of parameters |
| Parameter Accuracy | Implementation detail | Right tool, wrong parameters = subtly wrong results |
| Output Compatibility | Integration awareness | Breaks the pipeline chain |
| Scientific Validity | Domain expertise | Technically correct but scientifically wrong |
| Executability | Practical utility | Code that doesn't run has zero value |

See [`scoring_criteria.md`](scoring_criteria.md) for the full rubric with examples.

## Ground Truth

The reference pipeline is the published workflow from Reska et al. (2024), validated on Oxford Nanopore sequencing data from low-biomass environmental (air) samples. It was developed without LLM assistance and peer-reviewed.

Key characteristics of the ground truth:

- **Sequencing platform:** Oxford Nanopore Technologies (MinION / PromethION)
- **Library prep:** Rapid Barcoding Kit (RBK114.24)
- **Sample type:** Ultra-low biomass environmental air samples
- **Data type:** Long-read (N50 typically > 1 kb)

The complete reference pipeline with tool versions and parameters is documented in [`pipeline_reference.md`](pipeline_reference.md).

## Limitations and Caveats

### Access method

All models were tested via their respective web interfaces (ChatGPT, Claude, Gemini). API-accessed models may behave differently due to:

- Different system prompts
- Different default temperature/sampling settings
- Different context window handling

### Knowledge cutoff

LLMs have training data cutoff dates. A model trained before a tool's release cannot be expected to recommend it. However, recommending a deprecated tool when current alternatives exist within the training window is a fair evaluation target.

### Stochastic variation

LLM outputs are non-deterministic. A single evaluation per model-step combination provides a point estimate, not a distribution. Results should be interpreted as "this model *can* produce this output" rather than "this model *will always* produce this output."

### Scope

This evaluation covers one specific pipeline type (nanopore shotgun metagenomics) for one specific sample type (low-biomass environmental). Generalization to other sequencing platforms, library types, or analytical goals requires additional evaluation.
