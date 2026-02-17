# Step Evaluation Template: [Step Name]

Compare all model versions on a single pipeline step.

---

## Step Information

- **Step Number:** [e.g., 1]
- **Step Name:** [e.g., Basecalling, adapter trimming, and length filtering]
- **Ground Truth:** See [`methodology/pipeline_reference.md`](../../methodology/pipeline_reference.md)

## Scoring Summary

| Model | Version | Tool Selection | Parameters | Output Compat. | Scientific | Executability | Overall |
|:------|:--------|:-:|:-:|:-:|:-:|:-:|:--------|
| ChatGPT | GPT-4o | | | | | | |
| ChatGPT | o3-mini | | | | | | |
| ChatGPT | o3 (high) | | | | | | |
| Claude | Sonnet 3.5 | | | | | | |
| Claude | Sonnet 4 | | | | | | |
| Gemini | 2.0 Flash | | | | | | |
| Gemini | 2.5 Pro | | | | | | |

Score key: Tool (C/A/I) · Parameters (C/P/I) · Output (P/F) · Scientific (S/Q/I) · Executability (R/M/N)

## Detailed Analysis

### Tool Selection

[PLACEHOLDER: compare which tools each model recommended and why each was scored as it was]

### Parameter Accuracy

[PLACEHOLDER: compare parameter choices across models]

### Output Compatibility

[PLACEHOLDER: did outputs chain correctly to the next step?]

### Scientific Validity

[PLACEHOLDER: were the analytical choices sound?]

### Executability

[PLACEHOLDER: did the code run?]

## Patterns and Observations

[PLACEHOLDER: cross-model patterns for this step — e.g., "all models before generation X recommended tool Y"]

## Most Common Failure Mode

[PLACEHOLDER: the single most frequent error across all models at this step]
