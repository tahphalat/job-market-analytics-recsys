import argparse
from pathlib import Path
from typing import Optional

import pandas as pd
from sqlalchemy import create_engine

from utils.common import ensure_parent, set_seed
from utils.logging import get_logger

logger = get_logger(__name__)


def load(
    input_path: Path, output_path: Path, seed: int, sqlite_path: Optional[Path] = None
) -> Path:
    set_seed(seed)
    df = pd.read_csv(input_path)
    output_path = ensure_parent(output_path)
    df.to_csv(output_path, index=False)
    logger.info("Persisted processed CSV to %s (rows=%s)", output_path, len(df))

    if sqlite_path:
        sqlite_path = ensure_parent(sqlite_path)
        engine = create_engine(f"sqlite:///{sqlite_path}")
        df.to_sql("jobs", con=engine, if_exists="replace", index=False)
        logger.info("Loaded data into sqlite table 'jobs' at %s", sqlite_path)

    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Load processed data to storage targets.")
    parser.add_argument("--input", required=True, help="Path to cleaned CSV.")
    parser.add_argument("--output", required=True, help="Destination CSV for downstream tasks.")
    parser.add_argument("--sqlite", default=None, help="Optional sqlite path for persistence.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed.")
    return parser.parse_args()


def main():
    args = parse_args()
    sqlite_path = Path(args.sqlite) if args.sqlite else None
    load(Path(args.input), Path(args.output), seed=args.seed, sqlite_path=sqlite_path)


if __name__ == "__main__":
    main()
