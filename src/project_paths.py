from __future__ import annotations

from pathlib import Path


SRC_ROOT = Path(__file__).resolve().parent
REPO_ROOT = SRC_ROOT.parent
DATA_DIR = SRC_ROOT / "data"
PAPER_DIR = REPO_ROOT / "paper"
PAPER_FIG_DIR = PAPER_DIR / ("fig" if (PAPER_DIR / "fig").is_dir() else "figs")


def resolve_workspace_path(path: str | Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    if candidate.parts and candidate.parts[0] == "data":
        return DATA_DIR.joinpath(*candidate.parts[1:])
    if candidate.parts and candidate.parts[0] == "paper":
        return PAPER_DIR.joinpath(*candidate.parts[1:])
    return REPO_ROOT / candidate