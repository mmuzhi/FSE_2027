import random
from typing import List


class Node:
    __slots__ = ['val', 'count', 'weight', 'size', 'left', 'right']

    def __init__(self, val):
        self.val = val
        self.count = 1
        self.weight = random.random()
        self.size = 1
        self.left = self.right = None


def touch(root):
    if not root:
        return
    root.size = root.count + size(root.left) + size(root.right)


def size(root):
    if not root:
        return 0
    return root.size


def rotate_right(root):
    pivot = root.left
    root.left = pivot.right
    pivot.right = root
    touch(root)
    touch(pivot)
    return pivot


def rotate_left(root):
    pivot = root.right
    root.right = pivot.left
    pivot.left = root
    touch(root)
    touch(pivot)
    return pivot


def insert(root, val):
    if not root:
        return Node(val)
    if val == root.val:
        root.count += 1
    elif val < root.val:
        root.left = insert(root.left, val)
        if root.left.weight < root.weight:
            root = rotate_right(root)
    else:
        root.right = insert(root.right, val)
        if root.right.weight < root.weight:
            root = rotate_left(root)
    touch(root)
    return root


def remove(root, val):
    if not root:
        return None
    if val == root.val:
        if root.count > 1:
            root.count -= 1
            touch(root)
            return root
        if not root.left:
            return root.right
        if not root.right:
            return root.left
        if root.left.weight < root.right.weight:
            root = rotate_right(root)
            root.right = remove(root.right, val)
        else:
            root = rotate_left(root)
            root.left = remove(root.left, val)
        touch(root)
        return root
    elif val < root.val:
        root.left = remove(root.left, val)
    else:
        root.right = remove(root.right, val)
    touch(root)
    return root


def get(root, rank):
    left_size = size(root.left)
    if rank <= left_size:
        return get(root.left, rank)
    elif rank <= left_size + root.count:
        return root.val
    else:
        return get(root.right, rank - left_size - root.count)


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