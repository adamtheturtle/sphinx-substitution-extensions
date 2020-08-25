SHELL := /bin/bash -euxo pipefail

include lint.mk

.PHONY: lint
lint: \
    check-manifest \
    doc8 \
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
fix-lint: \
    autoflake \
    fix-yapf \
    fix-isort
