import pytest
from solution import length_of_longest_substring


@pytest.mark.parametrize("s, expected", [
    ("abcabcbb", 3),
    ("bbbbb", 1),
    ("pwwkew", 3),
    ("", 0),
    ("a", 1),
    ("dvdf", 3),
    ("anviaj", 5),
])
def test_length_of_longest_substring(s, expected):
    assert length_of_longest_substring(s) == expected
