PYTHON     := python3
PIP        := $(PYTHON) -m pip
VENV       := .venv
VENV_BIN   := $(VENV)/bin
VENV_PY    := $(VENV_BIN)/python
VENV_PIP   := $(VENV_BIN)/pip

.DEFAULT_GOAL := run

#creation venv
$(VENV)/bin/activate:
	$(PYTHON) -m venv $(VENV)

.PHONY: install
install: $(VENV)/bin/activate ## Crée le venv et installe les dépendances
	$(VENV_PIP) install --upgrade pip
	$(VENV_PIP) install python-sat

# lancement main 

.PHONY: run
run: install 
	$(VENV_PY) main.py

# TODO : add lancement tests

#delete cache
.PHONY: clean
clean: 
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -name "*.pyc" -delete

.PHONY: clean-all
clean-all: clean ## Supprime aussi le venv
	rm -rf $(VENV)

.PHONY: help
help: ## Affiche cette aide
	@grep -E '^[a-zA-Z_-]+:.*##' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*##"}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'