## 任务

请实现 `solution.py` 中的 `serialize` 和 `deserialize` 函数。

设计一个算法将二叉树序列化为字符串，并能从字符串反序列化回二叉树。

二叉树用嵌套字典表示：`{"val": 1, "left": {...}, "right": {...}}`，空节点为 `None`。

## 要求

- `serialize(root)` 将树转为字符串
- `deserialize(data)` 将字符串还原为树
- `deserialize(serialize(root))` 必须等于原始树
- 序列化格式自定义，只要能正确还原即可

## 约束

- 不要修改 `test_solution.py`
- 只修改 `solution.py`

来源：LeetCode #297 Serialize and Deserialize Binary Tree (Hard)
