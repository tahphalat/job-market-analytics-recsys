import argparse
import json
from pathlib import Path
from typing import Dict, Optional, Any

import pandas as pd

from src.config import ARTIFACTS_DIR, RAW_KAGGLE_DIR, RAW_REMOTIVE_DIR, SEED
from src.utils.common import set_seed
from src.utils.io import read_auto, write_json, safe_mkdir
from src.utils.logging import get_logger

logger = get_logger(__name__)


def schema_report(df: pd.DataFrame) -> Dict[str, Any]:
    if df is None or df.empty:
        return {"n_rows": 0, "n_cols": 0, "columns": []}

    def example_values(series: pd.Series, k: int = 3):
        non_null = series.dropna().astype(str).head(k).tolist()
        return non_null

    columns = []
    total = len(df)
    for col in df.columns:
        columns.append(
            {
                "name": col,
                "dtype": str(df[col].dtype),
                "missing_rate": float(df[col].isna().mean()) if total else 0.0,
                "example_values": example_values(df[col]),
            }
        )
    return {"n_rows": int(total), "n_cols": int(len(df.columns)), "columns": columns}


def build_report(kaggle_df: Optional[pd.DataFrame], remotive_df: Optional[pd.DataFrame]) -> Dict:
    report = {}
    if kaggle_df is not None:
        report["kaggle"] = schema_report(kaggle_df)
    if remotive_df is not None:
        report["remotive"] = schema_report(remotive_df)
    return report


def _load_optional(path: Optional[Path]) -> Optional[pd.DataFrame]:
    if path and path.exists():
        logger.info("Loading for schema report: %s", path)
        return read_auto(path)
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
        kaggle_path = RAW_KAGGLE_DIR / "jobs_kaggle_raw.parquet"
    if remotive_path is None:
        remotive_path = RAW_REMOTIVE_DIR / "jobs_remotive_raw.parquet"

    kaggle_df = _load_optional(kaggle_path)
    remotive_df = _load_optional(remotive_path)
    report = build_report(kaggle_df, remotive_df)

    output_path = Path(args.output)
    safe_mkdir(output_path.parent)
    write_json(report, output_path)
    logger.info("Schema report saved to %s", output_path)


if __name__ == "__main__":
    main()
