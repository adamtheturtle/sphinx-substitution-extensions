# Make commands for linting

SHELL := /bin/bash -euxo pipefail

.PHONY: black
black:
	black --check .

.PHONY: fix-black
fix-black:
	black .

.PHONY: mypy
mypy:
	mypy .

.PHONY: check-manifest
check-manifest:
	check-manifest .

.PHONY: doc8
doc8:
	doc8 .

.PHONY: flake8
flake8:
	flake8 .

.PHONY: isort
isort:
	isort --check-only .

.PHONY: fix-isort
fix-isort:
	isort .

.PHONY: pip-extra-reqs
pip-extra-reqs:
	# We ignore the sphinx-prompt because we do not import it but we require it
	# so that users can set it before our extension.
	pip-extra-reqs --requirements-file=requirements/requirements.txt --ignore-requirement sphinx-prompt src/

.PHONY: pip-missing-reqs
pip-missing-reqs:
	pip-missing-reqs --requirements-file=requirements/requirements.txt src/

.PHONY: pylint
pylint:
	pylint *.py src/ tests/

.PHONY: pyroma
pyroma:
	pyroma --min 10 .

.PHONY: vulture
vulture:
	vulture --min-confidence 100 --exclude _vendor --exclude .eggs .

.PHONY: autoflake
autoflake:
	autoflake \
	    --in-place \
	    --recursive \
	    --remove-all-unused-imports \
	    --remove-unused-variables \
	    --expand-star-imports \
	    --exclude _vendor,release \
	    .

.PHONY: pydocstyle
pydocstyle:
	pydocstyle
