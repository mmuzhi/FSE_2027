import random
from typing import List


class Node:
    __slots__ = ("val", "count", "size", "priority", "left", "right")

    def __init__(self, val: int):
        self.val = val
        self.count = 1
        self.size = 1
        self.priority = random.random()
        self.left = None
        self.right = None


def size(node):
    return node.size if node else 0


def update(node):
    node.size = node.count + size(node.left) + size(node.right)


def rotate_left(root):
    pivot = root.right
    root.right = pivot.left
    pivot.left = root
    update(root)
    update(pivot)
    return pivot


def rotate_right(root):
    pivot = root.left
    root.left = pivot.right
    pivot.right = root
    update(root)
    update(pivot)
    return pivot


def insert(node, val):
    if node is None:
        return Node(val)
    if val == node.val:
        node.count += 1
    elif val < node.val:
        node.left = insert(node.left, val)
        if node.left.priority < node.priority:
            node = rotate_right(node)
    else:
        node.right = insert(node.right, val)
        if node.right.priority < node.priority:
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
        elif node.left is None and node.right is None:
            return None
        elif node.left is None or (node.right is not None and node.right.priority < node.left.priority):
            node = rotate_left(node)
            node.left = remove(node.left, val)
        else:
            node = rotate_right(node)
            node.right = remove(node.right, val)
    update(node)
    return node


def get(node, k):
    left_size = size(node.left)
    if k <= left_size:
        return get(node.left, k)
    if k <= left_size + node.count:
        return node.val
    return get(node.right, k - left_size - node.count)


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