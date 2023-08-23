test:
	poetry run pytest -v --cov=winshift --cov-report=term-missing --cov-report=html

serv-coverage:
	poetry run python -m http.server 8000 --directory htmlcov

check:
	poetry run black --line-length 120 --check .
	poetry run prospector

format:
	poetry run black --line-length 120 .