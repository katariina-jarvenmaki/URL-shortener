# tests/test_routes.py

import pytest


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "URL Shortener API"}


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"message": "healthy"}


def test_shorten_url(client):
    response = client.post(
        "/shorten",
        json={"url": "https://google.com"},
    )

    assert response.status_code == 200
    data = response.json()

    assert "short_url" in data
    assert data["short_url"].startswith("http://")


def test_shorten_invalid_url(client):
    response = client.post(
        "/shorten",
        json={"url": "not-a-valid-url"},
    )

    assert response.status_code == 422  # Pydantic validation error


def test_duplicate_url_returns_same_code(client):
    r1 = client.post("/shorten", json={"url": "https://example.com"})
    r2 = client.post("/shorten", json={"url": "https://example.com"})

    assert r1.status_code == 200
    assert r2.status_code == 200

    assert r1.json()["short_url"] == r2.json()["short_url"]


def test_redirect_success(client):
    shorten = client.post(
        "/shorten",
        json={"url": "https://redirect-test.com"},
    )

    short_url = shorten.json()["short_url"]
    code = short_url.split("/")[-1]

    response = client.get(f"/{code}", follow_redirects=False)

    assert response.status_code in (302, 307)


def test_redirect_404(client):
    response = client.get("/nonexistent", follow_redirects=False)
    assert response.status_code == 404


def test_stats_success(client):
    shorten = client.post(
        "/shorten",
        json={"url": "https://stats-test.com"},
    )

    short_url = shorten.json()["short_url"]
    code = short_url.split("/")[-1]

    # Trigger one click
    client.get(f"/{code}", follow_redirects=False)

    stats = client.get(f"/stats/{code}")

    assert stats.status_code == 200
    data = stats.json()

    assert data["original_url"] == "https://stats-test.com"
    assert data["clicks"] == 1
    assert "created_at" in data


def test_stats_404(client):
    response = client.get("/stats/doesnotexist")
    assert response.status_code == 404