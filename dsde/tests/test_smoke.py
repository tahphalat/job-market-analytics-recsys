from pathlib import Path


def test_artifacts_exist():
    expected = [
        Path("data/processed/jobs_canonical.parquet"),
        Path("artifacts/kpi_summary.json"),
        Path("artifacts/top_titles.csv"),
        Path("artifacts/top_skills.csv"),
        Path("artifacts/demo_recs.json"),
        Path("artifacts/graphs/skill_graph.json"),
        Path("artifacts/figures/top_skills.png"),
    ]
    missing = [str(p) for p in expected if not p.exists()]
    assert not missing, f"Missing artifacts: {missing}"
