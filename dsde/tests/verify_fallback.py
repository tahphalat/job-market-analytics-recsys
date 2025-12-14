import sys
from pathlib import Path
import pandas as pd
import shutil

# Setup path
# File is in dsde/tests/verify_fallback.py
# We want to add 'dsde' to path to import 'src'
DSDE_DIR = Path(__file__).resolve().parent.parent
if str(DSDE_DIR) not in sys.path:
    sys.path.append(str(DSDE_DIR))

from src.config import PROCESSED_DIR
# Import the function to test
# Note: we need to mock streamlit since app_streamlit imports it
import unittest.mock as mock
sys.modules['streamlit'] = mock.MagicMock()
from src.app_streamlit import load_jobs

def test_fallback():
    print("Starting verification...")
    
    main_path = PROCESSED_DIR / "jobs_canonical.parquet"
    backup_path = PROCESSED_DIR / "jobs_canonical.parquet.bak"
    sample_path = PROCESSED_DIR / "jobs_canonical_sample.parquet"

    # 1. Ensure sample exists
    if not sample_path.exists():
        print("❌ Sample file not found!")
        return

    # 2. Simulate missing main file
    if main_path.exists():
        print(f"Moving {main_path.name} to backup...")
        shutil.move(main_path, backup_path)
    
    try:
        print("Calling load_jobs()...")
        # Clear cache mimic? load_jobs is st.cache_data wrapped. 
        # But we mocked streamlit, so the decorator is likely mocked too or just transparent if we didn't mock it perfectly.
        # Actually, if st is mocked, @st.cache_data might fail if not mocked properly.
        # Let's rely on the fact that we mocked the module, so the decorator is likely a Mock object.
        # Calling load_jobs might return the Mock object instead of execution if the decorator isn't implemented.
        # Basic mock of cache_data:
        
        # Re-import to handle the mock correctly if needed, or just define a simple wrapper
        # Easier: Let's just modify the import or assume the user has streamlit installed and we just want to run the function.
        # But we are in a script. Streamlit should be available.
        pass
    except Exception as e:
        print(f"Setup error: {e}")

    # Resetting modules to properly test with real functional logic but without full streamlit context would be hard.
    # Alternative: Just check file logic manually here without importing app_streamlit if it's too coupled.
    # But I modified app_streamlit.py, so I should test THAT code.
    
    # STRATEGY:
    # Since I cannot easily mock the streamlit decorator behavior perfectly in a simple script without a lot of boilerplate,
    # I will inspect the load_jobs source or just trust the logic if I can't run it. 
    # OR, I can use `streamlit` if installed.
    
    try:
        # We really want to run the logic inside load_jobs.
        # Clean up mocks
        if 'streamlit' in sys.modules:
            del sys.modules['streamlit']
        if 'src.app_streamlit' in sys.modules:
            del sys.modules['src.app_streamlit']
            
        # Re-import real modules
        import streamlit as st
        # We need to bypass the @st.cache_data if we are in a script context without streamlit run
        # We can patch it to be a transparent decorator
        # But wait, we deleted the mock. Now we are importing real streamlit.
        # Real streamlit will warn "No Streamlit's ... context" but should function.
        
        from src.app_streamlit import load_jobs
        
        # Determine expected size
        expected_sample_size = 10000 
        
        print("Invoking load_jobs (this might show Streamlit warnings)...")
        df = load_jobs()
        print(f"Loaded dataframe with shape: {df.shape}")
        
        if len(df) <= 10001 and len(df) > 0: # 10k sample
             print("✅ Success: Loaded sample data (size matches expected ~10k).")
        elif len(df) > 10001:
             print(f"❌ Failed: Loaded full data? Size: {len(df)}")
        else:
             print("❌ Failed: Loaded empty dataframe.")

    finally:
        # 3. Restore main file
        if backup_path.exists():
            print(f"Restoring {main_path.name}...")
            shutil.move(backup_path, main_path)

if __name__ == "__main__":
    test_fallback()
