#!/usr/bin/env python3
"""
Generate radar charts comparing scoring dimensions across model families.

Produces:
1. Per-family radar chart showing average dimension scores across versions
2. "First fully correct" comparison radar chart
3. Step difficulty radar chart

Usage:
    python scripts/generate_radar.py
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

SCORE_MAP = {
    "tool_selection": {"C": 1.0, "A": 0.5, "I": 0.0},
    "parameter_accuracy": {"C": 1.0, "P": 0.5, "I": 0.0},
    "output_compatibility": {"P": 1.0, "F": 0.0},
    "scientific_validity": {"S": 1.0, "Q": 0.5, "I": 0.0},
    "executability": {"R": 1.0, "M": 0.5, "N": 0.0},
}

DIMENSIONS = list(SCORE_MAP.keys())
DIM_LABELS = ["Tool\nSelection", "Parameter\nAccuracy", "Output\nCompat.", "Scientific\nValidity", "Execut-\nability"]

FAMILY_STYLES = {
    "openai": {"color": "#10b981", "label": "OpenAI"},
    "claude": {"color": "#8b5cf6", "label": "Claude"},
    "gemini": {"color": "#f43f5e", "label": "Gemini"},
}


def load_and_score(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    for dim in DIMENSIONS:
        df[f"{dim}_num"] = df[dim].map(SCORE_MAP[dim])
    return df


def radar_chart(ax, values_list, labels, colors, title):
    """Draw a radar chart on the given axes."""
    N = len(DIMENSIONS)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += angles[:1]

    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_rlabel_position(0)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(DIM_LABELS, fontsize=7, fontweight="500")
    ax.set_ylim(0, 1.05)
    ax.set_yticks([0.25, 0.5, 0.75, 1.0])
    ax.set_yticklabels(["0.25", "0.50", "0.75", "1.00"], fontsize=6, color="#94a3b8")

    for vals, label, color in zip(values_list, labels, colors):
        data = vals.tolist() + vals.tolist()[:1]
        ax.plot(angles, data, "o-", linewidth=1.8, label=label, color=color, markersize=4)
        ax.fill(angles, data, alpha=0.12, color=color)

    ax.set_title(title, fontsize=10, fontweight="bold", pad=18, color="#1e293b")
    ax.legend(loc="upper right", bbox_to_anchor=(1.35, 1.1), fontsize=7, frameon=False)


def plot_family_radars(df: pd.DataFrame, output_path: str):
    """Radar chart: average score per dimension per model family."""
    fig, axes = plt.subplots(1, 3, figsize=(14, 5), subplot_kw={"projection": "polar"})

    for idx, (family, style) in enumerate(FAMILY_STYLES.items()):
        fam_df = df[df["model_family"] == family]
        versions = fam_df["model_version"].unique()

        values_list = []
        labels = []
        n = len(versions)
        cmap = plt.cm.get_cmap("viridis", max(n, 2))

        for i, ver in enumerate(versions):
            ver_df = fam_df[fam_df["model_version"] == ver]
            means = np.array([ver_df[f"{d}_num"].mean() for d in DIMENSIONS])
            values_list.append(means)
            labels.append(ver.replace("_", " "))

        colors = [cmap(i / max(n - 1, 1)) for i in range(n)]
        radar_chart(axes[idx], values_list, labels, colors, style["label"])

    plt.tight_layout()
    fig.savefig(output_path, dpi=200, bbox_inches="tight", facecolor="white")
    print(f"Family radars saved to {output_path}")
    plt.close()


def plot_step_difficulty(df: pd.DataFrame, output_path: str):
    """Horizontal bar chart: average composite score per step, color-coded."""
    fig, ax = plt.subplots(figsize=(8, 5))

    steps = sorted(df["step_number"].unique())
    step_names = {
        1: "Basecalling", 2: "QC", 3: "Host Depletion",
        4: "Taxonomy", 5: "Assembly", 6: "Binning", 7: "Annotation"
    }

    scores = []
    for s in steps:
        sdf = df[df["step_number"] == s]
        vals = []
        for _, row in sdf.iterrows():
            row_scores = [row.get(f"{d}_num") for d in DIMENSIONS]
            if all(v is not None and not np.isnan(v) for v in row_scores):
                vals.append(np.mean(row_scores))
        scores.append(np.mean(vals) if vals else 0)

    colors = []
    for s in scores:
        if s >= 0.85:
            colors.append("#10b981")
        elif s >= 0.7:
            colors.append("#f59e0b")
        else:
            colors.append("#ef4444")

    y_pos = np.arange(len(steps))
    bars = ax.barh(y_pos, scores, color=colors, height=0.6, edgecolor="white", linewidth=0.5)

    ax.set_yticks(y_pos)
    ax.set_yticklabels([f"{s}. {step_names.get(s, '')}" for s in steps], fontsize=9)
    ax.set_xlim(0, 1.05)
    ax.set_xlabel("Average Composite Score (all models)", fontsize=9)
    ax.set_title("Step Difficulty Ranking", fontsize=12, fontweight="bold", color="#1e293b", pad=12)
    ax.invert_yaxis()

    for bar, score in zip(bars, scores):
        ax.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height() / 2,
                f"{score:.2f}", va="center", fontsize=8, fontweight="bold", color="#334155")

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_color("#e2e8f0")
    ax.spines["left"].set_color("#e2e8f0")

    plt.tight_layout()
    fig.savefig(output_path, dpi=200, bbox_inches="tight", facecolor="white")
    print(f"Step difficulty chart saved to {output_path}")
    plt.close()


def plot_version_timeline(df: pd.DataFrame, output_path: str):
    """Line chart: composite score over model versions (chronological) per family."""
    fig, ax = plt.subplots(figsize=(12, 5))

    version_order = {
        "openai": ["gpt4o", "o1_preview", "o1_mini", "o1", "o1_pro", "o3_mini", "o3_high", "o4_mini", "gpt5"],
        "claude": ["sonnet_3.5", "sonnet_4", "sonnet_4.5", "haiku_4.5", "opus_4.5", "opus_4.6"],
        "gemini": ["2.0_flash", "2.5_pro_preview", "2.5_flash", "2.5_pro_stable", "3_pro", "3_deep_think", "3_flash"],
    }

    version_labels = {
        "gpt4o": "GPT-4o", "o1_preview": "o1-prev", "o1_mini": "o1-mini", "o1": "o1",
        "o1_pro": "o1-pro", "o3_mini": "o3-mini", "o3_high": "o3", "o4_mini": "o4-mini", "gpt5": "GPT-5",
        "sonnet_3.5": "S3.5", "sonnet_4": "S4", "sonnet_4.5": "S4.5",
        "haiku_4.5": "H4.5", "opus_4.5": "Op4.5", "opus_4.6": "Op4.6",
        "2.0_flash": "2.0F", "2.5_pro_preview": "2.5PP", "2.5_flash": "2.5F",
        "2.5_pro_stable": "2.5P", "3_pro": "3P", "3_deep_think": "3DT", "3_flash": "3F",
    }

    for family, style in FAMILY_STYLES.items():
        versions = version_order.get(family, [])
        x_vals = []
        y_vals = []
        for i, ver in enumerate(versions):
            ver_df = df[(df["model_family"] == family) & (df["model_version"] == ver)]
            if len(ver_df) == 0:
                continue
            scores = []
            for _, row in ver_df.iterrows():
                row_scores = [row.get(f"{d}_num") for d in DIMENSIONS]
                if all(v is not None and not np.isnan(v) for v in row_scores):
                    scores.append(np.mean(row_scores))
            if scores:
                x_vals.append(i)
                y_vals.append(np.mean(scores))

        ax.plot(x_vals, y_vals, "o-", color=style["color"], linewidth=2, markersize=6,
                label=style["label"], zorder=3)

        # Label last point
        if x_vals and y_vals:
            ax.annotate(version_labels.get(versions[x_vals[-1]], versions[x_vals[-1]]),
                        (x_vals[-1], y_vals[-1]), textcoords="offset points",
                        xytext=(8, 4), fontsize=7, color=style["color"], fontweight="bold")

    # Perfect score line
    ax.axhline(1.0, color="#10b981", linewidth=1, linestyle="--", alpha=0.4)
    ax.text(-0.3, 1.01, "Perfect", fontsize=7, color="#10b981", alpha=0.6)

    ax.set_ylim(0.3, 1.08)
    ax.set_ylabel("Average Composite Score", fontsize=9)
    ax.set_xlabel("Model Version (chronological within family)", fontsize=9)
    ax.set_title("LLM Performance Trajectory: Nanopore Metagenomics Pipeline Generation",
                 fontsize=11, fontweight="bold", color="#1e293b", pad=12)
    ax.legend(fontsize=8, frameon=False, loc="lower right")

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_color("#e2e8f0")
    ax.spines["left"].set_color("#e2e8f0")
    ax.grid(True, alpha=0.15)

    plt.tight_layout()
    fig.savefig(output_path, dpi=200, bbox_inches="tight", facecolor="white")
    print(f"Timeline chart saved to {output_path}")
    plt.close()


def main():
    repo_root = Path(__file__).resolve().parent.parent
    csv_path = repo_root / "results" / "tables" / "scoring_matrix.csv"
    figs = repo_root / "results" / "figures"

    if not csv_path.exists():
        print(f"Error: {csv_path} not found.")
        sys.exit(1)

    df = load_and_score(str(csv_path))

    plot_family_radars(df, str(figs / "family_radar.png"))
    plot_step_difficulty(df, str(figs / "step_difficulty.png"))
    plot_version_timeline(df, str(figs / "version_timeline.png"))


if __name__ == "__main__":
    main()
