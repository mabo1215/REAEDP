"""
Membership inference evaluation on DP histogram release.

We report stronger attacks than the original summary-feature logistic model:
1. summary-feature logistic regression,
2. histogram-feature random forest,
3. likelihood-ratio attack using the Laplace release model,
4. linkage-style nearest-reference attack.
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


def release_histogram(D_counts: np.ndarray, eps_val: float, rng_inner) -> np.ndarray:
    noisy = laplace_mechanism(D_counts.astype(float), sensitivity=1.0, epsilon=eps_val, rng=rng_inner)
    return np.maximum(noisy, 0.0)


def summary_features(noisy: np.ndarray) -> np.ndarray:
    total = float(noisy.sum())
    norm = noisy / max(total, 1e-12)
    support = float((noisy > 1e-9).mean())
    return np.array([
        shannon_entropy(noisy),
        total,
        float(noisy.mean()),
        float(noisy.std()),
        support,
        float(norm.max()),
    ])


def build_attack_dataset(eps: float, rng: np.random.Generator, n_samples: int, bins: int,
                        counts_base: np.ndarray):
    X_summary, X_hist, y_label, pairs = [], [], [], []
    for _ in range(n_samples):
        idx_rm = int(rng.integers(0, bins))
        idx_add = int(rng.integers(0, bins))
        cD = counts_base.copy().astype(float)
        cD[idx_rm] = max(0, cD[idx_rm] - 1)
        cDp = counts_base.copy().astype(float)
        cDp[idx_add] += 1
        label = int(rng.random() >= 0.5)
        source = cDp if label == 1 else cD
        noisy = release_histogram(source, eps, rng)
        total = max(float(noisy.sum()), 1e-12)
        X_summary.append(summary_features(noisy))
        X_hist.append(np.concatenate([noisy / total, summary_features(noisy)]))
        y_label.append(label)
        pairs.append((cD, cDp, noisy))
    return np.array(X_summary), np.array(X_hist), np.array(y_label), pairs


def run_one_mia(eps: float, rng: np.random.Generator, n_trials: int, bins: int,
                counts_base: np.ndarray, seed: int) -> dict:
    """Train/evaluate stronger attackers on independent train/test releases."""
    from sklearn.linear_model import LogisticRegression
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import roc_auc_score

    Xs_train, Xh_train, y_train, _ = build_attack_dataset(eps, rng, n_trials, bins, counts_base)
    Xs_test, Xh_test, y_test, pairs_test = build_attack_dataset(eps, rng, n_trials, bins, counts_base)

    lr = LogisticRegression(max_iter=1000, random_state=seed)
    lr.fit(Xs_train, y_train)
    lr_probs = lr.predict_proba(Xs_test)[:, 1]
    lr_pred = (lr_probs >= 0.5).astype(int)

    rf = RandomForestClassifier(n_estimators=300, random_state=seed, min_samples_leaf=2)
    rf.fit(Xh_train, y_train)
    rf_probs = rf.predict_proba(Xh_test)[:, 1]
    rf_pred = (rf_probs >= 0.5).astype(int)

    b = 1.0 / max(eps, 1e-10)
    lr_attack = []
    linkage_attack = []
    for y_true, (cD, cDp, noisy) in zip(y_test, pairs_test):
        ll_D = -np.abs(noisy - cD).sum() / b
        ll_Dp = -np.abs(noisy - cDp).sum() / b
        lr_attack.append(int(ll_Dp > ll_D))

        rel_D = release_histogram(cD, eps, rng)
        rel_Dp = release_histogram(cDp, eps, rng)
        dist_D = np.linalg.norm(noisy - rel_D)
        dist_Dp = np.linalg.norm(noisy - rel_Dp)
        linkage_attack.append(0 if dist_D <= dist_Dp else 1)

    return {
        "summary_lr_acc": float((lr_pred == y_test).mean()),
        "summary_lr_auc": float(roc_auc_score(y_test, lr_probs)) if len(np.unique(y_test)) > 1 else 0.5,
        "hist_rf_acc": float((rf_pred == y_test).mean()),
        "hist_rf_auc": float(roc_auc_score(y_test, rf_probs)) if len(np.unique(y_test)) > 1 else 0.5,
        "likelihood_acc": float((np.array(lr_attack) == y_test).mean()),
        "linkage_acc": float((np.array(linkage_attack) == y_test).mean()),
    }


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

    metrics = {
        "summary_lr_acc": [], "summary_lr_acc_ci95": [],
        "summary_lr_auc": [], "summary_lr_auc_ci95": [],
        "hist_rf_acc": [], "hist_rf_acc_ci95": [],
        "hist_rf_auc": [], "hist_rf_auc_ci95": [],
        "likelihood_acc": [], "likelihood_acc_ci95": [],
        "linkage_acc": [], "linkage_acc_ci95": [],
    }
    for eps in epsilons:
        run_stats = {k: [] for k in ["summary_lr_acc", "summary_lr_auc", "hist_rf_acc", "hist_rf_auc", "likelihood_acc", "linkage_acc"]}
        for run in range(n_runs):
            stats = run_one_mia(eps, rng, n_trials, bins, counts_base, seed + run)
            for key, value in stats.items():
                run_stats[key].append(value)
        for key, values in run_stats.items():
            values = np.array(values, dtype=float)
            metrics[key].append(float(values.mean()))
            metrics[f"{key}_ci95"].append(float(1.96 * values.std(ddof=0) / np.sqrt(n_runs)) if n_runs > 1 else 0.0)

    os.makedirs(DATA_DIR, exist_ok=True)
    res_df = pd.DataFrame({"epsilon": epsilons, **metrics})
    res_df.to_csv(os.path.join(DATA_DIR, "mia_results.csv"), index=False)
    print(f"Saved {os.path.join(str(DATA_DIR), 'mia_results.csv')}")

    os.makedirs(FIG_DIR, exist_ok=True)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.4, 3.5))
    ax1.errorbar(epsilons, metrics["summary_lr_acc"], yerr=metrics["summary_lr_acc_ci95"], fmt="o-", color="C0", capsize=3, label="Summary LR")
    ax1.errorbar(epsilons, metrics["hist_rf_acc"], yerr=metrics["hist_rf_acc_ci95"], fmt="s-", color="C1", capsize=3, label="Histogram RF")
    ax1.errorbar(epsilons, metrics["likelihood_acc"], yerr=metrics["likelihood_acc_ci95"], fmt="^-", color="C2", capsize=3, label="Likelihood ratio")
    ax1.errorbar(epsilons, metrics["linkage_acc"], yerr=metrics["linkage_acc_ci95"], fmt="d-", color="C3", capsize=3, label="Linkage-style")
    ax1.axhline(0.5, color="gray", linestyle="--", label="Random guess")
    ax1.set_xlabel("$\\varepsilon$")
    ax1.set_ylabel("Attack accuracy")
    ax1.set_title("Attack accuracy vs $\\varepsilon$")
    ax1.grid(True, alpha=0.3)
    ax1.legend(fontsize=7)
    ax1.set_ylim(0.45, 1.0)

    ax2.errorbar(epsilons, metrics["summary_lr_auc"], yerr=metrics["summary_lr_auc_ci95"], fmt="o-", color="C0", capsize=3, label="Summary LR AUC")
    ax2.errorbar(epsilons, metrics["hist_rf_auc"], yerr=metrics["hist_rf_auc_ci95"], fmt="s-", color="C1", capsize=3, label="Histogram RF AUC")
    ax2.axhline(0.5, color="gray", linestyle="--", label="Random guess")
    ax2.set_xlabel("$\\varepsilon$")
    ax2.set_ylabel("AUC")
    ax2.set_title("MIA AUC vs $\\varepsilon$")
    ax2.grid(True, alpha=0.3)
    ax2.legend(fontsize=7)
    ax2.set_ylim(0.45, 1.0)

    plt.tight_layout()
    out = os.path.join(FIG_DIR, "fig_mia.png")
    plt.savefig(out, dpi=config.get("dpi", 150))
    plt.close()
    print(f"Saved {out}")


if __name__ == "__main__":
    main()
