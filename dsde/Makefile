PYTHON ?= python
PYTHONPATH ?= .
SEED ?= 42
SAMPLE_N ?= 2000

KAGGLE_DATASET ?= arshkon/linkedin-job-postings
KAGGLE_OUT_DIR ?= data/raw/kaggle
KAGGLE_INPUT ?=
KAGGLE_SCHEMA_PATH ?= $(KAGGLE_OUT_DIR)/jobs_kaggle_raw.parquet

REMOTIVE_OUT_DIR ?= data/raw/remotive
REMOTIVE_URL ?= https://remotive.com/api/remote-jobs
REMOTIVE_SCHEMA_PATH ?= $(REMOTIVE_OUT_DIR)/jobs_remotive_raw.parquet
SCHEMA_REPORT ?= artifacts/schema_report.json

RAW_INPUT ?= data/raw/input.csv
EXTRACT_OUT ?= data/raw/raw_jobs.csv
TRANSFORM_OUT ?= data/processed/clean_jobs.csv
EDA_OUT ?= artifacts/graphs/eda_summary.json
GRAPH_OUT ?= artifacts/figures/comp_value_by_category.html
MODEL_OUT ?= artifacts/recommender/simple_model.pkl
OUTPUT_DIR ?= data/processed

.PHONY: setup extract transform analytics graph train run_all smoke_test export_web

setup:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt

extract:
	@if [ -z "$(KAGGLE_INPUT)" ]; then echo "KAGGLE_INPUT is required (path to Kaggle CSV/Parquet)"; exit 1; fi
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m src.extract.fetch_kagglehub --dataset $(KAGGLE_DATASET) --out_dir $(KAGGLE_OUT_DIR) --seed $(SEED)
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m src.extract.ingest_kaggle $(if $(KAGGLE_INPUT),--input_path $(KAGGLE_INPUT),) --out_dir $(KAGGLE_OUT_DIR) --sample_n $(SAMPLE_N) --seed $(SEED)
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m src.extract.fetch_remotive --api_url $(REMOTIVE_URL) --out_dir $(REMOTIVE_OUT_DIR) --sample_n $(SAMPLE_N) --seed $(SEED)
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m src.utils.schema_report $(if $(KAGGLE_SCHEMA_PATH),--kaggle-path $(KAGGLE_SCHEMA_PATH),) --remotive-path $(REMOTIVE_SCHEMA_PATH) --output $(SCHEMA_REPORT) --seed $(SEED)

transform:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m src.transform.clean_kaggle --input $(KAGGLE_OUT_DIR)/jobs_kaggle_raw.parquet --output data/processed/jobs_kaggle_clean.parquet --seed $(SEED)
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m src.transform.clean_remotive --input $(REMOTIVE_OUT_DIR)/jobs_remotive_raw.parquet --output data/processed/jobs_remotive_clean.parquet --seed $(SEED)
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m src.transform.build_canonical_jobs --kaggle data/processed/jobs_kaggle_clean.parquet --remotive data/processed/jobs_remotive_clean.parquet --output data/processed/jobs_canonical.parquet --seed $(SEED)

eda:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m src.viz.eda --input $(TRANSFORM_OUT) --output $(EDA_OUT) --seed $(SEED)

analytics:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m src.analytics.build_tables --input data/processed/jobs_canonical.parquet --seed $(SEED)
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m src.analytics.make_figures --seed $(SEED)

graph:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m src.transform.skill_graph --input data/processed/jobs_canonical.parquet --output artifacts/graphs/skill_graph.json --min_edge_weight 5 --seed $(SEED)

train:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m src.models.train_recommender --input data/processed/jobs_canonical.parquet --model_dir artifacts/recommender --top_k 10 --seed $(SEED)

run_all:
	@if [ -z "$(KAGGLE_INPUT)" ] && [ "$(SKIP_EXTRACT)" != "1" ]; then echo "KAGGLE_INPUT is required unless SKIP_EXTRACT=1"; exit 1; fi
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m src.run_all $(if $(KAGGLE_INPUT),--kaggle_input $(KAGGLE_INPUT),) $(if $(KAGGLE_DATASET),--kaggle_dataset $(KAGGLE_DATASET),) $(if $(filter 1,$(SKIP_EXTRACT)),--skip_extract,) --seed $(SEED)

smoke_test:
	$(MAKE) run_all SKIP_EXTRACT=1
	PYTHONPATH=$(PYTHONPATH) pytest -q

export_web:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m src.utils.export_to_web --web_public_dir web/public/artifacts
