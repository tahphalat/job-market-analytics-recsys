import argparse
from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from src.utils.common import ensure_parent, set_seed
from src.utils.logging import get_logger

logger = get_logger(__name__)


def train(input_path: Path, output_path: Path, seed: int, test_size: float = 0.2) -> Path:
    set_seed(seed)
    df = pd.read_csv(input_path)
    df = df.dropna(subset=["comp_value"])

    if df.empty:
        raise ValueError("No rows with comp_value available for training.")

    feature_cols = [col for col in ["category", "position", "work_mode"] if col in df.columns]
    X = df[feature_cols].fillna("unknown")
    y = df["comp_value"]

    preprocess = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), feature_cols),
        ],
        remainder="drop",
    )
    model = Pipeline(steps=[("prep", preprocess), ("reg", LinearRegression())])
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=seed
    )

    model.fit(X_train, y_train)
    preds = model.predict(X_test) if len(y_test) else []
    mae = mean_absolute_error(y_test, preds) if len(y_test) else None

    output_path = ensure_parent(output_path)
    joblib.dump({"model": model, "feature_cols": feature_cols, "mae": mae}, output_path)
    logger.info("Trained model saved to %s", output_path)
    if mae is not None:
        logger.info("Validation MAE: %.2f", mae)
    else:
        logger.info("Validation MAE skipped (not enough holdout rows).")
    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train baseline compensation model.")
    parser.add_argument("--input", required=True, help="Path to cleaned CSV.")
    parser.add_argument("--output", required=True, help="Path to persist the trained model artifact.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for splits.")
    parser.add_argument(
        "--test-size",
        type=float,
        default=0.2,
        help="Proportion reserved for validation.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    train(Path(args.input), Path(args.output), seed=args.seed, test_size=args.test_size)


if __name__ == "__main__":
    main()
