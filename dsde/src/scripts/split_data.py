import pandas as pd
from pathlib import Path
import sys
import math

# Setup path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from src.config import PROCESSED_DIR

def split_parquet(max_size_mb=80):
    input_path = PROCESSED_DIR / "jobs_canonical.parquet"
    
    if not input_path.exists():
        print(f"❌ Input file not found: {input_path}")
        return

    print(f"Reading {input_path}...")
    df = pd.read_parquet(input_path)
    total_rows = len(df)
    file_size_mb = input_path.stat().st_size / (1024 * 1024)
    
    print(f"Total Rows: {total_rows:,}")
    print(f"File Size: {file_size_mb:.2f} MB")
    
    if file_size_mb <= max_size_mb:
        print("✅ File is small enough. No split needed.")
        return

    # Calculate splits
    num_parts = math.ceil(file_size_mb / max_size_mb)
    rows_per_part = math.ceil(total_rows / num_parts)
    
    print(f"Splitting into {num_parts} parts (~{rows_per_part:,} rows each)...")
    
    for i in range(num_parts):
        start_idx = i * rows_per_part
        end_idx = min((i + 1) * rows_per_part, total_rows)
        
        df_part = df.iloc[start_idx:end_idx]
        output_path = PROCESSED_DIR / f"jobs_canonical_part_{i}.parquet"
        
        print(f"Saving Part {i}: {output_path.name} ({len(df_part):,} rows)...")
        df_part.to_parquet(output_path, index=False)
        
    print("✅ Split complete.")

if __name__ == "__main__":
    split_parquet()
