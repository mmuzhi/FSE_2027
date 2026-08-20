from typing import List
import random


class _Node:
    __slots__ = ("val", "pri", "sz", "left", "right")

    def __init__(self, val):
        self.val = val
        self.pri = random.random()
        self.sz = 1
        self.left = None
        self.right = None


def size(tree):
    return tree.sz if tree is not None else 0


def _update(tree):
    tree.sz = 1 + size(tree.left) + size(tree.right)
    return tree


def _merge(a, b):
    # All values in a are <= all values in b.
    if a is None:
        return b
    if b is None:
        return a
    if a.pri > b.pri:
        a.right = _merge(a.right, b)
        return _update(a)
    b.left = _merge(a, b.left)
    return _update(b)


def _split(tree, val):
    # Split into (values < val, values >= val).
    if tree is None:
        return None, None
    if tree.val < val:
        tree.right, hi = _split(tree.right, val)
        return _update(tree), hi
    lo, tree.left = _split(tree.left, val)
    return lo, _update(tree)


def insert(tree, val):
    lo, hi = _split(tree, val)
    return _merge(_merge(lo, _Node(val)), hi)


def remove(tree, val):
    # Remove a single occurrence of val.
    if tree is None:
        return None
    if val < tree.val:
        tree.left = remove(tree.left, val)
        return _update(tree)
    if val > tree.val:
        tree.right = remove(tree.right, val)
        return _update(tree)
    return _merge(tree.left, tree.right)


def get(tree, k):
    # k-th smallest value, 1-indexed.
    while tree is not None:
        ls = size(tree.left)
        if k <= ls:
            tree = tree.left
        elif k == ls + 1:
            return tree.val
        else:
            k -= ls + 1
            tree = tree.right
    raise IndexError("k is out of range")


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
                    ans.append(get(tree, k // 2 + 1))
                else:
                    ans.append((get(tree, k // 2) + get(tree, k // 2 + 1)) / 2)
        return ans