"""
Download datasets to data/ according to data/download_config.json.

Config schema (in data/download_config.json):
  data_dir: str (default ".") — directory to save files (relative to this script).
  sources: list of:
    - type "url":  url, save_as, optional file_in_archive (if URL is a zip).
    - type "uci":  id (UCI dataset id, e.g. 1276), save_as, optional file_in_dataset.
    - type "kaggle": id (e.g. "owner/dataset-slug"), save_as, optional file_in_dataset.
    - type "kaggle_competition": id (competition slug, e.g. "house-prices-advanced-regression-techniques"), save_as, optional file_in_dataset (e.g. "train.csv"). Requires accepting competition rules on Kaggle website first.

Run from repo root:
  python data/download_data.py
  python data/download_data.py --config data/download_config.json

Requires: requests. Optional: ucimlrepo (for UCI), kaggle (for Kaggle).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import zipfile
from io import BytesIO
from urllib.request import urlopen

# data dir: where this script lives
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CONFIG_PATH = os.path.join(SCRIPT_DIR, "download_config.json")


def load_config(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def ensure_dir(path: str) -> None:
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)


def download_url(source: dict, data_dir: str) -> None:
    url = source["url"]
    save_as = source["save_as"]
    out_path = os.path.join(data_dir, save_as)
    ensure_dir(out_path)
    file_in_archive = source.get("file_in_archive")

    print(f"  URL: {url}")
    with urlopen(url) as resp:
        data = resp.read()

    if file_in_archive and (url.rstrip("/").endswith(".zip") or data[:4] == b"PK\x03\x04"):
        with zipfile.ZipFile(BytesIO(data), "r") as z:
            names = z.namelist()
            if file_in_archive in names:
                name = file_in_archive
            else:
                candidates = [n for n in names if n.endswith(os.path.basename(file_in_archive))]
                name = candidates[0] if candidates else names[0]
            with z.open(name) as zf:
                with open(out_path, "wb") as f:
                    f.write(zf.read())
        print(f"  Extracted {name} -> {out_path}")
    else:
        with open(out_path, "wb") as f:
            f.write(data)
        print(f"  Saved -> {out_path}")


def _download_uci_1276_fallback(source: dict, data_dir: str) -> None:
    """UCI 1276 无法通过 ucimlrepo 导入时，用归档 URL 下载。"""
    u = "https://archive.ics.uci.edu/static/public/1276/amazon+product+and+google+locations+reviews.zip"
    print("  Fallback: UCI 1276 不支持 Python 导入，改用归档 URL 下载...")
    try:
        with urlopen(u) as resp:
            data = resp.read()
    except OSError as e:
        print(f"  Fallback URL 失败: {e}")
        print("  请从 UCI 页面手动下载后放到 data/ 并命名为 save_as。")
        raise SystemExit(1) from e
    out_path = os.path.join(data_dir, source["save_as"])
    ensure_dir(out_path)
    with zipfile.ZipFile(BytesIO(data), "r") as z:
        csv_names = [n for n in z.namelist() if n.endswith(".csv")]
        name = csv_names[0] if csv_names else z.namelist()[0]
        with z.open(name) as zf:
            with open(out_path, "wb") as f:
                f.write(zf.read())
    print(f"  Saved -> {out_path}")


def download_uci(source: dict, data_dir: str) -> None:
    try:
        from ucimlrepo import fetch_ucirepo
        from ucimlrepo.fetch import DatasetNotFoundError
    except ImportError:
        print("  Install ucimlrepo: pip install ucimlrepo")
        if source.get("id") == 1276:
            _download_uci_1276_fallback(source, data_dir)
            return
        raise SystemExit("ucimlrepo required for UCI download. pip install ucimlrepo")

    uid = source["id"]
    save_as = source["save_as"]
    out_path = os.path.join(data_dir, save_as)
    ensure_dir(out_path)

    print(f"  UCI id: {uid}")
    try:
        ds = fetch_ucirepo(id=uid)
    except DatasetNotFoundError:
        if source.get("id") == 1276:
            _download_uci_1276_fallback(source, data_dir)
            return
        raise
    # Prefer features+targets as one frame, or features
    if hasattr(ds, "data") and ds.data is not None:
        if hasattr(ds.data, "frames") and ds.data.frames:
            df = ds.data.frames[0]
        elif hasattr(ds.data, "original") and ds.data.original is not None:
            df = ds.data.original
        else:
            import pandas as pd
            frames = []
            if getattr(ds.data, "features", None) is not None:
                frames.append(ds.data.features)
            if getattr(ds.data, "targets", None) is not None:
                frames.append(ds.data.targets)
            df = pd.concat(frames, axis=1) if frames else pd.DataFrame()
        if not df.empty:
            df.to_csv(out_path, index=False)
            print(f"  Saved -> {out_path}")
            return
    # Single table by name
    file_in_dataset = source.get("file_in_dataset")
    if file_in_dataset and hasattr(ds, "data"):
        for name, tab in (getattr(ds.data, "__dict__", {}) or {}).items():
            if hasattr(tab, "to_csv") and (file_in_dataset in name or name == file_in_dataset):
                tab.to_csv(out_path, index=False)
                print(f"  Saved -> {out_path}")
                return
    print("  Warning: could not build CSV from UCI response; check dataset structure.")


def _find_first_csv(root_dir: str, prefer_name: str | None = None) -> str | None:
    for dirpath, _dirnames, filenames in os.walk(root_dir):
        for f in filenames:
            if f.endswith(".csv"):
                path = os.path.join(dirpath, f)
                if prefer_name and (f == prefer_name or prefer_name in f):
                    return path
                return path
    return None


def download_kaggle(source: dict, data_dir: str) -> None:
    try:
        import kaggle
    except ImportError:
        print("  Install kaggle: pip install kaggle")
        print("  Then place API key in ~/.kaggle/kaggle.json (from Kaggle Account -> Create API Token)")
        raise SystemExit(1)

    kid = source["id"]
    save_as = source["save_as"]
    file_in_dataset = source.get("file_in_dataset")
    out_path = os.path.join(data_dir, save_as)
    ensure_dir(out_path)

    print(f"  Kaggle dataset: {kid}")
    if file_in_dataset:
        kaggle.api.dataset_download_file(kid, file_in_dataset, path=data_dir, quiet=False)
        # Usually downloads as .zip; extract and find the file
        for f in os.listdir(data_dir):
            if f.endswith(".zip"):
                zip_path = os.path.join(data_dir, f)
                with zipfile.ZipFile(zip_path, "r") as z:
                    names = z.namelist()
                    target = file_in_dataset if file_in_dataset in names else next((n for n in names if n.endswith(".csv")), names[0])
                    with z.open(target) as zf:
                        with open(out_path, "wb") as out:
                            out.write(zf.read())
                os.remove(zip_path)
                print(f"  Saved -> {out_path}")
                return
        # Single file downloaded without zip
        base = os.path.basename(file_in_dataset)
        if os.path.isfile(os.path.join(data_dir, base)):
            os.rename(os.path.join(data_dir, base), out_path)
            print(f"  Saved -> {out_path}")
            return
    else:
        kaggle.api.dataset_download_files(kid, path=data_dir, unzip=True, quiet=False)
        found = _find_first_csv(data_dir)
        if found and os.path.abspath(found) != os.path.abspath(out_path):
            import shutil
            shutil.copy2(found, out_path)
            print(f"  Saved -> {out_path}")
            return
    print("  Warning: no CSV found after Kaggle download.")


def download_kaggle_competition(source: dict, data_dir: str) -> None:
    try:
        import kaggle
        import requests
    except ImportError:
        print("  Install kaggle: pip install kaggle")
        print(r"  Kaggle 需要登录: 将 kaggle.json 放到 ~/.kaggle/ (Windows: C:\Users\<你>\.kaggle\)")
        raise SystemExit(1)

    comp = source["id"]
    save_as = source["save_as"]
    file_in_dataset = source.get("file_in_dataset")
    out_path = os.path.join(data_dir, save_as)
    ensure_dir(out_path)

    print(f"  Kaggle competition: {comp}")
    api = kaggle.KaggleApi()
    api.authenticate()
    try:
        if file_in_dataset:
            api.competition_download_file(comp, file_in_dataset, path=data_dir, quiet=False)
        else:
            api.competition_download_files(comp, path=data_dir, quiet=False)
    except requests.exceptions.HTTPError as e:
        if e.response is not None and e.response.status_code == 403:
            print("  403 Forbidden: 该竞赛需在 Kaggle 网页上先接受规则（Join Competition / Accept Rules）。")
            print(f"  请打开 https://www.kaggle.com/competitions/{comp} 点击加入并接受规则后再重试。")
        raise SystemExit(1) from e

    if file_in_dataset:
        direct = os.path.join(data_dir, os.path.basename(file_in_dataset))
        if os.path.isfile(direct):
            import shutil
            if os.path.abspath(direct) != os.path.abspath(out_path):
                shutil.copy2(direct, out_path)
            print(f"  Saved -> {out_path}")
            return
        # May have downloaded as zip
        for f in os.listdir(data_dir):
            if f.endswith(".zip"):
                zip_path = os.path.join(data_dir, f)
                with zipfile.ZipFile(zip_path, "r") as z:
                    names = [n for n in z.namelist() if n.endswith(".csv")]
                    name = file_in_dataset if any(file_in_dataset in n for n in names) else (names[0] if names else z.namelist()[0])
                    with z.open(name) as zf:
                        with open(out_path, "wb") as out:
                            out.write(zf.read())
                try:
                    os.remove(zip_path)
                except OSError:
                    pass
                print(f"  Saved -> {out_path}")
                return
        # Direct file
        base = os.path.basename(file_in_dataset)
        cand = os.path.join(data_dir, base)
        if os.path.isfile(cand):
            if os.path.abspath(cand) != os.path.abspath(out_path):
                import shutil
                shutil.copy2(cand, out_path)
            print(f"  Saved -> {out_path}")
            return
    else:
        zip_name = comp + ".zip"
        zip_path = os.path.join(data_dir, zip_name)
        if os.path.isfile(zip_path):
            with zipfile.ZipFile(zip_path, "r") as z:
                csv_names = [n for n in z.namelist() if n.endswith(".csv")]
                name = csv_names[0] if csv_names else z.namelist()[0]
                with z.open(name) as zf:
                    with open(out_path, "wb") as out:
                        out.write(zf.read())
            try:
                os.remove(zip_path)
            except OSError:
                pass
            print(f"  Saved -> {out_path}")
            return
    print("  Warning: no CSV found after competition download.")


def main() -> None:
    ap = argparse.ArgumentParser(description="Download data sources from data/download_config.json")
    ap.add_argument("--config", "-c", default=DEFAULT_CONFIG_PATH, help="Path to download_config.json")
    ap.add_argument("--list", "-l", action="store_true", help="Only list configured sources")
    args = ap.parse_args()

    if not os.path.isfile(args.config):
        print(f"Config not found: {args.config}")
        sys.exit(1)

    config = load_config(args.config)
    data_dir = config.get("data_dir", SCRIPT_DIR)
    if not os.path.isabs(data_dir):
        data_dir = os.path.join(SCRIPT_DIR, data_dir)
    data_dir = os.path.normpath(data_dir)
    sources = config.get("sources", [])

    if args.list:
        for i, s in enumerate(sources):
            print(f"{i+1}. [{s.get('type')}] {s.get('save_as')} — {s.get('description', '')}")
        return

    print(f"Data dir: {data_dir}")
    for i, source in enumerate(sources):
        typ = source.get("type", "").lower()
        desc = source.get("description", "")
        print(f"\n[{i+1}/{len(sources)}] {source.get('save_as')} — {desc}")
        try:
            if typ == "url":
                download_url(source, data_dir)
            elif typ == "uci":
                download_uci(source, data_dir)
            elif typ == "kaggle":
                download_kaggle(source, data_dir)
            elif typ == "kaggle_competition":
                download_kaggle_competition(source, data_dir)
            else:
                print(f"  Unknown type: {typ}")
        except Exception as e:
            print(f"  Error: {e}")
            raise

    print("\nDone.")


if __name__ == "__main__":
    main()
