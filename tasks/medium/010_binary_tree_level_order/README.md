## 任务

请实现 `solution.py` 中的 `level_order` 函数。

给定一棵二叉树（用嵌套列表表示），返回其节点值的层序遍历结果（逐层从左到右）。

二叉树的输入格式为层序列表，其中 `None` 表示空节点。例如 `[3, 9, 20, None, None, 15, 7]` 表示：
```
    3
   / \
  9  20
    /  \
   15   7
```

## 要求

- 输入为层序列表表示的二叉树
- 返回 `list[list[int]]`，每个子列表是一层的节点值

## 约束

- 不要修改 `test_solution.py`
- 只修改 `solution.py`

来源：LeetCode #102 Binary Tree Level Order Traversal (Medium)
