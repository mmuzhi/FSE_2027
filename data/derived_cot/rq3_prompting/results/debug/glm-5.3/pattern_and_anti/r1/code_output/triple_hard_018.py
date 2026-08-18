import random
from typing import List


class Node:
    __slots__ = ("val", "priority", "size", "count", "left", "right")

    def __init__(self, val):
        self.val = val
        self.priority = random.random()
        self.size = 1
        self.count = 1
        self.left = None
        self.right = None


def _update(node: "Node") -> None:
    node.size = node.count
    if node.left:
        node.size += node.left.size
    if node.right:
        node.size += node.right.size


def insert(node: "Node", val: int) -> "Node":
    if node is None:
        return Node(val)
    if val == node.val:
        node.count += 1
    elif val < node.val:
        node.left = insert(node.left, val)
        if node.left.priority > node.priority:
            tmp = node.left
            node.left = tmp.right
            tmp.right = node
            _update(node)
            _update(tmp)
            node = tmp
    else:
        node.right = insert(node.right, val)
        if node.right.priority > node.priority:
            tmp = node.right
            node.right = tmp.left
            tmp.left = node
            _update(node)
            _update(tmp)
            node = tmp
    _update(node)
    return node


def remove(node: "Node", val: int) -> "Node":
    if node is None:
        return None
    if val < node.val:
        node.left = remove(node.left, val)
    elif val > node.val:
        node.right = remove(node.right, val)
    else:
        if node.count > 1:
            node.count -= 1
        else:
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            if node.left.priority > node.right.priority:
                tmp = node.left
                node.left = tmp.right
                tmp.right = node
                _update(node)
                _update(tmp)
                node = tmp
                node.right = remove(node.right, val)
            else:
                tmp = node.right
                node.right = tmp.left
                tmp.left = node
                _update(node)
                _update(tmp)
                node = tmp
                node.left = remove(node.left, val)
    _update(node)
    return node


def size(node: "Node") -> int:
    return node.size if node else 0


def get(node: "Node", rank: int) -> int:
    left_size = node.left.size if node.left else 0
    if rank <= left_size:
        return get(node.left, rank)
    if rank <= left_size + node.count:
        return node.val
    return get(node.right, rank - left_size - node.count)


class Solution:
    def medianSlidingWindow(self, nums: List[int], k: int) -> List[float]:
        tree = None
        ans = []
        for i, x in enumerate(nums):
            tree = insert(tree, x)
            if size(tree) > k:
                tree = remove(tree, nums[i - k])
            if size(tree) == k:
                if k % 2 == 1:
                    ans.append(float(get(tree, k // 2 + 1)))
                else:
                    ans.append((get(tree, k // 2) + get(tree, k // 2 + 1)) / 2)
        return ans