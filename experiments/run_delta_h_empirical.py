"""
Empirical entropy sensitivity: estimate Delta_H_hat = max_{D~D'} |H(D)-H(D')|
over adjacent histogram pairs (replacement adjacency) and compare to theoretical bound.
Small-scale, controlled synthetic experiment for Theorem 4 alignment.
Output: paper/fig/fig_delta_h_empirical.png, data/delta_h_empirical.csv
"""
import sys
import os
import numpy as np
import math
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from reaedp.entropy import shannon_entropy, entropy_sensitivity_bound

ROOT = os.path.join(os.path.dirname(__file__), "..")
FIG_DIR = os.path.join(ROOT, "paper", "fig")
DATA_DIR = os.path.join(ROOT, "data")


def empirical_delta_h(counts: np.ndarray, rng: np.random.Generator, n_samples: int = 5000) -> float:
    """
    Over adjacent pairs (replacement: +1 at j1, -1 at j2), compute |H(D)-H(D')|;
    return max (empirical Delta_H_hat). counts must sum to n; at least two bins with count >= 1.
    """
    counts = np.asarray(counts, dtype=int)
    n = int(counts.sum())
    m = len(counts)
    if n <= 0 or m < 2:
        return 0.0
    max_dh = 0.0
    # Exhaustive when m and n are small; otherwise random sample
    if m * (m - 1) <= n_samples:
        for j1 in range(m):
            for j2 in range(m):
                if j1 == j2:
                    continue
                if counts[j2] < 1:
                    continue
                c = counts.copy().astype(float)
                h0 = shannon_entropy(c)
                c[j1] += 1
                c[j2] -= 1
                h1 = shannon_entropy(c)
                max_dh = max(max_dh, abs(h0 - h1))
    else:
        for _ in range(n_samples):
            j1, j2 = rng.integers(0, m), rng.integers(0, m)
            if j1 == j2 or counts[j2] < 1:
                continue
            c = counts.copy().astype(float)
            h0 = shannon_entropy(c)
            c[j1] += 1
            c[j2] -= 1
            h1 = shannon_entropy(c)
            max_dh = max(max_dh, abs(h0 - h1))
    return max_dh


def main(config=None):
    config = config or {}
    seed = config.get("seed", 42)
    rng = np.random.default_rng(seed)
    n_vals = config.get("n_vals", [50, 100, 200, 500, 1000])
    m_vals = config.get("m_vals", [10, 20, 30])
    n_trials_per_nm = config.get("n_trials_per_nm", 5)
    n_samples_adj = config.get("n_samples_adj", 5000)

    rows = []
    for n in n_vals:
        for m in m_vals:
            if m > n:
                continue
            bound = entropy_sensitivity_bound(n)
            emp_list = []
            for _ in range(n_trials_per_nm):
                # Random histogram with n records, m bins (multinomial)
                p = rng.dirichlet(np.ones(m))
                counts = rng.multinomial(n, p)
                if counts.max() == 0 or (counts >= 1).sum() < 2:
                    continue
                dh = empirical_delta_h(counts, rng, n_samples=n_samples_adj)
                emp_list.append(dh)
            if not emp_list:
                continue
            mean_emp = np.mean(emp_list)
            max_emp = np.max(emp_list)
            ratio = mean_emp / bound if bound > 0 else 0
            rows.append({
                "n": n, "m": m,
                "Delta_H_hat_mean": mean_emp, "Delta_H_hat_max": max_emp,
                "Delta_H_bound": bound, "ratio_mean_over_bound": ratio,
            })

    df = pd.DataFrame(rows)
    os.makedirs(DATA_DIR, exist_ok=True)
    csv_path = os.path.join(DATA_DIR, "delta_h_empirical.csv")
    df.to_csv(csv_path, index=False)
    print(f"Saved {csv_path}")

    os.makedirs(FIG_DIR, exist_ok=True)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3.5))
    # Left: Delta_H_hat and bound vs n (aggregate over m)
    if not df.empty:
        by_n = df.groupby("n").agg({"Delta_H_hat_mean": "mean", "Delta_H_hat_max": "max", "Delta_H_bound": "first"})
        x = by_n.index
        ax1.plot(x, by_n["Delta_H_bound"], "k--", label="$\\Delta_H$ bound (Th.4)")
        ax1.plot(x, by_n["Delta_H_hat_mean"], "o-", color="C0", label="$\\widehat{\\Delta H}$ mean")
        ax1.plot(x, by_n["Delta_H_hat_max"], "s--", color="C0", alpha=0.7, label="$\\widehat{\\Delta H}$ max")
        ax1.set_xlabel("$n$")
        ax1.set_ylabel("Sensitivity")
        ax1.set_title("Empirical $\\widehat{\\Delta H}$ vs bound")
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        ax1.set_xscale("log")
        # Right: ratio
        ax2.bar(range(len(x)), by_n["Delta_H_hat_mean"] / by_n["Delta_H_bound"], color="C0", alpha=0.8)
        ax2.set_xticks(range(len(x)))
        ax2.set_xticklabels([str(int(v)) for v in x])
        ax2.axhline(1.0, color="gray", linestyle="--")
        ax2.set_xlabel("$n$")
        ax2.set_ylabel("$\\widehat{\\Delta H}$ / $\\Delta_H$ bound")
        ax2.set_title("Ratio (mean); $<1$ = empirical below bound")
    plt.tight_layout()
    out = os.path.join(FIG_DIR, "fig_delta_h_empirical.png")
    plt.savefig(out, dpi=config.get("dpi", 150))
    plt.close()
    print(f"Saved {out}")


if __name__ == "__main__":
    main()
