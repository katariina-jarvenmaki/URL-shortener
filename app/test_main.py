from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "URL Shortener API"}

def test_shorten_url():
    response = client.post("/shorten", json={"url": "https://google.com"})
    assert response.status_code == 200
    data = response.json()
    assert "short_url" in data
    short_url = data["short_url"]
    assert short_url.startswith("http://localhost:8000/")