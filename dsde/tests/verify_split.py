import sys
from pathlib import Path
import pandas as pd
import shutil
import unittest.mock as mock

# Setup path
DSDE_DIR = Path(__file__).resolve().parent.parent
if str(DSDE_DIR) not in sys.path:
    sys.path.append(str(DSDE_DIR))

from src.config import PROCESSED_DIR

def test_fallback():
    print("Starting verification for Splitting Strategy...")
    
    main_path = PROCESSED_DIR / "jobs_canonical.parquet"
    backup_path = PROCESSED_DIR / "jobs_canonical.parquet.bak"
    
    # Check parts exist
    parts = list(PROCESSED_DIR.glob("jobs_canonical_part_*.parquet"))
    if not parts:
        print("❌ Split files not found! Run split_data.py first.")
        return
    print(f"Found {len(parts)} split files.")

    # Simulate missing main file
    if main_path.exists():
        print(f"Moving {main_path.name} to backup...")
        shutil.move(main_path, backup_path)
    
    try:
        # Clean up mocks/imports
        if 'streamlit' in sys.modules: del sys.modules['streamlit']
        if 'src.app_streamlit' in sys.modules: del sys.modules['src.app_streamlit']
            
        import streamlit as st
        from src.app_streamlit import load_jobs
        
        print("Invoking load_jobs...")
        df = load_jobs()
        print(f"Loaded dataframe with shape: {df.shape}")
        
        if len(df) > 100000:
             print(f"✅ Success: Loaded FULL data from split files (Size: {len(df):,} rows).")
        elif len(df) > 0:
             print(f"⚠️ Warning: Loaded data but size {len(df)} is smaller than expected (Sample?).")
        else:
             print("❌ Failed: Loaded empty dataframe.")

    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()

    finally:
        # Restore main file
        if backup_path.exists():
            print(f"Restoring {main_path.name}...")
            shutil.move(backup_path, main_path)

if __name__ == "__main__":
    test_fallback()
