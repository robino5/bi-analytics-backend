port=8000  # default django run port

clean: clean-pyc clean-build clean-test ## remove all build, test, coverage and Python artifacts

runprocess: test lint precommit clean

test: ## run tests for django api
	poetry run pytest

clean-build: ## remove build artifacts
	rm -rf -f build/
	rm -rf -f dist/
	rm -rf -f .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

migrate: ## run django migations & migrate
	poetry run python manage.py makemigrations
	poetry run python manage.py migrate

coverage: ## run the coverage checks
	poetry run coverage run -m pytest
	poetry run coverage report
	poetry run coverage html

install: ## install the project dependencies
	poetry install

precommit: ## run the pre-commit hook
	poetry run pre-commit run --all-files

run: # run the django server
	poetry run python manage.py runserver 0.0.0.0:${port} --noasgi

run-celery: # run the celery worker
	poetry run celery -A core worker -l info

lint: # lint the codes
	poetry run ruff --fix .
	poetry run pre-commit run --all-files -c .pre-commit-config.yaml
