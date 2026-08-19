import random
from typing import List


class Node:
    __slots__ = ('val', 'priority', 'left', 'right', 'count', 'sz')

    def __init__(self, val):
        self.val = val
        self.priority = random.random()
        self.left = None
        self.right = None
        self.count = 1
        self.sz = 1


def size(node):
    return node.sz if node else 0


def update(node):
    if node:
        node.sz = node.count + size(node.left) + size(node.right)


def rotate_right(node):
    root = node.left
    node.left = root.right
    root.right = node
    update(node)
    update(root)
    return root


def rotate_left(node):
    root = node.right
    node.right = root.left
    root.left = node
    update(node)
    update(root)
    return root


def insert(node, val):
    if node is None:
        return Node(val)
    if val == node.val:
        node.count += 1
    elif val < node.val:
        node.left = insert(node.left, val)
        if node.left.priority > node.priority:
            node = rotate_right(node)
    else:
        node.right = insert(node.right, val)
        if node.right.priority > node.priority:
            node = rotate_left(node)
    update(node)
    return node


def remove(node, val):
    if node is None:
        return None
    if val < node.val:
        node.left = remove(node.left, val)
    elif val > node.val:
        node.right = remove(node.right, val)
    else:
        if node.count > 1:
            node.count -= 1
        elif node.left is None:
            return node.right
        elif node.right is None:
            return node.left
        elif node.left.priority > node.right.priority:
            node = rotate_right(node)
            node.right = remove(node.right, val)
        else:
            node = rotate_left(node)
            node.left = remove(node.left, val)
    update(node)
    return node


def get(node, k):
    while node:
        left_size = size(node.left)
        if k <= left_size:
            node = node.left
        elif k <= left_size + node.count:
            return node.val
        else:
            k -= left_size + node.count
            node = node.right
    raise ValueError("k is out of range")


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