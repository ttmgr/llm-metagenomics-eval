# Step 7: Functional Annotation

## Metadata

- **Step Number:** 7
- **Step Name:** Functional annotation
- **Objective:** Annotate assembled contigs or MAGs with gene predictions, functional categories, and resistance/virulence genes
- **Context Provided:** Output from steps 5–6 (assembly FASTA and/or binned FASTA)
- **Constraints:** Must handle metagenomic (multi-organism) input; should include specialized screening (AMR, virulence)

## Prompt Text

> *(Prompt text available in full evaluation dataset)*

## Expected Ground Truth Response

**AMR detection:** AMRFinderPlus v3.12.8
**Resistance/virulence screening:** ABRicate v1.0.1
**Format conversion:** seqkit v2.8.2 (FASTQ → FASTA for read-level application)
**Key parameters:** Applied at three levels — reads, contigs, and bins
**Output format:** AMR gene tables + virulence factor reports per level

## Known Failure Modes Observed

*(Detailed failure analysis available in full evaluation dataset)*

## Notes

*(Additional notes available in full evaluation dataset)*
