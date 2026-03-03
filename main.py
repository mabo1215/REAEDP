#!/usr/bin/env python3
"""
REAEDP entry point: run experiments from config.json.
Usage:
  python main.py                    # run all tasks listed in config["run"]
  python main.py --config config.json
  python main.py --run entropy_sensitivity image_noise   # run only these
"""
import os
import sys
import json
import argparse

# Ensure project root is on path
ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


def load_config(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(description="Run REAEDP experiments from config")
    parser.add_argument("--config", "-c", type=str, default="config.json", help="Path to config.json")
    parser.add_argument("--run", "-r", nargs="*", default=None, help="Run only these tasks (default: all in config['run'])")
    args = parser.parse_args()

    config_path = os.path.join(ROOT, args.config) if not os.path.isabs(args.config) else args.config
    if not os.path.isfile(config_path):
        print(f"Config not found: {config_path}")
        sys.exit(1)

    cfg = load_config(config_path)
    to_run = args.run if args.run is not None else cfg.get("run", [])
    if not to_run:
        print("No tasks in config['run'] and no --run given.")
        sys.exit(0)

    # 一键生成全部论文图（含用下载数据做的熵图）时展开为下列任务
    PAPER_FIGURES_TASKS = [
        "privacy_test_fig1", "wiener_figures", "epsilon_utility_curve",
        "entropy_bound_curve", "metrics_comparison", "csv_entropy_all",
    ]
    to_run = [t for name in to_run for t in (PAPER_FIGURES_TASKS if name == "paper_figures" else [name])]

    name_to_module = {
        "entropy_sensitivity": ("experiments.run_entropy_sensitivity", "run_entropy_sensitivity"),
        "noisy_sgd": ("experiments.run_noisy_sgd_demo", "run_noisy_sgd_demo"),
        "wiener_figures": ("experiments.run_wiener_figures", "run_wiener_figures"),
        "privacy_test_fig1": ("experiments.run_privacy_test_fig1", "run_privacy_test_fig1"),
        "image_noise": ("experiments.run_image_noise", "run_image_noise"),
        "epsilon_utility_curve": ("experiments.run_epsilon_utility_curve", "run_epsilon_utility_curve"),
        "entropy_bound_curve": ("experiments.run_entropy_bound_curve", "run_entropy_bound_curve"),
        "metrics_comparison": ("experiments.run_metrics_comparison", "run_metrics_comparison"),
        "csv_entropy_experiment": ("experiments.run_csv_entropy_experiment", "run_csv_entropy_experiment"),
        "csv_entropy_all": ("experiments.run_csv_entropy_all", "main"),
    }

    for name in to_run:
        if name not in name_to_module:
            print(f"Unknown task: {name}. Skipping.")
            continue
        mod_path, mod_short = name_to_module[name]
        task_config = cfg.get(name, {})
        print(f"--- Running: {name} ---")
        try:
            mod = __import__(mod_path, fromlist=[mod_short])
            getattr(mod, "main")(config=task_config)
        except Exception as e:
            print(f"Error in {name}: {e}")
            raise
        print()

    print("Done.")


if __name__ == "__main__":
    main()
