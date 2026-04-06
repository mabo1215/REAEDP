"""
Membership inference attack (MIA) evaluation on DP histogram release.
Adversary sees one release M(D) or M(D') with D' = D \\cup {x}; guess which.
Features: entropy of release, total count; classifier: logistic regression.
Report: accuracy and AUC vs epsilon, with mean and 95%% CI over repeated runs.
Linkage-style attack: guess D vs D' by which reference release is closer (L2).
Output: paper/figs/fig_mia.png, data/mia_results.csv
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
from project_paths import DATA_DIR, PAPER_FIG_DIR, resolve_workspace_path

FIG_DIR = str(PAPER_FIG_DIR)


def run_one_mia(eps: float, rng: np.random.Generator, n_trials: int, bins: int,
                counts_base: np.ndarray, seed: int) -> tuple:
    """Single run: train LR on (release features, 0/1), return accuracy and AUC."""
    def release(D_counts: np.ndarray, eps_val: float, rng_inner):
        noisy = laplace_mechanism(D_counts.astype(float), sensitivity=1.0, epsilon=eps_val, rng=rng_inner)
        noisy = np.maximum(noisy, 0)
        h = shannon_entropy(noisy)
        total = noisy.sum()
        return np.array([h, total]), noisy

    X_list, y_list = [], []
    for _ in range(n_trials):
        idx_rm = rng.integers(0, bins)
        idx_add = rng.integers(0, bins)
        cD = counts_base.copy().astype(float)
        cD[idx_rm] = max(0, cD[idx_rm] - 1)
        cDp = counts_base.copy().astype(float)
        cDp[idx_add] += 1
        fD, _ = release(cD, eps, rng)
        fDp, _ = release(cDp, eps, rng)
        X_list.append(fD)
        y_list.append(0)
        X_list.append(fDp)
        y_list.append(1)
    X = np.array(X_list)
    y_label = np.array(y_list)
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import roc_auc_score
    clf = LogisticRegression(max_iter=500, random_state=seed)
    clf.fit(X, y_label)
    acc = clf.score(X, y_label)
    try:
        auc = roc_auc_score(y_label, clf.decision_function(X))
    except Exception:
        auc = 0.5
    return acc, auc


def linkage_attack_accuracy(eps: float, rng: np.random.Generator, n_trials: int, bins: int,
                            counts_base: np.ndarray) -> float:
    """
    Linkage-style: for each trial, release from D and D'; draw one release at random.
    Attacker sees the release and the two noised histograms (D and D'); guesses D if
    L2(release, release_D) < L2(release, release_D').
    """
    def release_vec(D_counts: np.ndarray, eps_val: float, rng_inner):
        noisy = laplace_mechanism(D_counts.astype(float), sensitivity=1.0, epsilon=eps_val, rng=rng_inner)
        return np.maximum(noisy, 0)

    correct = 0
    for _ in range(n_trials):
        idx_rm = rng.integers(0, bins)
        idx_add = rng.integers(0, bins)
        cD = counts_base.copy().astype(float)
        cD[idx_rm] = max(0, cD[idx_rm] - 1)
        cDp = counts_base.copy().astype(float)
        cDp[idx_add] += 1
        rel_D = release_vec(cD, eps, rng)
        rel_Dp = release_vec(cDp, eps, rng)
        if rng.random() < 0.5:
            observed, true_label = rel_D, 0
        else:
            observed, true_label = rel_Dp, 1
        dist_D = np.linalg.norm(observed - rel_D)
        dist_Dp = np.linalg.norm(observed - rel_Dp)
        guess = 0 if dist_D <= dist_Dp else 1
        if guess == true_label:
            correct += 1
    return correct / n_trials


def main(config=None):
    config = config or {}
    seed = config.get("seed", 42)
    rng = np.random.default_rng(seed)
    epsilons = np.array(config.get("epsilons", [0.5, 1.0, 2.0, 4.0, 8.0]))
    n_trials = config.get("n_trials", 200)
    n_runs = config.get("n_runs", 5)
    bins = config.get("bins", 30)
    max_rows = config.get("max_rows", 10000)
    csv_path = config.get("input") or str(DATA_DIR / "house-prices-train.csv")
    column = config.get("column", "SalePrice")
    csv_path = str(resolve_workspace_path(csv_path))

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
    counts_base, bin_edges = np.histogram(y, bins=bins)

    acc_means, acc_stds, auc_means, auc_stds = [], [], [], []
    linkage_accs = []
    for eps in epsilons:
        accs, aucs = [], []
        for run in range(n_runs):
            a, u = run_one_mia(eps, rng, n_trials, bins, counts_base, seed + run)
            accs.append(a)
            aucs.append(u)
        acc_means.append(np.mean(accs))
        acc_stds.append(1.96 * np.std(accs) / np.sqrt(n_runs) if n_runs > 1 else 0)
        auc_means.append(np.mean(aucs))
        auc_stds.append(1.96 * np.std(aucs) / np.sqrt(n_runs) if n_runs > 1 else 0)
        link_acc = linkage_attack_accuracy(eps, rng, min(200, n_trials), bins, counts_base)
        linkage_accs.append(link_acc)

    acc_means = np.array(acc_means)
    acc_stds = np.array(acc_stds)
    auc_means = np.array(auc_means)
    auc_stds = np.array(auc_stds)
    linkage_accs = np.array(linkage_accs)

    os.makedirs(DATA_DIR, exist_ok=True)
    res_df = pd.DataFrame({
        "epsilon": epsilons,
        "MIA_accuracy_mean": acc_means, "MIA_accuracy_ci95": acc_stds,
        "MIA_AUC_mean": auc_means, "MIA_AUC_ci95": auc_stds,
        "linkage_accuracy": linkage_accs,
    })
    res_df.to_csv(os.path.join(DATA_DIR, "mia_results.csv"), index=False)
    print(f"Saved {os.path.join(str(DATA_DIR), 'mia_results.csv')}")

    os.makedirs(FIG_DIR, exist_ok=True)
    fig, ax = plt.subplots(figsize=(5, 3.5))
    ax.errorbar(epsilons, acc_means, yerr=acc_stds, fmt="o-", color="C0", capsize=3, label="MIA accuracy")
    ax.plot(epsilons, auc_means, "s-", color="C1", label="MIA AUC")
    ax.plot(epsilons, linkage_accs, "^-", color="C2", alpha=0.8, label="Linkage-style accuracy")
    ax.axhline(0.5, color="gray", linestyle="--", label="Random guess")
    ax.set_xlabel("$\\varepsilon$")
    ax.set_ylabel("Accuracy / AUC")
    ax.set_title("Privacy evaluation: MIA and linkage-style attack on DP histogram")
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
