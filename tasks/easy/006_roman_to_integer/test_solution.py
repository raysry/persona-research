import pytest
from solution import roman_to_int


@pytest.mark.parametrize("s, expected", [
    ("III", 3),
    ("LVIII", 58),
    ("MCMXCIV", 1994),
    ("IV", 4),
    ("IX", 9),
    ("XL", 40),
    ("CD", 400),
    ("MMXXVI", 2026),
])
def test_roman_to_int(s, expected):
    assert roman_to_int(s) == expected
