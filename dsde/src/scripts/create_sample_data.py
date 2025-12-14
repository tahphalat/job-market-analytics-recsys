from pathlib import Path
import pandas as pd
import sys

# Ensure project root is importable
BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from src.config import PROCESSED_DIR

def create_sample():
    input_path = PROCESSED_DIR / "jobs_canonical.parquet"
    output_path = PROCESSED_DIR / "jobs_canonical_sample.parquet"
    
    if not input_path.exists():
        print(f"Error: {input_path} not found.")
        return

    print(f"Reading {input_path}...")
    try:
        df = pd.read_parquet(input_path)
    except Exception as e:
        print(f"Error reading parquet: {e}")
        csv_path = input_path.with_suffix(".csv")
        if csv_path.exists():
            print(f"Falling back to CSV: {csv_path}...")
            try:
                # Use low_memory=False to avoid DtypeWarning on large files, or specify dtypes if known
                df = pd.read_csv(csv_path, low_memory=False) 
            except Exception as e_csv:
                print(f"Error reading CSV: {e_csv}")
                return
        else:
            print("CSV fallback not found.")
            return

    if len(df) > 10000:
        print(f"Sampling 10,000 rows from {len(df)} rows...")
        df_sample = df.sample(n=10000, random_state=42)
    else:
        print(f"File has {len(df)} rows, using all.")
        df_sample = df

    print(f"Saving sample to {output_path}...")
    df_sample.to_parquet(output_path, index=False)
    print("Done.")

if __name__ == "__main__":
    create_sample()
