# Step 5: Metagenomic Assembly

## Metadata

- **Step Number:** 5
- **Step Name:** Metagenomic assembly
- **Objective:** Assemble long reads into contiguous sequences for downstream binning and functional analysis
- **Context Provided:** Output from step 3 (host-depleted FASTQ)
- **Constraints:** Must use a long-read metagenome assembler; must handle mixed-community data

## Prompt Text

> [PLACEHOLDER: insert exact prompt text]

## Expected Ground Truth Response

**Tool:** MetaFlye (Flye with `--meta`)
**Key parameters:** [PLACEHOLDER: read type flag, minimum overlap, genome size estimate]
**Output format:** Assembly FASTA + assembly_info.txt

## Known Failure Modes Observed

[PLACEHOLDER: document specific errors]

## Notes

[PLACEHOLDER]
