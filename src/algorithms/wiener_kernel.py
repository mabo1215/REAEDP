"""
Wiener kernel / RKHS-inspired private mean release for discretized trajectories.

The implementation uses a Wiener-kernel smoothing operator together with a
Gaussian mechanism on the smoothed mean curve. The regularization parameter
rho affects both smoothing bias and the sensitivity/noise scale through the
linear release operator.
"""
import numpy as np
from typing import Optional


def wiener_kernel_covariance(t: np.ndarray, rho: float = 1e-6) -> np.ndarray:
    """
    Approximate Wiener kernel on [0,1]: K(s,t) = min(s,t) (Brownian motion covariance).
    With penalty rho, regularized kernel is used for private mean.
    """
    s = np.asarray(t).reshape(-1, 1)
    t = np.asarray(t).reshape(1, -1)
    K = np.minimum(s, t)
    n = K.shape[0]
    K_reg = K + rho * np.eye(n)
    return K_reg


def wiener_smoothing_operator(t: np.ndarray, rho: float = 1e-6) -> np.ndarray:
    """Kernel-ridge-type smoothing operator S = K (K + rho I)^{-1}."""
    s = np.asarray(t).reshape(-1)
    K = np.minimum.outer(s, s)
    n = K.shape[0]
    return K @ np.linalg.inv(K + rho * np.eye(n))


def gaussian_mean_release_parameters(
    t: np.ndarray,
    X: np.ndarray,
    epsilon: float,
    delta: float,
    rho: float = 1e-6,
    sensitivity: Optional[float] = None,
) -> dict:
    """Return release metadata for the smoothed-mean Gaussian mechanism."""
    X = np.asarray(X)
    n = X.shape[0]
    S = wiener_smoothing_operator(t, rho=rho)
    operator_norm = float(np.linalg.norm(S, ord=2))
    if sensitivity is None:
        rad = float(np.abs(X).max())
        sensitivity = operator_norm * 2 * rad / max(n, 1)
    sigma = sensitivity * np.sqrt(2 * np.log(1.25 / max(delta, 1e-12))) / max(epsilon, 1e-10)
    return {
        "operator_norm": operator_norm,
        "sensitivity": float(sensitivity),
        "sigma": float(sigma),
        "n_paths": int(n),
        "rho": float(rho),
        "epsilon": float(epsilon),
        "delta": float(delta),
    }


def private_rkhs_mean(
    t: np.ndarray,
    X: np.ndarray,
    epsilon: float,
    delta: float,
    rho: float = 1e-6,
    sensitivity: Optional[float] = None,
    rng: Optional[np.random.Generator] = None,
) -> np.ndarray:
    """
    Compute empirical mean in RKHS (Wiener kernel) and add Gaussian DP noise.
    X: shape (n_samples, n_times) - observed trajectories at times t.
    Returns private smoothed mean curve at t.
    """
    rng = rng or np.random.default_rng()
    X = np.asarray(X)
    mean_curve = X.mean(axis=0)
    S = wiener_smoothing_operator(t, rho=rho)
    smoothed_mean = S @ mean_curve
    metadata = gaussian_mean_release_parameters(
        t, X, epsilon, delta, rho=rho, sensitivity=sensitivity
    )
    noise = rng.normal(0, metadata["sigma"], mean_curve.shape)
    return smoothed_mean + noise


def generate_chi_square_process(
    n_paths: int,
    t: np.ndarray,
    rng: Optional[np.random.Generator] = None,
) -> np.ndarray:
    """
    Simulate Chi-square-like process (sum of squared Gaussians) for experiments.
    Returns shape (n_paths, len(t)).
    """
    rng = rng or np.random.default_rng()
    n_t = len(t)
    dB = rng.standard_normal((n_paths, n_t)) * np.sqrt(np.diff(np.r_[0, t], axis=0))
    B = np.cumsum(dB, axis=1)
    X = B ** 2
    return X
