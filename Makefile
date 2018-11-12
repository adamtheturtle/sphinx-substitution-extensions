SHELL := /bin/bash -euxo pipefail

include lint.mk


.PHONY: lint
# We do not currently run pydocstyle as we have to ignore vendored items.
lint: \
    check-manifest \
    custom-linters \
    doc8 \
    flake8 \
    isort \
    mypy \
    pip-extra-reqs \
    pip-missing-reqs \
    pylint \
    pyroma \
    vulture \
    yapf

# Fix some linting errors.
.PHONY: fix-lint
fix-lint:
	# Move imports to a single line so that autoflake can handle them.
	# See https://github.com/myint/autoflake/issues/8.
	# Then later we put them back.
	isort --force-single-line --recursive --apply
	$(MAKE) autoflake
	isort --recursive --apply
	$(MAKE) fix-yapf

.PHONY: sample
sample:
	sphinx-build -b html sample/source sample/build
	python -c 'import os, webbrowser; webbrowser.open("file://" + os.path.abspath("sample/build/contents.html"))'
