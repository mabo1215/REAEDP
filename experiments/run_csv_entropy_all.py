"""
对多张 CSV 分别跑熵+DP 实验，每张表生成一张图到 paper/fig/。
配置中 "csv_entropy_all"."datasets" 为列表，每项: input, column, out_fig（可选）。
若 data_dir 给定，input 会相对 data_dir 解析；否则相对项目根目录。
"""
import os
import sys

ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, ROOT)

from experiments.run_csv_entropy_experiment import main as run_one


def main(config=None):
    if config is None:
        config = {}
    data_dir = config.get("data_dir", ROOT)
    if not os.path.isabs(data_dir):
        data_dir = os.path.join(ROOT, data_dir)
    datasets = config.get("datasets", [])
    defaults = {
        "bins": config.get("bins", 30),
        "epsilon": config.get("epsilon", 1.0),
        "max_rows": config.get("max_rows", 100000),
        "seed": config.get("seed", 42),
        "dpi": config.get("dpi", 150),
        "out_csv": "",  # 批量时不写单表 out_csv，可用 out_csv_all 汇总
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
    cfg_path = os.path.join(ROOT, "config.json")
    if os.path.isfile(cfg_path):
        with open(cfg_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        main(config=cfg.get("csv_entropy_all", {}))
    else:
        main(config={})
