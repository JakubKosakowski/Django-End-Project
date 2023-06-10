import pytest
from shop_app.views import array_merge, filter_products


def test_array_merge():
    """Test składania dwóch identycznych struktur danych"""
    assert array_merge([1, 1], [2, 2]) == [1, 1, 2, 2]
    assert array_merge({"1": 1}, {"2": 2}) == {"1": 1, "2": 2}
    assert array_merge({1, 2, 3}, {4, 5}) == {1, 2, 3, 4, 5}

