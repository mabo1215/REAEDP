"""Spectral private mean release for Wiener-type functional data."""
import numpy as np
from typing import Optional


def wiener_kernel_covariance(t: np.ndarray) -> np.ndarray:
    """Wiener covariance K(s,t)=min(s,t) on a discretized grid."""
    s = np.asarray(t).reshape(-1, 1)
    u = np.asarray(t).reshape(1, -1)
    return np.minimum(s, u)


def wiener_kl_basis(t: np.ndarray, rank: int) -> tuple[np.ndarray, np.ndarray]:
    """Return the first KL eigenfunctions and eigenvalues of the Wiener kernel."""
    t = np.asarray(t).reshape(-1)
    basis = []
    eigvals = []
    for idx in range(1, rank + 1):
        freq = (idx - 0.5) * np.pi
        basis.append(np.sqrt(2.0) * np.sin(freq * t))
        eigvals.append(1.0 / (freq ** 2))
    return np.column_stack(basis), np.asarray(eigvals, dtype=float)


def project_onto_wiener_basis(t: np.ndarray, curves: np.ndarray, rank: int) -> np.ndarray:
    """Project curves onto the first rank Wiener KL basis functions."""
    basis, _ = wiener_kl_basis(t, rank)
    dt = np.gradient(np.asarray(t).reshape(-1))
    weighted_basis = basis * dt[:, None]
    return np.asarray(curves) @ weighted_basis


def reconstruct_from_wiener_basis(t: np.ndarray, coeffs: np.ndarray) -> np.ndarray:
    """Reconstruct a curve from Wiener KL coefficients."""
    basis, _ = wiener_kl_basis(t, coeffs.shape[-1])
    return np.asarray(coeffs) @ basis.T


def _clip_curve_coefficients(coeffs: np.ndarray, clip_norm: float) -> np.ndarray:
    norms = np.linalg.norm(coeffs, axis=1, keepdims=True)
    scales = np.minimum(1.0, clip_norm / np.maximum(norms, 1e-12))
    return coeffs * scales


def gaussian_mean_release_parameters(
    t: np.ndarray,
    X: np.ndarray,
    epsilon: float,
    delta: float,
    rank: int = 8,
    clip_norm: Optional[float] = None,
) -> dict:
    """Return release metadata for the spectral Gaussian mean mechanism."""
    X = np.asarray(X)
    n = X.shape[0]
    coeffs = project_onto_wiener_basis(t, X, rank=rank)
    if clip_norm is None:
        clip_norm = float(np.quantile(np.linalg.norm(coeffs, axis=1), 0.9))
        clip_norm = max(clip_norm, 1e-6)
    clipped = _clip_curve_coefficients(coeffs, clip_norm=clip_norm)
    sensitivity = 2.0 * clip_norm / max(n, 1)
    sigma = sensitivity * np.sqrt(2 * np.log(1.25 / max(delta, 1e-12))) / max(epsilon, 1e-10)
    mean_coeffs = clipped.mean(axis=0)
    return {
        "sensitivity": float(sensitivity),
        "sigma": float(sigma),
        "n_paths": int(n),
        "rank": int(rank),
        "clip_norm": float(clip_norm),
        "mean_coeff_norm": float(np.linalg.norm(mean_coeffs)),
        "epsilon": float(epsilon),
        "delta": float(delta),
    }


def private_rkhs_mean(
    t: np.ndarray,
    X: np.ndarray,
    epsilon: float,
    delta: float,
    rank: int = 8,
    clip_norm: Optional[float] = None,
    rng: Optional[np.random.Generator] = None,
) -> np.ndarray:
    """Release a private mean curve via truncated Wiener KL coefficients."""
    rng = rng or np.random.default_rng()
    X = np.asarray(X)
    metadata = gaussian_mean_release_parameters(
        t, X, epsilon, delta, rank=rank, clip_norm=clip_norm
    )
    coeffs = project_onto_wiener_basis(t, X, rank=rank)
    clipped = _clip_curve_coefficients(coeffs, clip_norm=metadata["clip_norm"])
    mean_coeffs = clipped.mean(axis=0)
    noisy_coeffs = mean_coeffs + rng.normal(0.0, metadata["sigma"], size=mean_coeffs.shape)
    return reconstruct_from_wiener_basis(t, noisy_coeffs)


def generate_drifted_wiener_process(
    n_paths: int,
    t: np.ndarray,
    rng: Optional[np.random.Generator] = None,
) -> np.ndarray:
    """Generate Brownian-motion-like paths with a smooth deterministic drift."""
    rng = rng or np.random.default_rng()
    t = np.asarray(t).reshape(-1)
    n_t = len(t)
    dB = rng.standard_normal((n_paths, n_t)) * np.sqrt(np.diff(np.r_[0.0, t]))
    B = np.cumsum(dB, axis=1)
    drift = 0.35 * np.sin(np.pi * t) + 0.6 * t
    return drift[None, :] + 0.45 * B


def generate_chi_square_process(
    n_paths: int,
    t: np.ndarray,
    rng: Optional[np.random.Generator] = None,
) -> np.ndarray:
    """Backward-compatible alias used by older experiment code."""
    return generate_drifted_wiener_process(n_paths=n_paths, t=t, rng=rng)
