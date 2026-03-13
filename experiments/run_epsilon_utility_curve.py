"""
Privacy–utility tradeoff: PSNR and MAE vs epsilon for Laplace and Gaussian image noise.
Saves fig5.png to paper/fig/ for the paper.
"""
import sys
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from reaedp.image_noise import (
    add_laplace_noise_to_image,
    add_gaussian_noise_to_image,
    image_psnr,
    image_mae,
    create_demo_image,
)

ROOT = os.path.join(os.path.dirname(__file__), "..")
FIG_DIR = os.path.join(ROOT, "paper", "fig")


def main(config=None):
    config = config or {}
    seed = config.get("seed", 42)
    rng = np.random.default_rng(seed)
    delta = config.get("delta", 1e-5)
    epsilons = np.array(config.get("epsilons", [0.1, 0.25, 0.5, 1.0, 2.0, 4.0]))
    n_trials = config.get("n_trials", 5)

    img = create_demo_image((64, 64))
    psnr_laplace, psnr_gaussian = [], []
    mae_laplace, mae_gaussian = [], []

    for eps in epsilons:
        p_l, p_g = [], []
        m_l, m_g = [], []
        for _ in range(n_trials):
            lap = add_laplace_noise_to_image(img, eps, rng=rng)
            gau = add_gaussian_noise_to_image(img, eps, delta, rng=rng)
            p_l.append(image_psnr(img, lap))
            p_g.append(image_psnr(img, gau))
            m_l.append(image_mae(img, lap))
            m_g.append(image_mae(img, gau))
        psnr_laplace.append(np.mean(p_l))
        psnr_gaussian.append(np.mean(p_g))
        mae_laplace.append(np.mean(m_l))
        mae_gaussian.append(np.mean(m_g))

    os.makedirs(FIG_DIR, exist_ok=True)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3.5))

    ax1.plot(epsilons, psnr_laplace, "o-", label="Laplace", color="C0")
    ax1.plot(epsilons, psnr_gaussian, "s-", label="Gaussian", color="C1")
    ax1.set_xlabel("$\\varepsilon$")
    ax1.set_ylabel("PSNR (dB)")
    ax1.set_title("Utility: PSNR vs privacy parameter $\\varepsilon$")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    ax2.plot(epsilons, mae_laplace, "o-", label="Laplace", color="C0")
    ax2.plot(epsilons, mae_gaussian, "s-", label="Gaussian", color="C1")
    ax2.set_xlabel("$\\varepsilon$")
    ax2.set_ylabel("MAE")
    ax2.set_title("Utility: MAE vs privacy parameter $\\varepsilon$")
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    out = os.path.join(FIG_DIR, "fig5.png")
    plt.savefig(out, dpi=config.get("dpi", 150))
    plt.close()
    print(f"Saved {out}")


if __name__ == "__main__":
    main()
