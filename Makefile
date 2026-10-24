.PHONY: test run-sample install

install:
	pip install -r requirements.txt

test:
	pytest

run-sample:
	PYTHONPATH=. python -m archaudit.pipeline policies/controls.yaml samples/audit_pack
