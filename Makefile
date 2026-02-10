SHELL = /bin/bash

help: Makefile
	@echo
	@echo "Choose a command to run:"
	@echo
	@sed -n 's/^##//p' $< | column -t -s ':' |  sed -e 's/^/ /'
	@echo

## clean: Remove all build, test, coverage and Python artifacts
clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
	find . -name '*log' -exec rm -fr {} +
	rm -rf build/ dist/ *.egg-info src/*.egg-info .eggs/
	rm -rf .coverage htmlcov/ .pytest_cache/

## run: Run the application
run:
	uv run python main.py

## test: Run the test cases using pytest
test:
	uv run pytest .

## test-coverage: Run tests with coverage report
test-coverage:
	uv run pytest --cov=sort --cov-report=term-missing --cov-report=html

## uv: Install and manage uv package manager
uv: uv
	@command -v uv >/dev/null 2>&1 || { \
		echo "Installing uv package manager..."; \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
	}
	@echo "uv is installed at: $$(command -v uv)"

## venv-create: Create a virtual environment and install dependencies using uv
venv-create: uv
	uv venv
	uv pip install -e "."

## venv-delete: Delete the virtual environment
venv-delete:
	rm -rf .venv

## venv-lock: Generate uv.lock from pyproject.toml
venv-lock:
	uv lock

## venv-sync: Sync dependencies from uv.lock
venv-sync:
	uv sync --all-extras

## venv-upgrade: Update dependencies in the virtual environment
venv-upgrade:
	uv lock --upgrade
	uv sync --all-extras
