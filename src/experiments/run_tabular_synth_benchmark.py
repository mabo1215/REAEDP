"""Tabular synthetic-data benchmark with attribute inference and DP Gaussian copula."""

import os
import sys

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from reaedp.tabular_synthesizers import (
    fit_dp_gaussian_copula_discrete,
    privatize_discrete_marginals,
    sample_dp_gaussian_copula,
    sample_independent_synthetic,
)
from project_paths import DATA_DIR, PAPER_FIG_DIR, resolve_workspace_path

FIG_DIR = str(PAPER_FIG_DIR)


def _qcut_codes(series: pd.Series, q: int) -> pd.Series:
    ranked = series.astype(float).rank(method="first")
    return pd.qcut(ranked, q=q, labels=False, duplicates="drop").astype(int)


def prepare_home_credit(
    df: pd.DataFrame,
) -> tuple[pd.DataFrame, list[str], list[int], list[str], list[str]]:
    frame = df.copy()
    frame = frame[frame["CODE_GENDER"].isin(["F", "M"])]
    frame = frame.dropna(
        subset=[
            "TARGET",
            "CODE_GENDER",
            "FLAG_OWN_CAR",
            "FLAG_OWN_REALTY",
            "CNT_CHILDREN",
            "DAYS_BIRTH",
            "AMT_CREDIT",
            "AMT_ANNUITY",
            "AMT_INCOME_TOTAL",
        ]
    )
    frame = frame.iloc[:30000].copy()

    prepared = pd.DataFrame()
    prepared["gender"] = frame["CODE_GENDER"].map({"F": 0, "M": 1}).astype(int)
    prepared["own_car"] = frame["FLAG_OWN_CAR"].map({"N": 0, "Y": 1}).astype(int)
    prepared["own_realty"] = frame["FLAG_OWN_REALTY"].map({"N": 0, "Y": 1}).astype(int)
    prepared["children_bin"] = np.clip(frame["CNT_CHILDREN"].astype(int), 0, 3)
    ages = (-frame["DAYS_BIRTH"].astype(float) / 365.25).clip(18, 70)
    prepared["age_bin"] = pd.cut(
        ages,
        bins=[18, 30, 40, 50, 60, 71],
        labels=False,
        include_lowest=True,
        right=False,
    ).astype(int)
    prepared["credit_bin"] = _qcut_codes(frame["AMT_CREDIT"].clip(0, 4_500_000), q=5)
    prepared["annuity_bin"] = _qcut_codes(frame["AMT_ANNUITY"].clip(0, 300_000), q=5)
    prepared["income_bin"] = _qcut_codes(frame["AMT_INCOME_TOTAL"].clip(25_000, 1_200_000), q=4)
    prepared["target"] = frame["TARGET"].astype(int)

    columns = list(prepared.columns)
    domain_sizes = [int(prepared[col].max()) + 1 for col in columns]
    feature_cols = [
        "gender",
        "own_car",
        "own_realty",
        "children_bin",
        "age_bin",
        "credit_bin",
        "annuity_bin",
    ]
    task_cols = ["income_bin", "target"]
    return prepared.reset_index(drop=True), columns, domain_sizes, feature_cols, task_cols


def average_marginal_tv(real_data: np.ndarray, synth_data: np.ndarray, domain_sizes: list[int]) -> float:
    scores = []
    for idx, domain in enumerate(domain_sizes):
        p_real = np.bincount(real_data[:, idx], minlength=domain).astype(float)
        p_real /= max(p_real.sum(), 1.0)
        p_syn = np.bincount(synth_data[:, idx], minlength=domain).astype(float)
        p_syn /= max(p_syn.sum(), 1.0)
        scores.append(0.5 * np.abs(p_real - p_syn).sum())
    return float(np.mean(scores))


def average_pairwise_corr_error(real_data: np.ndarray, synth_data: np.ndarray) -> float:
    corr_real = np.corrcoef(real_data.T)
    corr_syn = np.corrcoef(synth_data.T)
    tri = np.triu_indices_from(corr_real, k=1)
    return float(np.mean(np.abs(corr_real[tri] - corr_syn[tri])))


def train_logistic_auc(train_df: pd.DataFrame, test_df: pd.DataFrame, feature_cols: list[str], label_col: str) -> float:
    from sklearn.compose import ColumnTransformer
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import roc_auc_score
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import OneHotEncoder

    if train_df[label_col].nunique() < 2:
        return 0.5

    model = Pipeline(
        [
            (
                "preprocess",
                ColumnTransformer(
                    [("cat", OneHotEncoder(handle_unknown="ignore"), feature_cols)]
                ),
            ),
            ("clf", LogisticRegression(max_iter=1000)),
        ]
    )
    model.fit(train_df[feature_cols], train_df[label_col])
    probs = model.predict_proba(test_df[feature_cols])[:, 1]
    if test_df[label_col].nunique() < 2:
        return 0.5
    return float(roc_auc_score(test_df[label_col], probs))


def train_attribute_inference(
    train_df: pd.DataFrame,
    test_df: pd.DataFrame,
    feature_cols: list[str],
    label_col: str,
) -> tuple[float, float]:
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import accuracy_score, f1_score

    clf = RandomForestClassifier(n_estimators=300, random_state=42, min_samples_leaf=2)
    clf.fit(train_df[feature_cols], train_df[label_col])
    pred = clf.predict(test_df[feature_cols])
    return float(accuracy_score(test_df[label_col], pred)), float(
        f1_score(test_df[label_col], pred, average="macro")
    )


def partial_record_inference_accuracy(
    reference_df: pd.DataFrame,
    target_df: pd.DataFrame,
    known_cols: list[str],
    hidden_col: str,
) -> float:
    reference_known = reference_df[known_cols].to_numpy(dtype=int)
    reference_hidden = reference_df[hidden_col].to_numpy(dtype=int)
    ref_patterns, ref_inverse = np.unique(reference_known, axis=0, return_inverse=True)
    hidden_domain = int(max(reference_hidden.max(), target_df[hidden_col].max())) + 1
    ref_hidden_counts = np.zeros((len(ref_patterns), hidden_domain), dtype=int)
    for idx, hidden in zip(ref_inverse, reference_hidden):
        ref_hidden_counts[idx, int(hidden)] += 1

    target_known = target_df[known_cols].to_numpy(dtype=int)
    target_patterns, target_inverse = np.unique(target_known, axis=0, return_inverse=True)
    pattern_predictions = np.zeros(len(target_patterns), dtype=int)
    for pattern_idx, pattern in enumerate(target_patterns):
        matches = np.all(ref_patterns == pattern, axis=1)
        candidate_counts = ref_hidden_counts[matches]
        if candidate_counts.size == 0:
            distances = (ref_patterns != pattern).sum(axis=1)
            nearest = np.flatnonzero(distances == distances.min())
            candidate_counts = ref_hidden_counts[nearest]
        pattern_predictions[pattern_idx] = int(candidate_counts.sum(axis=0).argmax())

    predictions = pattern_predictions[target_inverse]
    truth = target_df[hidden_col].to_numpy(dtype=int)
    return float((np.asarray(predictions) == truth).mean())


def linkage_target_accuracy(
    reference_df: pd.DataFrame,
    target_df: pd.DataFrame,
    known_cols: list[str],
    hidden_col: str,
) -> float:
    reference_known = reference_df[known_cols].to_numpy(dtype=int)
    reference_hidden = reference_df[hidden_col].to_numpy(dtype=int)
    ref_patterns, ref_inverse = np.unique(reference_known, axis=0, return_inverse=True)
    hidden_domain = int(max(reference_hidden.max(), target_df[hidden_col].max())) + 1
    ref_hidden_counts = np.zeros((len(ref_patterns), hidden_domain), dtype=int)
    for idx, hidden in zip(ref_inverse, reference_hidden):
        ref_hidden_counts[idx, int(hidden)] += 1

    target_known = target_df[known_cols].to_numpy(dtype=int)
    target_patterns, target_inverse = np.unique(target_known, axis=0, return_inverse=True)
    pattern_predictions = np.zeros(len(target_patterns), dtype=int)
    for pattern_idx, pattern in enumerate(target_patterns):
        distances = (ref_patterns != pattern).sum(axis=1)
        nearest = np.flatnonzero(distances == distances.min())
        pattern_predictions[pattern_idx] = int(ref_hidden_counts[nearest].sum(axis=0).argmax())

    predictions = pattern_predictions[target_inverse]
    truth = target_df[hidden_col].to_numpy(dtype=int)
    return float((np.asarray(predictions) == truth).mean())


def summarize_runs(values: list[float]) -> tuple[float, float]:
    arr = np.asarray(values, dtype=float)
    mean = float(arr.mean())
    ci = float(1.96 * arr.std(ddof=0) / np.sqrt(len(arr))) if len(arr) > 1 else 0.0
    return mean, ci


def main(config=None):
    config = config or {}
    csv_path = str(
        resolve_workspace_path(
            config.get("input") or str(DATA_DIR / "home-credit-application-train.csv")
        )
    )
    df = pd.read_csv(csv_path, nrows=config.get("max_rows", 50000))
    prepared, columns, domain_sizes, feature_cols, _ = prepare_home_credit(df)

    shuffled = prepared.sample(frac=1.0, random_state=config.get("seed", 42)).reset_index(drop=True)
    split = int(len(shuffled) * 0.8)
    train_df = shuffled.iloc[:split].reset_index(drop=True)
    test_df = shuffled.iloc[split:].reset_index(drop=True)
    train_data = train_df[columns].to_numpy(dtype=int)

    epsilons = np.asarray(config.get("epsilons", [0.5, 1.0, 2.0, 4.0]), dtype=float)
    delta = float(config.get("delta", 1e-5))
    n_runs = int(config.get("n_runs", 8))

    real_target_auc = train_logistic_auc(train_df, test_df, feature_cols + ["income_bin"], "target")
    real_attr_acc, real_attr_f1 = train_attribute_inference(train_df, test_df, feature_cols, "income_bin")
    partial_known_cols = ["gender", "own_car", "own_realty", "children_bin", "age_bin"]
    linkage_known_cols = feature_cols
    real_partial_acc = partial_record_inference_accuracy(train_df, test_df, partial_known_cols, "income_bin")
    real_linkage_acc = linkage_target_accuracy(train_df, test_df, linkage_known_cols, "income_bin")

    methods = {
        "independent": lambda data, eps, local_rng: sample_independent_synthetic(
            privatize_discrete_marginals(data, domain_sizes, eps, local_rng),
            len(data),
            local_rng,
        ),
        "gaussian_copula": lambda data, eps, local_rng: sample_dp_gaussian_copula(
            fit_dp_gaussian_copula_discrete(data, domain_sizes, eps, delta, local_rng),
            len(data),
            local_rng,
        ),
    }

    rows = []
    for eps in epsilons:
        for method_name, sampler in methods.items():
            metric_runs = {
                "marginal_tv": [],
                "pairwise_corr_error": [],
                "target_auc": [],
                "attribute_acc": [],
                "attribute_macro_f1": [],
                "partial_income_acc": [],
                "linkage_income_acc": [],
            }
            for run_idx in range(n_runs):
                local_rng = np.random.default_rng(
                    config.get("seed", 42) + 1000 * run_idx + int(100 * eps)
                )
                synth_data = sampler(train_data, eps, local_rng)
                synth_df = pd.DataFrame(synth_data, columns=columns)
                metric_runs["marginal_tv"].append(
                    average_marginal_tv(train_data, synth_data, domain_sizes)
                )
                metric_runs["pairwise_corr_error"].append(
                    average_pairwise_corr_error(train_data, synth_data)
                )
                metric_runs["target_auc"].append(
                    train_logistic_auc(synth_df, test_df, feature_cols + ["income_bin"], "target")
                )
                attr_acc, attr_f1 = train_attribute_inference(
                    synth_df, test_df, feature_cols, "income_bin"
                )
                metric_runs["attribute_acc"].append(attr_acc)
                metric_runs["attribute_macro_f1"].append(attr_f1)
                metric_runs["partial_income_acc"].append(
                    partial_record_inference_accuracy(
                        synth_df,
                        test_df,
                        partial_known_cols,
                        "income_bin",
                    )
                )
                metric_runs["linkage_income_acc"].append(
                    linkage_target_accuracy(
                        synth_df,
                        test_df,
                        linkage_known_cols,
                        "income_bin",
                    )
                )

            row = {"epsilon": float(eps), "method": method_name}
            for key, values in metric_runs.items():
                mean, ci = summarize_runs(values)
                row[key] = mean
                row[f"{key}_ci95"] = ci
            rows.append(row)

    results_df = pd.DataFrame(rows)
    results_df["real_target_auc"] = real_target_auc
    results_df["real_attribute_acc"] = real_attr_acc
    results_df["real_attribute_macro_f1"] = real_attr_f1
    results_df["real_partial_income_acc"] = real_partial_acc
    results_df["real_linkage_income_acc"] = real_linkage_acc

    out_csv = str(
        resolve_workspace_path(config.get("out_csv") or str(DATA_DIR / "tabular_synth_results.csv"))
    )
    os.makedirs(os.path.dirname(out_csv) or ".", exist_ok=True)
    results_df.to_csv(out_csv, index=False)
    print(f"Saved {out_csv}")

    os.makedirs(FIG_DIR, exist_ok=True)
    fig, axes = plt.subplots(2, 3, figsize=(10.0, 5.8))
    styles = {
        "independent": ("C1", "s-", "Independent marginals"),
        "gaussian_copula": ("C0", "o-", "DP Gaussian copula"),
    }
    for method_name, group in results_df.groupby("method"):
        color, fmt, label = styles[method_name]
        axes[0, 0].errorbar(
            group["epsilon"],
            group["marginal_tv"],
            yerr=group["marginal_tv_ci95"],
            fmt=fmt,
            color=color,
            capsize=3,
            label=label,
        )
        axes[0, 1].errorbar(
            group["epsilon"],
            group["pairwise_corr_error"],
            yerr=group["pairwise_corr_error_ci95"],
            fmt=fmt,
            color=color,
            capsize=3,
            label=label,
        )
        axes[1, 0].errorbar(
            group["epsilon"],
            group["target_auc"],
            yerr=group["target_auc_ci95"],
            fmt=fmt,
            color=color,
            capsize=3,
            label=label,
        )
        axes[1, 1].errorbar(
            group["epsilon"],
            group["attribute_acc"],
            yerr=group["attribute_acc_ci95"],
            fmt=fmt,
            color=color,
            capsize=3,
            label=label,
        )
        axes[1, 2].errorbar(
            group["epsilon"],
            group["partial_income_acc"],
            yerr=group["partial_income_acc_ci95"],
            fmt=fmt,
            color=color,
            capsize=3,
            label=label,
        )
        axes[0, 2].errorbar(
            group["epsilon"],
            group["linkage_income_acc"],
            yerr=group["linkage_income_acc_ci95"],
            fmt=fmt,
            color=color,
            capsize=3,
            label=label,
        )

    axes[0, 0].set_title("Marginal TV vs $\\varepsilon$")
    axes[0, 0].set_ylabel("Average TV")
    axes[0, 1].set_title("Dependence Error vs $\\varepsilon$")
    axes[0, 1].set_ylabel("Average |corr error|")
    axes[0, 2].set_title("Linkage Inference vs $\\varepsilon$")
    axes[0, 2].set_ylabel("Income accuracy")
    axes[1, 0].set_title("Downstream AUC vs $\\varepsilon$")
    axes[1, 0].set_ylabel("AUC on real holdout")
    axes[1, 1].set_title("Attribute Inference vs $\\varepsilon$")
    axes[1, 1].set_ylabel("Attack accuracy")
    axes[1, 2].set_title("Partial-Record Inference vs $\\varepsilon$")
    axes[1, 2].set_ylabel("Income accuracy")

    for ax in axes.ravel():
        ax.set_xlabel("$\\varepsilon$")
        ax.grid(True, alpha=0.3)

    axes[1, 0].axhline(
        real_target_auc,
        color="black",
        linestyle="--",
        linewidth=1.0,
        label="Real-train upper bound",
    )
    axes[1, 1].axhline(
        real_attr_acc,
        color="black",
        linestyle="--",
        linewidth=1.0,
        label="Real-train upper bound",
    )
    axes[1, 2].axhline(
        real_partial_acc,
        color="black",
        linestyle="--",
        linewidth=1.0,
        label="Real-train upper bound",
    )
    axes[0, 2].axhline(
        real_linkage_acc,
        color="black",
        linestyle="--",
        linewidth=1.0,
        label="Real-train upper bound",
    )
    axes[1, 1].axhline(0.25, color="gray", linestyle=":", linewidth=1.0, label="Random guess")
    axes[0, 0].legend(fontsize=7)
    axes[0, 2].legend(fontsize=7)
    axes[1, 0].legend(fontsize=7)
    axes[1, 1].legend(fontsize=7)
    axes[1, 2].legend(fontsize=7)

    plt.tight_layout()
    out_fig = os.path.join(FIG_DIR, config.get("out_fig", "fig_tabular_synth.png"))
    plt.savefig(out_fig, dpi=config.get("dpi", 150))
    plt.close()
    print(f"Saved {out_fig}")


if __name__ == "__main__":
    main()