import pytest
from solution import sort_colors


@pytest.mark.parametrize("nums, expected", [
    ([2, 0, 2, 1, 1, 0], [0, 0, 1, 1, 2, 2]),
    ([2, 0, 1], [0, 1, 2]),
    ([0], [0]),
    ([1], [1]),
    ([0, 0, 0], [0, 0, 0]),
    ([2, 2, 1, 1, 0, 0], [0, 0, 1, 1, 2, 2]),
])
def test_sort_colors(nums, expected):
    sort_colors(nums)
    assert nums == expected
