import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

import pandas as pd

from src.config import ARTIFACTS_DIR, PROCESSED_DIR, SEED
from src.utils.io import safe_mkdir, write_json
from src.utils.logging import get_logger

logger = get_logger(__name__)


def load_jobs(path: Path) -> pd.DataFrame:
    if not path.exists():
        logger.warning("Canonical jobs not found at %s, building empty dataframe", path)
        return pd.DataFrame()
    try:
        return pd.read_parquet(path)
    except Exception as exc:
        csv_fallback = path.with_suffix(".csv")
        if csv_fallback.exists():
            logger.warning("Failed to read %s (%s); falling back to %s", path, exc, csv_fallback)
            return pd.read_csv(csv_fallback)
        logger.warning("Failed to read %s (%s); returning empty dataframe", path, exc)
        return pd.DataFrame()


def top_counts(series: pd.Series, n: int = 50) -> pd.DataFrame:
    if series is None or series.empty:
        return pd.DataFrame(columns=["value", "count"])
    vc = series.dropna().astype(str).str.strip()
    vc = vc[vc != ""]
    df = vc.value_counts().head(n).reset_index()
    df.columns = ["value", "count"]
    return df


def flatten_skills(df: pd.DataFrame) -> pd.Series:
    if "skills" not in df.columns or df.empty:
        return pd.Series(dtype=object)
    flattened: List[str] = []
    for items in df["skills"]:
        if isinstance(items, list):
            for it in items:
                if it and isinstance(it, str) and it.strip():
                    flattened.append(it.strip())
        elif isinstance(items, str) and items.strip():
            flattened.extend([t.strip() for t in items.split(",") if t.strip()])
    return pd.Series(flattened)


def build_tables(input_path: Path) -> Dict[str, Path]:
    df = load_jobs(input_path)
    outputs: Dict[str, Path] = {}

    # KPI summary
    total_jobs = int(len(df))
    unique_companies = int(df["company"].nunique(dropna=True)) if not df.empty and "company" in df.columns else 0
    source_counts = df["source"].value_counts().to_dict() if not df.empty and "source" in df.columns else {}
    source_counts = {k: int(v) for k, v in source_counts.items()}
    top_locations_list: List[Dict] = []
    loc_df = top_counts(df["location_text"], n=10) if "location_text" in df.columns else pd.DataFrame()
    for _, row in loc_df.iterrows():
        top_locations_list.append({"location_text": row["value"], "count": int(row["count"])})

    kpi = {
        "total_jobs": total_jobs,
        "unique_companies": unique_companies,
        "sources": {s: source_counts.get(s, 0) for s in ["kaggle", "remotive"]},
        "top_locations": top_locations_list,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    kpi_path = ARTIFACTS_DIR / "kpi_summary.json"
    write_json(kpi, kpi_path)
    outputs["kpi_summary"] = kpi_path

    # Top titles
    titles_df = top_counts(df["title"], n=50) if "title" in df.columns else pd.DataFrame(columns=["value", "count"])
    titles_path = ARTIFACTS_DIR / "top_titles.csv"
    safe_mkdir(titles_path.parent)
    titles_df.to_csv(titles_path, index=False)
    outputs["top_titles"] = titles_path

    # Top skills
    skills_series = flatten_skills(df)
    skills_df = top_counts(skills_series, n=50)
    skills_path = ARTIFACTS_DIR / "top_skills.csv"
    skills_df.to_csv(skills_path, index=False)
    outputs["top_skills"] = skills_path

    # Source counts
    source_df = top_counts(df["source"], n=10) if "source" in df.columns else pd.DataFrame(columns=["value", "count"])
    source_df.rename(columns={"value": "source"}, inplace=True)
    source_path = ARTIFACTS_DIR / "source_counts.csv"
    source_df.to_csv(source_path, index=False)
    outputs["source_counts"] = source_path

    # Location counts (top 50)
    loc_df_full = top_counts(df["location_text"], n=50) if "location_text" in df.columns else pd.DataFrame(columns=["value", "count"])
    loc_df_full.rename(columns={"value": "location_text"}, inplace=True)
    loc_path = ARTIFACTS_DIR / "location_counts.csv"
    loc_df_full.to_csv(loc_path, index=False)
    outputs["location_counts"] = loc_path

    logger.info("Built analytics tables: %s", outputs)
    return outputs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build analytics summary tables for web consumption.")
    parser.add_argument("--input", default=PROCESSED_DIR / "jobs_canonical.parquet", help="Path to canonical jobs parquet.")
    parser.add_argument("--seed", type=int, default=SEED, help="Random seed (unused, for determinism).")
    return parser.parse_args()


def main():
    args = parse_args()
    build_tables(Path(args.input))


if __name__ == "__main__":
    main()
