# Repository Guidelines

## Project Structure & Module Organization
Analytics modules live in `modules/` with `src/`, `docs/`, and module `tests/`. The production pipeline lives in `core/` and is invoked through the runnable entry points in `scripts/`. Client engagements live under `clients/<client>/projects/<project>/` with subfolders for `runs/`, `docs/`, and `admin/`; keep generated artifacts in `outputs/` and stage intermediate datasets in `data/` or via the `storage/` pointers to `/Volumes/DATA`.

## Build, Test, and Development Commands
- `python -m venv venv && source venv/bin/activate` sets up a local env that matches the Apple Silicon accelerators expected by Torch and Whisper.
- `pip install -r requirements.txt` installs the multimodal stack (Torch, Whisper, transformers, ffmpeg bindings) needed by `core.pipeline` and the scripts.
- `python scripts/validate_pipeline.py data/raw/sample.mp4` performs the 90-second smoke test, writing diagnostics into `data/validation_*` before any large batch run.
- `pytest modules/category-intelligence/tests -m "unit and not slow"` executes the most complete pytest configuration (see `modules/category-intelligence/pytest.ini`) with coverage reports in `tests/coverage_html`.

## Coding Style & Naming Conventions
Python is the lingua franca: use 4-space indentation, module docstrings, and type hints as shown in `core/pipeline/extraction.py`. Reach for `pathlib.Path`, `yaml.safe_load`, and typed containers over loose dictionaries. Scripts stay verb-first (for example `extract_all_insights.py`, `validate_pipeline.py`); keep configs named `config.yaml` and `prompts.yaml` under each client so `core.models.ModelRegistry` can resolve them automatically.

## Testing Guidelines
Pytest discovers files via `test_*.py`, `Test*` classes, and `test_*` functions. Tag tests with the shared markers declared in `modules/category-intelligence/pytest.ini` (`unit`, `integration`, `collector`, etc.) and treat coverage regressions from the baked-in `--cov` options as blockers. Snapshot or report fixtures should live beside the code they validate (e.g., `modules/<module>/tests/data/`), and cross-module regressions belong in `tests/` at the repo root.

## Commit & Pull Request Guidelines
Follow the Conventional Commit style already in history (`feat: Major project reorganization and data cleanup`). Each PR should bundle a short business summary, links to the affected client folder or module docs, and before/after artifacts (screenshots, CSV samples, or `outputs/<run>/run-log.md`). Cite the run folder you touched (e.g., `clients/3m/projects/.../runs/jtbd/2025-01-15T0830Z`) and list the command used so others can reproduce locally.

## Security & Configuration Tips
Never commit credentials: `.env`, per-module `.env`, and `clients/<client>/config.yaml` hold API keys for Gemini, OpenAI, and Ollama targets managed by `ModelRegistry`. Keep AI assets, transcripts, and media on `/Volumes/DATA` and only check lightweight JSON summaries into Git. When sharing configs, strip tokens and add `_sample` variants so downstream agents can copy without exposing production secrets.
