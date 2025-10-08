.PHONY: help install test lint format clean run dev security

help:
	@echo "Available commands:"
	@echo "  install     Install dependencies"
	@echo "  test        Run tests"
	@echo "  lint        Run linting"
	@echo "  format      Format code"
	@echo "  typecheck   Run type checking"
	@echo "  security    Run security checks"
	@echo "  clean       Clean cache files"
	@echo "  run         Run production server"
	@echo "  dev         Run development server"

install:
	pip install --upgrade pip setuptools wheel
	pip install -r requirements.txt

install-dev: install
	pip install -e .

setup-venv:
	python -m venv .venv
	@echo "Virtual environment created. Activate with: source .venv/bin/activate"

clean-deps:
	pip freeze | grep -v "^-e" | xargs pip uninstall -y

reinstall: clean-deps install

test:
	pytest -v --cov=. --cov-report=html

lint:
	flake8 .
	pylint *.py

format:
	black .
	isort .

typecheck:
	mypy .

security:
	bandit -r .
	safety check

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -rf htmlcov/
	rm -f .coverage

run:
	python main.py

dev:
	uvicorn main:app --reload --host 0.0.0.0 --port 8000
