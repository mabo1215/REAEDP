"""Reproduce Figures 2--4 and a supplementary summary for the Wiener experiment."""
import sys
import os
import argparse
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from reaedp.wiener_kernel import (
    generate_chi_square_process,
    private_rkhs_mean,
    gaussian_mean_release_parameters,
)
from project_paths import DATA_DIR, PAPER_FIG_DIR, resolve_workspace_path

FIG_DIR = str(PAPER_FIG_DIR)


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
    summary_rows = []
    os.makedirs(FIG_DIR, exist_ok=True)
    rho_pairs = config.get("rho_figures", [(1e-6, "fig2"), (0.001, "fig3"), (0.1, "fig4")])
    for rho, fig_name in rho_pairs:
        params = gaussian_mean_release_parameters(t, X, epsilon, delta, rho=rho)
        private_mean = private_rkhs_mean(t, X, epsilon, delta, rho=rho, rng=rng)
        rows.append((rho, original_mean, private_mean))
        rmse = float(np.sqrt(np.mean((private_mean - original_mean) ** 2)))
        mae = float(np.mean(np.abs(private_mean - original_mean)))
        summary_rows.append({
            "rho": rho,
            "epsilon": epsilon,
            "delta": delta,
            "operator_norm": params["operator_norm"],
            "sensitivity": params["sensitivity"],
            "sigma": params["sigma"],
            "rmse": rmse,
            "mae": mae,
        })
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

    summary_df = None
    if summary_rows:
        summary_df = np.array([])
        import pandas as pd
        summary_df = pd.DataFrame(summary_rows)
        summary_csv = config.get("summary_csv", str(DATA_DIR / "wiener_summary.csv"))
        summary_csv = str(resolve_workspace_path(summary_csv))
        os.makedirs(os.path.dirname(summary_csv) or ".", exist_ok=True)
        summary_df.to_csv(summary_csv, index=False)
        print(f"Saved {summary_csv}")

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3.5))
        ax1.plot(summary_df["rho"], summary_df["rmse"], "o-", label="RMSE", color="C0")
        ax1.plot(summary_df["rho"], summary_df["mae"], "s-", label="MAE", color="C1")
        ax1.set_xscale("log")
        ax1.set_xlabel("$\\rho$")
        ax1.set_ylabel("Utility error")
        ax1.set_title("Wiener utility vs regularization")
        ax1.grid(True, alpha=0.3)
        ax1.legend(fontsize=8)

        ax2.plot(summary_df["rho"], summary_df["sensitivity"], "o-", label="L2 sensitivity", color="C2")
        ax2.plot(summary_df["rho"], summary_df["sigma"], "^-", label="Gaussian $\\sigma$", color="C3")
        ax2.set_xscale("log")
        ax2.set_xlabel("$\\rho$")
        ax2.set_ylabel("Mechanism parameter")
        ax2.set_title("Gaussian mechanism parameters")
        ax2.grid(True, alpha=0.3)
        ax2.legend(fontsize=8)

        plt.tight_layout()
        out_summary_fig = os.path.join(FIG_DIR, config.get("summary_fig", "fig8.png"))
        plt.savefig(out_summary_fig, dpi=config.get("dpi", 150))
        plt.close()
        print(f"Saved {out_summary_fig}")

    if out_csv:
        out_csv = str(resolve_workspace_path(out_csv))
        os.makedirs(os.path.dirname(out_csv) or ".", exist_ok=True)
        with open(out_csv, "w") as f:
            f.write("rho,index,t,original_mean,private_mean\n")
            for rho, orig, priv in rows:
                for i in range(len(t)):
                    f.write(f"{rho},{i},{t[i]:.6f},{orig[i]:.6f},{priv[i]:.6f}\n")
        print(f"Wrote {out_csv}")


if __name__ == "__main__":
    main()
