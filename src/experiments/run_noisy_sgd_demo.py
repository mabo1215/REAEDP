"""
Demo: Noisy-SGD (Equation 1) on a simple convex loss.
"""
import sys
import os
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from reaedp.noisy_sgd import NoisySGD


def main(config=None):
    config = config or {}
    b = np.array(config.get("target", [1.0, 2.0]))
    def gradient_fn(theta):
        return 2 * (theta - b)

    theta0 = np.zeros(2)
    eta = config.get("eta", 0.1)
    G = config.get("G", 1.0)
    steps = config.get("steps", 100)
    seed = config.get("seed", 42)
    sgd = NoisySGD(theta0, eta=eta, G=G, gradient_fn=gradient_fn, rng=np.random.default_rng(seed))
    for _ in range(steps):
        sgd.step()
    print("Noisy-SGD final theta:", sgd.params)
    print("Target b:", b)


if __name__ == "__main__":
    main()
