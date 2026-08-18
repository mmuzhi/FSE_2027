from typing import List
import random


class _Node:
    __slots__ = ("val", "priority", "size", "left", "right")

    def __init__(self, val: int):
        self.val = val
        self.priority = random.random()
        self.size = 1
        self.left = None
        self.right = None


def size(tree):
    return tree.size if tree else 0


def _update(tree):
    if tree:
        tree.size = 1 + size(tree.left) + size(tree.right)
    return tree


def _split_less(tree, key):
    # left part: values < key, right part: values >= key
    if tree is None:
        return None, None
    if tree.val < key:
        tree.right, right = _split_less(tree.right, key)
        return _update(tree), right
    left, tree.left = _split_less(tree.left, key)
    return left, _update(tree)


def _split_leq(tree, key):
    # left part: values <= key, right part: values > key
    if tree is None:
        return None, None
    if tree.val <= key:
        tree.right, right = _split_leq(tree.right, key)
        return _update(tree), right
    left, tree.left = _split_leq(tree.left, key)
    return left, _update(tree)


def _merge(a, b):
    if a is None:
        return b
    if b is None:
        return a
    if a.priority > b.priority:
        a.right = _merge(a.right, b)
        return _update(a)
    b.left = _merge(a.left, b)
    return _update(b)


def insert(tree, key):
    left, right = _split_less(tree, key)
    return _merge(_merge(left, _Node(key)), right)


def remove(tree, key):
    left, mid = _split_less(tree, key)
    mid, right = _split_leq(mid, key)  # mid now holds only nodes equal to key
    if mid is not None:
        mid = _merge(mid.left, mid.right)  # drop exactly one occurrence of key
    return _merge(_merge(left, mid), right)


def get(tree, rank):
    # rank is 1-indexed; returns the rank-th smallest value
    node = tree
    while node:
        left_size = size(node.left)
        if rank <= left_size:
            node = node.left
        elif rank == left_size + 1:
            return node.val
        else:
            rank -= left_size + 1
            node = node.right
    return None


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