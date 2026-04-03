import pytest
from solution import level_order


@pytest.mark.parametrize("tree, expected", [
    ([3, 9, 20, None, None, 15, 7], [[3], [9, 20], [15, 7]]),
    ([1], [[1]]),
    ([], []),
    ([1, 2, 3, 4, 5], [[1], [2, 3], [4, 5]]),
    ([1, None, 2, None, 3], [[1], [2], [3]]),
])
def test_level_order(tree, expected):
    assert level_order(tree) == expected
