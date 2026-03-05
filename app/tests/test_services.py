import pytest
from unittest.mock import patch

from app.services import url_service
from app.db.models import URL


def test_create_short_url_creates_new(db_session):
    short_url = url_service.create_short_url(
        db_session,
        "https://new-url.com",
    )

    assert short_url.startswith("http://")

    entry = db_session.query(URL).first()
    assert entry is not None
    assert entry.original_url == "https://new-url.com"


def test_create_short_url_returns_existing(db_session):
    first = url_service.create_short_url(
        db_session,
        "https://duplicate.com",
    )

    second = url_service.create_short_url(
        db_session,
        "https://duplicate.com",
    )

    assert first == second
    assert db_session.query(URL).count() == 1


def test_create_short_url_collision_failure(db_session):
    with patch(
        "app.services.url_service.generate_short_code",
        return_value="fixedcode",
    ):
        # First insert works
        url_service.create_short_url(db_session, "https://a.com")

        # Force collision repeatedly
        with pytest.raises(RuntimeError):
            url_service.create_short_url(db_session, "https://b.com")


def test_get_original_url_success(db_session):
    short_url = url_service.create_short_url(
        db_session,
        "https://lookup.com",
    )
    code = short_url.split("/")[-1]

    original = url_service.get_original_url(db_session, code)

    assert original == "https://lookup.com"


def test_get_original_url_not_found(db_session):
    result = url_service.get_original_url(db_session, "missing")
    assert result is None


def test_increment_clicks_success(db_session):
    short_url = url_service.create_short_url(
        db_session,
        "https://click-test.com",
    )
    code = short_url.split("/")[-1]

    success = url_service.increment_clicks(db_session, code)

    assert success is True

    entry = db_session.query(URL).first()
    assert entry.clicks == 1
    assert entry.last_accessed is not None


def test_increment_clicks_not_found(db_session):
    result = url_service.increment_clicks(db_session, "missing")
    assert result is False


def test_get_stats_success(db_session):
    short_url = url_service.create_short_url(
        db_session,
        "https://stats.com",
    )
    code = short_url.split("/")[-1]

    url_service.increment_clicks(db_session, code)

    stats = url_service.get_stats(db_session, code)

    assert stats is not None
    assert stats["original_url"] == "https://stats.com"
    assert stats["clicks"] == 1
    assert stats["created_at"] is not None


def test_get_stats_not_found(db_session):
    stats = url_service.get_stats(db_session, "missing")
    assert stats is None