PYTHON ?= python3
VENV_PYTHON = .venv/bin/python
VENV_PYTEST = .venv/bin/pytest

all: csrc test

csrc:
	$(MAKE) -C csrc

cmake-build:
	cmake -B build && cmake --build build

test: csrc
	PYTHONPATH=src $(VENV_PYTEST) tests/ -v

audit:
	$(PYTHON) scripts/audit_safety_invariants.py

demo: csrc
	PYTHONPATH=src $(VENV_PYTHON) -m symbolic_alpha.cli demo

benchmark: csrc
	PYTHONPATH=src $(VENV_PYTHON) -m symbolic_alpha.cli benchmark --rows 100000

mine: csrc
	PYTHONPATH=src $(VENV_PYTHON) -m symbolic_alpha.cli mine

clean:
	$(MAKE) -C csrc clean
	rm -rf build dist *.egg-info .pytest_cache
	find . -type d -name __pycache__ -exec rm -rf {} +

.PHONY: all csrc cmake-build test audit demo benchmark mine clean
