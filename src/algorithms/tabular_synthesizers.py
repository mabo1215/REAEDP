"""Discrete tabular DP synthesizers used in the paper benchmarks."""

from __future__ import annotations

from typing import Sequence

import numpy as np
from scipy.stats import norm

from .dp_mechanisms import gaussian_mechanism, laplace_mechanism


def _normalize_probs(values: np.ndarray) -> np.ndarray:
    values = np.maximum(values.astype(float), 1e-9)
    total = float(values.sum())
    if total <= 0:
        return np.full(len(values), 1.0 / max(len(values), 1), dtype=float)
    return values / total


def privatize_discrete_marginals(
    data: np.ndarray,
    domain_sizes: Sequence[int],
    epsilon: float,
    rng: np.random.Generator,
) -> list[np.ndarray]:
    """Release noisy marginal probabilities for discrete columns."""
    n_cols = data.shape[1]
    eps_per_col = epsilon / max(n_cols, 1)
    marginals: list[np.ndarray] = []
    for col_idx, domain_size in enumerate(domain_sizes):
        counts = np.bincount(data[:, col_idx], minlength=domain_size).astype(float)
        noisy = laplace_mechanism(counts, sensitivity=1.0, epsilon=eps_per_col, rng=rng)
        marginals.append(_normalize_probs(noisy))
    return marginals


def sample_independent_synthetic(
    marginals: Sequence[np.ndarray],
    n_rows: int,
    rng: np.random.Generator,
) -> np.ndarray:
    """Sample a synthetic table independently from private marginals."""
    columns = [rng.choice(len(probs), size=n_rows, p=probs) for probs in marginals]
    return np.column_stack(columns).astype(int)


def _latent_scores_from_probs(probs: np.ndarray) -> np.ndarray:
    edges = np.concatenate([[0.0], np.cumsum(probs)])
    mids = 0.5 * (edges[:-1] + edges[1:])
    mids = np.clip(mids, 1e-6, 1 - 1e-6)
    return norm.ppf(mids)


def _thresholds_from_probs(probs: np.ndarray) -> np.ndarray:
    cumulative = np.cumsum(probs[:-1])
    cumulative = np.clip(cumulative, 1e-6, 1 - 1e-6)
    return norm.ppf(cumulative)


def _nearest_psd(corr: np.ndarray) -> np.ndarray:
    corr = 0.5 * (corr + corr.T)
    eigvals, eigvecs = np.linalg.eigh(corr)
    eigvals = np.clip(eigvals, 1e-6, None)
    repaired = eigvecs @ np.diag(eigvals) @ eigvecs.T
    scale = np.sqrt(np.clip(np.diag(repaired), 1e-12, None))
    repaired = repaired / np.outer(scale, scale)
    np.fill_diagonal(repaired, 1.0)
    return repaired


def fit_dp_gaussian_copula_discrete(
    data: np.ndarray,
    domain_sizes: Sequence[int],
    epsilon: float,
    delta: float,
    rng: np.random.Generator,
    marginal_fraction: float = 0.45,
    row_clip_norm: float = 4.0,
) -> dict:
    """Fit a DP Gaussian copula over a discrete tabular dataset."""
    n_rows, n_cols = data.shape
    eps_marginals = max(epsilon * marginal_fraction, 1e-8)
    eps_corr = max(epsilon - eps_marginals, 1e-8)
    marginals = privatize_discrete_marginals(data, domain_sizes, eps_marginals, rng)

    latent_scores = [_latent_scores_from_probs(probs) for probs in marginals]
    thresholds = [_thresholds_from_probs(probs) for probs in marginals]
    latent = np.column_stack([
        latent_scores[col_idx][data[:, col_idx]] for col_idx in range(n_cols)
    ])
    latent = latent - latent.mean(axis=0, keepdims=True)
    row_norms = np.linalg.norm(latent, axis=1, keepdims=True)
    scales = np.minimum(1.0, row_clip_norm / np.maximum(row_norms, 1e-12))
    clipped = latent * scales
    second_moment = clipped.T @ clipped / max(n_rows, 1)

    sensitivity = 2.0 * (row_clip_norm ** 2) / max(n_rows, 1)
    noisy_second = gaussian_mechanism(
        second_moment,
        sensitivity_l2=sensitivity,
        epsilon=eps_corr,
        delta=delta,
        rng=rng,
    )
    noisy_second = 0.5 * (noisy_second + noisy_second.T)
    variances = np.clip(np.diag(noisy_second), 1e-6, None)
    corr = noisy_second / np.outer(np.sqrt(variances), np.sqrt(variances))
    corr = np.clip(corr, -0.98, 0.98)
    np.fill_diagonal(corr, 1.0)
    corr = _nearest_psd(corr)

    return {
        "marginals": marginals,
        "thresholds": thresholds,
        "correlation": corr,
        "row_clip_norm": float(row_clip_norm),
        "corr_sensitivity": float(sensitivity),
        "n_rows": int(n_rows),
        "epsilon": float(epsilon),
        "delta": float(delta),
    }


def sample_dp_gaussian_copula(model: dict, n_rows: int, rng: np.random.Generator) -> np.ndarray:
    """Sample from the DP Gaussian copula model returned by fit_dp_gaussian_copula_discrete."""
    corr = model["correlation"]
    samples = rng.multivariate_normal(np.zeros(corr.shape[0]), corr, size=n_rows)
    columns = []
    for col_idx, thresholds in enumerate(model["thresholds"]):
        columns.append(np.digitize(samples[:, col_idx], thresholds).astype(int))
    return np.column_stack(columns)