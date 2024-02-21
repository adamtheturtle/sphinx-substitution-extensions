SHELL := /bin/bash -euxo pipefail

include lint.mk

.PHONY: lint
lint: \
    actionlint \
    check-manifest \
    deptry \
    doc8 \
    mypy \
    pyproject-fmt \
    pyright \
    pyroma \
    ruff \
    vulture \
    pylint

.PHONY: fix-lint
fix-lint: \
    fix-pyproject-fmt \
    fix-ruff

.PHONY: build-sample
build-sample:
	rm -rf sample/build
	sphinx-build -W -b html sample/source sample/build

.PHONY: build-sample-parallel
build-sample-parallel:
	rm -rf sample/build
	sphinx-build -j 2 -W -b html sample/source sample/build

.PHONY: open-sample
open-sample:
	python -c 'import os, webbrowser; webbrowser.open("file://" + os.path.abspath("sample/build/index.html"))'

.PHONY: sample
sample: build-sample open-sample
