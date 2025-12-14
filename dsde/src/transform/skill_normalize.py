import json
from pathlib import Path
from typing import List, Iterable

from src.config import ARTIFACTS_DIR

SKILL_ALIASES = {
    "python": "Python",
    "py": "Python",
    "pandas": "Pandas",
    "numpy": "NumPy",
    "sql": "SQL",
    "postgres": "PostgreSQL",
    "postgresql": "PostgreSQL",
    "mysql": "MySQL",
    "excel": "Excel",
    "javascript": "JavaScript",
    "js": "JavaScript",
    "typescript": "TypeScript",
    "react": "React",
    "node": "Node.js",
    "node.js": "Node.js",
    "aws": "AWS",
    "azure": "Azure",
    "gcp": "GCP",
    "ml": "Machine Learning",
    "machine learning": "Machine Learning",
    "deep learning": "Deep Learning",
    "nlp": "NLP",
    "git": "Git",
    "docker": "Docker",
}


def normalize_token(token: str) -> str:
    key = token.strip().lower()
    if not key:
        return ""
    return SKILL_ALIASES.get(key, token.strip())


def normalize_skills(raw: Iterable[str]) -> List[str]:
    out: List[str] = []
    for token in raw:
        if token is None:
            continue
        norm = normalize_token(str(token))
        if norm and norm not in out:
            out.append(norm)
    return out


def export_skill_aliases(path: Path | None = None) -> Path:
    path = path or (ARTIFACTS_DIR / "skill_aliases.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(SKILL_ALIASES, f, indent=2)
    return path
