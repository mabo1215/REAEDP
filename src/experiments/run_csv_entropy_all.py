"""
Run the CSV entropy + DP experiment across multiple datasets.
Each dataset produces one paper figure under paper/figs/.
The csv_entropy_all.datasets config should provide input, column, and optional out_fig.
If data_dir is set, relative input paths are resolved from that directory.
"""
import os
import sys

SRC_ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, SRC_ROOT)

from experiments.run_csv_entropy_experiment import main as run_one
from project_paths import resolve_workspace_path


def main(config=None):
    if config is None:
        config = {}
    data_dir = str(resolve_workspace_path(config.get("data_dir", "data")))
    datasets = config.get("datasets", [])
    defaults = {
        "bins": config.get("bins", 30),
        "epsilon": config.get("epsilon", 1.0),
        "max_rows": config.get("max_rows", 100000),
        "seed": config.get("seed", 42),
        "dpi": config.get("dpi", 150),
        "out_csv": "",  # Skip per-dataset CSV by default during batch runs.
    }
    for i, item in enumerate(datasets):
        if isinstance(item, str):
            item = {"input": item, "column": None}
        inp = item.get("input")
        col = item.get("column")
        if not inp or not col:
            print(f"  Skip dataset[{i}]: need 'input' and 'column'. Got: {item}")
            continue
        if not os.path.isabs(inp):
            inp = os.path.join(data_dir, inp)
        if not os.path.isfile(inp):
            print(f"  Skip (file not found): {inp}")
            continue
        out_fig = item.get("out_fig") or ("fig_csv_entropy_" + os.path.splitext(os.path.basename(inp))[0] + ".png")
        one_cfg = {**defaults, "input": inp, "column": col, "out_fig": out_fig}
        if config.get("out_csv_all"):
            base = os.path.splitext(os.path.basename(inp))[0]
            one_cfg["out_csv"] = os.path.join(os.path.dirname(inp), f"csv_entropy_{base}.csv")
        print(f"  [{i+1}/{len(datasets)}] {os.path.basename(inp)} column={col} -> {out_fig}")
        try:
            run_one(config=one_cfg)
        except Exception as e:
            print(f"  Error: {e}")
            continue


if __name__ == "__main__":
    import json
    cfg_path = os.path.join(SRC_ROOT, "config.json")
    if os.path.isfile(cfg_path):
        with open(cfg_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        main(config=cfg.get("csv_entropy_all", {}))
    else:
        main(config={})
