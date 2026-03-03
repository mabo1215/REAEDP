"""
Reproduce Figures 2--4: original vs private RKHS mean for different penalty rho.
"""
import sys
import os
import argparse
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from reaedp.wiener_kernel import generate_chi_square_process, private_rkhs_mean

ROOT = os.path.join(os.path.dirname(__file__), "..")
FIG_DIR = os.path.join(ROOT, "latex", "fig")


def main(config=None):
    if config is None:
        parser = argparse.ArgumentParser(description="Wiener kernel figures (fig2–fig4)")
        parser.add_argument("--out_csv", type=str, default="", help="Optional: save curves to CSV")
        args = parser.parse_args()
        config = {"out_csv": args.out_csv}

    out_csv = config.get("out_csv", "")
    seed = config.get("seed", 42)
    rng = np.random.default_rng(seed)
    t = np.linspace(0, 1, config.get("n_t", 80))
    n_paths = config.get("n_paths", 50)
    X = generate_chi_square_process(n_paths, t, rng=rng)
    epsilon, delta = config.get("epsilon", 1.0), config.get("delta", 1e-5)
    original_mean = X.mean(axis=0)

    rows = []
    os.makedirs(FIG_DIR, exist_ok=True)
    for rho, fig_name in [(1e-6, "fig2"), (0.001, "fig3"), (0.1, "fig4")]:
        private_mean = private_rkhs_mean(t, X, epsilon, delta, rho=rho, rng=rng)
        rows.append((rho, original_mean, private_mean))
        plt.figure(figsize=(5, 3))
        plt.plot(t, original_mean, label="Original mean", color="C0")
        plt.plot(t, private_mean, label="Private mean", color="C1", alpha=0.8)
        plt.xlabel("Time $t$")
        plt.ylabel("$X_i(t)$ (Chi-square)")
        plt.title(f"Penalty $\\rho$ = {rho}")
        plt.legend()
        plt.tight_layout()
        out = os.path.join(FIG_DIR, f"{fig_name}.png")
        plt.savefig(out, dpi=config.get("dpi", 150))
        plt.close()
        print(f"Saved {out}")

    if out_csv:
        os.makedirs(os.path.dirname(out_csv) or ".", exist_ok=True)
        with open(out_csv, "w") as f:
            f.write("rho,index,t,original_mean,private_mean\n")
            for rho, orig, priv in rows:
                for i in range(len(t)):
                    f.write(f"{rho},{i},{t[i]:.6f},{orig[i]:.6f},{priv[i]:.6f}\n")
        print(f"Wrote {out_csv}")


if __name__ == "__main__":
    main()
