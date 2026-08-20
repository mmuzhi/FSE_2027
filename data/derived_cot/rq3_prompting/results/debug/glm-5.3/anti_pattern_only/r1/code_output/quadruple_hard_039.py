import random
from typing import List


class _Node:
    __slots__ = ("val", "cnt", "sz", "prio", "left", "right")

    def __init__(self, val):
        self.val = val
        self.cnt = 1
        self.sz = 1
        self.prio = random.random()
        self.left = None
        self.right = None


def size(t):
    return t.sz if t is not None else 0


def _update(t):
    t.sz = t.cnt + size(t.left) + size(t.right)


def _rotate_right(t):
    l = t.left
    t.left = l.right
    l.right = t
    _update(t)
    _update(l)
    return l


def _rotate_left(t):
    r = t.right
    t.right = r.left
    r.left = t
    _update(t)
    _update(r)
    return r


def insert(t, val):
    if t is None:
        return _Node(val)
    if val == t.val:
        t.cnt += 1
    elif val < t.val:
        t.left = insert(t.left, val)
        if t.left.prio > t.prio:
            t = _rotate_right(t)
    else:
        t.right = insert(t.right, val)
        if t.right.prio > t.prio:
            t = _rotate_left(t)
    _update(t)
    return t


def remove(t, val):
    if t is None:
        return None
    if val < t.val:
        t.left = remove(t.left, val)
    elif val > t.val:
        t.right = remove(t.right, val)
    else:
        if t.cnt > 1:
            t.cnt -= 1
        elif t.left is None or t.right is None:
            return t.left if t.left is not None else t.right
        elif t.left.prio > t.right.prio:
            t = _rotate_right(t)
            t.right = remove(t.right, val)
        else:
            t = _rotate_left(t)
            t.left = remove(t.left, val)
    _update(t)
    return t


def get(t, k):
    # k-th smallest element, 1-indexed
    while t is not None:
        left_sz = size(t.left)
        if k <= left_sz:
            t = t.left
        elif k <= left_sz + t.cnt:
            return t.val
        else:
            k -= left_sz + t.cnt
            t = t.right
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
                    ans.append(get(tree, k // 2 + 1))
                else:
                    ans.append((get(tree, k // 2) + get(tree, k // 2 + 1)) / 2)
        return ans