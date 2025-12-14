import argparse
import json
from pathlib import Path
from typing import Optional

import pandas as pd
import plotly.express as px

from utils.common import ensure_parent, set_seed
from utils.logging import get_logger

logger = get_logger(__name__)


def run_eda(input_path: Path, output_path: Path, seed: int, figure_path: Optional[Path] = None) -> None:
    set_seed(seed)
    df = pd.read_csv(input_path)
    summary = {
        "row_count": int(len(df)),
        "columns": list(df.columns),
        "missing_by_column": {col: int(df[col].isna().sum()) for col in df.columns},
    }

    if "comp_value" in df.columns:
        desc = df["comp_value"].describe(percentiles=[0.25, 0.5, 0.75, 0.9], include="all")
        summary["comp_value_stats"] = {k: (float(v) if pd.notna(v) else None) for k, v in desc.items()}

    output_path = ensure_parent(output_path)
    with open(output_path, "w") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    logger.info("EDA summary saved to %s", output_path)

    if figure_path and "comp_value" in df.columns and "category" in df.columns:
        fig = px.box(df.dropna(subset=["comp_value"]), x="category", y="comp_value", title="Comp value by category")
        figure_path = ensure_parent(figure_path)
        fig.write_html(figure_path)
        logger.info("EDA figure saved to %s", figure_path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate quick EDA artifacts.")
    parser.add_argument("--input", required=True, help="Path to cleaned CSV.")
    parser.add_argument("--output", required=True, help="Destination JSON summary.")
    parser.add_argument("--figure", default=None, help="Optional HTML path for an interactive figure.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed.")
    return parser.parse_args()


def main():
    args = parse_args()
    figure = Path(args.figure) if args.figure else None
    run_eda(Path(args.input), Path(args.output), seed=args.seed, figure_path=figure)


if __name__ == "__main__":
    main()
