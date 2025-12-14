import argparse
from pathlib import Path
from typing import List, Dict

import pandas as pd

from utils.common import ensure_parent, set_seed
from utils.logging import get_logger

logger = get_logger(__name__)


def build_feature_rows(df: pd.DataFrame) -> List[Dict]:
    rows: List[Dict] = []
    if "category" in df.columns:
        counts = df.groupby("category").size().to_dict()
        for category, count in counts.items():
            rows.append({"feature": "category_distribution", "group": category, "metric": "count", "value": count})

    if "work_mode" in df.columns:
        mode_counts = df.groupby("work_mode").size().to_dict()
        for mode, count in mode_counts.items():
            rows.append({"feature": "work_mode_distribution", "group": mode, "metric": "count", "value": count})

    if "comp_value" in df.columns:
        comp_series = df["comp_value"].dropna()
        rows.append({"feature": "comp_value_summary", "group": "all", "metric": "mean", "value": comp_series.mean()})
        rows.append({"feature": "comp_value_summary", "group": "all", "metric": "median", "value": comp_series.median()})
        rows.append({"feature": "comp_value_summary", "group": "all", "metric": "p90", "value": comp_series.quantile(0.9)})

        if "category" in df.columns:
            category_mean = (
                df.dropna(subset=["comp_value"])
                .groupby("category")["comp_value"]
                .mean()
                .to_dict()
            )
            for category, mean_value in category_mean.items():
                rows.append(
                    {
                        "feature": "category_comp_mean",
                        "group": category,
                        "metric": "mean_comp_value",
                        "value": mean_value,
                    }
                )

    if "company" in df.columns:
        top_companies = (
            df.groupby("company")
            .size()
            .sort_values(ascending=False)
            .head(20)
            .to_dict()
        )
        for company, count in top_companies.items():
            rows.append(
                {"feature": "top_companies", "group": company, "metric": "count", "value": count}
            )
    return rows


def build_features(input_path: Path, output_path: Path, seed: int) -> Path:
    set_seed(seed)
    df = pd.read_csv(input_path)
    rows = build_feature_rows(df)
    feature_df = pd.DataFrame(rows)
    output_path = ensure_parent(output_path)
    feature_df.to_csv(output_path, index=False)
    logger.info("Saved feature aggregates to %s (rows=%s)", output_path, len(feature_df))
    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create lightweight feature aggregates.")
    parser.add_argument("--input", required=True, help="Path to cleaned CSV.")
    parser.add_argument("--output", required=True, help="Destination CSV for features.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed.")
    return parser.parse_args()


def main():
    args = parse_args()
    build_features(Path(args.input), Path(args.output), seed=args.seed)


if __name__ == "__main__":
    main()
