from typing import List
import random


class _Node:
    __slots__ = ("val", "cnt", "size", "priority", "left", "right")

    def __init__(self, val: int):
        self.val = val
        self.cnt = 1
        self.size = 1
        self.priority = random.random()
        self.left = None
        self.right = None


def size(node):
    return node.size if node else 0


def _push_up(node):
    node.size = size(node.left) + size(node.right) + node.cnt


def _rotate_right(node):
    left = node.left
    node.left = left.right
    left.right = node
    _push_up(node)
    _push_up(left)
    return left


def _rotate_left(node):
    right = node.right
    node.right = right.left
    right.left = node
    _push_up(node)
    _push_up(right)
    return right


def insert(node, val):
    if node is None:
        return _Node(val)
    if val == node.val:
        node.cnt += 1
    elif val < node.val:
        node.left = insert(node.left, val)
        if node.left.priority > node.priority:
            node = _rotate_right(node)
    else:
        node.right = insert(node.right, val)
        if node.right.priority > node.priority:
            node = _rotate_left(node)
    _push_up(node)
    return node


def remove(node, val):
    if node is None:
        return None
    if val < node.val:
        node.left = remove(node.left, val)
    elif val > node.val:
        node.right = remove(node.right, val)
    else:
        if node.cnt > 1:
            node.cnt -= 1
            _push_up(node)
            return node
        if node.left is None:
            return node.right
        if node.right is None:
            return node.left
        if node.left.priority > node.right.priority:
            node = _rotate_right(node)
            node.right = remove(node.right, val)
        else:
            node = _rotate_left(node)
            node.left = remove(node.left, val)
    _push_up(node)
    return node


def get(node, rank):
    # 1-indexed rank select
    while node:
        left_size = size(node.left)
        if rank <= left_size:
            node = node.left
        elif rank <= left_size + node.cnt:
            return node.val
        rank -= left_size + node.cnt
        node = node.right
    raise ValueError("rank out of range")


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