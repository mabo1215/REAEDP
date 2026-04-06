"""
Baseline comparison: Laplace, Gaussian, and DP synthetic (Laplace/Gaussian + multinomial sample).
Utility: entropy preservation error |H_orig - H_noisy| and count MAE.
Output: paper/figs/fig_baseline.png
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
from project_paths import DATA_DIR, PAPER_FIG_DIR, resolve_workspace_path

FIG_DIR = str(PAPER_FIG_DIR)


def dp_synthetic_laplace(counts: np.ndarray, n: int, eps: float, rng: np.random.Generator) -> np.ndarray:
    """DP synthetic baseline: Laplace noise on counts, normalize, then multinomial(n, p) sample."""
    noisy = laplace_mechanism(counts.astype(float), sensitivity=1.0, epsilon=eps, rng=rng)
    noisy = np.maximum(noisy, 1e-9)
    p = noisy / noisy.sum()
    return rng.multinomial(n, p).astype(float)


def dp_synthetic_gaussian(counts: np.ndarray, n: int, eps: float, delta: float, rng: np.random.Generator) -> np.ndarray:
    """DP synthetic baseline: Gaussian noise on counts, normalize, then multinomial(n, p) sample."""
    noisy = gaussian_mechanism(counts.astype(float), sensitivity_l2=np.sqrt(2), epsilon=eps, delta=delta, rng=rng)
    noisy = np.maximum(noisy, 1e-9)
    p = noisy / noisy.sum()
    return rng.multinomial(n, p).astype(float)


def main(config=None):
    config = config or {}
    seed = config.get("seed", 42)
    rng = np.random.default_rng(seed)
    epsilons = np.array(config.get("epsilons", [0.25, 0.5, 1.0, 2.0, 4.0]))
    delta = config.get("delta", 1e-5)
    n_trials = config.get("n_trials", 10)
    bins = config.get("bins", 30)
    max_rows = config.get("max_rows", 50000)
    csv_path = config.get("input") or str(DATA_DIR / "y_amazon-google-large.csv")
    column = config.get("column", "y")
    csv_path = str(resolve_workspace_path(csv_path))

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

    err_entropy_lap, err_entropy_gau = [], []
    err_entropy_synth_lap, err_entropy_synth_gau = [], []
    mae_lap, mae_gau = [], []
    mae_synth_lap, mae_synth_gau = [], []

    for eps in epsilons:
        e_l, e_g, e_sl, e_sg = [], [], [], []
        m_l, m_g, m_sl, m_sg = [], [], [], []
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
            # DP synthetic baselines: noisy counts -> multinomial sample
            syn_l = dp_synthetic_laplace(counts, n, eps, rng)
            syn_g = dp_synthetic_gaussian(counts, n, eps, delta, rng)
            H_sl = shannon_entropy(syn_l)
            H_sg = shannon_entropy(syn_g)
            e_sl.append(abs(H_orig - H_sl))
            e_sg.append(abs(H_orig - H_sg))
            m_sl.append(np.abs(syn_l - counts).mean())
            m_sg.append(np.abs(syn_g - counts).mean())
        err_entropy_lap.append(np.mean(e_l))
        err_entropy_gau.append(np.mean(e_g))
        err_entropy_synth_lap.append(np.mean(e_sl))
        err_entropy_synth_gau.append(np.mean(e_sg))
        mae_lap.append(np.mean(m_l))
        mae_gau.append(np.mean(m_g))
        mae_synth_lap.append(np.mean(m_sl))
        mae_synth_gau.append(np.mean(m_sg))

    os.makedirs(FIG_DIR, exist_ok=True)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3.5))
    ax1.plot(epsilons, err_entropy_lap, "o-", label="Laplace", color="C0")
    ax1.plot(epsilons, err_entropy_gau, "s-", label="Gaussian", color="C1")
    ax1.plot(epsilons, err_entropy_synth_lap, "^-", label="DP synthetic (Laplace)", color="C2")
    ax1.plot(epsilons, err_entropy_synth_gau, "v-", label="DP synthetic (Gaussian)", color="C3")
    ax1.axhline(bound_H, color="gray", linestyle="--", label="$\\Delta_H$ bound (Th.4)")
    ax1.set_xlabel("$\\varepsilon$")
    ax1.set_ylabel("$|H_{\\mathrm{orig}} - H_{\\mathrm{noisy}}|$")
    ax1.set_title("Entropy preservation vs $\\varepsilon$")
    ax1.legend(fontsize=7)
    ax1.grid(True, alpha=0.3)

    ax2.plot(epsilons, mae_lap, "o-", label="Laplace", color="C0")
    ax2.plot(epsilons, mae_gau, "s-", label="Gaussian", color="C1")
    ax2.plot(epsilons, mae_synth_lap, "^-", label="DP synthetic (Laplace)", color="C2")
    ax2.plot(epsilons, mae_synth_gau, "v-", label="DP synthetic (Gaussian)", color="C3")
    ax2.set_xlabel("$\\varepsilon$")
    ax2.set_ylabel("MAE (counts)")
    ax2.set_title("Histogram count MAE vs $\\varepsilon$")
    ax2.legend(fontsize=7)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    out = os.path.join(FIG_DIR, "fig_baseline.png")
    plt.savefig(out, dpi=config.get("dpi", 150))
    plt.close()
    print(f"Saved {out}")


if __name__ == "__main__":
    main()
