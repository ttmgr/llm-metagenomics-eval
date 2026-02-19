#!/usr/bin/env python3
"""
Generate a scoring heatmap from the evaluation matrix.

Reads results/tables/scoring_matrix.csv and produces a heatmap with:
- X-axis: pipeline steps
- Y-axis: model versions (grouped by family)
- Color: composite score (green = correct, yellow = partial, red = incorrect)

Usage:
    python scripts/generate_heatmap.py
"""

import sys
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# --- Configuration ---

SCORE_MAP = {
    "tool_selection": {"C": 1.0, "A": 0.5, "I": 0.0},
    "parameter_accuracy": {"C": 1.0, "P": 0.5, "I": 0.0},
    "output_compatibility": {"P": 1.0, "F": 0.0},
    "scientific_validity": {"S": 1.0, "Q": 0.5, "I": 0.0},
    "executability": {"R": 1.0, "M": 0.5, "N": 0.0},
}

DIMENSIONS = list(SCORE_MAP.keys())

STEP_LABELS = {
    1: "Basecalling",
    2: "QC",
    3: "Host\nDepletion",
    4: "Taxonomy",
    5: "Assembly",
    6: "Binning",
    7: "Annotation",
}

MODEL_ORDER = [
    ("openai", "gpt4o"),
    ("openai", "o1_preview"),
    ("openai", "o1_mini"),
    ("openai", "o1"),
    ("openai", "o1_pro"),
    ("openai", "o3_mini"),
    ("openai", "o3_high"),
    ("openai", "o4_mini"),
    ("openai", "gpt5"),
    ("claude", "sonnet_3.5"),
    ("claude", "sonnet_4"),
    ("claude", "sonnet_4.5"),
    ("claude", "haiku_4.5"),
    ("claude", "opus_4.5"),
    ("claude", "opus_4.6"),
    ("gemini", "2.0_flash"),
    ("gemini", "2.5_pro_preview"),
    ("gemini", "2.5_flash"),
    ("gemini", "2.5_pro_stable"),
    ("gemini", "3_pro"),
    ("gemini", "3_deep_think"),
    ("gemini", "3_flash"),
]

MODEL_LABELS = {
    ("openai", "gpt4o"): "GPT-4o",
    ("openai", "o1_preview"): "o1-preview",
    ("openai", "o1_mini"): "o1-mini",
    ("openai", "o1"): "o1",
    ("openai", "o1_pro"): "o1-pro",
    ("openai", "o3_mini"): "o3-mini",
    ("openai", "o3_high"): "o3 (high)",
    ("openai", "o4_mini"): "o4-mini",
    ("openai", "gpt5"): "GPT-5",
    ("claude", "sonnet_3.5"): "Sonnet 3.5",
    ("claude", "sonnet_4"): "Sonnet 4",
    ("claude", "sonnet_4.5"): "Sonnet 4.5",
    ("claude", "haiku_4.5"): "Haiku 4.5",
    ("claude", "opus_4.5"): "Opus 4.5",
    ("claude", "opus_4.6"): "Opus 4.6",
    ("gemini", "2.0_flash"): "2.0 Flash",
    ("gemini", "2.5_pro_preview"): "2.5 Pro Prev",
    ("gemini", "2.5_flash"): "2.5 Flash",
    ("gemini", "2.5_pro_stable"): "2.5 Pro",
    ("gemini", "3_pro"): "3 Pro",
    ("gemini", "3_deep_think"): "3 Deep Think",
    ("gemini", "3_flash"): "3 Flash",
}

FAMILY_COLORS = {
    "openai": "#e8e8e8",
    "claude": "#f0f0f0",
    "gemini": "#e8e8e8",
}


def load_scores(csv_path: str) -> pd.DataFrame:
    """Load scoring matrix, skipping rows with no scores."""
    df = pd.read_csv(csv_path)
    return df


def compute_composite(row: pd.Series):
    """Compute mean numeric score across all dimensions. Returns None if any dimension is missing."""
    values = []
    for dim in DIMENSIONS:
        raw = row.get(dim)
        if pd.isna(raw) or str(raw).strip() == "":
            return None
        score = SCORE_MAP[dim].get(str(raw).strip().upper())
        if score is None:
            return None
        values.append(score)
    return np.mean(values) if values else None


def build_matrix(df: pd.DataFrame):
    """Build 2D score matrix (models × steps)."""
    steps = sorted(df["step_number"].unique())
    n_models = len(MODEL_ORDER)
    n_steps = len(steps)

    matrix = np.full((n_models, n_steps), np.nan)

    for i, (family, version) in enumerate(MODEL_ORDER):
        subset = df[(df["model_family"] == family) & (df["model_version"] == version)]
        for _, row in subset.iterrows():
            step_idx = steps.index(row["step_number"])
            score = compute_composite(row)
            if score is not None:
                matrix[i, step_idx] = score

    y_labels = [MODEL_LABELS.get(m, f"{m[0]}/{m[1]}") for m in MODEL_ORDER]
    x_labels = [STEP_LABELS.get(s, f"Step {s}") for s in steps]

    return matrix, y_labels, x_labels


def plot_heatmap(matrix, y_labels, x_labels, output_path):
    """Generate and save the heatmap."""
    fig, ax = plt.subplots(figsize=(10, 14))

    # Custom colormap: red → yellow → green
    from matplotlib.colors import LinearSegmentedColormap
    colors_list = ["#e74c3c", "#f39c12", "#2ecc71"]
    cmap = LinearSegmentedColormap.from_list("score", colors_list, N=256)
    cmap.set_bad(color="#f5f5f5")  # light gray for missing data

    # Mask NaN values
    masked = np.ma.masked_invalid(matrix)

    im = ax.imshow(masked, cmap=cmap, aspect="auto", vmin=0, vmax=1)

    # Axes
    ax.set_xticks(range(len(x_labels)))
    ax.set_xticklabels(x_labels, fontsize=9, ha="center")
    ax.set_yticks(range(len(y_labels)))
    ax.set_yticklabels(y_labels, fontsize=9)

    # Family group labels on the right
    families = [m[0] for m in MODEL_ORDER]
    prev_family = None
    family_spans = []
    start = 0
    for i, f in enumerate(families):
        if f != prev_family:
            if prev_family is not None:
                family_spans.append((prev_family, start, i - 1))
            start = i
            prev_family = f
    family_spans.append((prev_family, start, len(families) - 1))

    ax2 = ax.twinx()
    ax2.set_ylim(ax.get_ylim())
    ax2.set_yticks([(s + e) / 2 for _, s, e in family_spans])
    ax2.set_yticklabels([f.capitalize() for f, _, _ in family_spans], fontsize=10,
                        fontweight="bold")

    # Grid
    for i in range(len(y_labels) + 1):
        ax.axhline(i - 0.5, color="white", linewidth=1.5)
    for j in range(len(x_labels) + 1):
        ax.axvline(j - 0.5, color="white", linewidth=1.5)

    # Score text in cells
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            val = matrix[i, j]
            if np.isnan(val):
                ax.text(j, i, "—", ha="center", va="center", fontsize=9, color="#999")
            else:
                text_color = "white" if val < 0.4 else ("black" if val > 0.7 else "black")
                ax.text(j, i, f"{val:.1f}", ha="center", va="center", fontsize=9,
                        fontweight="bold", color=text_color)

    # Legend
    legend_patches = [
        mpatches.Patch(color="#2ecc71", label="Correct (1.0)"),
        mpatches.Patch(color="#f39c12", label="Partial (0.5)"),
        mpatches.Patch(color="#e74c3c", label="Incorrect (0.0)"),
        mpatches.Patch(color="#f5f5f5", label="Not evaluated"),
    ]
    ax.legend(handles=legend_patches, loc="upper left", bbox_to_anchor=(0, -0.08),
              ncol=4, fontsize=8, frameon=False)

    ax.set_title("LLM Nanopore Metagenomics Pipeline Evaluation", fontsize=13,
                 fontweight="bold", pad=15)
    ax.set_xlabel("Pipeline Step", fontsize=10, labelpad=10)

    plt.tight_layout()
    fig.savefig(output_path, dpi=200, bbox_inches="tight", facecolor="white")
    print(f"Heatmap saved to {output_path}")
    plt.close()


def main():
    repo_root = Path(__file__).resolve().parent.parent
    csv_path = repo_root / "results" / "tables" / "scoring_matrix.csv"
    output_path = repo_root / "results" / "figures" / "scoring_heatmap.png"

    if not csv_path.exists():
        print(f"Error: {csv_path} not found.")
        sys.exit(1)

    df = load_scores(str(csv_path))
    matrix, y_labels, x_labels = build_matrix(df)

    # Check if there is any data to plot
    if np.all(np.isnan(matrix)):
        print("No scores found in the matrix. Generating empty heatmap template.")

    plot_heatmap(matrix, y_labels, x_labels, str(output_path))


if __name__ == "__main__":
    main()
