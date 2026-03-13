"""
Baseline comparison: Laplace vs Gaussian histogram release (same epsilon).
Utility: entropy preservation error |H_orig - H_noisy| and count MAE.
For paper: compare proposed pipeline with standard DP mechanisms.
Output: paper/fig/fig_baseline.png
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
from reaedp.dp_mechanisms import laplace_mechanism, gaussian_mechanism

ROOT = os.path.join(os.path.dirname(__file__), "..")
FIG_DIR = os.path.join(ROOT, "paper", "fig")
DATA_DIR = os.path.join(ROOT, "data")


def main(config=None):
    config = config or {}
    seed = config.get("seed", 42)
    rng = np.random.default_rng(seed)
    epsilons = np.array(config.get("epsilons", [0.25, 0.5, 1.0, 2.0, 4.0]))
    delta = config.get("delta", 1e-5)
    n_trials = config.get("n_trials", 10)
    bins = config.get("bins", 30)
    max_rows = config.get("max_rows", 50000)
    csv_path = config.get("input") or os.path.join(DATA_DIR, "y_amazon-google-large.csv")
    column = config.get("column", "y")
    if not os.path.isabs(csv_path):
        csv_path = os.path.join(ROOT, csv_path)

    if not os.path.isfile(csv_path):
        print(f"CSV not found: {csv_path}. Skipping baseline comparison.")
        return

    df = pd.read_csv(csv_path, nrows=max_rows)
    if column not in df.columns:
        print(f"Column '{column}' not in CSV. Skipping.")
        return
    y = df[column].dropna().values.astype(float)
    n = len(y)
    counts, _ = np.histogram(y, bins=bins)
    counts = counts.astype(float)
    H_orig = shannon_entropy(counts)
    bound_H = entropy_sensitivity_bound(n)

    err_entropy_lap = []
    err_entropy_gau = []
    mae_lap = []
    mae_gau = []

    for eps in epsilons:
        e_l, e_g = [], []
        m_l, m_g = [], []
        for _ in range(n_trials):
            noisy_l = laplace_mechanism(counts, sensitivity=1.0, epsilon=eps, rng=rng)
            noisy_l = np.maximum(noisy_l, 0)
            noisy_g = gaussian_mechanism(counts, sensitivity_l2=np.sqrt(2), epsilon=eps, delta=delta, rng=rng)
            noisy_g = np.maximum(noisy_g, 0)
            H_l = shannon_entropy(noisy_l)
            H_g = shannon_entropy(noisy_g)
            e_l.append(abs(H_orig - H_l))
            e_g.append(abs(H_orig - H_g))
            m_l.append(np.abs(noisy_l - counts).mean())
            m_g.append(np.abs(noisy_g - counts).mean())
        err_entropy_lap.append(np.mean(e_l))
        err_entropy_gau.append(np.mean(e_g))
        mae_lap.append(np.mean(m_l))
        mae_gau.append(np.mean(m_g))

    os.makedirs(FIG_DIR, exist_ok=True)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3.5))
    ax1.plot(epsilons, err_entropy_lap, "o-", label="Laplace", color="C0")
    ax1.plot(epsilons, err_entropy_gau, "s-", label="Gaussian", color="C1")
    ax1.axhline(bound_H, color="gray", linestyle="--", label="$\\Delta_H$ bound (Th.4)")
    ax1.set_xlabel("$\\varepsilon$")
    ax1.set_ylabel("$|H_{\\mathrm{orig}} - H_{\\mathrm{noisy}}|$")
    ax1.set_title("Entropy preservation vs $\\varepsilon$")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    ax2.plot(epsilons, mae_lap, "o-", label="Laplace", color="C0")
    ax2.plot(epsilons, mae_gau, "s-", label="Gaussian", color="C1")
    ax2.set_xlabel("$\\varepsilon$")
    ax2.set_ylabel("MAE (counts)")
    ax2.set_title("Histogram count MAE vs $\\varepsilon$")
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    out = os.path.join(FIG_DIR, "fig_baseline.png")
    plt.savefig(out, dpi=config.get("dpi", 150))
    plt.close()
    print(f"Saved {out}")


if __name__ == "__main__":
    main()
