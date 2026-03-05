run:
	uvicorn app.main:app --reload --port 9995

test:
	pytest --cov=app --cov-report=term-missing

docker:
	docker compose up --build

lint:
	ruff check .