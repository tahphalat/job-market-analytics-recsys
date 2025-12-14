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

## Job Market Analytics & RecSys

> [!NOTE]
> **Project Goal & Problem Statement**
>
> **Pain Points (Why this matters):**
> - **For Job Seekers**: "Too many jobs, don't know where to start." Descriptions are long and skill requirements are vague. It's hard to choose the right role or know what to upskill.
> - **Market Blindness**: Tech trends change fast (e.g., GenAI, Data Engineering). It's hard to see which skills are becoming "standard."
> - **Salary Opacity**: Hard to know which skills pay a premium or which locations have high demand.
> - **For Recruiters/Teams**: Need a bird's-eye view of "what is the market hiring for?"
>
> **Problem Statement**:
> "Build a system that aggregates job postings from multiple sources to analyze market trends, extract key skills, and provide a job recommendation system with clear upskilling paths."
>
> **Our Solution:** A Batch + Streaming pipeline with an Internal Analytics Dashboard that visualizes Demand, Salary, and Skill Relations.

## System Overview

### Data Pipeline Flow
`Raw` → `Cleaned` → `Curated` → `Artifacts`

- **Raw**: Ingestion from Kaggle/Remotive.
- **Cleaned**: Deduplication and schema enforcement.
- **Curated**: Feature engineering (Skill extraction, TF-IDF vectors).
- **Artifacts**: Aggregated views serving this dashboard.

### Data Modeling
We use a **Star Schema** design:
- **Fact**: `fact_jobs`
- **Dimensions**: `dim_company`, `dim_location`, `dim_skill`
See [Data Modeling Docs](docs/data_modeling.md) for details.

## Streamlit visualization
- Generate artifacts first (e.g., `make -C dsde run_all SKIP_EXTRACT=1` or at least `make -C dsde analytics graph train`).
- From the `dsde` directory run `streamlit run src/app_streamlit.py` to browse KPIs, top skills/titles/locations, the job table, and demo recommendations.
- The app reads from `artifacts/` and `data/processed/jobs_canonical.*`; it will fall back to CSV if Parquet is unreadable.

## Notes
- Column names are read from files at runtime; schema mapping handles aliases to avoid guessing.
- Use `--input`, `--output`, and `--seed` on every CLI for reproducibility.
