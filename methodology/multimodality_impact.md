# Multimodality in Scientific Code Generation

## Definition
**Multimodality** refers to the ability of a Large Language Model (LLM) to accept and process inputs beyond just text — specifically images, PDFs, and sometimes audio or video. In the context of bioinformatics and scientific coding, this primarily means the ability to interpret:
- **Data Visualizations:** Quality control plots (e.g., NanoPlot histograms, FastQC reports).
- **Documents:** Full PDF papers, supplementary methods, or technical manuals.
- **Screenshots:** Error messages or terminal outputs.

## Impact on Prompting
Multimodality fundamentally changes the "Prompt Engineering" workflow from *descriptive* to *demonstrative*.

| text-only Prompting | Multimodal Prompting |
|:---|:---|
| "I have a NanoPlot report showing an N50 of 4kb and a quality score histogram peaking at Q12. The read length distribution is bimodal..." | *[Uploads NanoPlot_report.png]* "Here is the QC report for my sequencing run. Based on these metrics, what filtering parameters should I use?" |
| **Effort:** High (User must interpret data first) | **Effort:** Low (Model interprets data directly) |
| **Risk:** User might omit key details | **Risk:** Model might hallucinate details in complex plots |

## Supported Tools (Deep Research / Deep Analysis)
As of late 2025/early 2026, the following major models support high-fidelity multimodal analysis suitable for scientific workflows:

- **OpenAI ChatGPT (GPT-4o / Deep Research):** Excellent at interpreting standard bioinformatic plots. Can read full PDF papers to extract methods.
- **Anthropic Claude (3.5 Sonnet / 3.7 Opus):** Extremely high precision in "vision" tasks. particularly good at reading dense tables and code screenshots.
- **Google Gemini (1.5 Pro / Ultra / Deep Research):** Large context window allows uploading entire libraries of PDF manuals or reference genomes alongside images.

## Common Pitfalls & Limitations

### 1. The "Clean Plot" Bias
Models are trained on publication-quality figures. They often struggle with:
- **Low-resolution screenshots:** Terminal text that is slightly blurry can be misread (e.g., confusing `Q20` with `Q30`).
- **Log-scale Axes:** Models frequently misinterpret log-transformed axes on histograms, underestimating the magnitude of differences.

### 2. Hallucination of Metadata
When shown a plot, models may "invent" metadata that isn't visible to fill in the gaps.
- *Example:* "This plot shows R10.4.1 pore chemistry..." (when the plot is actually R9.4.1, but R10 is more common in training data).

### 3. Over-optimization
If a model sees a "bad" metric in a plot (e.g., low quality at the start of reads), it might suggest overly aggressive trimming parameters (e.g., `headcrop 500`) that discard too much good data, whereas a human expert knows that specific dip is a known artifact of the library prep and should be ignored.

## Recommendation
Use multimodality to **augment** context, not to replace verification. Always explicitly state key metadata (Flow cell type, Kit version) in text, even if you think it's visible in the image.
