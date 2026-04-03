import pytest
from solution import coin_change


@pytest.mark.parametrize("coins, amount, expected", [
    ([1, 5, 10, 25], 30, 2),
    ([2], 3, -1),
    ([1], 0, 0),
    ([1, 2, 5], 11, 3),
    ([186, 419, 83, 408], 6249, 20),
    ([1], 1, 1),
    ([2, 5, 10, 1], 27, 4),
])
def test_coin_change(coins, amount, expected):
    assert coin_change(coins, amount) == expected
