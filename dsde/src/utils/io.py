from pathlib import Path
from typing import Union, Any
import json

import pandas as pd


def safe_mkdir(path: Union[str, Path]) -> Path:
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def read_auto(path: Union[str, Path]) -> pd.DataFrame:
    path = Path(path)
    if path.suffix.lower() == ".parquet":
        return pd.read_parquet(path)
    return pd.read_csv(path)


def write_parquet(df: pd.DataFrame, path: Union[str, Path]) -> Path:
    path = Path(path)
    safe_mkdir(path.parent)
    df.to_parquet(path, index=False)
    return path


def write_json(obj: Any, path: Union[str, Path]) -> Path:
    path = Path(path)
    safe_mkdir(path.parent)
    with open(path, "w") as f:
        json.dump(obj, f, indent=2)
    return path


# Backward-compatible alias
def read_csv_or_parquet(path: Union[str, Path]) -> pd.DataFrame:
    return read_auto(path)
