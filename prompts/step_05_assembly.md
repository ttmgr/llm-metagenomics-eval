# Step 5: Metagenomic Assembly

## Metadata

- **Step Number:** 5
- **Step Name:** Metagenomic assembly
- **Objective:** Assemble long reads into contiguous sequences for downstream binning and functional analysis
- **Context Provided:** Output from step 3 (host-depleted FASTQ)
- **Constraints:** Must use a long-read metagenome assembler; must handle mixed-community data

## Prompt Text

> *(Prompt text available in full evaluation dataset)*

## Expected Ground Truth Response

**Assembler:** MetaFlye v2.9.1 (Flye with `--meta`)
**Polishing:** minimap2 v2.17 + Racon v1.5 (3 rounds)
**Key parameters:** `--nano-hq` read type flag, `--meta` for metagenomic data
**Output format:** Polished assembly FASTA + assembly_info.txt

## Known Failure Modes Observed

*(Detailed failure analysis available in full evaluation dataset)*

## Notes

*(Additional notes available in full evaluation dataset)*
