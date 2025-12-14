import argparse
import os
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

from src.config import ARTIFACTS_DIR, FIGURES_DIR, SEED
from src.utils.io import safe_mkdir
from src.utils.logging import get_logger

logger = get_logger(__name__)


def load_counts(path: Path, value_col: str, count_col: str = "count") -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame(columns=[value_col, count_col])
    return pd.read_csv(path)


def placeholder_fig(title: str, path: Path) -> None:
    plt.figure(figsize=(6, 4))
    plt.text(0.5, 0.5, "No data available", ha="center", va="center")
    plt.title(title)
    plt.axis("off")
    safe_mkdir(path.parent)
    plt.tight_layout()
    plt.savefig(path)
    plt.close()


def bar_chart(df: pd.DataFrame, value_col: str, count_col: str, title: str, path: Path, top_n: int = 20) -> None:
    safe_mkdir(path.parent)
    if df.empty:
        placeholder_fig(title, path)
        return
    df = df.head(top_n)
    plt.figure(figsize=(8, 5))
    plt.barh(df[value_col], df[count_col])
    plt.gca().invert_yaxis()
    plt.title(title)
    plt.xlabel("count")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()


def make_figures(base_artifacts: Path = ARTIFACTS_DIR) -> None:
    # Ensure headless + writable cache for matplotlib
    matplotlib.use("Agg")
    os.environ.setdefault("MPLCONFIGDIR", str(ARTIFACTS_DIR / ".matplotlib"))
    safe_mkdir(os.environ["MPLCONFIGDIR"])

    top_titles_path = base_artifacts / "top_titles.csv"
    top_skills_path = base_artifacts / "top_skills.csv"
    source_counts_path = base_artifacts / "source_counts.csv"
    location_counts_path = base_artifacts / "location_counts.csv"

    bar_chart(load_counts(top_titles_path, "value"), "value", "count", "Top Titles", FIGURES_DIR / "top_titles.png")
    bar_chart(load_counts(top_skills_path, "value"), "value", "count", "Top Skills", FIGURES_DIR / "top_skills.png")
    bar_chart(load_counts(source_counts_path, "source"), "source", "count", "Jobs by Source", FIGURES_DIR / "jobs_by_source.png")
    bar_chart(load_counts(location_counts_path, "location_text"), "location_text", "count", "Jobs by Location", FIGURES_DIR / "jobs_by_location.png", top_n=20)
    logger.info("Figures saved under %s", FIGURES_DIR)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build PNG figures for analytics.")
    parser.add_argument("--artifacts-dir", default=ARTIFACTS_DIR, help="Directory containing summary CSVs.")
    parser.add_argument("--seed", type=int, default=SEED, help="Random seed (unused).")
    return parser.parse_args()


def main():
    args = parse_args()
    make_figures(Path(args.artifacts_dir))


if __name__ == "__main__":
    main()
