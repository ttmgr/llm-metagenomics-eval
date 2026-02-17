# Prompt Template

Use this format for documenting each standardized prompt used in the evaluation.

---

## Metadata

- **Step Number:** [e.g., 1]
- **Step Name:** [e.g., Basecalling, adapter trimming, and length filtering]
- **Objective:** [What this step should accomplish]
- **Context Provided:** [What information about previous steps was included in the prompt]
- **Constraints:** [Any specific requirements or limitations stated in the prompt]

## Prompt Text

> [Exact prompt text as delivered to the model, verbatim]

## Expected Ground Truth Response

**Tool:** [Expected tool]
**Key parameters:** [Critical parameters the model should include]
**Output format:** [Expected output that chains to the next step]

See [`methodology/pipeline_reference.md`](../methodology/pipeline_reference.md) for the full reference.

## Notes

[Any observations about prompt design, ambiguity, or edge cases]
