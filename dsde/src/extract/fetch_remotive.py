import argparse
import json
import time
from datetime import datetime
from pathlib import Path

import pandas as pd
import requests

from src.config import RAW_REMOTIVE_DIR, REMOTIVE_API_URL, SAMPLE_N, SEED
from src.utils.common import set_seed
from src.utils.logging import get_logger

logger = get_logger(__name__)


def fetch_remotive(api_url: str, out_dir: Path, sample_n: int, seed: int) -> None:
    set_seed(seed)
    out_dir.mkdir(parents=True, exist_ok=True)

    max_attempts = 3
    backoff = 2
    data = None
    for attempt in range(1, max_attempts + 1):
        try:
            resp = requests.get(api_url, timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                break
            logger.warning("Attempt %s failed with status %s", attempt, resp.status_code)
        except requests.RequestException as exc:
            logger.warning("Attempt %s failed: %s", attempt, exc)
        time.sleep(backoff * attempt)

    if data is None:
        raise RuntimeError("Failed to fetch Remotive API after retries.")

    fetched_at = datetime.utcnow().isoformat() + "Z"
    raw_path = out_dir / "remotive_raw.json"
    with open(raw_path, "w") as f:
        json.dump({"fetched_at": fetched_at, "payload": data}, f, indent=2)
    logger.info("Saved raw Remotive JSON to %s", raw_path)

    jobs = data.get("jobs", [])
    df = pd.json_normalize(jobs)
    df["source"] = "remotive"
    df["fetched_at"] = fetched_at

    parquet_path = out_dir / "jobs_remotive_raw.parquet"
    sample_path = out_dir / "jobs_remotive_raw.sample.csv"

    df.to_parquet(parquet_path, index=False)
    logger.info("Saved Remotive parquet to %s (rows=%s, cols=%s)", parquet_path, len(df), len(df.columns))

    sample_n = min(sample_n, len(df)) if sample_n else len(df)
    sample_df = df.sample(n=sample_n, random_state=seed) if sample_n else df
    sample_df.to_csv(sample_path, index=False)
    logger.info("Saved Remotive sample (%s rows) to %s", len(sample_df), sample_path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch Remotive API and persist raw/sample data.")
    parser.add_argument("--api_url", default=REMOTIVE_API_URL, help="Remotive endpoint URL.")
    parser.add_argument("--out_dir", default=RAW_REMOTIVE_DIR, help="Directory to store outputs.")
    parser.add_argument("--sample_n", type=int, default=SAMPLE_N, help="Sample size for preview CSV.")
    parser.add_argument("--seed", type=int, default=SEED, help="Random seed for sampling.")
    return parser.parse_args()


def main():
    args = parse_args()
    fetch_remotive(args.api_url, Path(args.out_dir), sample_n=args.sample_n, seed=args.seed)


if __name__ == "__main__":
    main()
