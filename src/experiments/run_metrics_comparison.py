"""
Compare Laplace vs Gaussian mechanisms: PSNR, MAE, SSIM at several epsilon values.
Bar chart for paper (fig7.png).
"""
import sys
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from reaedp.image_noise import (
    create_demo_image,
    add_laplace_noise_to_image,
    add_gaussian_noise_to_image,
    image_psnr,
    image_mae,
    image_ssim_simple,
)
from project_paths import PAPER_FIG_DIR

FIG_DIR = str(PAPER_FIG_DIR)


def main(config=None):
    config = config or {}
    seed = config.get("seed", 42)
    rng = np.random.default_rng(seed)
    delta = config.get("delta", 1e-5)
    epsilons = config.get("epsilons", [0.5, 1.0, 2.0])
    img = create_demo_image((64, 64))

    laplace_psnr, laplace_mae, laplace_ssim = [], [], []
    gaussian_psnr, gaussian_mae, gaussian_ssim = [], [], []

    for eps in epsilons:
        lap = add_laplace_noise_to_image(img, eps, rng=rng)
        gau = add_gaussian_noise_to_image(img, eps, delta, rng=rng)
        laplace_psnr.append(image_psnr(img, lap))
        laplace_mae.append(image_mae(img, lap))
        laplace_ssim.append(image_ssim_simple(img, lap))
        gaussian_psnr.append(image_psnr(img, gau))
        gaussian_mae.append(image_mae(img, gau))
        gaussian_ssim.append(image_ssim_simple(img, gau))

    x = np.arange(len(epsilons))
    width = 0.35

    fig, axes = plt.subplots(1, 3, figsize=(9, 3.5))

    axes[0].bar(x - width / 2, laplace_psnr, width, label="Laplace", color="C0")
    axes[0].bar(x + width / 2, gaussian_psnr, width, label="Gaussian", color="C1")
    axes[0].set_ylabel("PSNR (dB)")
    axes[0].set_xticks(x)
    axes[0].set_xticklabels([str(e) for e in epsilons])
    axes[0].set_xlabel("$\\varepsilon$")
    axes[0].set_title("PSNR")
    axes[0].legend()

    axes[1].bar(x - width / 2, laplace_mae, width, label="Laplace", color="C0")
    axes[1].bar(x + width / 2, gaussian_mae, width, label="Gaussian", color="C1")
    axes[1].set_ylabel("MAE")
    axes[1].set_xticks(x)
    axes[1].set_xticklabels([str(e) for e in epsilons])
    axes[1].set_xlabel("$\\varepsilon$")
    axes[1].set_title("MAE")

    axes[2].bar(x - width / 2, laplace_ssim, width, label="Laplace", color="C0")
    axes[2].bar(x + width / 2, gaussian_ssim, width, label="Gaussian", color="C1")
    axes[2].set_ylabel("SSIM")
    axes[2].set_xticks(x)
    axes[2].set_xticklabels([str(e) for e in epsilons])
    axes[2].set_xlabel("$\\varepsilon$")
    axes[2].set_title("SSIM")

    plt.suptitle("Utility metrics: Laplace vs Gaussian mechanism")
    plt.tight_layout()
    os.makedirs(FIG_DIR, exist_ok=True)
    out = os.path.join(FIG_DIR, "fig7.png")
    plt.savefig(out, dpi=config.get("dpi", 150))
    plt.close()
    print(f"Saved {out}")


if __name__ == "__main__":
    main()
