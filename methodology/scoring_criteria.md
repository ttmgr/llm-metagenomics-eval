# Scoring Criteria

Rubric for evaluating LLM-generated nanopore metagenomics pipeline steps. Each dimension uses a three-level scale with concrete examples specific to nanopore long-read metagenomics.

---

## 1. Tool Selection

Does the model recommend the appropriate tool for Oxford Nanopore long-read data?

| Score | Definition | Examples |
|:------|:-----------|:---------|
| **Correct** | The recommended tool is the standard or best-practice choice for this step with nanopore data | Dorado for basecalling; Kraken2 for taxonomic classification; MetaFlye for long-read metagenomic assembly |
| **Acceptable** | The tool works for nanopore data and is a defensible choice, but is not the standard recommendation | Guppy instead of Dorado (deprecated but functional); minimap2 + MEGAN instead of Kraken2 for taxonomy |
| **Incorrect** | The tool is inappropriate for nanopore long-read data, is deprecated beyond usability, or does not exist | Trimmomatic for adapter trimming (designed for short reads); MEGAHIT for assembly (short-read assembler); Albacore for basecalling (discontinued) |

### Common failure patterns

- Recommending **short-read tools** (FastQC, Trimmomatic, MEGAHIT, SPAdes) for long-read data
- Recommending **deprecated ONT tools** (Albacore, older Guppy versions with incorrect syntax)
- Recommending tools that exist but are **inappropriate for metagenomics** (e.g., Canu for metagenomic assembly — designed for isolate genomes)
- **Hallucinating tools** that do not exist

---

## 2. Parameter Accuracy

Are the flags, thresholds, and kit-specific settings appropriate?

| Score | Definition | Examples |
|:------|:-----------|:---------|
| **Correct** | All parameters are appropriate for the data type, kit, and analytical context | Correct Dorado model for the chemistry version; appropriate quality threshold for nanopore data (Q8-Q10); correct Kraken2 confidence threshold |
| **Partially Correct** | Most parameters are reasonable, but one or more are suboptimal or slightly wrong | Quality threshold too stringent for nanopore (e.g., Q30, which is Illumina-appropriate); correct tool but missing a critical flag; reasonable but non-standard database choice |
| **Incorrect** | Parameters are wrong in ways that would produce incorrect or misleading results | Wrong basecalling model for the chemistry; adapter sequences for a different kit; assembly parameters that assume short reads |

### Common failure patterns

- **Illumina-appropriate thresholds** applied to nanopore data (Q30 filtering would remove nearly all nanopore reads)
- **Missing kit-specific parameters** (e.g., not specifying the correct barcode kit for demultiplexing)
- **Version-specific syntax errors** (flags that changed between tool versions)
- **Default parameters** that are technically valid but inappropriate for the specific sample type (e.g., not adjusting minimum contig length for low-biomass metagenomes)

---

## 3. Output Compatibility

Does the output of this step work as input for the next step?

| Score | Definition | Examples |
|:------|:-----------|:---------|
| **Pass** | Output format, naming conventions, and content are compatible with the next step as written | FASTQ output from basecalling → FASTQ input expected by QC tool; BAM output from host depletion properly converted to FASTQ for downstream use |
| **Fail** | Output format, path, or content would cause the next step to fail or produce wrong results | Output written to a path the next step doesn't reference; BAM output where FASTQ is expected; gzipped output where the next tool expects uncompressed |

### What this dimension captures

This is the **most critical** dimension for sequential pipeline evaluation. It tests whether the model understands the data flow between tools, not just the tools themselves. Common failures include:

- **Path mismatches:** Step N writes to `output/filtered_reads.fastq` but step N+1 reads from `results/qc_passed.fastq`
- **Format mismatches:** One step produces BAM, the next expects FASTQ, with no conversion
- **Compression mismatches:** One step outputs `.fastq.gz`, the next tool cannot read gzipped input
- **Missing index files:** A step requires a BAM index (`.bai`) that the previous step didn't generate

---

## 4. Scientific Validity

Are the analytical choices defensible for this data type and experimental context?

| Score | Definition | Examples |
|:------|:-----------|:---------|
| **Sound** | Choices reflect current best practices for nanopore metagenomics | Including host depletion before taxonomy; using a protein-level database for functional annotation of error-prone long reads; appropriate assembly strategy for metagenomic data |
| **Questionable** | Choices are technically possible but reflect poor understanding of the domain | Skipping host depletion for environmental samples that may contain host DNA; using nucleotide-level alignment for functional annotation of nanopore reads (high error rate makes this unreliable); not accounting for chimeric reads |
| **Incorrect** | Choices would produce scientifically wrong or misleading results | Treating nanopore reads as if they have Illumina-level accuracy; assembling without metagenomic mode; using a database inappropriate for the sample type |

### What this dimension captures

This dimension tests **domain expertise**, not just tool knowledge. A model might select the right tool with correct parameters, producing code that runs — but the analytical approach is wrong for the biological question or data type.

---

## 5. Executability

Does the generated code actually run?

| Score | Definition | Examples |
|:------|:-----------|:---------|
| **Runs** | Code executes without modification on appropriately configured system | All commands valid; paths use variables or clear placeholders; syntax correct for specified tool versions |
| **Runs with Minor Fixes** | Code requires small, obvious fixes to run | Missing quotes around a path with spaces; typo in a flag name; missing `mkdir -p` for output directory; trivially wrong variable name |
| **Does Not Run** | Code has fundamental errors that prevent execution | Non-existent flags; completely wrong command syntax; logical errors in shell scripting (e.g., unmatched quotes, broken pipes); references to undefined variables |

### Scope

This dimension evaluates syntactic and structural correctness, not whether the system has the required tools installed. Code is evaluated assuming a correctly configured bioinformatics environment with all referenced tools available.

---

## Scoring Summary Table

For quick reference, each step is scored as:

| Dimension | Levels |
|:----------|:-------|
| Tool Selection | `C` (Correct) · `A` (Acceptable) · `I` (Incorrect) |
| Parameter Accuracy | `C` (Correct) · `P` (Partially Correct) · `I` (Incorrect) |
| Output Compatibility | `P` (Pass) · `F` (Fail) |
| Scientific Validity | `S` (Sound) · `Q` (Questionable) · `I` (Incorrect) |
| Executability | `R` (Runs) · `M` (Minor Fixes) · `N` (Does Not Run) |

A step is considered **fully correct** only if it scores C/C/P/S/R across all five dimensions.

A model is considered to have **produced a fully correct pipeline** only if all steps are fully correct.
