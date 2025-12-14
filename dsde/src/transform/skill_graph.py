import argparse
import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import pandas as pd

from src.config import ARTIFACTS_DIR, PROCESSED_DIR, SEED
from src.utils.io import safe_mkdir
from src.utils.logging import get_logger

logger = get_logger(__name__)


def read_jobs(path: Path) -> pd.DataFrame:
    if path.exists():
        try:
            return pd.read_parquet(path)
        except Exception as exc:
            csv_path = path.with_suffix(".csv")
            if csv_path.exists():
                logger.warning("Failed to read %s (%s); falling back to %s", path, exc, csv_path)
                return pd.read_csv(csv_path)
            logger.error("Failed to read canonical jobs: %s", exc)
    return pd.DataFrame()


def normalize_skills(series: Iterable) -> List[str]:
    skills: List[str] = []
    for val in series:
        if isinstance(val, list):
            skills.extend([s for s in val if isinstance(s, str) and s.strip()])
        elif isinstance(val, str):
            tokens = [t.strip() for t in val.replace(";", ",").split(",") if t.strip()]
            skills.extend(tokens)
    return [s.strip() for s in skills if s.strip()]


def build_skill_sets(df: pd.DataFrame) -> List[List[str]]:
    skill_sets: List[List[str]] = []
    for _, row in df.iterrows():
        skills = []
        if "skills" in df.columns and isinstance(row.get("skills"), list):
            skills = [s for s in row["skills"] if isinstance(s, str) and s.strip()]
        if not skills and "skills_text" in df.columns:
            skills = [t.strip() for t in str(row["skills_text"]).replace(";", ",").split(",") if t.strip()]
        skills = list(dict.fromkeys(skills))  # dedupe preserve order
        if skills:
            skill_sets.append(skills)
    return skill_sets


def build_graph(skill_sets: List[List[str]], min_edge_weight: int) -> Tuple[List[Dict], List[Dict]]:
    node_counter = Counter()
    edge_counter: Dict[Tuple[str, str], int] = defaultdict(int)

    for skills in skill_sets:
        # update node counts
        node_counter.update(skills)
        for a, b in itertools.combinations(sorted(set(skills)), 2):
            edge_counter[(a, b)] += 1

    nodes = [{"id": skill, "label": skill, "count": int(count)} for skill, count in node_counter.items()]
    links = [
        {"source": a, "target": b, "weight": int(w)}
        for (a, b), w in edge_counter.items()
        if w >= min_edge_weight
    ]
    return nodes, links


def export_graph(nodes: List[Dict], links: List[Dict], output_path: Path) -> Path:
    safe_mkdir(output_path.parent)
    output_path.write_text(json.dumps({"nodes": nodes, "links": links}, indent=2))
    logger.info("Skill graph saved to %s (nodes=%s links=%s)", output_path, len(nodes), len(links))
    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build skill co-occurrence graph JSON for frontend.")
    parser.add_argument("--input", default=PROCESSED_DIR / "jobs_canonical.parquet", help="Path to canonical jobs parquet.")
    parser.add_argument("--min_edge_weight", type=int, default=5, help="Minimum co-occurrence to include an edge.")
    parser.add_argument("--output", default=ARTIFACTS_DIR / "graphs" / "skill_graph.json", help="Output JSON path.")
    parser.add_argument("--seed", type=int, default=SEED, help="Random seed (unused).")
    return parser.parse_args()


def main():
    args = parse_args()
    df = read_jobs(Path(args.input))
    skill_sets = build_skill_sets(df)
    nodes, links = build_graph(skill_sets, min_edge_weight=args.min_edge_weight)
    export_graph(nodes, links, Path(args.output))


if __name__ == "__main__":
    main()
