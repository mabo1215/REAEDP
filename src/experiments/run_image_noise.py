"""
Image-based noise testing: load images, add Laplace/Gaussian DP noise,
save noisy images and comparison figures. Supports single file, directory, or synthetic demo.
"""
import sys
import os
import argparse
from typing import Tuple
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from reaedp.image_noise import (
    load_image,
    save_image,
    list_images,
    add_laplace_noise_to_image,
    add_gaussian_noise_to_image,
    image_psnr,
    image_mae,
)
from project_paths import resolve_workspace_path


def create_demo_image(size: Tuple[int, int] = (64, 64)) -> np.ndarray:
    """Create a small synthetic image for demo when no input is given."""
    h, w = size
    y = np.linspace(0, 1, h).reshape(-1, 1)
    x = np.linspace(0, 1, w).reshape(1, -1)
    img = 255 * (0.5 + 0.3 * np.sin(4 * np.pi * x) * np.cos(2 * np.pi * y))
    return np.clip(img, 0, 255).astype(np.float64)


def main(config=None):
    if config is None:
        parser = argparse.ArgumentParser(description="Image DP noise test: add Laplace/Gaussian noise")
        parser.add_argument("--input", "-i", type=str, default="", help="Image file or directory of images")
        parser.add_argument("--output", "-o", type=str, default="data/image_noise", help="Output directory")
        parser.add_argument("--epsilon", type=float, default=1.0, help="Privacy parameter epsilon")
        parser.add_argument("--delta", type=float, default=1e-5, help="Privacy parameter delta (Gaussian only)")
        parser.add_argument("--mechanism", choices=["laplace", "gaussian", "both"], default="both")
        parser.add_argument("--out_csv", type=str, default="", help="Optional: save PSNR/MAE to CSV")
        parser.add_argument("--seed", type=int, default=42)
        args = parser.parse_args()
        config = {
            "input": args.input,
            "output": args.output,
            "epsilon": args.epsilon,
            "delta": args.delta,
            "mechanism": args.mechanism,
            "out_csv": args.out_csv,
            "seed": args.seed,
        }

    input_path = config.get("input", "")
    output_dir = str(resolve_workspace_path(config.get("output", "data/image_noise")))
    epsilon = config.get("epsilon", 1.0)
    delta = config.get("delta", 1e-5)
    mechanism = config.get("mechanism", "both")
    out_csv = config.get("out_csv", "")
    seed = config.get("seed", 42)

    rng = np.random.default_rng(seed)
    os.makedirs(output_dir, exist_ok=True)

    if input_path:
        input_path = str(resolve_workspace_path(input_path))

    if input_path and os.path.isfile(input_path):
        paths = [input_path]
    elif input_path and os.path.isdir(input_path):
        paths = list_images(input_path)
        if not paths:
            print(f"No images found in {input_path}, using demo image.")
            paths = []
    else:
        paths = []

    if not paths:
        print("Using synthetic demo image (use config 'input' for your own images).")
        demo = create_demo_image((64, 64))
        save_image(demo, os.path.join(output_dir, "demo_original.png"))
        images = [("demo", demo)]
    else:
        images = [(os.path.basename(p), load_image(p)) for p in paths]

    rows = []
    for name, img in images:
        base_name = os.path.splitext(name)[0]
        results = {"name": base_name, "epsilon": epsilon, "delta": delta}

        if mechanism in ("laplace", "both"):
            lap = add_laplace_noise_to_image(img, epsilon, rng=rng)
            save_image(lap, os.path.join(output_dir, f"{base_name}_laplace_eps{epsilon}.png"))
            results["psnr_laplace"] = image_psnr(img, lap)
            results["mae_laplace"] = image_mae(img, lap)

        if mechanism in ("gaussian", "both"):
            gau = add_gaussian_noise_to_image(img, epsilon, delta, rng=rng)
            save_image(gau, os.path.join(output_dir, f"{base_name}_gaussian_eps{epsilon}.png"))
            results["psnr_gaussian"] = image_psnr(img, gau)
            results["mae_gaussian"] = image_mae(img, gau)

        rows.append(results)

        if img.ndim == 2:
            disp = img
        else:
            disp = img[:, :, 0] if img.shape[2] >= 1 else img
        n_cols = 1 + (1 if mechanism in ("laplace", "both") else 0) + (1 if mechanism in ("gaussian", "both") else 0)
        fig, axes = plt.subplots(1, n_cols, figsize=(4 * n_cols, 4))
        if n_cols == 1:
            axes = [axes]
        idx = 0
        axes[idx].imshow(disp, cmap="gray", vmin=0, vmax=255)
        axes[idx].set_title("Original")
        axes[idx].axis("off")
        idx += 1
        if mechanism in ("laplace", "both"):
            axes[idx].imshow(lap if img.ndim == 2 else lap[:, :, 0], cmap="gray", vmin=0, vmax=255)
            axes[idx].set_title(f"Laplace $\\varepsilon$={epsilon}")
            axes[idx].axis("off")
            idx += 1
        if mechanism in ("gaussian", "both"):
            axes[idx].imshow(gau if img.ndim == 2 else gau[:, :, 0], cmap="gray", vmin=0, vmax=255)
            axes[idx].set_title(f"Gaussian $\\varepsilon$={epsilon}")
            axes[idx].axis("off")
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f"{base_name}_compare.png"), dpi=150)
        plt.close()
        print(f"Saved comparison figure: {base_name}_compare.png")

    for r in rows:
        print(r)

    if out_csv:
        out_csv = str(resolve_workspace_path(out_csv))
        os.makedirs(os.path.dirname(out_csv) or ".", exist_ok=True)
        headers = ["name", "epsilon", "delta", "psnr_laplace", "mae_laplace", "psnr_gaussian", "mae_gaussian"]
        with open(out_csv, "w") as f:
            f.write(",".join(headers) + "\n")
            for r in rows:
                def _str(v):
                    if hasattr(v, "item"):
                        return str(v.item())
                    return str(v)
                f.write(",".join(_str(r.get(h, "")) for h in headers) + "\n")
        print(f"Wrote {out_csv}")

    print(f"Outputs written to {output_dir}")


if __name__ == "__main__":
    main()
