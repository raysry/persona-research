import pytest
from solution import longest_valid_parentheses


@pytest.mark.parametrize("s, expected", [
    ("(()", 2),
    (")()())", 4),
    ("", 0),
    ("()()", 4),
    ("()(())", 6),
    (")(" , 0),
    ("(()()", 4),
    ("(()))(()", 4),
])
def test_longest_valid_parentheses(s, expected):
    assert longest_valid_parentheses(s) == expected
