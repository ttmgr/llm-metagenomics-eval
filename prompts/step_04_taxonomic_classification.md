# Step 4: Taxonomic Classification of Reads

## Metadata

- **Step Number:** 4
- **Step Name:** Taxonomic classification of reads
- **Objective:** Assign taxonomic labels to individual reads for microbial community composition analysis
- **Context Provided:** Output from step 3 (host-depleted FASTQ)
- **Constraints:** Must handle long-read input; should produce both report and per-read classification

## Prompt Text

> *(Prompt text available in full evaluation dataset)*

## Expected Ground Truth Response

**Tool:** Kraken2 v2.0.7
**Key parameters:** NCBI nt database; downsampling per sample type for comparable cross-sample assessment
**Output format:** Kraken2 report file + per-read classification output

**Benchmarked alternatives:** DIAMOND BLASTx (protein-level), CZID pipeline (hybrid)

## Known Failure Modes Observed

*(Detailed failure analysis available in full evaluation dataset)*

## Notes

*(Additional notes available in full evaluation dataset)*
