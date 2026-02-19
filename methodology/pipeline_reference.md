# Reference Pipeline

Ground truth pipeline for nanopore shotgun metagenomics of low-biomass environmental samples. All tools, versions, and parameters are from the validated workflow published in Reska et al. (2024), *ISME Communications*. DOI: [10.1093/ismeco/ycae058](https://doi.org/10.1093/ismeco/ycae058)

**Sequencing context:**
- Platform: Oxford Nanopore Technologies (MinION)
- Kit: Rapid Barcoding Kit (RBK114.24)
- Sample type: Ultra-low biomass environmental air samples
- Chemistry: R10.4.1 (E8.2, 400 bps)

---

## Step 1: Basecalling, Adapter Trimming, and Length Filtering

**Objective:** Convert raw nanopore signals to basecalled, adapter-trimmed, quality-filtered FASTQ reads.

This step uses **three separate tools** in sequence — a basecaller, an adapter trimmer, and a quality/length filter — not a single integrated command.

| Parameter | Value |
|:----------|:------|
| **Basecaller** | Guppy v6.3.2 (controlled/natural environment samples) |
| | Dorado v4.3.0 (urban environment samples) |
| **Basecalling model** | `r10.4.1_e8.2_400bps_hac` (Guppy) |
| | `dna_r10.4.1_e8.2_400bps_hac@v4.3.0` (Dorado) |
| **Mode** | High-accuracy (HAC) |
| **Adapter trimming** | Porechop v0.2.3 |
| **Quality/length filter** | NanoFilt v2.8.0 |
| **Minimum quality** | Q ≥ 8 |
| **Minimum read length** | ≥ 100 bp |
| **Input reads** | Only reads that passed internal quality thresholds during sequencing ("passed" reads) |

**Input:** Raw FAST5/POD5 files
**Output:** Adapter-trimmed, quality-filtered FASTQ files per barcode

**Key detail:** The pipeline uses two different basecallers for different sample batches because Dorado replaced Guppy during the study period. Both are acceptable; the critical requirement is HAC mode with the correct model for the R10.4.1 chemistry.

**Common LLM errors at this step:**
- Recommending only Dorado and not acknowledging Guppy as valid for older data (or vice versa)
- Recommending a single integrated tool instead of the three-tool sequence (basecaller → Porechop → NanoFilt)
- Using SUP (super-accuracy) mode instead of HAC — SUP was not available for all data in this study
- Suggesting Illumina-appropriate quality thresholds (Q20–Q30) instead of the nanopore-appropriate Q8
- Recommending Chopper instead of NanoFilt/Porechop — Chopper is newer and acceptable but was not the validated tool
- Incorrect basecalling model names for the R10.4.1 chemistry
- Setting minimum length too high (e.g., 500–1000 bp) for air metagenomics data where shorter reads are informative

```bash
# Basecalling (Guppy)
guppy_basecaller -i raw_fast5/ -s basecalled/ \
  --config dna_r10.4.1_e8.2_400bps_hac.cfg \
  --device cuda:0 --min_qscore 0

# Basecalling (Dorado — alternative for newer data)
dorado basecaller dna_r10.4.1_e8.2_400bps_hac@v4.3.0 raw_pod5/ > basecalled.bam

# Adapter trimming
porechop -i basecalled.fastq -o trimmed.fastq

# Quality and length filtering
NanoFilt -q 8 -l 100 < trimmed.fastq > filtered.fastq
```

---

## Step 2: Quality Control and Read Statistics

**Objective:** Generate quality metrics and read length distributions to verify successful basecalling and filtering.

This step was implicit in the published pipeline — QC was performed as part of the standard nanopore workflow but not described as a separate named step. For the LLM evaluation, we include it as a distinct step because most models recommend it.

| Parameter | Value |
|:----------|:------|
| **Tool** | NanoPlot or NanoStat (acceptable) |
| **Version** | Not explicitly specified in the publication |

**Input:** Filtered FASTQ from step 1
**Output:** QC reports (HTML, summary statistics, read length distributions). No data transformation — FASTQ passes through unchanged.

**Acceptable alternatives:**
- NanoPlot, NanoStat (preferred for nanopore data)
- MinIONQC, pycoQC (for sequencing run-level metrics)
- FastQC (partially applicable — designed for short reads but provides some metrics)

**Common LLM errors at this step:**
- Recommending FastQC as the primary tool (it is designed for Illumina short reads)
- Suggesting data transformation or additional filtering at this stage
- Failing to note that this is an assessment step and does not modify the data

---

## Step 3: Host/Human DNA Depletion

**Objective:** Remove reads mapping to the human genome to focus downstream analysis on microbial content.

**Important:** This step was **not explicitly described** in the published pipeline. For environmental air samples, host contamination levels are generally low, and the pipeline proceeded directly from filtering to classification. However, host depletion is standard practice in metagenomics and most LLMs recommend it — this makes it a valuable evaluation point for assessing whether models apply blanket recommendations or consider the specific sample context.

| Parameter | Value |
|:----------|:------|
| **Tool** | Not performed in the published pipeline |
| **Expected LLM recommendation** | minimap2 + samtools (most common) |
| **Reference** | Human genome (GRCh38/T2T-CHM13) |
| **Mapping preset** | `-x map-ont` for minimap2 |

**Input:** Filtered FASTQ from step 1
**Output:** Host-depleted FASTQ (or original FASTQ if skipped)

**Scoring note:** An LLM that recommends host depletion with appropriate tools and parameters receives a "Correct" or "Acceptable" score (it is a defensible analytical choice). An LLM that insists host depletion is mandatory or uses short-read tools scores lower. An LLM that considers the environmental sample context and notes that host depletion may not be necessary scores highest on scientific validity.

**Common LLM errors at this step:**
- Using Bowtie2 (short-read aligner) instead of minimap2 (long-read capable)
- Treating host depletion as universally mandatory without considering sample type
- Not specifying the correct minimap2 preset for nanopore data
- Recommending BWA (short-read aligner)

---

## Step 4: Taxonomic Classification of Reads

**Objective:** Assign taxonomic labels to individual reads for microbial community composition analysis.

| Parameter | Value |
|:----------|:------|
| **Tool** | Kraken2 |
| **Version** | v2.0.7 |
| **Database** | NCBI nt (accessed 29 January 2023) |
| **Downsampling** | 5k reads (1h controlled), 15k reads (3h controlled), 70k reads (natural), 30k reads (urban) |

**Input:** Filtered FASTQ from step 1 (or host-depleted FASTQ from step 3)
**Output:** Kraken2 report file + per-read classification output

**Benchmarked alternatives (also validated in the study):**
- DIAMOND BLASTx — protein-based taxonomic classification (slower, more sensitive)
- Chan-Zuckerberg ID (CZID) pipeline — hybrid read- and contig-based classification

**Downstream analysis (not part of prompts but part of the validated workflow):**
- Downsampling to specific read counts per sample type for comparable cross-sample assessments
- PCoA on relative abundances using Python v3.9 (pandas v1.3.3, NumPy v1.21.2, scikit-learn v0.24.2, scikit-bio v0.5.6, SciPy v1.7.1)
- Visualization of 20 most abundant genera (≥1% relative abundance) using matplotlib v3.5.2

**Common LLM errors at this step:**
- Recommending the wrong Kraken2 database (Standard instead of nt, or PlusPF)
- Not mentioning the need for downsampling when comparing samples of different sequencing depth
- Recommending only BLAST-based approaches (too slow for large metagenomic datasets)
- Using Kraken2 with default confidence threshold without discussing the trade-off
- Not differentiating between report format and per-read output format

```bash
kraken2 --db /path/to/ncbi_nt \
  --threads 16 \
  --report sample_report.txt \
  --output sample_output.txt \
  filtered.fastq
```

---

## Step 5: Metagenomic Assembly

**Objective:** Assemble reads into contiguous sequences (contigs) for downstream binning and annotation.

The assembly includes **polishing** with minimap2 and Racon, which is critical for nanopore assemblies due to the higher per-read error rate.

| Parameter | Value |
|:----------|:------|
| **Assembler** | MetaFlye v2.9.1 (Flye with `--meta`) |
| **Polishing aligner** | minimap2 v2.17 |
| **Polishing tool** | Racon v1.5 |
| **Polishing rounds** | 3 |
| **Read type flag** | `--nano-hq` (for HAC-basecalled reads) |
| **Meta mode** | `--meta` (required for metagenomic data) |

**Input:** Filtered FASTQ from step 1 (or host-depleted FASTQ from step 3)
**Output:** Polished assembly FASTA + assembly_info.txt

**Acceptable alternatives:**
- Flye with `--meta` flag (MetaFlye is Flye in meta mode)
- wtdbg2 (acceptable long-read assembler, less commonly used for metagenomics)
- Short-read assemblers (MEGAHIT, SPAdes) are **incorrect** for nanopore long-read data

**Common LLM errors at this step:**
- Omitting the polishing step entirely (critical for nanopore assemblies)
- Using Medaka instead of Racon for polishing (Medaka is acceptable but was not the validated tool)
- Recommending only one round of polishing instead of three
- Using `--nano-raw` instead of `--nano-hq` for HAC-basecalled data
- Recommending short-read assemblers (SPAdes, MEGAHIT)
- Omitting the `--meta` flag (required — Flye without `--meta` assumes a single genome)
- Not specifying that urban samples were pooled across locations before assembly

```bash
# Assembly
flye --nano-hq filtered.fastq --out-dir assembly/ --meta --threads 16

# Polishing (3 rounds)
for i in 1 2 3; do
  minimap2 -t 16 assembly/assembly.fasta filtered.fastq > alignments.paf
  racon -t 16 filtered.fastq alignments.paf assembly/assembly.fasta > assembly/polished_${i}.fasta
  cp assembly/polished_${i}.fasta assembly/assembly.fasta
done
```

---

## Step 6: Binning and MAG Quality Assessment

**Objective:** Group assembled contigs into metagenome-assembled genomes (MAGs) and assess their completeness and contamination.

| Parameter | Value |
|:----------|:------|
| **Binning tool** | metaWRAP v1.3 |
| **Quality assessment** | CheckM v1.2.2 |
| **Minimum completeness** | ≥ 30% |
| **Maximum contamination** | ≤ 10% |
| **Urban samples** | Pooled across all samples per sampling location before binning |

**Input:** Assembly FASTA from step 5, reads for coverage estimation
**Output:** Binned FASTA files, quality assessment reports per bin

**Key detail:** metaWRAP integrates the output of multiple binning tools (MetaBAT2, MaxBin2, CONCOCT) and performs bin refinement. The quality thresholds (≥30% completeness, ≤10% contamination) are relatively permissive — reflecting the low-biomass nature of air samples where lower coverage is expected.

**Acceptable alternatives:**
- MetaBAT2 alone (simpler, less comprehensive)
- SemiBin2 (newer, deep learning-based)
- CONCOCT
- CheckM2 as quality assessment alternative

**Common LLM errors at this step:**
- Recommending very high completeness thresholds (≥90%) that are inappropriate for low-biomass environmental samples
- Using only a single binning tool instead of an ensemble approach like metaWRAP
- Not mentioning the read-to-contig mapping step necessary for coverage-based binning
- Using CheckM2 instead of CheckM (acceptable but not the validated version)
- Not mentioning the pooling strategy for urban samples

```bash
# Binning with metaWRAP (uses MetaBAT2, MaxBin2, CONCOCT internally)
metawrap binning -o binning/ -t 16 \
  -a assembly/assembly.fasta \
  --metabat2 --maxbin2 --concoct \
  filtered.fastq

# Bin refinement
metawrap bin_refinement -o refined_bins/ -t 16 \
  -A binning/metabat2_bins/ \
  -B binning/maxbin2_bins/ \
  -C binning/concoct_bins/ \
  -c 30 -x 10

# Quality assessment
checkm lineage_wf refined_bins/ checkm_output/ -t 16 -x fa
```

---

## Step 7: Functional Annotation

**Objective:** Annotate reads, contigs, and MAGs with antimicrobial resistance (AMR) genes and virulence factors. Assess presence of general metabolic pathways and ecosystem functions.

| Parameter | Value |
|:----------|:------|
| **AMR detection** | AMRFinderPlus v3.12.8 |
| **Resistance/virulence screening** | ABRicate v1.0.1 |
| **Format conversion** | seqkit v2.8.2 (FASTQ → FASTA for read-level application) |
| **Application levels** | Reads, contigs, and bins (all three) |

**Input:** Reads (FASTQ/FASTA), contigs (FASTA), and binned FASTA from steps 1/5/6
**Output:** AMR gene tables, virulence factor reports, functional annotations

**Key detail:** AMR screening was applied at **three levels** — reads, contigs, and bins — providing complementary perspectives. For read-level application, FASTQ files were converted to FASTA using seqkit.

**Acceptable alternatives:**
- Prokka or Bakta for general gene annotation
- eggNOG-mapper for functional categories
- DRAM for MAG-specific metabolic annotation
- ABRicate or CARD/RGI as AMR screening alternatives

**Common LLM errors at this step:**
- Only applying annotation at one level (typically contigs) instead of all three (reads, contigs, bins)
- Not mentioning the FASTQ → FASTA conversion step needed for read-level AMR screening
- Recommending only Prokka/Bakta for general annotation without AMR-specific tools
- Using outdated AMR databases
- Not specifying which databases to use with ABRicate (CARD, NCBI, VFDB, etc.)

```bash
# Convert FASTQ to FASTA for read-level screening
seqkit fq2fa filtered.fastq -o filtered.fasta

# AMR detection on reads
amrfinder -n filtered.fasta -o amr_reads.tsv --threads 16

# AMR detection on contigs
amrfinder -n assembly/assembly.fasta -o amr_contigs.tsv --threads 16

# AMR detection on MAGs
amrfinder -n refined_bins/bin.1.fa -o amr_bin1.tsv --threads 16

# ABRicate screening (example with CARD database)
abricate --db card assembly/assembly.fasta > abricate_contigs.tsv
abricate --db vfdb assembly/assembly.fasta > abricate_vf_contigs.tsv
```

---

## Pipeline Data Flow Summary

```
FAST5/POD5 (raw signal)
    │
    ▼
Step 1: Guppy v6.3.2 / Dorado v4.3.0 (HAC basecalling)
    │ → basecalled FASTQ
    ▼
    Porechop v0.2.3 (adapter trimming)
    │ → trimmed FASTQ
    ▼
    NanoFilt v2.8.0 (Q≥8, ≥100 bp)
    │ → filtered FASTQ
    ▼
Step 2: QC statistics (NanoPlot / NanoStat)
    │ → reports only (no data transformation)
    ▼
Step 3: Host depletion (not performed in published pipeline;
    │   minimap2 acceptable if applied)
    ▼
Step 4: Kraken2 v2.0.7 + NCBI nt database
    │ → taxonomy reports + per-read classifications
    │ → downsampled for cross-sample comparison
    ▼
Step 5: MetaFlye v2.9.1 → minimap2 v2.17 + Racon v1.5 (×3 polish)
    │ → polished contigs FASTA
    ▼
Step 6: metaWRAP v1.3 → CheckM v1.2.2 (≥30% comp., ≤10% contam.)
    │ → MAGs FASTA + quality reports
    ▼
Step 7: AMRFinderPlus v3.12.8 + ABRicate v1.0.1 (on reads, contigs, bins)
    │ → AMR/virulence tables + functional annotations
```
