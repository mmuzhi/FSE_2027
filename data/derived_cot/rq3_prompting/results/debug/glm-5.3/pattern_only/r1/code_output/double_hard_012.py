import random
from typing import List


def size(node):
    return node[2] if node else 0


def update(node):
    node[2] = 1 + size(node[3]) + size(node[4])
    return node


def split_le(node, key):
    # left: keys <= key, right: keys > key
    if not node:
        return None, None
    if node[0] <= key:
        left, right = split_le(node[4], key)
        node[4] = left
        return update(node), right
    left, right = split_le(node[3], key)
    node[3] = right
    return left, update(node)


def split_lt(node, key):
    # left: keys < key, right: keys >= key
    if not node:
        return None, None
    if node[0] < key:
        left, right = split_lt(node[4], key)
        node[4] = left
        return update(node), right
    left, right = split_lt(node[3], key)
    node[3] = right
    return left, update(node)


def merge(a, b):
    if not a or not b:
        return a or b
    if a[1] > b[1]:
        a[4] = merge(a[4], b)
        return update(a)
    b[3] = merge(a, b[3])
    return update(b)


def insert(node, key):
    left, right = split_le(node, key)
    return merge(merge(left, [key, random.random(), 1, None, None]), right)


def remove(node, key):
    left, rest = split_le(node, key)      # left: <= key, rest: > key
    lt, eq = split_lt(left, key)          # lt: < key, eq: rooted at key
    eq = merge(eq[3], eq[4])              # drop one occurrence of key
    return merge(merge(lt, eq), rest)


def get(node, rank):
    # rank-th smallest (1-indexed)
    while True:
        ls = size(node[3])
        if rank <= ls:
            node = node[3]
        elif rank == ls + 1:
            return node[0]
        else:
            rank -= ls + 1
            node = node[4]


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