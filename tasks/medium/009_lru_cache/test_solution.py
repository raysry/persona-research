from solution import LRUCache


def test_basic_operations():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    assert cache.get(1) == 1
    cache.put(3, 3)  # 淘汰 key 2
    assert cache.get(2) == -1
    cache.put(4, 4)  # 淘汰 key 1
    assert cache.get(1) == -1
    assert cache.get(3) == 3
    assert cache.get(4) == 4


def test_update_existing():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    cache.put(1, 10)  # 更新 key 1
    assert cache.get(1) == 10
    cache.put(3, 3)  # 淘汰 key 2（key 1 刚被访问）
    assert cache.get(2) == -1


def test_get_refreshes():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    cache.get(1)  # 刷新 key 1
    cache.put(3, 3)  # 淘汰 key 2
    assert cache.get(2) == -1
    assert cache.get(1) == 1


def test_capacity_one():
    cache = LRUCache(1)
    cache.put(1, 1)
    cache.put(2, 2)
    assert cache.get(1) == -1
    assert cache.get(2) == 2


def test_miss():
    cache = LRUCache(2)
    assert cache.get(99) == -1
