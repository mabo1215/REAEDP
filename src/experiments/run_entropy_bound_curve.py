"""
Entropy sensitivity bound (Theorem 4): plot Delta_H bound vs dataset size n.
Saves fig6.png to paper/figs/ for the paper.
"""
import sys
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from reaedp.entropy import entropy_sensitivity_bound
from project_paths import PAPER_FIG_DIR

FIG_DIR = str(PAPER_FIG_DIR)


def main(config=None):
    config = config or {}
    n_vals = config.get("n_vals", [50, 100, 200, 500, 1000, 2000, 5000])
    n_vals = np.array(n_vals)
    bounds = [entropy_sensitivity_bound(int(n)) for n in n_vals]

    os.makedirs(FIG_DIR, exist_ok=True)
    plt.figure(figsize=(5, 3.5))
    plt.semilogx(n_vals, bounds, "o-", color="C0")
    plt.xlabel("Dataset size $n$")
    plt.ylabel("$\\Delta_H$ bound (Theorem 4)")
    plt.title("Entropy sensitivity bound: $\\Delta_H \\leq \\frac{1}{n}(2 + \\frac{1}{\\ln 2} + 2\\log_2 n)$")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    out = os.path.join(FIG_DIR, "fig6.png")
    plt.savefig(out, dpi=config.get("dpi", 150))
    plt.close()
    print(f"Saved {out}")


if __name__ == "__main__":
    main()
