PYTHON ?= python
SEED ?= 42

RAW_INPUT ?= dsde/data/raw/input.csv
EXTRACT_OUT ?= dsde/data/raw/raw_jobs.csv
TRANSFORM_OUT ?= dsde/data/processed/clean_jobs.csv
EDA_OUT ?= dsde/artifacts/graphs/eda_summary.json
GRAPH_OUT ?= dsde/artifacts/figures/comp_value_by_category.html
MODEL_OUT ?= dsde/artifacts/recommender/simple_model.pkl
OUTPUT_DIR ?= dsde/data/processed

.PHONY: setup extract transform eda graph train run_all smoke_test export_web

setup:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r dsde/requirements.txt

extract:
	$(PYTHON) dsde/src/extract/extract.py --input $(RAW_INPUT) --output $(EXTRACT_OUT) --seed $(SEED)

transform:
	$(PYTHON) dsde/src/transform/transform.py --input $(EXTRACT_OUT) --output $(TRANSFORM_OUT) --seed $(SEED)

eda:
	$(PYTHON) dsde/src/viz/eda.py --input $(TRANSFORM_OUT) --output $(EDA_OUT) --seed $(SEED)

graph:
	$(PYTHON) dsde/src/viz/eda.py --input $(TRANSFORM_OUT) --output $(EDA_OUT) --figure $(GRAPH_OUT) --seed $(SEED)

train:
	$(PYTHON) dsde/src/models/train_model.py --input $(TRANSFORM_OUT) --output $(MODEL_OUT) --seed $(SEED)

run_all:
	$(PYTHON) dsde/src/run_all.py --input $(RAW_INPUT) --output $(OUTPUT_DIR) --seed $(SEED)

smoke_test:
	$(PYTHON) dsde/src/run_all.py --help

export_web:
	mkdir -p web
	@if [ -d dsde/reports ]; then cp -R dsde/reports web/; fi
