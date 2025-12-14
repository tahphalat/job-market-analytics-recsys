from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_KAGGLE_DIR = BASE_DIR / "data" / "raw" / "kaggle"
RAW_REMOTIVE_DIR = BASE_DIR / "data" / "raw" / "remotive"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

ARTIFACTS_DIR = BASE_DIR / "artifacts"
FIGURES_DIR = ARTIFACTS_DIR / "figures"
GRAPHS_DIR = ARTIFACTS_DIR / "graphs"
RECOMMENDER_DIR = ARTIFACTS_DIR / "recommender"

REMOTIVE_URL = "https://remotive.com/api/remote-jobs"

SAMPLE_N = 2000
SEED = 42
