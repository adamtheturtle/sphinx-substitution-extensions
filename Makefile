SHELL := /bin/bash -euxo pipefail

include lint.mk

.PHONY: lint
lint: \
    black \
    check-manifest \
    doc8 \
    flake8 \
    isort \
    mypy \
    pip-extra-reqs \
    pip-missing-reqs \
    pyroma \
    vulture \
    pylint \
    pydocstyle

.PHONY: fix-lint
fix-lint: \
    autoflake \
    fix-black \
    fix-isort

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
