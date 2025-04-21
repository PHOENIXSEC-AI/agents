.PHONY: clean clean-pyc clean-test clean-all update update-lock install-full

clean: clean-pyc clean-test ## Remove all build, test, and Python artifacts

clean-pyc: ## Remove Python file artifacts
	find . -name '*.pyc' -delete
	find . -name '*.pyo' -delete
	find . -name '*~' -delete
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '.pytest_cache' -exec rm -rf {} +
	find . -name '.coverage' -delete

clean-test: ## Remove test and coverage artifacts
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache
	rm -rf .tox/

clean-all: clean-pyc ## Remove all .venv and dist folders recursively from all subdirectories
	find . -type d -name '.venv' -exec rm -rf {} +
	find . -type d -name 'dist' -exec rm -rf {} +
	find . -type d -name 'build' -exec rm -rf {} +
	find . -type f -name 'poetry.lock' -exec rm -f {} \;

install-full: clean-all ## Build distribution packages
	./scripts/poetry-install.sh

update-lock:
	./scripts/poetry-lock-no-update.sh

update:
	./scripts/poetry-lock-update.sh

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)