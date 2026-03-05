from app.core.config import get_settings

def test_get_settings_returns_same_instance():
    s1 = get_settings()
    s2 = get_settings()

    assert s1 is s2  # lru_cache should return same instance

def test_default_settings_values():
    settings = get_settings()

    assert settings.app_name == "URL Shortener"
    assert settings.host == "0.0.0.0"
    assert settings.port == 9995
    assert settings.debug is True
    assert isinstance(settings.allowed_hosts, list)