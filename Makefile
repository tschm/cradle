# This file is part of the tschm/.config-templates repository
# (https://github.com/tschm/.config-templates).
#
# Colors for pretty output
BLUE := \033[36m
BOLD := \033[1m
GREEN := \033[32m
RESET := \033[0m

SOURCE_FOLDER := src/$(shell find src -mindepth 1 -maxdepth 1 -type d -not -path "*/\.*" | head -1 | sed 's|^src/||')
TESTS_FOLDER := tests
MARIMO_FOLDER := book/marimo
OPTIONS ?=

# Variables you can customize
BOOK_TITLE := "$(shell basename $(CURDIR))"
BOOK_SUBTITLE := "Documentation and Reports"

# Reads links.json content into a shell variable for uvx
BOOK_LINKS := $(shell cat _book/links.json)

.DEFAULT_GOAL := help

.PHONY: help verify install fmt lint deptry test build check marimo clean docs book marimushka

##@ Development Setup

uv:
	@printf "$(BLUE)Creating virtual environment...$(RESET)\n"
	@curl -LsSf https://astral.sh/uv/install.sh | sh

install: uv ## Install all dependencies using uv
	@printf "$(BLUE)Installing dependencies...$(RESET)\n"
	@uv venv --clear --python 3.12
	@if [ -f "pyproject.toml" ]; then \
		uv sync --all-extras --frozen; \
	else \
		printf "$(BLUE)No pyproject.toml found, skipping uv sync$(RESET)\n"; \
	fi

##@ Code Quality

fmt: uv ## Run code formatters only
	@printf "$(BLUE)Running formatters...$(RESET)\n"
	@uvx ruff format .

lint: uv ## Run linters only
	@printf "$(BLUE)Running linters...$(RESET)\n"
	@uvx pre-commit run --all-files

check: lint fmt deptry test ## Run all checks (lint and test)
	@printf "$(GREEN)All checks passed!$(RESET)\n"

deptry: uv ## Run deptry (use OPTIONS="--your-options" to pass options)
	@printf "$(BLUE)Running deptry...$(RESET)\n"
	@if [ -f "pyproject.toml" ]; then \
		uvx deptry $(SOURCE_FOLDER) $(OPTIONS); \
	else \
		printf "$(BLUE)No pyproject.toml found, skipping deptry$(RESET)\n"; \
	fi

##@ Testing

test: install
	@printf "$(BLUE)Running tests...$(RESET)\n"
	@if [ ! -f "README.md" ]; then \
		printf "$(BLUE)No README.md file found, skipping tests$(RESET)\n"; \
	elif [ -z "$(SOURCE_FOLDER)" ] || [ -z "$(TESTS_FOLDER)" ]; then \
		printf "$(BLUE)No valid source folder structure found, skipping tests$(RESET)\n"; \
	else \
		echo "$$GITHUB_REPOSITORY"; \
		uv pip install pytest pytest-cov pytest-html python-dotenv; \
		mkdir -p _tests/html-coverage _tests/html-report; \
		uv run pytest $(TESTS_FOLDER) \
			--cov=$(SOURCE_FOLDER) \
			--cov-report=term \
			--cov-report=html:_tests/html-coverage \
			--html=_tests/html-report/report.html; \
	fi

##@ Building

build: install ## Build the package
	@printf "$(BLUE)Building package...$(RESET)\n"
	@if [ -f "pyproject.toml" ]; then \
		uv pip install hatch; \
		uv run hatch build; \
	else \
		printf "$(BLUE)No pyproject.toml found, skipping build$(RESET)\n"; \
	fi

##@ Documentation

docs: install ## Build documentation
	@printf "$(BLUE)Building documentation...$(RESET)\n"
	@if [ -f "pyproject.toml" ]; then \
		uv pip install pdoc; \
		uv run pdoc -o _pdoc $(SOURCE_FOLDER); \
	else \
		printf "$(BLUE)No pyproject.toml found, skipping docs$(RESET)\n"; \
	fi

marimushka: install ## Export Marimo notebooks to HTML
	@printf "$(BLUE)Exporting notebooks from $(MARIMO_FOLDER)...$(RESET)\n"
	mkdir -p _marimushka

	@if [ ! -d "$(MARIMO_FOLDER)" ]; then \
		printf "$(BLUE)Warning: Directory $(MARIMO_FOLDER) does not exist$(RESET)\n"; \
		echo "<html><head><title>Marimo Notebooks</title></head><body><h1>Marimo Notebooks</h1><p>No notebooks directory found.</p></body></html>" > _marimushka/index.html; \
	else \
		py_files=$$(find "$(MARIMO_FOLDER)" -name "*.py" | tr '\n' ' '); \
		if [ -z "$$py_files" ]; then \
			printf "$(BLUE)No Python files found in $(MARIMO_FOLDER)$(RESET)\n"; \
			echo "<html><head><title>Marimo Notebooks</title></head><body><h1>Marimo Notebooks</h1><p>No notebooks found.</p></body></html>" > _marimushka/index.html; \
		else \
			printf "$(BLUE)Found Python files: $$py_files$(RESET)\n"; \
			for py_file in $$py_files; do \
				printf "$(BLUE)Processing $$py_file...$(RESET)\n"; \
				rel_path=$$(echo "$$py_file" | sed "s|^$(MARIMO_FOLDER)/||"); \
				dir_path=$$(dirname "$$rel_path"); \
				base_name=$$(basename "$$rel_path" .py); \
				mkdir -p "_marimushka/$$dir_path"; \
				uvx marimo export html --include-code --sandbox --output "_marimushka/$$dir_path/$$base_name.html" "$$py_file"; \
			done; \
			echo "<html><head><title>Marimo Notebooks</title></head><body><h1>Marimo Notebooks</h1><ul>" > _marimushka/index.html; \
			find _marimushka -name "*.html" -not -path "*index.html" | sort | while read html_file; do \
				rel_path=$$(echo "$$html_file" | sed "s|^_marimushka/||"); \
				name=$$(basename "$$rel_path" .html); \
				echo "<li><a href=\"$$rel_path\">$$name</a></li>" >> _marimushka/index.html; \
			done; \
			echo "</ul></body></html>" >> _marimushka/index.html; \
		fi; \
	fi

	# Create .nojekyll file to prevent GitHub Pages from processing with Jekyll
	touch _marimushka/.nojekyll

# Build the combined book
book:

	@echo "Building combined documentation..."
	mkdir -p _book

	# Copy API docs
	@if [ -d _pdoc ]; then \
		mkdir -p _book/pdoc; \
		cp -r _pdoc/* _book/pdoc; \
		echo '{"API": "./pdoc/index.html"}' > _book/links.json; \
	else \
		echo '{}' > _book/links.json; \
	fi

	# Copy coverage report
	@if [ -d _tests/html-coverage ]; then \
  		mkdir -p _book/tests/html-coverage; \
		cp -r _tests/html-coverage/* _book/tests/html-coverage; \
		jq '. + {"Coverage": "./tests/html-coverage/index.html"}' _book/links.json > _book/tmp && mv _book/tmp _book/links.json; \
	fi

	# Copy test report
	@if [ -d _tests/html-report ]; then \
  		mkdir -p _book/tests/html-report; \
		cp -r _tests/html-report/* _book/tests/html-report; \
		jq '. + {"Test Report": "./tests/html-report/report.html"}' _book/links.json > _book/tmp && mv _book/tmp _book/links.json; \
	fi

	# Copy marimushka report
	@if [ -d _marimushka ]; then \
		mkdir -p _book/marimushka; \
		cp -r _marimushka/* _book/marimushka; \
		jq '. + {"Notebooks": "./marimushka/index.html"}' _book/links.json > _book/tmp && mv _book/tmp _book/links.json; \
		echo "Copied notebooks from $(MARIMO_FOLDER) to _book/marimushka"; \
	fi

	@echo "Generated links.json:"
	@cat _book/links.json

	@echo "Generating landing page with uvx minibook..."
	@echo "Parsing links:"
	@if [ -f "_book/links.json" ]; then \
		if jq empty _book/links.json 2>/dev/null; then \
			echo "JSON is valid, using it directly"; \
			uvx minibook@v0.0.16 --title $(BOOK_TITLE) --subtitle $(BOOK_SUBTITLE) --links "$$(cat _book/links.json)" --output "_book"; \
		else \
			echo "JSON parsing failed, falling back to legacy format"; \
			uvx minibook@v0.0.16 --title $(BOOK_TITLE) --subtitle $(BOOK_SUBTITLE) --output "_book"; \
		fi; \
	else \
		echo "links.json not found, using default settings"; \
		uvx minibook@v0.0.16 --title $(BOOK_TITLE) --subtitle $(BOOK_SUBTITLE) --output "_book"; \
	fi

	# Create .nojekyll file to prevent GitHub Pages from processing with Jekyll
	touch "_book/.nojekyll"
	echo "Created .nojekyll file"


##@ Cleanup

clean: ## Clean generated files and directories
	@printf "$(BLUE)Cleaning project...$(RESET)\n"
	@git clean -d -X -f
	@rm -rf dist build *.egg-info .coverage .pytest_cache
	@printf "$(BLUE)Removing local branches with no remote counterpart...$(RESET)\n"
	@git fetch -p
	@git branch -vv | grep ': gone]' | awk '{print $$1}' | xargs -r git branch -D

##@ Marimo

marimo: install ## Start a Marimo server
	@printf "$(BLUE)Start Marimo server with $(MARIMO_FOLDER)...$(RESET)\n"
	@uv pip install marimo
	@uv run marimo edit $(MARIMO_FOLDER)

##@ Help

help: ## Display this help message
	@printf "$(BOLD)Usage:$(RESET)\n"
	@printf "  make $(BLUE)<target>$(RESET)\n\n"
	@printf "$(BOLD)Targets:$(RESET)\n"
	@awk 'BEGIN {FS = ":.*##"; printf ""} /^[a-zA-Z_-]+:.*?##/ { printf "  $(BLUE)%-15s$(RESET) %s\n", $$1, $$2 } /^##@/ { printf "\n$(BOLD)%s$(RESET)\n", substr($$0, 5) }' $(MAKEFILE_LIST)
