# Make commands for linting

SHELL := /bin/bash -euxo pipefail

.PHONY: mypy
mypy:
	mypy .

.PHONY: pyright
pyright:
	pyright .

.PHONY: check-manifest
check-manifest:
	check-manifest .

.PHONY: doc8
doc8:
	doc8 .

.PHONY: ruff
ruff:
	ruff .
	ruff format --check .

.PHONY: fix-ruff
fix-ruff:
	ruff --fix .
	ruff format .

.PHONY: pip-extra-reqs
pip-extra-reqs:
	# We ignore the sphinx-prompt because we do not import it but we require it
	# so that users can set it before our extension.
	pip-extra-reqs --requirements-file=<(pdm export --pyproject) --ignore-requirement sphinx-prompt src/

.PHONY: pip-missing-reqs
pip-missing-reqs:
	pip-missing-reqs --requirements-file=<(pdm export --pyproject) src/

.PHONY: pylint
pylint:
	pylint src/ tests/

.PHONY: pyroma
pyroma:
	pyroma --min 10 .

.PHONY: pyproject-fmt
 pyproject-fmt:
	pyproject-fmt --check  pyproject.toml

 .PHONY: fix-pyproject-fmt
 fix-pyproject-fmt:
	pyproject-fmt  pyproject.toml

.PHONY: vulture
vulture:
	vulture --min-confidence 100 --exclude _vendor --exclude .eggs .
