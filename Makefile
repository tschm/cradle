.DEFAULT_GOAL := help

venv:
	@curl -LsSf https://astral.sh/uv/install.sh | sh
	@uv venv --python 3.12


.PHONY: verify
verify:  ## Run a simple verification
	ssh -T git@github.com || true
	gh --version


.PHONY: clean
clean: ## clean the folder
	@git clean -d -X -f


.PHONY: install
install: venv ## Install all dependencies (in the virtual environment) defined in requirements.txt
	@uv sync --dev --frozen


.PHONY: help
help:  ## Display this help screen
	@echo -e "\033[1mAvailable commands:\033[0m"
	@grep -E '^[a-z.A-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}' | sort


.PHONY: test
test: install ## Run all notebooks in a test
	@uv pip install pytest
	@uv run pytest src/tests


.PHONY: cradle
cradle: install ## Run the cradle app
	@uv run cradle


.PHONY: fmt
fmt: venv ## Run autoformatting and linting
	@uv pip install pre-commit
	@uv run pre-commit install
	@uv run pre-commit run --all-files
