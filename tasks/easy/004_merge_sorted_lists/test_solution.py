import pytest
from solution import merge_two_lists


@pytest.mark.parametrize("list1, list2, expected", [
    ([1, 2, 4], [1, 3, 4], [1, 1, 2, 3, 4, 4]),
    ([], [], []),
    ([], [0], [0]),
    ([1], [2], [1, 2]),
    ([1, 3, 5, 7], [2, 4, 6, 8], [1, 2, 3, 4, 5, 6, 7, 8]),
])
def test_merge_two_lists(list1, list2, expected):
    assert merge_two_lists(list1, list2) == expected
