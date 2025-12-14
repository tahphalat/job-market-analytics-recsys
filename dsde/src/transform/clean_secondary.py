import argparse
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import pandas as pd

from src.config import PROCESSED_DIR, RAW_KAGGLE_DIR, SEED
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

def clean_secondary(input_path: Path, output_path: Path, seed: int) -> Path:
    # 1. Detection/Read
    try:
        # The secondary fetcher puts files in data/raw/kaggle/secondary
        # We need to find the CSV. It's usually a single file in the dir or subdirs.
        # But this function takes input_path. 
        # If input_path is a directory, find the csv.
        if input_path.is_dir():
            candidates = list(input_path.rglob("*.csv")) + list(input_path.rglob("*.parquet"))
            if not candidates:
                 raise FileNotFoundError(f"No data files found in {input_path}")
            target_file = candidates[0] # Pick first
        else:
            target_file = input_path

        df = read_auto(target_file)
    except Exception as exc:
        logger.error("Failed to read secondary data: %s", exc)
        return Path() # Return empty path to signal failure/skip

    logger.info("Secondary Kaggle raw rows=%s cols=%s", len(df), len(df.columns))
    
    # 2. Map Columns (Ad-hoc based on common Kaggle schemas, adjust if known)
    # The 'yusifmohammed/data-engineering-job-postings' dataset typically has:
    # 'Job Title', 'Company Name', 'Location', 'Job Description', 'Skills' possibly
    # We'll normalize broadly.
    
    out = pd.DataFrame(index=df.index)
    
    # Heuristic column mapping
    def get_col(candidates):
        for c in candidates:
            for col in df.columns:
                if c.lower() in col.lower():
                    return df[col]
        return pd.Series([None]*len(df), index=df.index)

    out["title"] = get_col(["Job Title", "title", "role"])
    out["company"] = get_col(["Company Name", "company"])
    out["location_text"] = get_col(["Location", "city", "country"])
    out["description_text"] = get_col(["Job Description", "description", "summary"])
    
    # 3. Source metadata
    out["source"] = "kaggle_secondary"
    out["source_url"] = None 
    out["source_job_id"] = None

    # 4. Skills extraction
    # If there's a skills column, use it, else raw text analysis (not implemented deep here)
    raw_skills = get_col(["Skills", "Key Skills", "Tags"])
    
    skill_lists = []
    for val in raw_skills.fillna(""):
        tokens = str(val).split(",") 
        skill_lists.append(normalize_skills(tokens))
    
    out["skills"] = skill_lists
    out["skills_text"] = out["skills"].apply(lambda x: ", ".join(x))

    # 5. Salary (Placeholders)
    out["salary_min"] = None
    out["salary_max"] = None
    out["salary_text"] = get_col(["Salary", "Pay"])
    
    # 6. Dates
    out["published_at"] = pd.to_datetime(get_col(["Date", "Posted"]), errors='coerce', utc=True)
    out["ingested_at"] = datetime.now(timezone.utc).isoformat()
    
    # 7. IDs extraction
    out["source"] = "kaggle_secondary"
    out["country"] = None # Simple parse skipped

    def make_id(row):
        base = f"{row['title']}|{row['company']}|{str(row['published_at'])}"
        return hashlib.sha1(base.encode()).hexdigest()
        
    out["job_id"] = out.apply(make_id, axis=1)

    # Filter to Canonical
    for col in CANONICAL_COLUMNS:
        if col not in out.columns:
            out[col] = None
    
    out = out[CANONICAL_COLUMNS]
    
    # 8. Save
    safe_mkdir(output_path.parent)
    out.to_parquet(output_path, index=False)
    logger.info("Saved Secondary Clean to %s (rows=%s)", output_path, len(out))
    return output_path

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Clean Secondary Kaggle dataset.")
    parser.add_argument("--input", default=RAW_KAGGLE_DIR / "secondary", help="Path to raw input dir or file.")
    parser.add_argument("--output", default=PROCESSED_DIR / "jobs_secondary_clean.parquet", help="Path for cleaned output.")
    parser.add_argument("--seed", type=int, default=SEED, help="Random seed.")
    return parser.parse_args()

def main():
    args = parse_args()
    clean_secondary(Path(args.input), Path(args.output), seed=args.seed)

if __name__ == "__main__":
    main()
