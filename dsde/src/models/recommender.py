import argparse
import json
from pathlib import Path
from typing import List, Dict, Any

import joblib
import numpy as np
import pandas as pd
from scipy import sparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

from src.config import ARTIFACTS_DIR, PROCESSED_DIR, SEED
from src.utils.io import safe_mkdir
from src.utils.logging import get_logger

logger = get_logger(__name__)


def load_jobs(path: Path) -> pd.DataFrame:
    if path.exists():
        try:
            return pd.read_parquet(path)
        except Exception as exc:
            csv_path = path.with_suffix(".csv")
            if csv_path.exists():
                logger.warning("Failed to read %s (%s); falling back to %s", path, exc, csv_path)
                return pd.read_csv(csv_path)
            logger.error("Failed to read canonical jobs: %s", exc)
    return pd.DataFrame()


def build_corpus(df: pd.DataFrame) -> pd.Series:
    def combine(row) -> str:
        parts = [
            str(row.get("title") or ""),
            str(row.get("skills_text") or ""),
            str(row.get("description_text") or "")[:800],
        ]
        return " ".join(parts)

    return df.apply(combine, axis=1)


def build_tfidf_index(df: pd.DataFrame) -> tuple[TfidfVectorizer, sparse.csr_matrix]:
    corpus = build_corpus(df)
    vectorizer = TfidfVectorizer(stop_words="english", max_features=50000)
    matrix = vectorizer.fit_transform(corpus)
    return vectorizer, matrix


def explain(query_vec: sparse.csr_matrix, doc_vec: sparse.csr_matrix, vectorizer: TfidfVectorizer, top_n: int = 5) -> List[str]:
    if query_vec.nnz == 0 or doc_vec.nnz == 0:
        return []
    # elementwise product to find overlapping terms
    doc_coo = doc_vec.tocoo()
    query_coo = query_vec.tocoo()
    query_dict = {i: v for i, v in zip(query_coo.col, query_coo.data)}
    scores = []
    for i, v in zip(doc_coo.col, doc_coo.data):
        if i in query_dict:
            scores.append((i, v * query_dict[i]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)[:top_n]
    feature_names = vectorizer.get_feature_names_out()
    return [feature_names[i] for i, _ in scores]


def recommend(profile_text: str, vectorizer: TfidfVectorizer, matrix: sparse.csr_matrix, jobs_df: pd.DataFrame, top_k: int = 10) -> List[Dict[str, Any]]:
    query_vec = vectorizer.transform([profile_text])
    sims = linear_kernel(query_vec, matrix).flatten()
    top_idx = sims.argsort()[::-1][:top_k]
    recs = []
    for idx in top_idx:
        row = jobs_df.iloc[idx]
        doc_vec = matrix[idx]
        reasons = explain(query_vec, doc_vec, vectorizer, top_n=5)
        if not reasons:
            # fallback to skills overlap if tfidf empty
            skills_tokens = str(row.get("skills_text") or "").split(",")
            reasons = [s.strip() for s in skills_tokens if s.strip()][:5]
        recs.append(
            {
                "job_id": row.get("job_id"),
                "title": row.get("title"),
                "company": row.get("company"),
                "source": row.get("source"),
                "source_url": row.get("source_url"),
                "score": float(sims[idx]),
                "reasons": reasons,
            }
        )
    return recs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Recommender inference (TF-IDF baseline).")
    parser.add_argument("--model-dir", default=ARTIFACTS_DIR / "recommender", help="Directory with vectorizer + matrix + jobs index.")
    parser.add_argument("--jobs", default=PROCESSED_DIR / "jobs_canonical.parquet", help="Canonical jobs parquet.")
    parser.add_argument("--profile", required=False, help="Profile text to recommend for.")
    parser.add_argument("--top_k", type=int, default=10, help="Number of recs.")
    parser.add_argument("--seed", type=int, default=SEED, help="Random seed.")
    return parser.parse_args()


def load_model(model_dir: Path):
    vectorizer = joblib.load(model_dir / "vectorizer.joblib")
    matrix = sparse.load_npz(model_dir / "matrix.npz")
    jobs_df = pd.read_parquet(model_dir / "jobs_index.parquet")
    return vectorizer, matrix, jobs_df


def main():
    args = parse_args()
    model_dir = Path(args.model_dir)
    vectorizer, matrix, jobs_df = load_model(model_dir)
    if args.profile:
        recs = recommend(args.profile, vectorizer, matrix, jobs_df, top_k=args.top_k)
        print(json.dumps(recs, indent=2, ensure_ascii=False))
    else:
        print("Model loaded. Provide --profile to get recommendations.")


if __name__ == "__main__":
    main()
