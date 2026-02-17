#!/usr/bin/env python3
"""
Aggregate scoring results and produce summary statistics.

Reads results/tables/scoring_matrix.csv and reports:
- First fully correct version per model family
- Hardest step (lowest average score across all models)
- Most common failure mode per step

Usage:
    python scripts/aggregate_scores.py [--markdown]

Options:
    --markdown    Output results as a markdown file to evaluations/summary_generated.md
"""

import argparse
import sys
from collections import Counter
from pathlib import Path

import pandas as pd

SCORE_MAP = {
    "tool_selection": {"C": 1.0, "A": 0.5, "I": 0.0},
    "parameter_accuracy": {"C": 1.0, "P": 0.5, "I": 0.0},
    "output_compatibility": {"P": 1.0, "F": 0.0},
    "scientific_validity": {"S": 1.0, "Q": 0.5, "I": 0.0},
    "executability": {"R": 1.0, "M": 0.5, "N": 0.0},
}

FULLY_CORRECT = {
    "tool_selection": "C",
    "parameter_accuracy": "C",
    "output_compatibility": "P",
    "scientific_validity": "S",
    "executability": "R",
}

DIMENSIONS = list(SCORE_MAP.keys())


def load_scores(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    # Strip whitespace from score columns
    for dim in DIMENSIONS:
        df[dim] = df[dim].astype(str).str.strip().replace("nan", "")
    return df


def is_step_correct(row: pd.Series) -> bool:
    """Check if a single step has all-correct scores."""
    for dim, expected in FULLY_CORRECT.items():
        val = row.get(dim, "")
        if val.upper() != expected:
            return False
    return True


def has_all_scores(row: pd.Series) -> bool:
    """Check if all dimensions have been scored."""
    for dim in DIMENSIONS:
        val = row.get(dim, "")
        if val == "" or val == "nan":
            return False
    return True


def first_fully_correct(df: pd.DataFrame) -> dict[str, str | None]:
    """Find the first model version per family that got all steps correct."""
    results = {}
    for family in df["model_family"].unique():
        family_df = df[df["model_family"] == family]
        versions = family_df["model_version"].unique()
        results[family] = None
        for version in versions:
            version_df = family_df[family_df["model_version"] == version]
            if len(version_df) == 0:
                continue
            # All steps must have scores and all must be correct
            all_scored = all(has_all_scores(row) for _, row in version_df.iterrows())
            if not all_scored:
                continue
            all_correct = all(is_step_correct(row) for _, row in version_df.iterrows())
            if all_correct:
                results[family] = version
                break
    return results


def hardest_step(df: pd.DataFrame) -> list[tuple[int, str, float]]:
    """Rank steps by average composite score (lowest = hardest)."""
    step_scores = []
    for step_num in sorted(df["step_number"].unique()):
        step_df = df[df["step_number"] == step_num]
        scores = []
        for _, row in step_df.iterrows():
            if not has_all_scores(row):
                continue
            vals = []
            for dim in DIMENSIONS:
                val = row[dim].upper()
                mapped = SCORE_MAP[dim].get(val)
                if mapped is not None:
                    vals.append(mapped)
            if vals:
                scores.append(sum(vals) / len(vals))
        avg = sum(scores) / len(scores) if scores else float("nan")
        step_name = step_df["step_name"].iloc[0] if len(step_df) > 0 else "unknown"
        step_scores.append((step_num, step_name, avg))
    return sorted(step_scores, key=lambda x: x[2])


def common_failures_per_step(df: pd.DataFrame) -> dict[int, dict[str, str]]:
    """Find the most common non-correct score per dimension per step."""
    results = {}
    for step_num in sorted(df["step_number"].unique()):
        step_df = df[df["step_number"] == step_num]
        step_failures = {}
        for dim in DIMENSIONS:
            correct_val = FULLY_CORRECT[dim]
            failures = []
            for _, row in step_df.iterrows():
                val = row[dim].upper()
                if val and val != correct_val and val != "NAN":
                    failures.append(val)
            if failures:
                most_common = Counter(failures).most_common(1)[0]
                step_failures[dim] = f"{most_common[0]} ({most_common[1]}×)"
        results[step_num] = step_failures
    return results


def format_output(first_correct: dict, steps_ranked: list, failures: dict,
                  as_markdown: bool = False) -> str:
    lines = []

    if as_markdown:
        lines.append("# Aggregated Scoring Results\n")
        lines.append("*Auto-generated from `scoring_matrix.csv`*\n")

    # Section 1: First fully correct
    lines.append("\n## First Fully Correct Pipeline per Model Family\n")
    for family, version in first_correct.items():
        status = version if version else "None (no fully correct version)"
        lines.append(f"- **{family.capitalize()}:** {status}")

    # Section 2: Hardest step
    lines.append("\n## Steps Ranked by Difficulty (lowest average score first)\n")
    lines.append("| Rank | Step | Avg Score |")
    lines.append("|:-----|:-----|:----------|")
    for rank, (step_num, step_name, avg) in enumerate(steps_ranked, 1):
        score_str = f"{avg:.2f}" if not pd.isna(avg) else "no data"
        lines.append(f"| {rank} | {step_num}. {step_name} | {score_str} |")

    # Section 3: Common failures
    lines.append("\n## Most Common Failure Mode per Step\n")
    for step_num, dims in failures.items():
        if dims:
            lines.append(f"\n**Step {step_num}:**")
            for dim, val in dims.items():
                lines.append(f"  - {dim}: {val}")
        else:
            lines.append(f"\n**Step {step_num}:** no failures recorded (or no scores yet)")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Aggregate LLM evaluation scores.")
    parser.add_argument("--markdown", action="store_true",
                        help="Output as markdown file")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    csv_path = repo_root / "results" / "tables" / "scoring_matrix.csv"

    if not csv_path.exists():
        print(f"Error: {csv_path} not found.")
        sys.exit(1)

    df = load_scores(str(csv_path))

    # Check if any scores exist
    has_data = False
    for dim in DIMENSIONS:
        if any(v != "" and v != "nan" for v in df[dim]):
            has_data = True
            break

    if not has_data:
        print("No scores have been entered yet. Fill in scoring_matrix.csv and re-run.")
        sys.exit(0)

    first_correct = first_fully_correct(df)
    steps_ranked = hardest_step(df)
    failures = common_failures_per_step(df)

    output = format_output(first_correct, steps_ranked, failures, as_markdown=args.markdown)
    print(output)

    if args.markdown:
        md_path = repo_root / "evaluations" / "summary_generated.md"
        md_path.write_text(output)
        print(f"\nMarkdown summary written to {md_path}")


if __name__ == "__main__":
    main()
