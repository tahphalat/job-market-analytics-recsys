import argparse
from pathlib import Path
from typing import Optional

from src.config import SEED
from src.pipeline.core import Pipeline
from src.quality.guard import DataGuard
from src.utils.logging import get_logger

# Import pipeline steps directly
from src.extract.fetch_kagglehub import fetch_kagglehub_dataset
from src.extract.ingest_kaggle import ingest_kaggle_file
# from src.extract.fetch_secondary_kaggle import fetch_secondary_dataset
from src.transform.clean_kaggle import clean_kaggle
# from src.transform.clean_secondary import clean_secondary
from src.transform.build_canonical_jobs import build_canonical
from src.analytics.build_tables import build_tables
from src.analytics.make_figures import make_figures
# Skill graph components
from src.transform.skill_graph import read_jobs, build_skill_sets, build_graph, export_graph
from src.models.train_recommender import train as train_recommender

logger = get_logger(__name__)

def run_pipeline(kaggle_input: Optional[str], kaggle_dataset: str, skip_extract: bool, seed: int) -> None:
    pipe = Pipeline("JobScope_ETL")

    # --- 1. Ingestion Layer ---
    @pipe.task(name="Extract_Kaggle_Primary")
    def step_extract_kaggle():
        if not skip_extract:
            if not kaggle_input:
                download_path = fetch_kagglehub_dataset(kaggle_dataset, Path("data/raw/kaggle"), seed)
                ingest_kaggle_file(None, Path("data/raw/kaggle"), 2000, seed)
            else:
                ingest_kaggle_file(Path(kaggle_input), Path("data/raw/kaggle"), 2000, seed)

    @pipe.task(name="Extract_Kaggle_Secondary")
    def step_extract_secondary():
        if not skip_extract:
            # Fetches yusifmohammed/data-engineering-job-postings
            fetch_secondary_dataset("yusifmohammed/data-engineering-job-postings", Path("data/raw/kaggle/secondary"), seed)

    # --- 2. Quality Check (Raw) ---
    @pipe.task(name="DQ_Raw_Check")
    def step_dq_raw():
        # Validate schemas of ingested data before processing
        if not skip_extract:
            DataGuard.validate_parquet("data/raw/kaggle/jobs_kaggle_raw.parquet", 
                                     expected_columns=["title", "company_name", "description"])
            # Secondary check (it might be CSV or Parquet depending on download, skip rigid check or assume generic)
            # DataGuard.validate_csv(...) 

    # --- 3. Transformation Layer ---
    @pipe.task(name="Transform_Clean")
    def step_transform():
        clean_kaggle(Path("data/raw/kaggle/jobs_kaggle_raw.parquet"), 
                     Path("data/processed/jobs_kaggle_clean.parquet"), seed)

    @pipe.task(name="Transform_Canonical")
    def step_canonical():
        build_canonical(Path("data/processed/jobs_kaggle_clean.parquet"),
                        Path("data/processed/jobs_canonical.parquet"), seed)

    # --- 4. Quality Check (Trusted/Curated) ---
    @pipe.task(name="DQ_Curated_Check")
    def step_dq_curated():
        DataGuard.validate_parquet("data/processed/jobs_canonical.parquet", 
                                 expected_columns=["job_id", "title", "company", "location_text", "skills"],
                                 check_not_null=["title", "company"])

    # --- 5. Application Layer (Analytics/AI) ---
    @pipe.task(name="Analytics_Build")
    def step_analytics():
        build_tables(Path("data/processed/jobs_canonical.parquet")) # func doesn't take seed
        make_figures() # func doesn't take seed

    @pipe.task(name="AI_Models")
    def step_ai():
        # Skill Graph logic replicated
        job_df = read_jobs(Path("data/processed/jobs_canonical.parquet"))
        skill_sets = build_skill_sets(job_df)
        nodes, links = build_graph(skill_sets, min_edge_weight=5)
        export_graph(nodes, links, Path("artifacts/graphs/skill_graph.json"))
        
        # Train Recommender
        train_recommender(Path("data/processed/jobs_canonical.parquet"), 
                          Path("artifacts/recommender"), top_k=10)


    # Execution
    # Execution
    pipe.add_task(step_extract_kaggle)
    # pipe.add_task(step_extract_secondary) # Removed
    pipe.add_task(step_dq_raw)
    pipe.add_task(step_transform)
    pipe.add_task(step_canonical)
    pipe.add_task(step_dq_curated)
    pipe.add_task(step_analytics)
    pipe.add_task(step_ai)

    pipe.run()
    logger.info("Pipeline completed successfully.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run full pipeline (Python-Native with DQ).")
    parser.add_argument("--kaggle_input", default=None, help="Path to Kaggle CSV/Parquet file.")
    parser.add_argument("--kaggle_dataset", default="arshkon/linkedin-job-postings", help="Kaggle dataset slug.")
    parser.add_argument("--skip_extract", action="store_true", help="Skip extraction.")
    parser.add_argument("--seed", type=int, default=SEED, help="Random seed.")
    return parser.parse_args()


def main():
    args = parse_args()
    run_pipeline(args.kaggle_input, args.kaggle_dataset, args.skip_extract, args.seed)


if __name__ == "__main__":
    main()
