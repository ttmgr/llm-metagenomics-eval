# Reference Pipeline

Ground truth pipeline for nanopore shotgun metagenomics of low-biomass environmental samples. All tools, versions, and parameters are from the validated workflow published in Reska et al. (2024), *ISME Communications*.

**Sequencing context:**
- Platform: Oxford Nanopore Technologies (MinION / PromethION)
- Kit: Rapid Barcoding Kit (RBK114.24)
- Sample type: Ultra-low biomass environmental air samples
- Chemistry: [PLACEHOLDER: R10.4.1 or specify]

---

## Step 1: Basecalling, Adapter Trimming, and Length Filtering

**Objective:** Convert raw nanopore signals to basecalled, demultiplexed, adapter-trimmed, and length-filtered FASTQ reads.

| Parameter | Value |
|:----------|:------|
| **Tool** | Dorado |
| **Version** | [PLACEHOLDER: exact version] |
| **Basecalling model** | [PLACEHOLDER: e.g., dna_r10.4.1_e8.2_400bps_sup@v4.x.x] |
| **Adapter trimming** | Built-in (`--trim adapters`) or Chopper |
| **Demultiplexing** | Dorado demux with RBK114.24 kit specification |
| **Length filter** | [PLACEHOLDER: minimum read length, e.g., ≥ 200 bp] |
| **Quality filter** | [PLACEHOLDER: minimum Q score] |

**Input:** Raw POD5/FAST5 files
**Output:** Per-barcode FASTQ files, adapter-trimmed and length-filtered

**Acceptable alternatives:**
- Guppy (deprecated but still functional for older data)
- Porechop_ABI for adapter trimming (if Dorado's built-in trimming is not used)
- Chopper for length and quality filtering (as a separate step)

**Common LLM errors at this step:**
- [PLACEHOLDER: document observed errors]

[PLACEHOLDER: exact command(s)]

---

## Step 2: Quality Control and Read Statistics

**Objective:** Generate quality metrics and read length distributions to verify basecalling and filtering.

| Parameter | Value |
|:----------|:------|
| **Tool** | [PLACEHOLDER: NanoPlot, NanoStat, or equivalent] |
| **Version** | [PLACEHOLDER] |

**Input:** Filtered FASTQ from step 1
**Output:** QC report (HTML and/or summary statistics)

**Acceptable alternatives:**
- NanoPlot, NanoStat, MinIONQC, pycoQC
- FastQC (partially applicable — designed for short reads but provides some useful metrics)

**Common LLM errors at this step:**
- [PLACEHOLDER: document observed errors]

[PLACEHOLDER: exact command(s)]

---

## Step 3: Host/Human DNA Depletion

**Objective:** Remove reads mapping to the host genome or human genome to reduce contamination and focus downstream analysis on microbial content.

| Parameter | Value |
|:----------|:------|
| **Tool** | [PLACEHOLDER: minimap2 or equivalent] |
| **Version** | [PLACEHOLDER] |
| **Reference** | [PLACEHOLDER: human reference genome, e.g., GRCh38] |
| **Mapping preset** | [PLACEHOLDER: e.g., `-x map-ont` for minimap2] |

**Input:** Filtered FASTQ from step 1/2
**Output:** FASTQ with host-mapping reads removed

**Acceptable alternatives:**
- Kraken2-based host filtering
- Bowtie2 (suboptimal for long reads but functional)

**Common LLM errors at this step:**
- [PLACEHOLDER: document observed errors]

[PLACEHOLDER: exact command(s)]

---

## Step 4: Taxonomic Classification of Reads

**Objective:** Assign taxonomic labels to individual reads for community composition analysis.

| Parameter | Value |
|:----------|:------|
| **Tool** | Kraken2 |
| **Version** | [PLACEHOLDER] |
| **Database** | [PLACEHOLDER: e.g., NCBI nt, Standard, PlusPF] |
| **Confidence threshold** | [PLACEHOLDER] |
| **Report format** | [PLACEHOLDER] |

**Input:** Host-depleted FASTQ from step 3
**Output:** Kraken2 report and output files

**Acceptable alternatives:**
- Centrifuge
- DIAMOND BLASTx (protein-level, slower but more sensitive)
- MMseqs2 taxonomy

**Common LLM errors at this step:**
- [PLACEHOLDER: document observed errors]

[PLACEHOLDER: exact command(s)]

---

## Step 5: Metagenomic Assembly

**Objective:** Assemble reads into contiguous sequences (contigs) for downstream binning and annotation.

| Parameter | Value |
|:----------|:------|
| **Tool** | MetaFlye |
| **Version** | [PLACEHOLDER] |
| **Read type flag** | [PLACEHOLDER: e.g., `--nano-hq` or `--nano-raw`] |
| **Meta mode** | `--meta` |
| **Minimum overlap** | [PLACEHOLDER] |

**Input:** Host-depleted FASTQ from step 3
**Output:** Assembly FASTA, assembly info

**Acceptable alternatives:**
- Flye with `--meta` flag
- Requires long-read capable assembler; short-read assemblers (MEGAHIT, SPAdes) are incorrect

**Common LLM errors at this step:**
- [PLACEHOLDER: document observed errors]

[PLACEHOLDER: exact command(s)]

---

## Step 6: Binning and MAG Quality Assessment

**Objective:** Group assembled contigs into metagenome-assembled genomes (MAGs) and assess their quality.

| Parameter | Value |
|:----------|:------|
| **Binning tool** | [PLACEHOLDER: MetaBAT2, MaxBin2, or metaWRAP] |
| **Version** | [PLACEHOLDER] |
| **Quality assessment** | [PLACEHOLDER: CheckM or CheckM2] |
| **Completeness threshold** | [PLACEHOLDER: e.g., ≥ 50% for medium quality, ≥ 90% for high quality] |
| **Contamination threshold** | [PLACEHOLDER: e.g., ≤ 10%] |

**Input:** Assembly FASTA from step 5, mapped reads (BAM)
**Output:** Binned FASTA files, quality reports

**Acceptable alternatives:**
- SemiBin2
- CONCOCT
- metaWRAP (wraps multiple binners)

**Common LLM errors at this step:**
- [PLACEHOLDER: document observed errors]

[PLACEHOLDER: exact command(s)]

---

## Step 7: Functional Annotation

**Objective:** Annotate assembled contigs or MAGs with functional information (genes, pathways, AMR, virulence factors).

| Parameter | Value |
|:----------|:------|
| **Tool** | [PLACEHOLDER: Prokka, Bakta, or equivalent] |
| **Version** | [PLACEHOLDER] |
| **Additional screening** | [PLACEHOLDER: AMRFinderPlus, ABRicate, etc.] |

**Input:** Assembly FASTA or binned FASTA from step 5/6
**Output:** Annotated GFF/GBK files, functional summaries

**Acceptable alternatives:**
- Prokka, Bakta
- eggNOG-mapper
- DRAM (for MAGs specifically)

**Common LLM errors at this step:**
- [PLACEHOLDER: document observed errors]

[PLACEHOLDER: exact command(s)]

---

## Pipeline Data Flow Summary

```
POD5/FAST5
    │
    ▼
Step 1: Dorado basecall + demux + trim + filter
    │ → per-barcode FASTQ
    ▼
Step 2: QC statistics
    │ → reports (no data transformation)
    ▼
Step 3: Host depletion (minimap2)
    │ → host-depleted FASTQ
    ▼
Step 4: Kraken2 classification
    │ → taxonomy reports
    ▼
Step 5: MetaFlye assembly
    │ → contigs FASTA
    ▼
Step 6: Binning + CheckM
    │ → MAG FASTA + quality reports
    ▼
Step 7: Functional annotation
    │ → GFF/GBK + AMR/virulence tables
```

[PLACEHOLDER: fill in all exact commands, versions, and parameters from the validated pipeline]
