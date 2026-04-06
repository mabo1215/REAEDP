"""
Image-based DP noise: load images, add Laplace/Gaussian noise for privacy testing.
Pixel values treated as bounded (e.g. 0--255); sensitivity is set by pixel range.
"""
import os
import numpy as np
from typing import Tuple, List, Optional

from .dp_mechanisms import laplace_mechanism, gaussian_mechanism


def load_image(path: str) -> np.ndarray:
    """Load image as numpy array (H, W) or (H, W, C), float in [0, 255]."""
    try:
        from PIL import Image
    except ImportError:
        raise ImportError("Pillow is required for image loading: pip install Pillow")
    img = Image.open(path)
    arr = np.asarray(img)
    if arr.ndim == 2:
        return arr.astype(np.float64)
    return arr.astype(np.float64)


def save_image(arr: np.ndarray, path: str) -> None:
    """Save array as image; values clipped to [0, 255]."""
    try:
        from PIL import Image
    except ImportError:
        raise ImportError("Pillow is required for image saving: pip install Pillow")
    arr = np.clip(np.round(arr), 0, 255).astype(np.uint8)
    Image.fromarray(arr).save(path)


def add_laplace_noise_to_image(
    image: np.ndarray,
    epsilon: float,
    pixel_sensitivity: float = 255.0,
    rng: Optional[np.random.Generator] = None,
) -> np.ndarray:
    """
    Add Laplace noise to every pixel for epsilon-DP (delta=0).
    L1 sensitivity per pixel is pixel_sensitivity (default 255 for one pixel change).
    """
    noisy = laplace_mechanism(image, sensitivity=pixel_sensitivity, epsilon=epsilon, rng=rng)
    return np.clip(noisy, 0, 255)


def add_gaussian_noise_to_image(
    image: np.ndarray,
    epsilon: float,
    delta: float,
    pixel_sensitivity_l2: float = 255.0,
    rng: Optional[np.random.Generator] = None,
) -> np.ndarray:
    """
    Add Gaussian noise to every pixel for (epsilon, delta)-DP.
    L2 sensitivity per pixel is pixel_sensitivity_l2 (default 255).
    """
    noisy = gaussian_mechanism(
        image,
        sensitivity_l2=pixel_sensitivity_l2,
        epsilon=epsilon,
        delta=delta,
        rng=rng,
    )
    return np.clip(noisy, 0, 255)


def image_psnr(original: np.ndarray, noisy: np.ndarray) -> float:
    """Peak signal-to-noise ratio (dB). Higher is closer to original."""
    mse = np.mean((original - noisy) ** 2)
    if mse <= 0:
        return float("inf")
    max_val = 255.0
    return 10 * np.log10(max_val ** 2 / mse)


def image_mae(original: np.ndarray, noisy: np.ndarray) -> float:
    """Mean absolute error per pixel."""
    return float(np.mean(np.abs(original - noisy)))


def image_ssim_simple(original: np.ndarray, noisy: np.ndarray) -> float:
    """
    Global SSIM-like metric (single scale): luminance and contrast comparison.
    Returns value in [0, 1]; higher is closer to original. No extra dependency.
    """
    if original.shape != noisy.shape:
        return 0.0
    if original.ndim > 2:
        original = original[:, :, 0]
        noisy = noisy[:, :, 0]
    o = np.asarray(original, dtype=np.float64).ravel()
    n = np.asarray(noisy, dtype=np.float64).ravel()
    C1, C2 = 6.5025, 58.5225
    mu_o, mu_n = np.mean(o), np.mean(n)
    var_o = np.var(o)
    var_n = np.var(n)
    cov = np.mean((o - mu_o) * (n - mu_n))
    ssim = ((2 * mu_o * mu_n + C1) * (2 * cov + C2)) / (
        (mu_o ** 2 + mu_n ** 2 + C1) * (var_o + var_n + C2)
    )
    return float(np.clip(ssim, 0, 1))


def create_demo_image(size: Tuple[int, int] = (64, 64)) -> np.ndarray:
    """Create a small synthetic image for demo (e.g. epsilon sweep)."""
    h, w = size
    y = np.linspace(0, 1, h).reshape(-1, 1)
    x = np.linspace(0, 1, w).reshape(1, -1)
    img = 255 * (0.5 + 0.3 * np.sin(4 * np.pi * x) * np.cos(2 * np.pi * y))
    return np.clip(img, 0, 255).astype(np.float64)


def list_images(directory: str, extensions: Tuple[str, ...] = (".png", ".jpg", ".jpeg", ".bmp")) -> List[str]:
    """List image file paths in a directory."""
    paths = []
    for name in os.listdir(directory):
        if name.lower().endswith(extensions):
            paths.append(os.path.join(directory, name))
    return sorted(paths)
