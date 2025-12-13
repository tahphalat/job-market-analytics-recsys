from typing import Dict, Iterable, Tuple
import re

import pandas as pd


CANONICAL_COLUMNS = [
    "category",
    "company",
    "position",
    "work_mode",
    "compensation",
    "compensation_normalized",
    "comp_value",
    "page",
]

COLUMN_ALIASES: Dict[str, Iterable[str]] = {
    "category": ("category", "job_category", "field", "domain"),
    "company": ("company", "employer", "organization", "org", "company_name"),
    "position": ("position", "role", "title", "job_title"),
    "work_mode": ("work_mode", "workmode", "work_type", "worktype", "location_type"),
    "compensation": ("compensation", "salary", "pay", "comp", "comp_raw"),
    "compensation_normalized": (
        "compensation_normalized",
        "comp_normalized",
        "comp_norm",
        "normalized_compensation",
    ),
    "comp_value": ("comp_value", "comp_amount", "comp_num", "comp_norm_value"),
    "page": ("page", "source_page", "page_number"),
}

WORK_MODE_ALIASES: Dict[str, str] = {
    "onsite": "on-site",
    "remote": "remote",
    "wfh": "remote",
    "workfromhome": "remote",
    "hybrid": "hybrid",
    "flex": "hybrid",
    "flexible": "hybrid",
}


def infer_column_mapping(columns: Iterable[str]) -> Dict[str, str]:
    normalized = {col.lower().strip(): col for col in columns}
    mapping: Dict[str, str] = {}
    for canonical, aliases in COLUMN_ALIASES.items():
        for alias in aliases:
            key = alias.lower()
            if key in normalized:
                mapping[normalized[key]] = canonical
                break
    return mapping


def rename_with_aliases(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, str]]:
    mapping = infer_column_mapping(df.columns)
    renamed = df.rename(columns=mapping)
    for col in CANONICAL_COLUMNS:
        if col not in renamed.columns:
            renamed[col] = pd.NA
    return renamed, mapping


def normalize_work_mode(value) -> str:
    if pd.isna(value):
        return "unspecified"
    text = str(value).strip().lower().replace(" ", "").replace("-", "").replace("_", "")
    mapped = WORK_MODE_ALIASES.get(text)
    if mapped:
        return mapped
    # fallback to readable original
    return str(value).strip()


def parse_comp_value(raw) -> float:
    if pd.isna(raw):
        return None
    text = str(raw)
    numbers = re.findall(r"[-+]?[0-9]*\.?[0-9]+", text.replace(",", ""))
    if not numbers:
        return None
    try:
        return float(numbers[0])
    except ValueError:
        return None
