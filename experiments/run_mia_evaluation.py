"""
Membership inference attack (MIA) evaluation on DP histogram release.
Adversary sees one release M(D) or M(D') with D' = D \\cup {x}; guess which.
Feature: entropy of release, total count; classifier: logistic regression.
Report MIA accuracy vs epsilon (expect near 0.5 when DP is strong).
Output: paper/fig/fig_mia.png
"""
import sys
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from reaedp.entropy import shannon_entropy
from reaedp.dp_mechanisms import laplace_mechanism

ROOT = os.path.join(os.path.dirname(__file__), "..")
FIG_DIR = os.path.join(ROOT, "paper", "fig")
DATA_DIR = os.path.join(ROOT, "data")


def main(config=None):
    config = config or {}
    seed = config.get("seed", 42)
    rng = np.random.default_rng(seed)
    epsilons = np.array(config.get("epsilons", [0.5, 1.0, 2.0, 4.0, 8.0]))
    n_trials = config.get("n_trials", 200)
    bins = config.get("bins", 30)
    max_rows = config.get("max_rows", 10000)
    csv_path = config.get("input") or os.path.join(DATA_DIR, "house-prices-train.csv")
    column = config.get("column", "SalePrice")
    if not os.path.isabs(csv_path):
        csv_path = os.path.join(ROOT, csv_path)

    if not os.path.isfile(csv_path):
        print(f"CSV not found: {csv_path}. Skipping MIA.")
        return

    df = pd.read_csv(csv_path, nrows=max_rows)
    if column not in df.columns:
        col = df.columns[0]
        print(f"Using column {col} instead of {column}")
        column = col
    y = df[column].dropna().values.astype(float)
    n = min(len(y), 2000)
    y = y[:n]

    def release(D_counts: np.ndarray, eps: float, rng: np.random.Generator):
        noisy = laplace_mechanism(D_counts.astype(float), sensitivity=1.0, epsilon=eps, rng=rng)
        noisy = np.maximum(noisy, 0)
        h = shannon_entropy(noisy)
        total = noisy.sum()
        return np.array([h, total])

    accuracies = []
    for eps in epsilons:
        X_list, y_list = [], []
        counts_base, bin_edges = np.histogram(y, bins=bins)
        for _ in range(n_trials):
            # D: drop one random record; D': add one (so D' = D ∪ {x}); we simulate D vs D' by shifting one count
            idx_rm = rng.integers(0, bins)
            idx_add = rng.integers(0, bins)
            cD = counts_base.copy().astype(float)
            cD[idx_rm] = max(0, cD[idx_rm] - 1)
            cDp = counts_base.copy().astype(float)
            cDp[idx_add] += 1
            fD = release(cD, eps, rng)
            fDp = release(cDp, eps, rng)
            X_list.append(fD)
            y_list.append(0)
            X_list.append(fDp)
            y_list.append(1)
        X = np.array(X_list)
        y_label = np.array(y_list)
        from sklearn.linear_model import LogisticRegression
        clf = LogisticRegression(max_iter=500, random_state=seed)
        clf.fit(X, y_label)
        acc = clf.score(X, y_label)
        accuracies.append(acc)
    accuracies = np.array(accuracies)

    os.makedirs(FIG_DIR, exist_ok=True)
    fig, ax = plt.subplots(figsize=(5, 3.5))
    ax.plot(epsilons, accuracies, "o-", color="C0", label="MIA accuracy")
    ax.axhline(0.5, color="gray", linestyle="--", label="Random guess")
    ax.set_xlabel("$\\varepsilon$")
    ax.set_ylabel("Membership inference accuracy")
    ax.set_title("Privacy evaluation: MIA on DP histogram release")
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0.45, 1.0)
    plt.tight_layout()
    out = os.path.join(FIG_DIR, "fig_mia.png")
    plt.savefig(out, dpi=config.get("dpi", 150))
    plt.close()
    print(f"Saved {out}")


if __name__ == "__main__":
    main()
