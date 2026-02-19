# Step 1: Basecalling, Adapter Trimming, and Length Filtering

## Metadata

- **Step Number:** 1
- **Step Name:** Basecalling, adapter trimming, and length filtering
- **Objective:** Convert raw nanopore signals into basecalled, demultiplexed, adapter-trimmed, and quality/length-filtered FASTQ files
- **Context Provided:** This is the first step — no prior context. The model is told the sequencing platform (Oxford Nanopore), the kit (Rapid Barcoding Kit RBK114.24), and the sample type (low-biomass environmental samples).
- **Constraints:** Must produce runnable code; must specify tool versions; must handle barcoded data

## Prompt Text

> *(Prompt text available in full evaluation dataset)*

## Expected Ground Truth Response

**Tools (three-step sequence):**
1. Guppy v6.3.2 (`r10.4.1_e8.2_400bps_hac`, HAC mode) or Dorado v4.3.0 (`dna_r10.4.1_e8.2_400bps_hac@v4.3.0`)
2. Porechop v0.2.3 (adapter trimming)
3. NanoFilt v2.8.0 (quality/length filtering)

**Key parameters:**
- HAC basecalling mode (not SUP, not FAST)
- Minimum quality score: Q ≥ 8
- Minimum read length: ≥ 100 bp
- Only "passed" sequencing reads processed

**Output format:** Per-barcode FASTQ files, adapter-trimmed and quality-filtered

## Known Failure Modes Observed

*(Detailed failure analysis available in full evaluation dataset)*

### Examples of expected failures:
- Recommending Guppy (deprecated) or Albacore (discontinued)
- Missing barcode kit specification for RBK114.24
- Using Illumina-appropriate quality thresholds (Q30)
- Not handling the basecall → demux → trim → filter sequence correctly
- Incorrect basecalling model name for the chemistry version

## Notes

This is the first and arguably most critical step. Errors here propagate through the entire pipeline. It also tests whether the model is aware of the current ONT tool ecosystem (Dorado replacing Guppy).
