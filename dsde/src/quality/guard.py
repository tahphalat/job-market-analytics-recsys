import pandas as pd
import logging
from pathlib import Path
from typing import List, Optional

logger = logging.getLogger("DataGuard")

class DataGuard:
    """
    Simulates a Data Quality (DQ) framework like Great Expectations.
    Ensures data passing through the pipeline meets 'Refined' standards.
    """
    
    @staticmethod
    def validate_csv(file_path: Path, expected_columns: Optional[List[str]] = None, check_not_null: Optional[List[str]] = None):
        """Reads a CSV and performs basic validation."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"DQ Failed: File not found {path}")
            
        df = pd.read_csv(path)
        DataGuard.validate_df(df, f"CSV::{path.name}", expected_columns, check_not_null)
        
    @staticmethod
    def validate_parquet(file_path: Path, expected_columns: Optional[List[str]] = None):
        """Reads Parquet and performs basic validation."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"DQ Failed: File not found {path}")
            
        df = pd.read_parquet(path)
        DataGuard.validate_df(df, f"Parquet::{path.name}", expected_columns)

    @staticmethod
    def validate_df(df: pd.DataFrame, source_name: str, expected_columns: Optional[List[str]] = None, check_not_null: Optional[List[str]] = None):
        logger.info(f"🛡️  DQ CHECK: {source_name}")
        
        # 1. Schema Check
        if expected_columns:
            missing = set(expected_columns) - set(df.columns)
            if missing:
                raise ValueError(f"❌ Schema Violation in {source_name}. Missing columns: {missing}")
            logger.info(f"   - Schema Check Passed ({len(expected_columns)} cols)")

        # 2. Null Check
        if check_not_null:
            for col in check_not_null:
                if col in df.columns:
                    null_count = df[col].isna().sum()
                    if null_count > 0:
                        logger.warning(f"   ⚠️  Null Warning: {col} has {null_count} nulls in {source_name}")
                    else:
                        logger.info(f"   - Null Check Passed for {col}")

        # 3. Volume Check
        row_count = len(df)
        if row_count == 0:
            logger.warning(f"   ⚠️  Volume Warning: {source_name} is empty!")
        else:
            logger.info(f"   - Volume Check: {row_count} rows")
        
        logger.info(f"✅ DQ Verified for {source_name}")
