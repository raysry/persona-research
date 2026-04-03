import pytest
from solution import reverse_string


@pytest.mark.parametrize("s, expected", [
    (["h", "e", "l", "l", "o"], ["o", "l", "l", "e", "h"]),
    (["H", "a", "n", "n", "a", "h"], ["h", "a", "n", "n", "a", "H"]),
    (["a"], ["a"]),
    (["a", "b"], ["b", "a"]),
    ([], []),
])
def test_reverse_string(s, expected):
    reverse_string(s)
    assert s == expected
