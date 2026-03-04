# URL-shortener
URL-shortener project to showcase python use

## Create venv
```bash
cd /opt/kjc/int/URL-shortener
python3 -m venv venv
source venv/bin/activate
```

## Run locally
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
Then check:<br> 
http://127.0.0.1:8000<br>
http://127.0.0.1:8000/docs

Test Short URL Endpoint:<br>
http://127.0.0.1:8000/shorten

## Running a test
```bash
PYTHONPATH=./ pytest
export PYTHONPATH=$(pwd)
python -m pytest --cov=app --cov-report=term-missing
```

## Running Alembic revision
```bash
cd /opt/kjc/int/URL-shortener
alembic revision --autogenerate -m "create urls table"
```

## Running project in Docker container
```bash
cd /opt/kjc/int/URL-shortener
docker compose up --build
```