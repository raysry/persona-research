import pytest
from solution import is_palindrome


@pytest.mark.parametrize("x, expected", [
    (121, True),
    (-121, False),
    (10, False),
    (0, True),
    (12321, True),
    (12345, False),
    (1001, True),
])
def test_is_palindrome(x, expected):
    assert is_palindrome(x) == expected
