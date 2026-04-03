## 任务

请实现 `solution.py` 中的 `LRUCache` 类。

设计一个满足 LRU（最近最少使用）缓存约束的数据结构：

- `LRUCache(capacity: int)` — 以正整数 capacity 初始化缓存
- `get(key: int) -> int` — 如果 key 存在则返回 value，否则返回 -1
- `put(key: int, value: int) -> None` — 如果 key 已存在则更新 value，否则插入。当缓存满时淘汰最近最少使用的项

## 要求

- `get` 和 `put` 必须以 O(1) 平均时间复杂度运行

## 约束

- 不要修改 `test_solution.py`
- 只修改 `solution.py`

来源：LeetCode #146 LRU Cache (Medium)
