# Step 6: Binning and MAG Quality Assessment

## Metadata

- **Step Number:** 6
- **Step Name:** Binning and MAG quality assessment
- **Objective:** Group assembled contigs into metagenome-assembled genomes (MAGs) and assess their completeness and contamination
- **Context Provided:** Output from step 5 (assembly FASTA) and read alignments
- **Constraints:** Requires both assembly and read mapping; must produce quality metrics per bin

## Prompt Text

> *(Prompt text available in full evaluation dataset)*

## Expected Ground Truth Response

**Binning tool:** metaWRAP v1.3 (integrates MetaBAT2, MaxBin2, CONCOCT)
**Quality assessment:** CheckM v1.2.2
**Key parameters:** Minimum completeness ≥ 30%, maximum contamination ≤ 10% (permissive thresholds for low-biomass samples)
**Output format:** Refined bin FASTA files + CheckM quality reports

## Known Failure Modes Observed

*(Detailed failure analysis available in full evaluation dataset)*

## Notes

*(Additional notes available in full evaluation dataset)*
