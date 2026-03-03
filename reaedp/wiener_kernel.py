"""
Wiener kernel / RKHS private mean (Figures 2--4 in main.tex).
K(x,.) = sum_i lambda_i psi_i(x) phi_i(.). Private release with penalty parameter rho.
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
    Returns private mean curve at t.
    """
    rng = rng or np.random.default_rng()
    X = np.asarray(X)
    mean_curve = X.mean(axis=0)
    n = X.shape[0]
    if sensitivity is None:
        rad = np.abs(X).max()
        sensitivity = 2 * rad / max(n, 1)
    sigma = sensitivity * np.sqrt(2 * np.log(1.25 / max(delta, 1e-12))) / max(epsilon, 1e-10)
    noise = rng.normal(0, sigma, mean_curve.shape)
    return mean_curve + noise


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
