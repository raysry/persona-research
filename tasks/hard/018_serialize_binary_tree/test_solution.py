import pytest
from solution import serialize, deserialize


TREES = [
    {"val": 1, "left": {"val": 2, "left": None, "right": None},
     "right": {"val": 3, "left": {"val": 4, "left": None, "right": None},
               "right": {"val": 5, "left": None, "right": None}}},
    None,
    {"val": 1, "left": None, "right": None},
    {"val": 1, "left": {"val": 2, "left": {"val": 3, "left": None, "right": None},
                         "right": None}, "right": None},
    {"val": -1, "left": {"val": 0, "left": None, "right": None},
     "right": {"val": 100, "left": None, "right": None}},
]


@pytest.mark.parametrize("tree", TREES)
def test_roundtrip(tree):
    assert deserialize(serialize(tree)) == tree


def test_serialize_returns_string():
    tree = {"val": 1, "left": None, "right": None}
    assert isinstance(serialize(tree), str)


def test_none_roundtrip():
    assert deserialize(serialize(None)) is None
