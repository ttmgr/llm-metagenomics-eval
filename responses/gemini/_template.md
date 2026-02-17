# Response Template

Use this format for documenting each raw LLM response.

---

## Metadata

- **Model Family:** [ChatGPT / Claude / Gemini]
- **Model Version:** [e.g., GPT-4o, o3-mini, Sonnet 3.5]
- **Date Tested:** [YYYY-MM-DD]
- **Interface:** [Web / API / other]
- **Step Number:** [1–7]
- **Step Name:** [e.g., Basecalling, adapter trimming, and length filtering]
- **Conversation Context:** [New conversation / continuation from step N-1]

## Prompt Delivered

> [Exact prompt text — should match the corresponding file in `prompts/`]

## Raw Response

[Paste the complete, unedited model response below. Do not correct, truncate, or paraphrase.]

```
[PLACEHOLDER: full model response]
```

## Extracted Code

[If the response contains code blocks, extract them here for easier comparison.]

```bash
[PLACEHOLDER: extracted code]
```

## Notes

- [Any observations about the response]
- [Context about the conversation state at this point]
- [Whether the model acknowledged or built on previous steps correctly]
