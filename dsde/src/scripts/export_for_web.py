
import sys
from pathlib import Path
import pandas as pd
import shutil

# Add project root to path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BASE_DIR))

from src.config import PROCESSED_DIR, ARTIFACTS_DIR

WEB_ARTIFACTS_DIR = BASE_DIR.parent / "web" / "public" / "artifacts"

def export_jobs_lite():
    print(f"Loading jobs from {PROCESSED_DIR}...")
    # Load canonical parquet
    parquet_path = PROCESSED_DIR / "jobs_canonical.parquet"
    if not parquet_path.exists():
        print("Canonical parquet not found. Trying sample.")
        parquet_path = PROCESSED_DIR / "jobs_canonical_sample.parquet"
    
    if not parquet_path.exists():
        print("No job data found!")
        return

    df = pd.read_parquet(parquet_path)
    
    # Process similar to app_streamlit.py
    if "description_text" in df.columns:
        df.drop(columns=["description_text"], inplace=True)
    
    # Select cols for web
    cols = ["title", "company", "location_text", "skills_display", "published_at", "salary_min", "salary_max", "source"]
    # Ensure cols exist
    existing_cols = [c for c in cols if c in df.columns]
    df = df[existing_cols]
    
    # Sort by date (descending) and take top 5000
    if "published_at" in df.columns:
        df["published_at"] = pd.to_datetime(df["published_at"], utc=True)
        df = df.sort_values("published_at", ascending=False)
    
    df_lite = df.head(5000)
    
    # Export
    output_path = WEB_ARTIFACTS_DIR / "jobs_lite.csv"
    WEB_ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    
    print(f"Exporting {len(df_lite)} jobs to {output_path}...")
    df_lite.to_csv(output_path, index=False)
    print("Done.")

def copy_artifacts():
    # Copy other artifacts from dsde/artifacts to web/public/artifacts
    artifacts_to_copy = [
        "kpi_summary.json",
        "top_titles.csv",
        "top_skills.csv",
        "source_counts.csv",
        "demo_recs.json",
        "demo_profiles.json",
        "graphs/skill_graph.json"
    ]
    
    for item in artifacts_to_copy:
        src = ARTIFACTS_DIR / item
        dst = WEB_ARTIFACTS_DIR / item
        if src.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(src, dst)
            print(f"Copied {item} to {dst}")
        else:
            print(f"Warning: {item} not found in artifacts.")

if __name__ == "__main__":
    export_jobs_lite()
    copy_artifacts()
