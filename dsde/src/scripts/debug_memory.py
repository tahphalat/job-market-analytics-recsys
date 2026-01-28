import sys
from pathlib import Path
import pandas as pd
import numpy as np

# Setup path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from src.config import PROCESSED_DIR
from src.app_streamlit import load_jobs

def check_memory():
    print("Loading jobs...")
    try:
        df = load_jobs()
    except Exception as e:
        print(f"Failed to load via load_jobs: {e}")
        # Try manual load of parts
        parts = sorted(PROCESSED_DIR.glob("jobs_canonical_part_*.parquet"))
        dfs = [pd.read_parquet(p) for p in parts]
        df = pd.concat(dfs, ignore_index=True)

    print(f"Rows: {len(df):,}")
    mem_usage = df.memory_usage(deep=True).sum() / (1024 * 1024)
    print(f"Memory Usage (Deep): {mem_usage:.2f} MB")
    
    print("\nColumn Memory Breakdown:")
    print(df.memory_usage(deep=True) / (1024 * 1024))

if __name__ == "__main__":
    check_memory()
