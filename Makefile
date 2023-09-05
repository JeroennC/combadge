.PHONY: all
all: install lint test build docs

.PHONY: clean
clean:
	poetry run ruff --clean
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -rf *.coverage coverage.*
	rm -rf dist

.PHONY: install
install:
	poetry install --all-extras --with=dev --with=docs

.PHONY: check
check: lint test

.PHONY: lint
lint: lint/ruff lint/mypy

.PHONY: lint/ruff
lint/ruff:
	poetry run ruff combadge tests

.PHONY: lint/mypy
lint/mypy:
	poetry run mypy combadge tests

.PHONY: format
format: format/ruff

.PHONY: format/ruff
format/ruff:
	poetry run ruff --fix combadge tests

.PHONY: test
test:
	poetry run pytest tests

.PHONY: build
build:
	poetry build

.PHONY: docs
docs:
	poetry run mkdocs build --site-dir _site
