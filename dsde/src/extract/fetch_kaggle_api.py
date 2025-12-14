import argparse
import json
import zipfile
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from kaggle.api.kaggle_api_extended import KaggleApi

from src.config import RAW_KAGGLE_DIR, SEED
from src.utils.common import set_seed
from src.utils.io import safe_mkdir
from src.utils.logging import get_logger

logger = get_logger(__name__)


def _detect_zip_path(out_dir: Path, dataset: str) -> Optional[Path]:
    expected = out_dir / f"{dataset.replace('/', '_')}.zip"
    if expected.exists():
        return expected
    candidates = sorted(out_dir.glob("*.zip"), key=lambda p: p.stat().st_mtime, reverse=True)
    return candidates[0] if candidates else None


def download_kaggle_dataset(dataset: str, out_dir: Path, unzip: bool, force: bool, seed: int) -> Path:
    set_seed(seed)
    out_dir = safe_mkdir(out_dir)

    api = KaggleApi()
    api.authenticate()

    logger.info("Downloading Kaggle dataset %s into %s", dataset, out_dir)
    api.dataset_download_files(dataset, path=out_dir, force=force, quiet=False, unzip=False)
    zip_path = _detect_zip_path(out_dir, dataset)
    if not zip_path:
        raise FileNotFoundError("Dataset zip not found after download.")

    files: List[str] = []
    with zipfile.ZipFile(zip_path, "r") as zf:
        files = zf.namelist()
        if unzip:
            zf.extractall(out_dir)
            logger.info("Unzipped %s files into %s", len(files), out_dir)
    meta = {
        "dataset": dataset,
        "downloaded_at": datetime.utcnow().isoformat() + "Z",
        "zip_path": str(zip_path),
        "files": files,
    }
    meta_path = out_dir / "kaggle_download_meta.json"
    with open(meta_path, "w") as f:
        json.dump(meta, f, indent=2)
    logger.info("Wrote download metadata to %s", meta_path)
    return zip_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch Kaggle dataset via Kaggle API.")
    parser.add_argument("--dataset", required=True, help="Kaggle dataset slug (owner/dataset).")
    parser.add_argument("--out_dir", default=RAW_KAGGLE_DIR, help="Directory to store downloads.")
    parser.add_argument(
        "--unzip",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Whether to unzip the downloaded archive.",
    )
    parser.add_argument("--force", action="store_true", help="Force re-download even if files exist.")
    parser.add_argument("--seed", type=int, default=SEED, help="Random seed (for reproducibility).")
    return parser.parse_args()


def main():
    args = parse_args()
    download_kaggle_dataset(
        dataset=args.dataset,
        out_dir=Path(args.out_dir),
        unzip=args.unzip,
        force=args.force,
        seed=args.seed,
    )


if __name__ == "__main__":
    main()
