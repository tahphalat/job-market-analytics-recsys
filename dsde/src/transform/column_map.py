from typing import Dict, Iterable, Optional

import pandas as pd

TITLE_ALIASES = ["title", "job_title", "position"]
COMPANY_ALIASES = ["company_name", "company", "employer"]
LOCATION_ALIASES = ["location", "candidate_required_location", "formatted_location", "city_state", "city"]
DESCRIPTION_ALIASES = ["description", "job_description", "details"]
URL_ALIASES = ["job_posting_url", "url", "application_url", "job_url"]
DATE_ALIASES = ["listed_time", "original_listed_time", "publication_date", "posted_at", "date"]
SALARY_ALIASES = ["salary", "compensation", "salary_text", "pay", "pay_range"]
SKILL_ALIASES = ["skills", "tags"]


def pick_first_existing_column(df: pd.DataFrame, aliases: Iterable[str]) -> Optional[pd.Series]:
    for col in aliases:
        if col in df.columns:
            return df[col]
    return None


def resolve_column(df: pd.DataFrame, aliases: Iterable[str], default=None) -> pd.Series:
    col = pick_first_existing_column(df, aliases)
    if col is None:
        return pd.Series([default] * len(df))
    return col


ALIAS_MAP: Dict[str, Iterable[str]] = {
    "title": TITLE_ALIASES,
    "company": COMPANY_ALIASES,
    "location_text": LOCATION_ALIASES,
    "description_text": DESCRIPTION_ALIASES,
    "source_url": URL_ALIASES,
    "published_at": DATE_ALIASES,
    "salary_text": SALARY_ALIASES,
    "skills": SKILL_ALIASES,
}
