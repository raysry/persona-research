import pytest
from solution import trap


@pytest.mark.parametrize("height, expected", [
    ([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1], 6),
    ([4, 2, 0, 3, 2, 5], 9),
    ([], 0),
    ([1], 0),
    ([1, 2, 3, 4, 5], 0),
    ([5, 4, 3, 2, 1], 0),
    ([3, 0, 0, 2, 0, 4], 10),
])
def test_trap(height, expected):
    assert trap(height) == expected
