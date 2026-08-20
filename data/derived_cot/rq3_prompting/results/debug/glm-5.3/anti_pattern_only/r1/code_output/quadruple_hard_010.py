import random
from typing import List


class Node:
    __slots__ = ("val", "prio", "left", "right", "size")

    def __init__(self, val):
        self.val = val
        self.prio = random.random()
        self.left = None
        self.right = None
        self.size = 1


def size(t):
    return t.size if t else 0


def upd(t):
    t.size = size(t.left) + size(t.right) + 1
    return t


def merge(a, b):
    if a is None:
        return b
    if b is None:
        return a
    if a.prio > b.prio:
        a.right = merge(a.right, b)
        return upd(a)
    b.left = merge(a, b.left)
    return upd(b)


def split(t, val):
    # left tree: keys < val, right tree: keys >= val
    if t is None:
        return None, None
    if t.val < val:
        t.right, right = split(t.right, val)
        return upd(t), right
    left, t.left = split(t.left, val)
    return left, upd(t)


def insert(t, val):
    left, right = split(t, val)
    return merge(merge(left, Node(val)), right)


def remove(t, val):
    if t.val == val:
        return merge(t.left, t.right)
    if val < t.val:
        t.left = remove(t.left, val)
    else:
        t.right = remove(t.right, val)
    return upd(t)


def get(t, rank):
    # rank-th smallest key (1-indexed)
    while t is not None:
        ls = size(t.left)
        if rank <= ls:
            t = t.left
        elif rank == ls + 1:
            return t.val
        else:
            rank -= ls + 1
            t = t.right


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