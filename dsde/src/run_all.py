import argparse
import subprocess
from pathlib import Path
from typing import Optional

from src.config import SEED
from src.utils.logging import get_logger

logger = get_logger(__name__)


def run_cmd(cmd: list[str]) -> None:
    logger.info("Running: %s", " ".join(cmd))
    subprocess.run(cmd, check=True)


def run_pipeline(kaggle_input: Optional[str], kaggle_dataset: str, skip_extract: bool, seed: int) -> None:
    env = {"PYTHONPATH": "."}
    if not skip_extract:
        if not kaggle_input:
            raise ValueError("kaggle_input is required unless --skip_extract is set.")
        run_cmd(
            ["python", "-m", "src.extract.fetch_kagglehub", "--dataset", kaggle_dataset, "--out_dir", "data/raw/kaggle", "--seed", str(seed)]
        )
        run_cmd(
            [
                "python",
                "-m",
                "src.extract.ingest_kaggle",
                "--input_path",
                kaggle_input,
                "--out_dir",
                "data/raw/kaggle",
                "--sample_n",
                "2000",
                "--seed",
                str(seed),
            ]
        )
        run_cmd(
            ["python", "-m", "src.extract.fetch_remotive", "--out_dir", "data/raw/remotive", "--sample_n", "2000", "--seed", str(seed)]
        )
        run_cmd(
            [
                "python",
                "-m",
                "src.utils.schema_report",
                "--kaggle-path",
                "data/raw/kaggle/jobs_kaggle_raw.parquet",
                "--remotive-path",
                "data/raw/remotive/jobs_remotive_raw.parquet",
                "--output",
                "artifacts/schema_report.json",
                "--seed",
                str(seed),
            ]
        )

    # Transform
    run_cmd(
        [
            "python",
            "-m",
            "src.transform.clean_kaggle",
            "--input",
            "data/raw/kaggle/jobs_kaggle_raw.parquet",
            "--output",
            "data/processed/jobs_kaggle_clean.parquet",
            "--seed",
            str(seed),
        ]
    )
    run_cmd(
        [
            "python",
            "-m",
            "src.transform.clean_remotive",
            "--input",
            "data/raw/remotive/jobs_remotive_raw.parquet",
            "--output",
            "data/processed/jobs_remotive_clean.parquet",
            "--seed",
            str(seed),
        ]
    )
    run_cmd(
        [
            "python",
            "-m",
            "src.transform.build_canonical_jobs",
            "--kaggle",
            "data/processed/jobs_kaggle_clean.parquet",
            "--remotive",
            "data/processed/jobs_remotive_clean.parquet",
            "--output",
            "data/processed/jobs_canonical.parquet",
            "--seed",
            str(seed),
        ]
    )

    # Analytics
    run_cmd(["python", "-m", "src.analytics.build_tables", "--input", "data/processed/jobs_canonical.parquet", "--seed", str(seed)])
    run_cmd(["python", "-m", "src.analytics.make_figures", "--seed", str(seed)])

    # Graph + Recommender
    run_cmd(
        [
            "python",
            "-m",
            "src.transform.skill_graph",
            "--input",
            "data/processed/jobs_canonical.parquet",
            "--output",
            "artifacts/graphs/skill_graph.json",
            "--min_edge_weight",
            "5",
            "--seed",
            str(seed),
        ]
    )
    run_cmd(
        [
            "python",
            "-m",
            "src.models.train_recommender",
            "--input",
            "data/processed/jobs_canonical.parquet",
            "--model_dir",
            "artifacts/recommender",
            "--top_k",
            "10",
            "--seed",
            str(seed),
        ]
    )

    logger.info("run_all completed.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run full pipeline end-to-end (extract -> transform -> analytics -> graph -> train).")
    parser.add_argument("--kaggle_input", default=None, help="Path to Kaggle CSV/Parquet file (required unless --skip_extract).")
    parser.add_argument("--kaggle_dataset", default="arshkon/linkedin-job-postings", help="Kaggle dataset slug for fetch_kagglehub.")
    parser.add_argument("--skip_extract", action="store_true", help="Skip extraction (reuse existing raw files).")
    parser.add_argument("--seed", type=int, default=SEED, help="Random seed.")
    return parser.parse_args()


def main():
    args = parse_args()
    run_pipeline(args.kaggle_input, args.kaggle_dataset, args.skip_extract, args.seed)


if __name__ == "__main__":
    main()
