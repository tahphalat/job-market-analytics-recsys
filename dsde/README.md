# DSDE JobScope MVP (Phase 0)

## Objective
- Scaffold a DSDE pipeline (extract ➜ transform ➜ load ➜ viz/graph ➜ model) with CLI entrypoints and lightweight logging, ready for data from Kaggle/Remotive.

## Data layout
- Raw inputs: `dsde/data/raw/kaggle/`, `dsde/data/raw/remotive/`
- Processed outputs: `dsde/data/processed/`
- Artifacts: `dsde/artifacts/{figures,graphs,recommender}`

## How to run
- Install deps (Python 3.11): `make -C dsde setup`
- Pipeline help: `python dsde/src/run_all.py --help`
- Stage targets: `make -C dsde extract`, `transform`, `eda`, `graph`, `train`, `run_all`, `smoke_test`, `export_web`
- Default ingestion dataset: KaggleHub `arshkon/linkedin-job-postings` (override via `KAGGLE_DATASET=...`). After download, ingestion auto-detects the first CSV/Parquet in `data/raw/kaggle`; specify `KAGGLE_INPUT=...` to force a file.

## Notes
- Column names are read from files at runtime; schema mapping handles aliases to avoid guessing.
- Use `--input`, `--output`, and `--seed` on every CLI for reproducibility.
