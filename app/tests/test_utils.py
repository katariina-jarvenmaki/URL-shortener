import string
from app.utils.short_code import generate_short_code

def test_generate_short_code_length():
    code = generate_short_code(8)
    assert len(code) == 8

def test_generate_short_code_is_alphanumeric():
    code = generate_short_code(12)
    allowed = string.ascii_letters + string.digits

    for char in code:
        assert char in allowed

def test_generate_short_code_randomness():
    code1 = generate_short_code()
    code2 = generate_short_code()

    assert code1 != code2  # extremely unlikely to fail