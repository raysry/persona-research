import pytest
from solution import group_anagrams


def normalize(groups):
    """归一化分组结果以便比较"""
    return sorted([sorted(g) for g in groups])


@pytest.mark.parametrize("strs, expected", [
    (["eat", "tea", "tan", "ate", "nat", "bat"],
     [["ate", "eat", "tea"], ["bat"], ["nat", "tan"]]),
    ([""], [[""]]),
    (["a"], [["a"]]),
    (["abc", "bca", "cab", "xyz", "zyx"],
     [["abc", "bca", "cab"], ["xyz", "zyx"]]),
    ([], []),
])
def test_group_anagrams(strs, expected):
    result = group_anagrams(strs)
    assert normalize(result) == normalize(expected)
