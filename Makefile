# YouTube Transcriptor Makefile
# Provides convenient commands for development and testing

.PHONY: help install test test-cov lint format clean build run docs setup

# Default target
help: ## Show this help message
	@echo "YouTube Transcriptor Development Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

# Setup and Installation
setup: ## Set up development environment
	@echo "Setting up development environment..."
	@if command -v uv >/dev/null 2>&1; then \
		uv sync --dev; \
		echo "Environment setup complete with uv"; \
	else \
		echo "uv not found. Please install uv first: https://github.com/astral-sh/uv"; \
		exit 1; \
	fi

install: ## Install the package in development mode
	uv pip install -e ".[dev]"

# Development Commands
test: ## Run all tests
	@echo "Running test suite..."
	uv run python -m pytest tests/ -v

test-cov: ## Run tests with coverage report
	@echo "Running tests with coverage..."
	uv run python -m pytest tests/ --cov=src --cov-report=html --cov-report=term

test-specific: ## Run specific test file (usage: make test-specific TEST=test_utils.py)
	@echo "Running specific test: $(TEST)"
	uv run python -m pytest tests/$(TEST) -v

# Code Quality
lint: ## Run code linting
	@echo "Running code linting..."
	@if command -v flake8 >/dev/null 2>&1; then \
		flake8 src/ tests/; \
	else \
		echo "flake8 not found. Install with: uv add --dev flake8"; \
	fi

format: ## Format code with black
	@echo "Formatting code..."
	@if command -v black >/dev/null 2>&1; then \
		black src/ tests/; \
	else \
		echo "black not found. Install with: uv add --dev black"; \
	fi

format-check: ## Check code formatting without modifying files
	@echo "Checking code formatting..."
	@if command -v black >/dev/null 2>&1; then \
		black --check src/ tests/; \
	else \
		echo "black not found. Install with: uv add --dev black"; \
	fi

# Build and Distribution
clean: ## Clean up build artifacts and cache files
	@echo "Cleaning up..."
	@rm -rf build/
	@rm -rf dist/
	@rm -rf *.egg-info/
	@rm -rf .pytest_cache/
	@rm -rf htmlcov/
	@find . -type d -name __pycache__ -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete
	@echo "Clean complete"

build: clean ## Build the package
	@echo "Building package..."
	@if command -v python >/dev/null 2>&1; then \
		python -m build; \
	else \
		echo "Python not found in PATH"; \
		exit 1; \
	fi

# Documentation
docs: ## Generate documentation
	@echo "Documentation available in docs/ directory"
	@echo "- API Documentation: docs/API.md"
	@echo "- Architecture Guide: docs/ARCHITECTURE.md"
	@echo "- Development Guide: docs/DEVELOPMENT.md"
	@echo "- Contributing Guidelines: docs/CONTRIBUTING.md"

# Running the Application
run: ## Run the application with help
	@echo "Running YouTube Transcriptor..."
	uv run python -m src.main --help

run-example: ## Run with example URL
	@echo "Running example with test URL..."
	uv run python -m src.main "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --output ./example_output

# Quality Checks
check-all: format-check lint test ## Run all quality checks (format, lint, test)
	@echo "All quality checks completed!"

ci: format-check lint test-cov ## Run CI pipeline (format check, lint, test with coverage)
	@echo "CI pipeline completed!"

# Development Utilities
dev-setup: setup ## Alias for setup
	@echo "Development environment ready!"

quick-test: ## Run tests without coverage (faster)
	@echo "Running quick tests..."
	uv run python -m pytest tests/ -x --tb=short

watch-test: ## Watch for changes and run tests (requires watchdog)
	@echo "Watching for changes and running tests..."
	@if command -v watchmedo >/dev/null 2>&1; then \
		watchmedo shell-command --patterns="*.py" --recursive --command="make quick-test"; \
	else \
		echo "watchdog not found. Install with: uv add --dev watchdog"; \
		echo "Or manually run: make quick-test"; \
	fi

# Project Information
info: ## Show project information
	@echo "YouTube Transcriptor Project Information:"
	@echo "======================================="
	@echo "Python Version: $(shell python --version 2>/dev/null || echo 'Python not found')"
	@echo "UV Version: $(shell uv --version 2>/dev/null || echo 'uv not found')"
	@echo "Working Directory: $(shell pwd)"
	@echo "Git Branch: $(shell git branch --show-current 2>/dev/null || echo 'Not a git repository')"
	@echo "Git Status: $(shell git status --porcelain 2>/dev/null | wc -l) files changed"

coverage-report: ## Open coverage report in browser
	@if [ -f "htmlcov/index.html" ]; then \
		@echo "Opening coverage report..."
		@if command -v python >/dev/null 2>&1; then \
			python -m webbrowser htmlcov/index.html; \
		else \
			echo "Open htmlcov/index.html in your browser"; \
		fi; \
	else \
		echo "Coverage report not found. Run 'make test-cov' first."; \
	fi

# Advanced Commands
benchmark: ## Run performance benchmarks
	@echo "Running performance benchmarks..."
	@echo "Note: This requires benchmark test cases to be implemented"
	uv run python -m pytest tests/ -k benchmark -v

security-check: ## Run security checks on dependencies
	@echo "Running security checks..."
	@if command -v safety >/dev/null 2>&1; then \
		safety check; \
	else \
		echo "safety not found. Install with: uv add --dev safety"; \
	fi

# Release Preparation
pre-release: clean format-check lint test-cov docs ## Prepare for release
	@echo "Pre-release checks completed!"
	@echo "Ready to create a release."

# Installation verification
verify-install: ## Verify installation and setup
	@echo "Verifying installation..."
	@echo "Python version: $(shell python --version)"
	@echo "Package location: $(shell python -c "import src; print(src.__file__)" 2>/dev/null || echo "Package not installed")"
	@echo "Running import test..."
	@python -c "from src.transcriptor import get_transcript; print('✓ Imports successful')" 2>/dev/null || echo "✗ Import failed"
	@echo "Verification complete"