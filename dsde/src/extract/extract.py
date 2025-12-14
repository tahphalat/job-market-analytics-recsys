import argparse
from pathlib import Path
from typing import Optional

import pandas as pd

from src.utils.common import ensure_parent, set_seed
from src.utils.logging import get_logger

logger = get_logger(__name__)


def extract(input_path: Path, output_path: Path, seed: int, limit: Optional[int] = None) -> Path:
    set_seed(seed)
    df = pd.read_csv(input_path)
    logger.info("Detected columns: %s", list(df.columns))
    if limit:
        df = df.sample(n=min(limit, len(df)), random_state=seed)
        logger.info("Sampled %s rows for quick runs", len(df))
    output_path = ensure_parent(output_path)
    df.to_csv(output_path, index=False)
    logger.info("Saved raw snapshot to %s (rows=%s)", output_path, len(df))
    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract raw job data.")
    parser.add_argument("--input", required=True, help="Path to the source CSV.")
    parser.add_argument("--output", required=True, help="Destination for the raw snapshot CSV.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for sampling.")
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional row cap for development runs (after shuffling).",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    extract(Path(args.input), Path(args.output), seed=args.seed, limit=args.limit)


if __name__ == "__main__":
    main()
