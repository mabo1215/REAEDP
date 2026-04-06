"""
Entropy and sensitivity (Theorem 4 in main.tex).
Shannon entropy H(z), Rényi entropy H_alpha(z), and sensitivity bound Delta_H.
"""
import numpy as np


def shannon_entropy(counts: np.ndarray) -> float:
    """
    Shannon entropy H(z) = log2(n) - (1/n) * sum_i c_i log2(c_i).
    counts: histogram (c_1, ..., c_m), shape (m,).
    """
    counts = np.asarray(counts, dtype=float)
    n = counts.sum()
    if n <= 0:
        return 0.0
    p = counts / n
    with np.errstate(divide="ignore", invalid="ignore"):
        terms = np.where(p > 0, p * np.log2(p), 0.0)
    return -terms.sum()


def renyi_entropy(counts: np.ndarray, alpha: float) -> float:
    """
    Rényi entropy of order alpha: H_alpha(z) = 1/(1-alpha) * log2( sum_i (c_i/n)^alpha ).
    When alpha -> 1, converges to Shannon entropy.
    """
    counts = np.asarray(counts, dtype=float)
    n = counts.sum()
    if n <= 0:
        return 0.0
    if abs(alpha - 1.0) < 1e-10:
        return shannon_entropy(counts)
    p = counts / n
    s = (p ** alpha).sum()
    if s <= 0:
        return 0.0
    return np.log2(s) / (1.0 - alpha)


def entropy_sensitivity_bound(n: int) -> float:
    """
    Theorem 4: For adjacent datasets of size n, sensitivity of H satisfies
    Delta_H <= (1/n) * (2 + 1/ln(2) + 2*log2(n)).
    """
    import math
    return (2.0 + 1.0 / math.log(2) + 2.0 * math.log2(max(n, 1))) / max(n, 1)


def sensitivity_entropy_adjacent(counts: np.ndarray, j1: int, j2: int) -> float:
    """
    |H(z) - H(z')| when z' differs from z by +1 at j1 and -1 at j2 (adjacent histograms).
    """
    c = np.asarray(counts, dtype=float).copy()
    n = c.sum()
    if n <= 0:
        return 0.0
    h0 = shannon_entropy(c)
    c[j1] += 1
    c[j2] -= 1
    if c[j2] < 0:
        return np.nan
    h1 = shannon_entropy(c)
    return abs(h0 - h1)
