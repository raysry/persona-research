import pytest
from solution import is_valid


@pytest.mark.parametrize("s, expected", [
    ("()", True),
    ("()[]{}", True),
    ("(]", False),
    ("([)]", False),
    ("{[]}", True),
    ("", True),
    ("((()))", True),
    ("}{", False),
])
def test_is_valid(s, expected):
    assert is_valid(s) == expected
