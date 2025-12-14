import argparse
import hashlib
from pathlib import Path
from typing import Optional

import pandas as pd

from src.config import PROCESSED_DIR, SEED, ARTIFACTS_DIR
from src.transform.skill_normalize import export_skill_aliases
from src.utils.io import safe_mkdir
from src.utils.logging import get_logger

logger = get_logger(__name__)

CANONICAL_COLUMNS = [
    "job_id",
    "source",
    "source_job_id",
    "source_url",
    "title",
    "company",
    "location_text",
    "country",
    "description_text",
    "skills",
    "skills_text",
    "salary_text",
    "salary_min",
    "salary_max",
    "published_at",
    "ingested_at",
]


def normalize_key(title: str, company: str, location: str) -> str:
    parts = [title or "", company or "", location or ""]
    parts = [p.strip().lower() for p in parts]
    return "|".join(parts)


def dedupe(df: pd.DataFrame) -> pd.DataFrame:
    # Priority dedupe by source_url, else by normalized title/company/location
    df = df.copy()
    df["dedupe_key"] = df["source_url"].fillna("").astype(str)
    df["fallback_key"] = df.apply(lambda r: normalize_key(r["title"], r["company"], r["location_text"]), axis=1)

    def pick_first(group: pd.DataFrame, key_col: str) -> pd.DataFrame:
        return group.sort_index().drop_duplicates(subset=[key_col], keep="first")

    with_url = df[df["dedupe_key"] != ""]
    without_url = df[df["dedupe_key"] == ""]
    deduped = pd.concat(
        [
            pick_first(with_url, "dedupe_key"),
            pick_first(without_url, "fallback_key"),
        ],
        ignore_index=True,
    )
    return deduped.drop(columns=["dedupe_key", "fallback_key"])


def ensure_job_id(df: pd.DataFrame) -> pd.Series:
    def safe_str(val: Optional[str]) -> str:
        if val is None:
            return ""
        if pd.isna(val):
            return ""
        return str(val)

    def make_id(row) -> str:
        parts = [
            safe_str(row.get("source")),
            safe_str(row.get("source_job_id")),
            safe_str(row.get("source_url")),
            safe_str(row.get("title")),
            safe_str(row.get("company")),
            safe_str(row.get("location_text")),
        ]
        base = "|".join(parts)
        return hashlib.sha1(base.encode("utf-8")).hexdigest()

    return df.apply(make_id, axis=1)


def build_canonical(kaggle_path: Path, remotive_path: Path, output_path: Path, seed: int) -> Path:
    pd.set_option("mode.copy_on_write", True)
    dfs = []
    for path in [kaggle_path, remotive_path]:
        if path.exists():
            dfs.append(pd.read_parquet(path))
        else:
            logger.warning("Missing input for canonical build: %s", path)
    if not dfs:
        raise FileNotFoundError("No cleaned job tables found for canonical build.")

    df = pd.concat(dfs, ignore_index=True)
    df = dedupe(df)
    df["job_id"] = ensure_job_id(df)
    df = df[CANONICAL_COLUMNS]

    safe_mkdir(output_path.parent)
    df.to_parquet(output_path, index=False)
    # Also persist CSV for downstream fallbacks
    csv_path = output_path.with_suffix(".csv")
    df.to_csv(csv_path, index=False)
    export_skill_aliases()  # ensure aliases file exists for downstream
    logger.info(
        "Canonical jobs saved to %s and %s (rows=%s sources=%s)",
        output_path,
        csv_path,
        len(df),
        df["source"].value_counts().to_dict(),
    )
    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build canonical jobs table from Kaggle + Remotive clean tables.")
    parser.add_argument("--kaggle", default=PROCESSED_DIR / "jobs_kaggle_clean.parquet", help="Path to Kaggle clean parquet.")
    parser.add_argument("--remotive", default=PROCESSED_DIR / "jobs_remotive_clean.parquet", help="Path to Remotive clean parquet.")
    parser.add_argument("--output", default=PROCESSED_DIR / "jobs_canonical.parquet", help="Output canonical parquet.")
    parser.add_argument("--seed", type=int, default=SEED, help="Random seed.")
    return parser.parse_args()


def main():
    args = parse_args()
    build_canonical(Path(args.kaggle), Path(args.remotive), Path(args.output), seed=args.seed)


if __name__ == "__main__":
    main()
