import argparse
import json
from pathlib import Path
from typing import List, Dict

import joblib
import pandas as pd
from scipy import sparse

from src.config import ARTIFACTS_DIR, PROCESSED_DIR, SEED
from src.models.recommender import build_tfidf_index, recommend, load_jobs
from src.utils.io import safe_mkdir
from src.utils.logging import get_logger

logger = get_logger(__name__)


DEMO_PROFILES = [
    {"name": "Data Engineer", "profile": "data engineer cloud pipelines spark airflow snowflake kafka aws python sql"},
    {"name": "Data Analyst", "profile": "data analyst dashboards sql excel tableau business intelligence reporting"},
    {"name": "Data Scientist", "profile": "data scientist machine learning python pandas sklearn nlp deep learning"},
]


def train(input_path: Path, model_dir: Path, top_k: int = 10) -> Dict[str, Path]:
    df = load_jobs(input_path)
    if df.empty:
        raise ValueError(f"Jobs dataframe empty at {input_path}")

    vectorizer, matrix = build_tfidf_index(df)

    safe_mkdir(model_dir)
    joblib.dump(vectorizer, model_dir / "vectorizer.joblib")
    sparse.save_npz(model_dir / "matrix.npz", matrix)
    df[["job_id", "title", "company", "source", "source_url", "skills_text", "description_text"]].to_parquet(
        model_dir / "jobs_index.parquet", index=False
    )
    logger.info("Saved recommender artifacts to %s", model_dir)

    demo_profiles_path = ARTIFACTS_DIR / "demo_profiles.json"
    with open(demo_profiles_path, "w") as f:
        json.dump(DEMO_PROFILES, f, indent=2)

    demo_recs = {}
    for profile in DEMO_PROFILES:
        recs = recommend(profile["profile"], vectorizer, matrix, df, top_k=top_k)
        demo_recs[profile["name"]] = recs
    demo_recs_path = ARTIFACTS_DIR / "demo_recs.json"
    with open(demo_recs_path, "w") as f:
        json.dump(demo_recs, f, indent=2)

    logger.info("Demo profiles saved to %s and demo recs saved to %s", demo_profiles_path, demo_recs_path)
    return {
        "vectorizer": model_dir / "vectorizer.joblib",
        "matrix": model_dir / "matrix.npz",
        "jobs_index": model_dir / "jobs_index.parquet",
        "demo_profiles": demo_profiles_path,
        "demo_recs": demo_recs_path,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train TF-IDF recommender and emit demo outputs.")
    parser.add_argument("--input", default=PROCESSED_DIR / "jobs_canonical.parquet", help="Canonical jobs parquet.")
    parser.add_argument("--model_dir", default=ARTIFACTS_DIR / "recommender", help="Directory for recommender artifacts.")
    parser.add_argument("--top_k", type=int, default=10, help="Recommendations per profile.")
    parser.add_argument("--seed", type=int, default=SEED, help="Random seed.")
    return parser.parse_args()


def main():
    args = parse_args()
    train(Path(args.input), Path(args.model_dir), top_k=args.top_k)


if __name__ == "__main__":
    main()
