SHELL := /bin/bash -euxo pipefail

include lint.mk

.PHONY: lint
lint: \
    check-manifest \
    flake8 \
    isort \
    mypy \
    pip-extra-reqs \
    pip-missing-reqs \
    pyroma \
    shellcheck \
    vulture \
    pylint \
    pydocstyle \
    yapf

.PHONY: fix-lint
fix-lint:
	# Move imports to a single line so that autoflake can handle them.
	# See https://github.com/myint/autoflake/issues/8.
	# Then later we put them back.
	isort --force-single-line --recursive --apply
	$(MAKE) autoflake
	$(MAKE) fix-yapf
	isort --recursive --apply

.PHONY: build-sample
build-sample:
	rm -rf sample/build
	sphinx-build -W -b html sample/source sample/build

.PHONY: open-sample
open-sample:
	python -c 'import os, webbrowser; webbrowser.open("file://" + os.path.abspath("sample/build/index.html"))'

.PHONY: sample
sample: build-sample open-sample
