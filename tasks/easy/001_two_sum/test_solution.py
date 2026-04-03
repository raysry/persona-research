import pytest
from solution import two_sum


@pytest.mark.parametrize("nums, target, expected", [
    ([2, 7, 11, 15], 9, [0, 1]),
    ([3, 2, 4], 6, [1, 2]),
    ([3, 3], 6, [0, 1]),
    ([1, 5, 3, 7, 8, 2], 10, [2, 3]),
    ([-1, -2, -3, -4, -5], -8, [2, 4]),
])
def test_two_sum(nums, target, expected):
    result = sorted(two_sum(nums, target))
    assert result == sorted(expected)
