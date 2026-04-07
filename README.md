# REAEDP

REAEDP is a research repository for the paper "Renyi Entropy Analysis and Evaluation Based $(\varepsilon,\delta)$-Differential Privacy Protection Method under the Wiener Kernel Space". It contains the manuscript source in `paper/` and reproducible experiment code in `src/`.

## Repository Layout

| Path | Purpose |
|------|---------|
| `main.py` | Root shim that forwards to `src/main.py`. |
| `src/main.py` | Main experiment entry point. |
| `src/config.json` | Default experiment configuration. |
| `src/algorithms/` | Core privacy and release mechanisms. |
| `src/experiments/` | Experiment drivers used to generate tables, CSV files, and figures. |
| `src/data/` | Input data and generated CSV outputs. |
| `paper/` | LaTeX sources, build script, and paper figures. |
| `paper/figs/` | Figures consumed by the manuscript. |
| `requirements.txt` | Python dependencies. |

## Environment Setup

REAEDP is developed with Python 3.8+.

### Windows

```powershell
cd C:\source\REAEDP
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

### Linux or macOS

```bash
cd /path/to/REAEDP
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running Experiments

From the repository root:

```powershell
cd C:\source\REAEDP
python main.py
```

This runs every task listed in `src/config.json` under `run`.

To run selected tasks only:

```powershell
python main.py --run privacy_test_fig1 wiener_figures tabular_synth_benchmark
```

To use a different configuration file:

```powershell
python main.py --config path\to\config.json
```

## Key Experiment Tasks

`src/config.json` defines the available tasks and their parameters. Common entries include:

- `entropy_sensitivity`
- `baseline_comparison`
- `mia_evaluation`
- `tabular_synth_benchmark`
- `wiener_figures`
- `csv_entropy_all`

The alias `paper_figures` expands to the full figure-generation pipeline used by the manuscript.

## Data and Outputs

- Raw or downloaded datasets live in `src/data/`.
- Generated CSV summaries are written to `src/data/`.
- Manuscript figures are written to `paper/figs/`.
- Image-noise outputs are written to the folder configured by `image_noise.output`.

To download configured datasets:

```powershell
python src/data/download_data.py
```

The download sources are defined in `src/data/download_config.json`.

## Building the Paper

The canonical build entry point is `paper/build.bat`.

```powershell
cd C:\source\REAEDP\paper
.\build.bat
```

This builds:

- `paper/main.pdf`
- `paper/appendix.pdf`

Intermediate build files are stored under `paper/build/`.

You need a LaTeX distribution that provides `pdflatex` and `bibtex`, such as MiKTeX or TeX Live.

## Typical Workflow

1. Create and activate a virtual environment.
2. Install dependencies from `requirements.txt`.
3. Run the required experiment tasks.
4. Check that the updated figures appear in `paper/figs/`.
5. Rebuild the paper with `paper/build.bat`.

## Citation

If you use this repository, please cite the corresponding paper described in `paper/main.tex`.
