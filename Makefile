SHELL=/bin/bash

.DEFAULT_GOAL := help

#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PYTHON_INTERPRETER = python3
CONFIG_FILE=configs.ini
CONFIG_KEY_NAME=required_python

#################################################################################
# BLOCK TO TEST PYTHON INSTALLATION                                             #
#################################################################################

# Test if python is installed

ifeq (,$(shell $(PYTHON_INTERPRETER) --version))
$(error "Python is not installed!")
endif


#################################################################################
# COMMANDS                                                                      #
#################################################################################

# Verify Python Version
check_installed_python:
	$(eval INSTALLED := $(shell $(PYTHON_INTERPRETER) --version | tr -cd '[[:digit:][:punct:]]'))
	$(eval REQUIRED := $(shell [ -f $(CONFIG_FILE) ] && cat $(CONFIG_FILE) | grep -w $(CONFIG_KEY_NAME) | cut -f2 -d "="))

	@if [ -z "$(REQUIRED)" ] | [ $(shell echo -n "$(REQUIRED)" | wc -c ) -lt 3 ]; then \
		echo "Missing configurarion file or key"; \
		return 1; \
	fi

	@if { echo "$(REQUIRED)" ; echo "$(INSTALLED)"; } | sort --version-sort --check=quiet; then \
		echo "Python interpreter is up to date: required Python '$(REQUIRED)' found Python '$(INSTALLED)'"; \
	else \
		echo "Python version error: required Python '$(REQUIRED)' found Python '$(INSTALLED)'" ; \
		exit 1; \
	fi

.PHONY: help
help: ## Shows this help text
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: init
init: clean install checkov test ## Clean environment and reinstall all dependencies

.PHONY: clean
clean: ## Removes project virtual env
	rm -rf .venv cdk.out build dist **/*.egg-info .pytest_cache node_modules .coverage

.PHONY: install
install: check_installed_python ## Install the project dependencies and pre-commit using pip.
	python3 -m venv .venv
	source .venv/bin/activate && pip install -r requirements.txt
	pip install -r requirements.txt
	pip install pre-commit
	pre-commit install --hook-type pre-commit --hook-type commit-msg --hook-type pre-push

.PHONY: test
test: ## Run tests
	python -m pytest

.PHONY: lint
lint: ## Apply linters to all files
	pre-commit run --all-files

.PHONY: synth
synth: ## Synthetize all Cdk stacks
	cdk synth

.PHONY: checkov
checkov: synth ## Run Checkov against IAC code
	checkov --config-file .checkov --baseline .checkov.baseline

.PHONY: checkov-baseline
checkov-baseline: synth ## Run checkov and create a new baseline for future checks
	checkov --config-file .checkov --create-baseline --soft-fail
	mv cdk.out/.checkov.baseline .checkov.baseline

###### Docker Commands

.PHONY: docker-build
docker-build: ## Build Docker containers
	docker-compose build

.PHONY: docker-start
docker-start: ## Start ETL and Dash app using Docker
	docker-compose up

.PHONY: docker-stop
docker-stop: ## Stop all running Docker containers related to this project
	docker-compose down

.PHONY: docker-logs
docker-logs: ## View real-time logs from the Docker containers
	docker-compose logs -f

.PHONY: docker-etl
docker-etl: ## Run the ETL process using Docker
	docker-compose run etl

.PHONY: docker-app
docker-app: ## Start only the Dash app using Docker
	docker-compose up dash-app
