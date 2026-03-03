"""
Verify Theorem 4: entropy sensitivity bound.
"""
import sys
import os
import argparse
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from reaedp.entropy import shannon_entropy, entropy_sensitivity_bound, sensitivity_entropy_adjacent


def main(config=None):
    if config is None:
        parser = argparse.ArgumentParser(description="Entropy sensitivity experiment")
        parser.add_argument("--out_csv", type=str, default="", help="Optional: save results to CSV")
        args = parser.parse_args()
        config = {"out_csv": args.out_csv}

    out_csv = config.get("out_csv", "")
    np.random.seed(42)
    n = config.get("n", 100)
    m = config.get("m", 10)
    bound = entropy_sensitivity_bound(n)
    print(f"n={n}, bound Delta_H <= {bound:.6f}")

    max_delta = 0
    for _ in range(config.get("n_trials", 500)):
        counts = np.random.dirichlet(np.ones(m)) * n
        counts = np.maximum(np.round(counts).astype(int), 0)
        counts[0] += n - counts.sum()
        if counts.sum() != n or counts.min() < 0:
            continue
        for j1 in range(m):
            for j2 in range(m):
                if j1 == j2 or counts[j2] < 1:
                    continue
                d = sensitivity_entropy_adjacent(counts, j1, j2)
                if not np.isnan(d):
                    max_delta = max(max_delta, d)

    print(f"Empirical max |H(z)-H(z')| over samples: {max_delta:.6f}")
    print(f"Bound holds: {max_delta <= bound + 1e-6}")

    if out_csv:
        os.makedirs(os.path.dirname(out_csv) or ".", exist_ok=True)
        with open(out_csv, "w") as f:
            f.write("n,m,bound,max_delta,bound_holds\n")
            f.write(f"{n},{m},{bound:.6f},{max_delta:.6f},{max_delta <= bound + 1e-6}\n")
        print(f"Wrote {out_csv}")


if __name__ == "__main__":
    main()
