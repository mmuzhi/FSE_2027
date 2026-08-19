import random
from typing import List


class Solution:
    def medianSlidingWindow(self, nums: List[int], k: int) -> List[float]:
        class Node:
            __slots__ = ('val', 'pri', 'left', 'right', 'sz')

            def __init__(self, val: int):
                self.val = val
                self.pri = random.random()
                self.left = None
                self.right = None
                self.sz = 1

        def size(t):
            return t.sz if t is not None else 0

        def update(t):
            t.sz = 1 + size(t.left) + size(t.right)
            return t

        def split(t, key):
            # -> (< key, >= key)
            if t is None:
                return None, None
            if t.val < key:
                t.right, r = split(t.right, key)
                return update(t), r
            else:
                l, t.left = split(t.left, key)
                return l, update(t)

        def split_le(t, key):
            # -> (<= key, > key)
            if t is None:
                return None, None
            if t.val <= key:
                t.right, r = split_le(t.right, key)
                return update(t), r
            else:
                l, t.left = split_le(t.left, key)
                return l, update(t)

        def merge(a, b):
            if a is None:
                return b
            if b is None:
                return a
            if a.pri > b.pri:
                a.right = merge(a.right, b)
                return update(a)
            else:
                b.left = merge(a, b.left)
                return update(b)

        def insert(t, key):
            l, r = split_le(t, key)
            return merge(merge(l, Node(key)), r)

        def remove(t, key):
            l, rest = split(t, key)       # l: < key
            eq, r = split_le(rest, key)   # eq: == key, r: > key
            if eq is not None:            # drop exactly one occurrence of key
                eq = merge(eq.left, eq.right)
            return merge(merge(l, eq), r)

        def get(t, r):
            # r-th smallest element, 1-indexed
            while True:
                ls = size(t.left)
                if r <= ls:
                    t = t.left
                elif r == ls + 1:
                    return t.val
                else:
                    r -= ls + 1
                    t = t.right

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