# URL Shortener API

Production-ready URL Shortener built with FastAPI, PostgreSQL, Docker, and Alembic.

![Tests](https://img.shields.io/badge/tests-passing-brightgreen)
![Coverage](https://img.shields.io/badge/coverage-90%25-brightgreen)
![Python](https://img.shields.io/badge/python-3.12-blue)

## Techstack

FastAPI, PostgreSQL, SQLAlchemy 2.0, Alembic, Docker, Pytest and Pydantic v2

## Features

Shorten URLs, Redirect, Click tracking, Stats endpoint, Collision handling, 90%+ test coverage, Dockerized and Alembic migrations

## Local Setup

```bash
cd <your-repo-url>
python3 -m venv venv
source venv/bin/activate
```

Create .env:
```
DATABASE_URL=sqlite:///./test.db
BASE_URL=http://localhost:8000
```

Run:
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 9995
```

Then check:<br> 
http://localhost:9995<br>
http://localhost:9995/docs

Test Short URL Endpoint:<br>
http://localhost:9995/shorten

## Running Alembic revision
```bash
cd <your-repo-url>
alembic revision --autogenerate -m "create urls table"
```

## Running project in Docker container
```bash
cd <your-repo-url>
docker compose up --build
```

## Running tests in Docker container
```bash
cd <your-repo-url>
docker compose up --build
docker compose exec app pytest --cov=app --cov-report=term-missing
```