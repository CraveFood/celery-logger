.PHONY: help
.DEFAULT_GOAL := help

clean: clean-build clean-pyc ## remove all build, test, coverage and Python artifacts

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

help:
	@python3 -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

lint: ## check style with flake8
	flake8 celerylogger tests sample-project

install-requirements: clean ## installs requirements locally
	pip install -r requirements/dev.txt
	pip install -r requirements/tests.txt
	pip install -r requirements/base.txt

build: clean-build ## Builds python package
	python3 setup.py sdist bdist_wheel

upload: ## Upload package to pypi
	python -m twine upload dist/*  --repository pypi --verbose
