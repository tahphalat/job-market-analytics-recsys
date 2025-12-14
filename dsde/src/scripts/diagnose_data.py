import pandas as pd
from pathlib import Path
import sys

# Setup path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from src.config import PROCESSED_DIR

def diagnose():
    parquet_path = PROCESSED_DIR / "jobs_canonical.parquet"
    csv_path = PROCESSED_DIR / "jobs_canonical.csv"
    sample_path = PROCESSED_DIR / "jobs_canonical_sample.parquet"

    print(f"Checking {parquet_path}...")
    try:
        df = pd.read_parquet(parquet_path)
        print(f"✅ Parquet read success. Shape: {df.shape}")
    except Exception as e:
        print(f"❌ Parquet read failed: {e}")
        
        # Try CSV
        if csv_path.exists():
            print(f"Reading CSV {csv_path}...")
            try:
                df = pd.read_csv(csv_path, low_memory=False)
                print(f"✅ CSV read success. Shape: {df.shape}")
                
                # Regenerate sample if missing
                if not sample_path.exists():
                    print("Regenerating missing sample file...")
                    df.sample(10000).to_parquet(sample_path)
                    print("✅ Sample file regenerated.")
                    
                # Regenerate main parquet from CSV if corrupt
                print("Regenerating valid parquet from CSV...")
                df.to_parquet(parquet_path)
                print("✅ Main parquet file repaired.")
                
            except Exception as csv_e:
                print(f"❌ CSV read failed: {csv_e}")
        else:
            print("❌ CSV Not Found.")

if __name__ == "__main__":
    diagnose()
