.PHONY: test run-sample install

install:
	pip install -r requirements.txt

test:
	PYTHONPATH=. pytest -v

run-sample:
	PYTHONPATH=. python -c "from src.ccm.nodes import run_pipeline; run_pipeline()"
