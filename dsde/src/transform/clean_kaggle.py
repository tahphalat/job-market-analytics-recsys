import argparse
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Tuple, List

import pandas as pd

from src.config import PROCESSED_DIR, RAW_KAGGLE_DIR, SEED
from src.transform.column_map import ALIAS_MAP, resolve_column, pick_first_existing_column
from src.transform.skill_normalize import normalize_skills
from src.utils.io import read_auto, safe_mkdir
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


def parse_datetime_series(series: pd.Series) -> pd.Series:
    if series is None:
        return pd.Series(dtype="datetime64[ns, UTC]")
    numeric = pd.to_numeric(series, errors="coerce")
    # If values look like ms timestamps, convert with unit="ms"
    if numeric.notna().any() and numeric.dropna().abs().median() > 1e12:
        return pd.to_datetime(numeric, unit="ms", errors="coerce", utc=True)
    return pd.to_datetime(series, errors="coerce", utc=True)


def parse_salary(series_min: pd.Series, series_max: pd.Series, salary_text: pd.Series) -> Tuple[pd.Series, pd.Series, pd.Series]:
    sal_min = pd.to_numeric(series_min, errors="coerce")
    sal_max = pd.to_numeric(series_max, errors="coerce")
    text = salary_text.fillna("")
    return sal_min, sal_max, text


def extract_country(location_series: pd.Series) -> pd.Series:
    def _country(loc: str) -> Optional[str]:
        if not isinstance(loc, str):
            return None
        parts = [p.strip() for p in loc.split(",") if p.strip()]
        return parts[-1] if parts else None

    return location_series.apply(_country)


def build_skills(df: pd.DataFrame) -> Tuple[pd.Series, pd.Series]:
    skills_series = pick_first_existing_column(df, ALIAS_MAP["skills"])
    lists: List[List[str]] = []
    for val in (skills_series if skills_series is not None else []):
        if isinstance(val, str):
            tokens = [t.strip() for t in val.replace(";", ",").split(",") if t.strip()]
        elif isinstance(val, list):
            tokens = val
        else:
            tokens = []
        lists.append(normalize_skills(tokens))
    if not lists:
        lists = [[] for _ in range(len(df))]
    skills_text = pd.Series([", ".join(lst) if lst else "" for lst in lists])
    return pd.Series(lists, dtype=object), skills_text


def compute_job_id(source: str, source_job_id: Optional[str], source_url: Optional[str], title: str, company: str, location: str) -> str:
    def safe(val) -> str:
        if val is None or pd.isna(val):
            return ""
        return str(val)

    base = "|".join(
        [
            safe(source),
            safe(source_job_id),
            safe(source_url),
            safe(title),
            safe(company),
            safe(location),
        ]
    )
    return hashlib.sha1(base.encode("utf-8")).hexdigest()


def load_skills_data(base_dir: Path) -> pd.DataFrame:
    """Load and join job_skills.csv with mappings/skills.csv"""
    try:
        # Try to locate files relative to base_dir
        # Structure is usually: .../kaggle/ -> jobs/job_skills.csv, mappings/skills.csv
        # But input_path might be .../kaggle/jobs_kaggle_raw.parquet
        root = base_dir.parent if base_dir.is_file() else base_dir
        
        # Look for jobs/job_skills.csv
        job_skills_path = root / "jobs" / "job_skills.csv"
        if not job_skills_path.exists():
             # Fallback: check if they are in same dir
             job_skills_path = root / "job_skills.csv"
             
        mapping_path = root / "mappings" / "skills.csv"
        
        if not job_skills_path.exists() or not mapping_path.exists():
            logger.warning("Skills auxiliary files not found at %s. Skills will be empty.", root)
            return pd.DataFrame(columns=["job_id", "skill_name"])
            
        js_df = pd.read_csv(job_skills_path)
        map_df = pd.read_csv(mapping_path)
        
        # Merge to get names
        merged = js_df.merge(map_df, on="skill_abr", how="left")
        merged["skill_name"] = merged["skill_name"].fillna(merged["skill_abr"]) # Fallback to abr
        
        return merged[["job_id", "skill_name"]]
    except Exception as e:
        logger.warning("Failed to load skills data: %s", e)
        return pd.DataFrame(columns=["job_id", "skill_name"])

def clean_kaggle(input_path: Path, output_path: Path, seed: int) -> Path:
    try:
        df = read_auto(input_path)
    except Exception as exc:
        fallback = input_path.with_suffix(".csv")
        if fallback.exists():
            logger.warning("Failed to read %s (%s); falling back to %s", input_path, exc, fallback)
            df = read_auto(fallback)
        else:
            raise
    logger.info("Kaggle raw rows=%s cols=%s", len(df), len(df.columns))

    out = pd.DataFrame(index=df.index)
    out["source"] = pd.Series(["kaggle"] * len(df), index=df.index)
    # job_id in raw is typically integers (e.g. 3884428798). Ensure it matches job_skills.csv
    out["source_job_id"] = pick_first_existing_column(df, ["job_id"]).astype("Int64").astype(str)
    
    out["source_url"] = resolve_column(df, ALIAS_MAP["source_url"], default=None)
    out["title"] = resolve_column(df, ALIAS_MAP["title"], default=None)
    out["company"] = resolve_column(df, ALIAS_MAP["company"], default=None)
    out["location_text"] = resolve_column(df, ALIAS_MAP["location_text"], default=None)
    out["country"] = extract_country(out["location_text"])
    out["description_text"] = resolve_column(df, ALIAS_MAP["description_text"], default=None)

    # --- Skills Merging ---
    # 1. Load external skills
    skills_df = load_skills_data(input_path)
    # 2. Group by job_id
    if not skills_df.empty:
        # skills_df job_id might be int, source_job_id is str. convert for join
        skills_df["job_str"] = skills_df["job_id"].astype(str)
        grouped = skills_df.groupby("job_str")["skill_name"].apply(lambda x: sorted(list(set(x))))
        # 3. Map to main df
        out["skills"] = out["source_job_id"].map(grouped)
        # Fill NaNs with empty list
        out["skills"] = out["skills"].apply(lambda x: x if isinstance(x, list) else [])
    else:
        # Fallback to internal column (likely empty now that we removed skills_desc)
        skills_list, _ = build_skills(df)
        out["skills"] = skills_list

    out["skills_text"] = out["skills"].apply(lambda x: ", ".join(x) if x else "")

    salary_min, salary_max, salary_text = parse_salary(
        df.get("min_salary", pd.Series([None] * len(df))),
        df.get("max_salary", pd.Series([None] * len(df))),
        resolve_column(df, ALIAS_MAP["salary_text"], default=None),
    )
    out["salary_text"] = salary_text
    out["salary_min"] = salary_min
    out["salary_max"] = salary_max

    out["published_at"] = parse_datetime_series(resolve_column(df, ALIAS_MAP["published_at"], default=None))
    out["ingested_at"] = datetime.now(timezone.utc).isoformat()

    out["job_id"] = [
        compute_job_id("kaggle", sjid if sjid != "<NA>" else None, url, title or "", company or "", loc or "")
        for sjid, url, title, company, loc in zip(out["source_job_id"], out["source_url"], out["title"], out["company"], out["location_text"])
    ]

    out = out[CANONICAL_COLUMNS]
    safe_mkdir(output_path.parent)
    out.to_parquet(output_path, index=False)
    logger.info("Saved Kaggle clean to %s (rows=%s)", output_path, len(out))
    return output_path

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Clean Kaggle raw jobs into canonical schema.")
    parser.add_argument("--input", default=RAW_KAGGLE_DIR / "jobs_kaggle_raw.parquet", help="Path to Kaggle raw parquet.")
    parser.add_argument("--output", default=PROCESSED_DIR / "jobs_kaggle_clean.parquet", help="Path for cleaned output.")
    parser.add_argument("--seed", type=int, default=SEED, help="Random seed.")
    return parser.parse_args()

def main():
    args = parse_args()
    clean_kaggle(Path(args.input), Path(args.output), seed=args.seed)

if __name__ == "__main__":
    main()
