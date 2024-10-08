SHELL := /bin/bash -euxo pipefail

.PHONY: build-sample
build-sample:
	rm -rf sample/build
	uv run --extra=dev sphinx-build -W -b html sample/source sample/build

.PHONY: build-sample-parallel
build-sample-parallel:
	rm -rf sample/build
	uv run --extra=dev sphinx-build -j 2 -W -b html sample/source sample/build

.PHONY: open-sample
open-sample:
	python -c 'import os, webbrowser; webbrowser.open("file://" + os.path.abspath("sample/build/index.html"))'

.PHONY: sample
sample: build-sample open-sample
