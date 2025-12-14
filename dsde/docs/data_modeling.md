# Data Modeling Strategy

## Schema Overview (Star Schema)

We utilize a Star Schema approach to organize our data for efficient querying and aggregation.

### **Fact Table**
- **`fact_jobs`**: Contains the core transactional data (individual job postings).
    - `job_id` (PK)
    - `company_id` (FK) -> `dim_company`
    - `location_id` (FK) -> `dim_location`
    - `published_at` (Timestamp)
    - `salary_min`, `salary_max` (Measures)
    - `source` (Dimension/Degenerate)

### **Dimension Tables**
- **`dim_company`**:
    - `company_id` (PK)
    - `company_name`
    - `industry`
- **`dim_location`**:
    - `location_id` (PK)
    - `city`
    - `country`
    - `remote_policy`
- **`dim_skill`** (Many-to-Many Bridge often needed, or simplified as array in Fact for lightweight analytics):
    - `skill_id` (PK)
    - `skill_name`
    - `category`

## Pipeline Layers

1. **Raw**: Original JSON/HTML from scrapers.
2. **Cleaned**: Standardized formats, deduplication (dedup key: `title` + `company` + `date`).
3. **Curated**: Enriched data (Skills parsed, Salary normalized), Model-ready.
4. **Artifacts**: Aggregated views, KPI summaries, Recommendation matrices.

## Deduplication Logic
We define a unique job by the composite key of `(normalized_title, company_name, location, published_date)`. Exact duplicates are dropped; similar ones are flagged.

## Future Scaling
- **Partitioning**: `fact_jobs` partitioned by `published_date` (Month/Year).
- **Streaming**: Real-time ingestion via Kafka would land in `raw` (S3/MinIO) and trigger micro-batch updates to `fact_jobs`.
