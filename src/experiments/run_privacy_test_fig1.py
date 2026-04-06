"""
Simulate privacy test pass rate (Figure 1).
"""
import sys
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from project_paths import PAPER_FIG_DIR

FIG_DIR = str(PAPER_FIG_DIR)


def pass_test(k: int, t: int, gamma: float, rng: np.random.Generator) -> bool:
    eps0 = 0.1
    fail_prob = np.exp(-eps0 * max(k - t, 0)) * (1.0 / (1 + gamma))
    return rng.random() > fail_prob


def main(config=None):
    config = config or {}
    rng = np.random.default_rng(config.get("seed", 42))
    t = config.get("t", 2)
    max_check = config.get("max_check", 10000)
    k_vals = config.get("k_vals", [5, 10, 20, 50])
    gamma_vals = np.linspace(config.get("gamma_min", 1), config.get("gamma_max", 12), config.get("gamma_n", 10))
    results = np.zeros((len(k_vals), len(gamma_vals)))

    for i, k in enumerate(k_vals):
        for j, gamma in enumerate(gamma_vals):
            passed = sum(1 for _ in range(max_check) if pass_test(k, t, gamma, rng))
            results[i, j] = passed / max_check

    plt.figure(figsize=(5, 3))
    for i, k in enumerate(k_vals):
        plt.plot(gamma_vals, results[i], label=f"k={k}", marker="o", markersize=3)
    plt.xlabel("$\\gamma$")
    plt.ylabel("Fraction passing privacy test")
    plt.title("t=2, max_check=10000")
    plt.legend()
    plt.tight_layout()
    os.makedirs(FIG_DIR, exist_ok=True)
    out = os.path.join(FIG_DIR, "fig1.png")
    plt.savefig(out, dpi=config.get("dpi", 150))
    plt.close()
    print(f"Saved {out}")


if __name__ == "__main__":
    main()
