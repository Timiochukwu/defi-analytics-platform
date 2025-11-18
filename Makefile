.PHONY: help install install-dev test lint format clean docker-build docker-up docker-down run-api run-dashboard

help:
	@echo "DeFi Analytics Platform - Available Commands"
	@echo "============================================"
	@echo "install          Install production dependencies"
	@echo "install-dev      Install development dependencies"
	@echo "test             Run tests"
	@echo "test-cov         Run tests with coverage"
	@echo "lint             Run linters"
	@echo "format           Format code with black and isort"
	@echo "clean            Clean build artifacts"
	@echo "docker-build     Build Docker images"
	@echo "docker-up        Start Docker containers"
	@echo "docker-down      Stop Docker containers"
	@echo "run-api          Run FastAPI server locally"
	@echo "run-dashboard    Run Streamlit dashboard locally"
	@echo "setup-db         Setup database schema"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

test:
	pytest tests/

test-cov:
	pytest tests/ --cov=src --cov-report=html --cov-report=term

lint:
	flake8 src/ tests/
	mypy src/
	black --check src/ tests/
	isort --check-only src/ tests/

format:
	black src/ tests/
	isort src/ tests/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/ dist/ .pytest_cache/ htmlcov/ .coverage

docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

run-api:
	uvicorn src.api.main:app --reload --port 8000

run-dashboard:
	streamlit run dashboard/defi_dashboard.py

setup-db:
	python scripts/setup_database.py

migrate:
	alembic upgrade head

seed-data:
	python scripts/seed_data.py
