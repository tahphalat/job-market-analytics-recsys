# DSDE Workflow Logic & Improvement

We have refactored the project to align with modern Data Engineering best practices (Airflow, Data Lakes, Data Quality).

## 1. Architecture: "Mini-Airflow"
Instead of running loose scripts via `subprocess` (shell commands), we implemented a **Code-First Pipeline**.

### **Pipeline Structure (DAG Concept)**
The new `Pipeline` class in `src/pipeline/core.py` acts as a lightweight Orchestrator.
- **Task**: Each Python function is wrapped as a `Task` (similar to Airflow Operator).
- **Logging**: Centralized logs for task duration and status (🟢 START, ✅ COMPLETED, ❌ FAILED).
- **Dependencies**: Tasks are executed in a defined order (Ingest → Check → Transform → Check → Load).

## 2. Data Quality (DataGuard)
We introduced a semantic layer for quality checks: **`src/quality/guard.py`**.
Simulating tools like *Great Expectations*, it enforces:
- **Schema Validation**: Ensures incoming data has required columns (e.g., `title`, `company`).
- **Null Checks**: Fails the pipeline if critical fields (like `job_id`) are missing.
- **Volume Checks**: Warns if a stage produces zero rows.

## 3. Data Lake Layers
The pipeline strictly follows the **Medallion Architecture**:
| Layer | Folder | Responsibility |
|-------|--------|----------------|
| **Raw** | `data/raw/` | Landing zone for external data (Kaggle, Remotive). Validated by `DQ_Raw_Check`. |
| **Trusted** | `data/processed/*_clean` | Deduplicated and standardized text. |
| **Refined** | `data/processed/canonical` | Enriched business-level data (Fact/Dimensions). Validated by `DQ_Curated_Check`. |

## 4. Why this is better?
- **Debuggable**: Python exceptions trace directly to the line of code (no more opaque shell errors).
- **Safe**: Bad data is caught *before* it breaks the dashboard.
- **Extensible**: easy to swap the `Pipeline` class for real Airflow later.
