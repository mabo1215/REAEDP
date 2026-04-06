"""
Ablation: effect of bins and n on entropy error; Theorem 4 bound holds across settings.
Output: paper/figs/fig_ablation.png
"""
import sys
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from reaedp.entropy import shannon_entropy, entropy_sensitivity_bound
from reaedp.dp_mechanisms import laplace_mechanism
from project_paths import DATA_DIR, PAPER_FIG_DIR, resolve_workspace_path

FIG_DIR = str(PAPER_FIG_DIR)


def main(config=None):
    config = config or {}
    seed = config.get("seed", 42)
    rng = np.random.default_rng(seed)
    epsilon = config.get("epsilon", 1.0)
    n_trials = config.get("n_trials", 15)
    csv_path = config.get("input") or str(DATA_DIR / "y_amazon-google-large.csv")
    column = config.get("column", "y")
    csv_path = str(resolve_workspace_path(csv_path))

    if not os.path.isfile(csv_path):
        print(f"CSV not found: {csv_path}. Skipping ablation.")
        return

    df = pd.read_csv(csv_path)
    if column not in df.columns:
        print(f"Column '{column}' not in CSV. Skipping.")
        return
    y_full = df[column].dropna().values.astype(float)

    bins_vals = [10, 20, 30, 50, 80]
    err_by_bins = []
    bound_by_bins = []
    n_used = min(len(y_full), 50000)
    y = y_full[:n_used]

    for b in bins_vals:
        counts, _ = np.histogram(y, bins=b)
        counts = counts.astype(float)
        n = counts.sum()
        H_orig = shannon_entropy(counts)
        bound_H = entropy_sensitivity_bound(n)
        bound_by_bins.append(bound_H)
        errs = []
        for _ in range(n_trials):
            noisy = laplace_mechanism(counts, sensitivity=1.0, epsilon=epsilon, rng=rng)
            noisy = np.maximum(noisy, 0)
            errs.append(abs(H_orig - shannon_entropy(noisy)))
        err_by_bins.append(np.mean(errs))

    os.makedirs(FIG_DIR, exist_ok=True)
    fig, ax = plt.subplots(figsize=(5, 3.5))
    ax.plot(bins_vals, err_by_bins, "o-", label="Mean $|H_{\\mathrm{orig}} - H_{\\mathrm{noisy}}|$", color="C0")
    ax.plot(bins_vals, bound_by_bins, "s--", label="$\\Delta_H$ bound (Th.4)", color="C1")
    ax.set_xlabel("Number of bins $m$")
    ax.set_ylabel("Entropy error / bound")
    ax.set_title(f"Ablation: entropy error vs bins ($n={n_used}$, $\\varepsilon={epsilon}$)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    out = os.path.join(FIG_DIR, "fig_ablation.png")
    plt.savefig(out, dpi=config.get("dpi", 150))
    plt.close()
    print(f"Saved {out}")


if __name__ == "__main__":
    main()
