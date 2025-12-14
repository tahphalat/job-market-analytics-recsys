import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict

from src.config import ARTIFACTS_DIR
from src.utils.logging import get_logger

logger = get_logger(__name__)


def list_files(base: Path) -> List[Path]:
    return [p for p in base.rglob("*") if p.is_file()]


def copy_artifacts(src_dir: Path, dest_dir: Path) -> List[Path]:
    copied: List[Path] = []
    for path in list_files(src_dir):
        rel = path.relative_to(src_dir)
        dest_path = dest_dir / rel
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dest_path)
        copied.append(dest_path)
    return copied


def write_index(files: List[Path], dest_dir: Path) -> Path:
    data: List[Dict] = []
    for f in files:
        data.append({"path": str(f.relative_to(dest_dir)), "size": f.stat().st_size})
    index = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "files": data,
    }
    index_path = dest_dir / "index.json"
    with open(index_path, "w") as fh:
        json.dump(index, fh, indent=2)
    return index_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Copy artifacts to web/public and emit index.json")
    parser.add_argument("--web_public_dir", default=Path("web/public/artifacts"), help="Destination for public artifacts.")
    return parser.parse_args()


def main():
    args = parse_args()
    src_dir = ARTIFACTS_DIR
    dest_dir = Path(args.web_public_dir)
    copied = copy_artifacts(src_dir, dest_dir)
    index_path = write_index(copied, dest_dir)
    logger.info("Exported %s files to %s (index: %s)", len(copied), dest_dir, index_path)


if __name__ == "__main__":
    main()
