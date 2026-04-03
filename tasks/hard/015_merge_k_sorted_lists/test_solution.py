import pytest
from solution import merge_k_lists


@pytest.mark.parametrize("lists, expected", [
    ([[1, 4, 5], [1, 3, 4], [2, 6]], [1, 1, 2, 3, 4, 4, 5, 6]),
    ([], []),
    ([[]], []),
    ([[1]], [1]),
    ([[1, 2], [3, 4], [5, 6], [0, 7]], [0, 1, 2, 3, 4, 5, 6, 7]),
    ([[], [1], []], [1]),
])
def test_merge_k_lists(lists, expected):
    assert merge_k_lists(lists) == expected
