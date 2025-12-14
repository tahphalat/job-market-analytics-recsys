import argparse
from pathlib import Path
from typing import Optional

import pandas as pd

from src.config import RAW_KAGGLE_DIR, SAMPLE_N, SEED
from src.utils.common import set_seed
from src.utils.io import read_csv_or_parquet
from src.utils.logging import get_logger

logger = get_logger(__name__)


def _auto_detect_file(out_dir: Path) -> Optional[Path]:
    candidates = list(out_dir.glob("*.csv")) + list(out_dir.glob("*.parquet"))
    return candidates[0] if candidates else None


def ingest_kaggle_file(input_path: Optional[Path], out_dir: Path, sample_n: int, seed: int) -> None:
    set_seed(seed)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = input_path or _auto_detect_file(out_dir)
    if path is None:
        raise FileNotFoundError(f"No CSV/Parquet found in {out_dir}. Specify --input_path.")

    df = read_csv_or_parquet(path)
    logger.info("Loaded Kaggle file %s with rows=%s cols=%s", path, len(df), len(df.columns))
    logger.info("Columns: %s", list(df.columns)[:15])

    ext = path.suffix.lower()
    raw_out = out_dir / f"jobs_kaggle_raw{ext}"
    sample_out = out_dir / "jobs_kaggle_raw.sample.csv"

    if ext == ".parquet":
        df.to_parquet(raw_out, index=False)
    else:
        df.to_csv(raw_out, index=False)
    logger.info("Saved full Kaggle raw to %s", raw_out)

    sample_n = min(sample_n, len(df)) if sample_n else len(df)
    sample_df = df.sample(n=sample_n, random_state=seed) if sample_n else df
    sample_df.to_csv(sample_out, index=False)
    logger.info("Saved Kaggle sample (%s rows) to %s", len(sample_df), sample_out)

    summary = {
        "rows": int(len(df)),
        "cols": int(len(df.columns)),
        "head": df.head(3).to_dict(orient="records"),
    }
    logger.info("Summary: %s", summary)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ingest Kaggle dataset file (csv/parquet).")
    parser.add_argument("--input_path", default=None, help="Path to Kaggle file (csv/parquet). If omitted, auto-detects first CSV/Parquet in out_dir.")
    parser.add_argument("--out_dir", default=RAW_KAGGLE_DIR, help="Directory to write raw outputs.")
    parser.add_argument("--sample_n", type=int, default=SAMPLE_N, help="Sample size for preview CSV.")
    parser.add_argument("--seed", type=int, default=SEED, help="Random seed for sampling.")
    return parser.parse_args()


def main():
    args = parse_args()
    path = Path(args.input_path) if args.input_path else None
    ingest_kaggle_file(path, Path(args.out_dir), sample_n=args.sample_n, seed=args.seed)


if __name__ == "__main__":
    main()
