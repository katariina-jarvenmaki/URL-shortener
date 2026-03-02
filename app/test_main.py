from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.main import app
from app import settings
import tempfile
import pytest

@pytest.fixture
def test_client():
    with tempfile.NamedTemporaryFile() as tmp:
        settings.database_url = tmp.name
        with TestClient(app) as c:
            yield c

@pytest.fixture
def use_temp_db():
    with tempfile.NamedTemporaryFile() as tmp:
        settings.database_url = tmp.name
        yield

def test_home(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "URL Shortener API"}

def test_shorten_url(test_client):
    response = test_client.post("/shorten", json={"url": "https://google.com"})
    assert response.status_code == 200
    data = response.json()
    assert "short_url" in data
    short_url = data["short_url"]
    assert short_url.startswith("http://localhost:8000/")

def test_redirect(test_client):
    response = test_client.post("/shorten", json={"url": "https://google.com"})
    short_url = response.json()["short_url"]
    code = short_url.split("/")[-1]

    redirect = test_client.get(f"/{code}", follow_redirects=False)
    assert redirect.status_code == 307

def test_duplicate_url_returns_same_code(test_client):
    r1 = test_client.post("/shorten", json={"url": "https://example.com"})
    r2 = test_client.post("/shorten", json={"url": "https://example.com"})

    assert r1.status_code == 200
    assert r2.status_code == 200
    assert r1.json()["short_url"] == r2.json()["short_url"]

def test_stats_endpoint(test_client):
    response = test_client.post("/shorten", json={"url": "https://stats-test.com"})
    code = response.json()["short_url"].split("/")[-1]

    test_client.get(f"/{code}", follow_redirects=False)

    stats = test_client.get(f"/stats/{code}")
    assert stats.status_code == 200
    data = stats.json()
    assert data["clicks"] == 1

def test_redirect_404(test_client):
    response = test_client.get("/nonexistent", follow_redirects=False)
    assert response.status_code == 404