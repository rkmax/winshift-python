test:
	poetry run pytest -v --cov=divvy --cov-fail-under=90 --cov-report=term-missing --cov-report=html

serv-coverage:
	poetry run python -m http.server 8000 --directory htmlcov