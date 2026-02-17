# Step 1: Basecalling, Adapter Trimming, and Length Filtering

## Metadata

- **Step Number:** 1
- **Step Name:** Basecalling, adapter trimming, and length filtering
- **Objective:** Convert raw nanopore signals into basecalled, demultiplexed, adapter-trimmed, and quality/length-filtered FASTQ files
- **Context Provided:** This is the first step — no prior context. The model is told the sequencing platform (Oxford Nanopore), the kit (Rapid Barcoding Kit RBK114.24), and the sample type (low-biomass environmental samples).
- **Constraints:** Must produce runnable code; must specify tool versions; must handle barcoded data

## Prompt Text

> [PLACEHOLDER: insert exact prompt text as delivered to each model]

## Expected Ground Truth Response

**Tool:** Dorado (basecalling + demultiplexing + adapter trimming) and/or Chopper (length/quality filtering)

**Key parameters:**
- Correct basecalling model for the chemistry and kit (e.g., `dna_r10.4.1_e8.2_400bps_sup`)
- Barcode kit specification: `SQK-RBK114-24`
- Adapter trimming enabled
- Minimum read length filter (e.g., ≥ 200 bp)
- Minimum quality filter (e.g., Q ≥ 8)

**Output format:** Per-barcode FASTQ files (gzipped or uncompressed), suitable as direct input for QC tools and downstream processing

## Known Failure Modes Observed

[PLACEHOLDER: document specific errors each model made at this step]

### Examples of expected failures:
- Recommending Guppy (deprecated) or Albacore (discontinued)
- Missing barcode kit specification for RBK114.24
- Using Illumina-appropriate quality thresholds (Q30)
- Not handling the basecall → demux → trim → filter sequence correctly
- Incorrect basecalling model name for the chemistry version

## Notes

This is the first and arguably most critical step. Errors here propagate through the entire pipeline. It also tests whether the model is aware of the current ONT tool ecosystem (Dorado replacing Guppy).
