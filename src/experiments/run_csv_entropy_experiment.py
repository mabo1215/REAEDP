"""
Real-data experiment: load a CSV (e.g. y_amazon-google-large.csv), compute histogram
and Shannon entropy, add DP noise to the histogram, and plot original vs private.
Saves figure to paper/figs/ for the paper.
"""
import sys
import os
import argparse
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from reaedp.entropy import shannon_entropy, entropy_sensitivity_bound
from reaedp.dp_mechanisms import laplace_mechanism
from project_paths import PAPER_FIG_DIR, resolve_workspace_path

FIG_DIR = str(PAPER_FIG_DIR)


def main(config=None):
    if config is None:
        parser = argparse.ArgumentParser(description="CSV entropy + DP experiment for paper")
        parser.add_argument("--input", "-i", type=str, default="data/y_amazon-google-large.csv")
        parser.add_argument("--column", type=str, default="y")
        parser.add_argument("--bins", type=int, default=30)
        parser.add_argument("--epsilon", type=float, default=1.0)
        parser.add_argument("--out_csv", type=str, default="")
        parser.add_argument("--out_fig", type=str, default="fig_csv_entropy.png")
        parser.add_argument("--max_rows", type=int, default=100000)
        args = parser.parse_args()
        config = {
            "input": args.input,
            "column": args.column,
            "bins": args.bins,
            "epsilon": args.epsilon,
            "out_csv": args.out_csv,
            "out_fig": args.out_fig,
            "max_rows": args.max_rows,
        }

    input_path = config.get("input", "data/y_amazon-google-large.csv")
    column = config.get("column", "y")
    n_bins = config.get("bins", 30)
    epsilon = config.get("epsilon", 1.0)
    out_csv = config.get("out_csv", "")
    out_fig = config.get("out_fig", "fig_csv_entropy.png")
    max_rows = config.get("max_rows", 100000)
    seed = config.get("seed", 42)
    rng = np.random.default_rng(seed)

    input_path = str(resolve_workspace_path(input_path))
    if not os.path.isfile(input_path):
        print(f"CSV not found: {input_path}. Skip or set config 'input'.")
        return

    df = pd.read_csv(input_path, nrows=max_rows)
    if column not in df.columns:
        print(f"Column '{column}' not in CSV. Columns: {list(df.columns)}")
        return
    y = df[column].dropna().values.astype(float)
    n = len(y)
    if n == 0:
        print("No numeric values in column.")
        return

    counts, bin_edges = np.histogram(y, bins=n_bins)
    counts = counts.astype(float)
    H_orig = shannon_entropy(counts)
    bound = entropy_sensitivity_bound(n)

    sensitivity = 1.0  # L1 sensitivity for one record change in histogram
    noisy_counts = laplace_mechanism(counts, sensitivity=sensitivity, epsilon=epsilon, rng=rng)
    noisy_counts = np.maximum(noisy_counts, 0)
    H_noisy = shannon_entropy(noisy_counts)

    os.makedirs(FIG_DIR, exist_ok=True)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3.5))
    x_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    width = (bin_edges[1] - bin_edges[0]) * 0.4
    ax1.bar(x_centers - width / 2, counts, width, label="Original", color="C0", alpha=0.8)
    ax1.bar(x_centers + width / 2, noisy_counts, width, label=f"Private ($\\varepsilon$={epsilon})", color="C1", alpha=0.8)
    ax1.set_xlabel(column)
    ax1.set_ylabel("Count")
    ax1.set_title(f"Histogram: {os.path.basename(input_path)} (n={n})")
    ax1.legend()

    ax2.bar([0], [H_orig], width=0.35, label="Original", color="C0")
    ax2.bar([0.4], [H_noisy], width=0.35, label=f"Private ($\\varepsilon$={epsilon})", color="C1")
    ax2.set_ylabel("Shannon entropy $H$")
    ax2.set_xticks([0.2])
    ax2.set_xticklabels(["Entropy"])
    ax2.legend()
    ax2.set_title(f"$H$: {H_orig:.3f} $\\to$ {H_noisy:.3f}")

    plt.tight_layout()
    fig_path = os.path.join(FIG_DIR, out_fig)
    plt.savefig(fig_path, dpi=config.get("dpi", 150))
    plt.close()
    print(f"Saved {fig_path}")
    print(f"  n={n}, bins={n_bins}, H_orig={H_orig:.4f}, H_noisy={H_noisy:.4f}, Delta_H bound={bound:.6f}")

    if out_csv:
        out_csv = str(resolve_workspace_path(out_csv))
        os.makedirs(os.path.dirname(out_csv) or ".", exist_ok=True)
        with open(out_csv, "w") as f:
            f.write("dataset,n,bins,epsilon,H_orig,H_noisy,Delta_H_bound\n")
            f.write(f"{os.path.basename(input_path)},{n},{n_bins},{epsilon},{H_orig:.6f},{H_noisy:.6f},{bound:.6f}\n")
        print(f"Wrote {out_csv}")


if __name__ == "__main__":
    main()
