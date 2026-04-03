import pytest
from solution import is_valid_bst


@pytest.mark.parametrize("tree, expected", [
    ([2, 1, 3], True),
    ([5, 1, 4, None, None, 3, 6], False),
    ([1], True),
    ([], True),
    ([5, 3, 7, 2, 4, 6, 8], True),
    ([5, 3, 7, 2, 6, None, None], False),  # 左子树含6>5
    ([10, 5, 15, None, None, 6, 20], False),  # 右子树含6<10
])
def test_is_valid_bst(tree, expected):
    assert is_valid_bst(tree) == expected
