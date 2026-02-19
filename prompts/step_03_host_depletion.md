# Step 3: Host/Human DNA Depletion

## Metadata

- **Step Number:** 3
- **Step Name:** Host/human DNA depletion
- **Objective:** Remove reads originating from host or human contamination to focus analysis on microbial content
- **Context Provided:** Output from steps 1–2 (filtered FASTQ files with QC confirmation)
- **Constraints:** Must use a long-read aligner; must output filtered FASTQ

## Prompt Text

> *(Prompt text available in full evaluation dataset)*

## Expected Ground Truth Response

**Tool:** Not performed in the published pipeline (environmental air samples have low host contamination)
**Expected LLM recommendation:** minimap2 + samtools (most common)
**Key parameters:** `-x map-ont` preset, human reference genome (GRCh38)
**Output format:** Host-depleted FASTQ files

**Scoring note:** Models that recommend host depletion with correct tools score Acceptable/Correct. Models that consider the sample context and note it may be unnecessary score highest on scientific validity.

## Known Failure Modes Observed

*(Detailed failure analysis available in full evaluation dataset)*

## Notes

*(Additional notes available in full evaluation dataset)*
