import argparse
from pathlib import Path

import pandas as pd

from utils.common import ensure_parent, set_seed
from utils.logging import get_logger
from utils.schema import (
    CANONICAL_COLUMNS,
    normalize_work_mode,
    parse_comp_value,
    rename_with_aliases,
)

logger = get_logger(__name__)


def transform(input_path: Path, output_path: Path, seed: int) -> Path:
    set_seed(seed)
    df = pd.read_csv(input_path)
    df, mapping = rename_with_aliases(df)
    logger.info("Column mapping applied: %s", mapping)
    df["work_mode"] = df["work_mode"].apply(normalize_work_mode)

    # Normalize numeric compensation
    if "comp_value" in df.columns:
        df["comp_value"] = df["comp_value"].apply(parse_comp_value)
    if df["comp_value"].isna().all():
        df["comp_value"] = df["compensation_normalized"].apply(parse_comp_value)
    if df["comp_value"].isna().all():
        df["comp_value"] = df["compensation"].apply(parse_comp_value)
    df["comp_value"] = pd.to_numeric(df["comp_value"], errors="coerce")

    df["compensation_normalized"] = df["compensation_normalized"].fillna(df["compensation"])

    df = df.drop_duplicates()
    ordered_cols = [col for col in CANONICAL_COLUMNS if col in df.columns]
    remainder = [col for col in df.columns if col not in ordered_cols]
    df = df[ordered_cols + remainder]

    output_path = ensure_parent(output_path)
    df.to_csv(output_path, index=False)
    logger.info("Saved transformed data to %s (rows=%s)", output_path, len(df))
    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Transform job data with schema alignment.")
    parser.add_argument("--input", required=True, help="Path to raw snapshot CSV.")
    parser.add_argument("--output", required=True, help="Destination for cleaned CSV.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for deterministic steps.")
    return parser.parse_args()


def main():
    args = parse_args()
    transform(Path(args.input), Path(args.output), seed=args.seed)


if __name__ == "__main__":
    main()
