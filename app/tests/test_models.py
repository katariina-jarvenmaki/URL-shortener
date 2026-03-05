from app.db.models import URL

def test_url_model_defaults(db_session):
    url = URL(
        short_code="abc123",
        original_url="https://example.com",
    )

    db_session.add(url)
    db_session.commit()
    db_session.refresh(url)

    assert url.id is not None
    assert url.clicks == 0
    assert url.created_at is not None
    assert url.last_accessed is None

def test_url_repr(db_session):
    url = URL(
        short_code="xyz789",
        original_url="https://repr-test.com",
    )

    db_session.add(url)
    db_session.commit()
    db_session.refresh(url)

    repr_output = repr(url)

    assert "URL" in repr_output
    assert "xyz789" in repr_output
    assert "https://repr-test.com" in repr_output