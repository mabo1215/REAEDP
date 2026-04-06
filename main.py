#!/usr/bin/env python3
import importlib.util
import pathlib
import sys


def main() -> None:
    src_main = pathlib.Path(__file__).resolve().parent / "src" / "main.py"
    spec = importlib.util.spec_from_file_location("reaedp_src_main", src_main)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load entrypoint: {src_main}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    module.main()


if __name__ == "__main__":
    main()