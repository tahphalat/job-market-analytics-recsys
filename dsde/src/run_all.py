import argparse
from pathlib import Path
from typing import Optional

import argparse

from config import ARTIFACTS_DIR, PROCESSED_DIR, SEED
from extract.extract import extract
from features.build_features import build_features
from load.load import load
from models.train_model import train
from transform.transform import transform
from utils.common import ensure_parent, set_seed
from utils.logging import get_logger
from viz.eda import run_eda

logger = get_logger(__name__)


def run_pipeline(
    input_path: Path,
    output_dir: Path,
    seed: int,
    figure_path: Optional[Path] = None,
) -> None:
    set_seed(seed)
    output_dir.mkdir(parents=True, exist_ok=True)

    raw_output = output_dir / "raw_snapshot.csv"
    transform_output = output_dir / "clean_jobs.csv"
    load_output = output_dir / "clean_jobs_loaded.csv"
    feature_output = output_dir / "features_summary.csv"
    eda_output = ARTIFACTS_DIR / "graphs" / "eda_summary.json"
    model_output = ARTIFACTS_DIR / "recommender" / "simple_model.pkl"
    sqlite_output = ARTIFACTS_DIR / "graphs" / "jobs.db"
    figure_output = figure_path or ARTIFACTS_DIR / "figures" / "comp_value_by_category.html"

    logger.info("Starting pipeline with input=%s", input_path)
    raw_path = extract(input_path, raw_output, seed=seed)
    transformed_path = transform(raw_path, transform_output, seed=seed)
    loaded_path = load(transformed_path, load_output, seed=seed, sqlite_path=sqlite_output)
    build_features(loaded_path, feature_output, seed=seed)
    run_eda(loaded_path, eda_output, seed=seed, figure_path=figure_output)

    try:
        train(loaded_path, model_output, seed=seed)
    except ValueError as exc:
        logger.warning("Model training skipped: %s", exc)

    logger.info("Pipeline finished. Outputs stored under %s", output_dir)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the JobScope DSDE pipeline end-to-end.")
    parser.add_argument("--input", required=True, help="Path to the raw input CSV.")
    parser.add_argument(
        "--output",
        required=True,
        help="Base directory for processed outputs (clean data, features, reports).",
    )
    parser.add_argument("--seed", type=int, default=SEED, help="Random seed for all steps.")
    parser.add_argument(
        "--figure",
        default=None,
        help="Optional HTML figure path for the EDA boxplot.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    figure = Path(args.figure) if args.figure else None
    run_pipeline(Path(args.input), ensure_parent(Path(args.output)), seed=args.seed, figure_path=figure)


if __name__ == "__main__":
    main()
