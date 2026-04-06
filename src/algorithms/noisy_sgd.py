"""
Noisy Stochastic Gradient Descent (Equation 1 in main.tex):
  argmin_{GD} { E_{x~P_r}[log D(x)] + N(0, eta^2 G^2 I) }
Gradient descent with Gaussian noise on updates for differential privacy.
"""
import numpy as np
from typing import Callable, Optional


class NoisySGD:
    """
    Noisy-SGD: at each step, take a stochastic gradient and add N(0, eta^2 * G^2 * I).
    """

    def __init__(
        self,
        theta: np.ndarray,
        eta: float,
        G: float,
        gradient_fn: Callable[[np.ndarray], np.ndarray],
        rng: Optional[np.random.Generator] = None,
    ):
        self.theta = np.asarray(theta, dtype=float).copy()
        self.eta = eta
        self.G = G
        self.gradient_fn = gradient_fn
        self.rng = rng or np.random.default_rng()

    def step(self) -> np.ndarray:
        """One noisy gradient descent step."""
        g = self.gradient_fn(self.theta)
        noise_scale = self.eta * self.G
        noise = self.rng.normal(0, noise_scale, self.theta.shape)
        self.theta = self.theta - self.eta * (g + noise)
        return self.theta.copy()

    @property
    def params(self) -> np.ndarray:
        return self.theta.copy()


def noisy_sgd_step(
    theta: np.ndarray,
    gradient: np.ndarray,
    eta: float,
    G: float,
    rng: Optional[np.random.Generator] = None,
) -> np.ndarray:
    """
    Single step: theta_new = theta - eta * (gradient + N(0, eta*G)^2 * I).
    Convention: gradient is the current derivative (e.g. from E[log D(x)]).
    """
    rng = rng or np.random.default_rng()
    noise = rng.normal(0, eta * G, theta.shape)
    return theta - eta * (gradient + noise)
