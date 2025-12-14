import argparse
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import List

import kagglehub

from src.config import RAW_KAGGLE_DIR, SEED
from src.utils.common import set_seed
from src.utils.io import safe_mkdir
from src.utils.logging import get_logger

logger = get_logger(__name__)


def copy_downloaded_files(download_path: Path, out_dir: Path) -> List[str]:
    files: List[str] = []
    if download_path.is_file():
        target = out_dir / download_path.name
        shutil.copy2(download_path, target)
        files.append(target.name)
        return files

    for item in download_path.iterdir():
        dest = out_dir / item.name
        if item.is_dir():
            shutil.copytree(item, dest, dirs_exist_ok=True)
            for sub in dest.rglob("*"):
                if sub.is_file():
                    files.append(str(sub.relative_to(out_dir)))
        else:
            shutil.copy2(item, dest)
            files.append(dest.name)
    return files


def fetch_kagglehub_dataset(dataset: str, out_dir: Path, seed: int) -> Path:
    set_seed(seed)
    out_dir = safe_mkdir(out_dir)
    logger.info("Downloading KaggleHub dataset %s into %s", dataset, out_dir)

    download_path = Path(kagglehub.dataset_download(dataset))
    if not download_path.exists():
        raise FileNotFoundError(f"Downloaded path not found: {download_path}")

    copied_files = copy_downloaded_files(download_path, out_dir)
    meta = {
        "dataset": dataset,
        "downloaded_at": datetime.utcnow().isoformat() + "Z",
        "download_path": str(download_path),
        "out_dir": str(out_dir),
        "files": copied_files,
    }
    meta_path = out_dir / "kaggle_download_meta.json"
    with open(meta_path, "w") as f:
        json.dump(meta, f, indent=2)
    logger.info("Wrote download metadata to %s", meta_path)
    return download_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch a Kaggle dataset via KaggleHub.")
    parser.add_argument(
        "--dataset",
        default="arshkon/linkedin-job-postings",
        help="Kaggle dataset slug for KaggleHub download.",
    )
    parser.add_argument("--out_dir", default=RAW_KAGGLE_DIR, help="Destination directory for downloads.")
    parser.add_argument("--seed", type=int, default=SEED, help="Random seed (consistency).")
    return parser.parse_args()


def main():
    args = parse_args()
    fetch_kagglehub_dataset(args.dataset, Path(args.out_dir), seed=args.seed)


if __name__ == "__main__":
    main()
