import argparse
import json
from pathlib import Path
from typing import Dict, Optional

import pandas as pd

from src.config import ARTIFACTS_DIR, RAW_KAGGLE_DIR, RAW_REMOTIVE_DIR, SEED
from src.utils.common import set_seed
from src.utils.io import read_csv_or_parquet
from src.utils.logging import get_logger

logger = get_logger(__name__)


def generate_schema_report(df: pd.DataFrame) -> Dict[str, Dict[str, float]]:
    if df is None or df.empty:
        return {}
    total = len(df)
    return {
        col: {
            "dtype": str(df[col].dtype),
            "missing_rate": float(df[col].isna().mean()) if total else 0.0,
        }
        for col in df.columns
    }


def build_report(kaggle_df: Optional[pd.DataFrame], remotive_df: Optional[pd.DataFrame]) -> Dict:
    report = {}
    if kaggle_df is not None:
        report["kaggle"] = {
            "rows": int(len(kaggle_df)),
            "columns": list(kaggle_df.columns),
            "schema": generate_schema_report(kaggle_df),
        }
    if remotive_df is not None:
        report["remotive"] = {
            "rows": int(len(remotive_df)),
            "columns": list(remotive_df.columns),
            "schema": generate_schema_report(remotive_df),
        }
    return report


def _load_optional(path: Optional[Path]) -> Optional[pd.DataFrame]:
    if path and path.exists():
        logger.info("Loading for schema report: %s", path)
        return read_csv_or_parquet(path)
    logger.warning("Path not found for schema report: %s", path)
    return None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate combined schema report for Kaggle and Remotive sources.")
    parser.add_argument("--kaggle-path", default=None, help="Path to Kaggle raw file (csv/parquet).")
    parser.add_argument("--remotive-path", default=None, help="Path to Remotive parquet/csv.")
    parser.add_argument("--output", default=ARTIFACTS_DIR / "schema_report.json", help="Output JSON path.")
    parser.add_argument("--seed", type=int, default=SEED, help="Random seed.")
    return parser.parse_args()


def main():
    args = parse_args()
    set_seed(args.seed)

    kaggle_path = Path(args.kaggle_path) if args.kaggle_path else None
    remotive_path = Path(args.remotive_path) if args.remotive_path else None

    if kaggle_path is None:
        kaggle_path = next((p for p in [RAW_KAGGLE_DIR / "jobs_kaggle_raw.parquet", RAW_KAGGLE_DIR / "jobs_kaggle_raw.csv"] if p.exists()), None)
    if remotive_path is None:
        remotive_path = next((p for p in [RAW_REMOTIVE_DIR / "jobs_remotive_raw.parquet", RAW_REMOTIVE_DIR / "jobs_remotive_raw.csv"] if p.exists()), None)

    kaggle_df = _load_optional(kaggle_path)
    remotive_df = _load_optional(remotive_path)
    report = build_report(kaggle_df, remotive_df)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(report, f, indent=2)
    logger.info("Schema report saved to %s", output_path)


if __name__ == "__main__":
    main()
