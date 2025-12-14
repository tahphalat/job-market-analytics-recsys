import argparse
import hashlib
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Tuple, List
from html import unescape

import pandas as pd

from src.config import PROCESSED_DIR, RAW_REMOTIVE_DIR, SEED
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


def strip_html(text: Optional[str]) -> str:
    if not isinstance(text, str):
        return ""
    clean = re.sub(r"<[^>]+>", " ", text)
    clean = re.sub(r"\s+", " ", clean)
    return unescape(clean).strip()


def parse_salary_text(salary_text: pd.Series) -> Tuple[pd.Series, pd.Series, pd.Series]:
    text = salary_text.fillna("")

    def extract_range(s: str) -> Tuple[Optional[float], Optional[float]]:
        numbers = re.findall(r"[0-9]+(?:[.,][0-9]+)?", s.replace(",", ""))
        if not numbers:
            return None, None
        vals = [float(n.replace(",", "")) for n in numbers]
        if len(vals) == 1:
            return vals[0], vals[0]
        return min(vals), max(vals)

    mins, maxs = zip(*(extract_range(t) for t in text))
    return text, pd.Series(mins), pd.Series(maxs)


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
        if isinstance(val, list):
            tokens = val
        elif isinstance(val, str):
            tokens = [t.strip() for t in val.replace(";", ",").split(",") if t.strip()]
        else:
            tokens = []
        lists.append(normalize_skills(tokens))
    if not lists:
        lists = [[] for _ in range(len(df))]
    skills_text = pd.Series([", ".join(lst) if lst else "" for lst in lists])
    return pd.Series(lists, dtype=object), skills_text


def compute_job_id(source: str, source_job_id: Optional[str], source_url: Optional[str], title: str, company: str, location: str) -> str:
    base = source + "|" + (source_job_id or "") + "|" + (source_url or "") + "|" + (title or "") + "|" + (company or "") + "|" + (location or "")
    return hashlib.sha1(base.encode("utf-8")).hexdigest()


def clean_remotive(input_path: Path, output_path: Path, seed: int) -> Path:
    try:
        df = read_auto(input_path)
    except Exception as exc:
        csv_fallback = input_path.with_suffix(".csv")
        if csv_fallback.exists():
            logger.warning("Failed to read %s (%s); falling back to %s", input_path, exc, csv_fallback)
            df = read_auto(csv_fallback)
        else:
            raw_json = RAW_REMOTIVE_DIR / "remotive_raw.json"
            if raw_json.exists():
                logger.warning("Failed to read %s (%s); rebuilding from %s", input_path, exc, raw_json)
                import json

                with open(raw_json) as f:
                    payload = json.load(f)
                jobs = payload.get("payload", {}).get("jobs", []) or payload.get("jobs", [])
                df = pd.json_normalize(jobs)
            else:
                raise
    logger.info("Remotive raw rows=%s cols=%s", len(df), len(df.columns))

    out = pd.DataFrame(index=df.index)
    out["source"] = pd.Series(["remotive"] * len(df), index=df.index)
    out["source_job_id"] = pick_first_existing_column(df, ["id"]).astype("Int64").astype(str)
    out["source_url"] = resolve_column(df, ALIAS_MAP["source_url"], default=None)
    out["title"] = resolve_column(df, ALIAS_MAP["title"], default=None)
    out["company"] = resolve_column(df, ALIAS_MAP["company"], default=None)
    out["location_text"] = resolve_column(df, ALIAS_MAP["location_text"], default=None)
    out["country"] = extract_country(out["location_text"])

    desc_series = resolve_column(df, ALIAS_MAP["description_text"], default=None)
    out["description_text"] = desc_series.apply(strip_html)

    skills_list, skills_text = build_skills(df)
    out["skills"] = skills_list
    out["skills_text"] = skills_text

    salary_text = resolve_column(df, ALIAS_MAP["salary_text"], default=None)
    salary_text, salary_min, salary_max = parse_salary_text(salary_text)
    out["salary_text"] = salary_text
    out["salary_min"] = salary_min
    out["salary_max"] = salary_max

    out["published_at"] = pd.to_datetime(resolve_column(df, ALIAS_MAP["published_at"], default=None), errors="coerce", utc=True)
    out["ingested_at"] = datetime.now(timezone.utc).isoformat()

    out["job_id"] = [
        compute_job_id("remotive", sjid if sjid != "<NA>" else None, url, title or "", company or "", loc or "")
        for sjid, url, title, company, loc in zip(out["source_job_id"], out["source_url"], out["title"], out["company"], out["location_text"])
    ]

    out = out[CANONICAL_COLUMNS]
    safe_mkdir(output_path.parent)
    out.to_parquet(output_path, index=False)
    logger.info("Saved Remotive clean to %s (rows=%s)", output_path, len(out))
    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Clean Remotive raw jobs into canonical schema.")
    parser.add_argument("--input", default=RAW_REMOTIVE_DIR / "jobs_remotive_raw.parquet", help="Path to Remotive raw parquet.")
    parser.add_argument("--output", default=PROCESSED_DIR / "jobs_remotive_clean.parquet", help="Path for cleaned output.")
    parser.add_argument("--seed", type=int, default=SEED, help="Random seed.")
    return parser.parse_args()


def main():
    args = parse_args()
    clean_remotive(Path(args.input), Path(args.output), seed=args.seed)


if __name__ == "__main__":
    main()
