# Make commands for linting

SHELL := /bin/bash -euxo pipefail

.PHONY: yapf
yapf:
	yapf \
	    --diff \
	    --recursive \
	    --exclude .eggs \
	    .

.PHONY: fix-yapf
fix-yapf:
	yapf \
	    --in-place \
	    --recursive \
	    --exclude .eggs \
	    .

.PHONY: mypy
mypy:
	mypy *.py src/ tests/ admin

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
	isort --recursive --check-only

.PHONY: pip-extra-reqs
pip-extra-reqs:
	# We do nothing here.
	#
	# We want to ignore the sphinx-prompt because we cannot directly import
	# sphinx-prompt because it has a hyphen.
	# However, --ignore-requirement does not work:
	# https://github.com/r1chardj0n3s/pip-check-reqs/issues/6
	#
	# pip-extra-reqs --ignore-requirement sphinx-prompt src/

.PHONY: pip-missing-reqs
pip-missing-reqs:
	pip-missing-reqs src/

.PHONY: pylint
pylint:
	pylint *.py src/ tests/ admin/

.PHONY: pyroma
pyroma:
	pyroma --min 10 .

.PHONY: vulture
vulture:
	vulture --min-confidence 100 --exclude _vendor --exclude .eggs .

.PHONY: linkcheck
linkcheck:
	$(MAKE) -C docs/ linkcheck SPHINXOPTS=$(SPHINXOPTS)

.PHONY: spelling
spelling:
	$(MAKE) -C docs/ spelling SPHINXOPTS=$(SPHINXOPTS)

.PHONY: shellcheck
shellcheck:
	shellcheck --exclude SC2164,SC1091 */*.sh

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
