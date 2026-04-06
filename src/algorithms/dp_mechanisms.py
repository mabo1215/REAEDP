"""
(epsilon, delta)-Differential privacy mechanisms (Laplace and Gaussian).
"""
import numpy as np


def laplace_mechanism(
    value: np.ndarray,
    sensitivity: float,
    epsilon: float,
    rng: np.random.Generator | None = None,
) -> np.ndarray:
    """
    Laplace mechanism: add Lap(sensitivity/epsilon) for epsilon-DP (delta=0).
    For 1-dimensional or L1 sensitivity.
    """
    rng = rng or np.random.default_rng()
    scale = sensitivity / max(epsilon, 1e-10)
    noise = rng.laplace(0, scale, value.shape)
    return value + noise


def gaussian_mechanism(
    value: np.ndarray,
    sensitivity_l2: float,
    epsilon: float,
    delta: float,
    rng: np.random.Generator | None = None,
) -> np.ndarray:
    """
    Gaussian mechanism for (epsilon, delta)-DP.
    Noise scale sigma such that 2*ln(1.25/delta) * (sensitivity^2/sigma^2) <= epsilon^2,
    e.g. sigma >= sensitivity * sqrt(2*ln(1.25/delta)) / epsilon.
    """
    rng = rng or np.random.default_rng()
    import math
    c = math.sqrt(2 * math.log(1.25 / max(delta, 1e-12)))
    sigma = sensitivity_l2 * c / max(epsilon, 1e-10)
    noise = rng.normal(0, sigma, value.shape)
    return value + noise
