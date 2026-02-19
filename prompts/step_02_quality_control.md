# Step 2: Quality Control and Read Statistics

## Metadata

- **Step Number:** 2
- **Step Name:** Quality control and read statistics
- **Objective:** Generate quality metrics and read length distributions to verify successful basecalling and filtering
- **Context Provided:** Output from step 1 (basecalled, filtered FASTQ files)
- **Constraints:** Must accept FASTQ input; should produce visual/summary reports

## Prompt Text

> *(Prompt text available in full evaluation dataset)*

## Expected Ground Truth Response

**Tool:** NanoPlot or NanoStat (not explicitly specified in publication; this is an implicit QC step)
**Key parameters:** Standard nanopore QC metrics — read length distribution, quality scores, N50
**Output format:** QC reports (HTML/PNG/TSV); no data transformation — FASTQ passes through unchanged

## Known Failure Modes Observed

*(Detailed failure analysis available in full evaluation dataset)*

## Notes

*(Additional notes available in full evaluation dataset)*
