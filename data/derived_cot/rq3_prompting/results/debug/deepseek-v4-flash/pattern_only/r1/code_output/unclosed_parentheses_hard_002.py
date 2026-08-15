from typing import List
import random

class Node:
    __slots__ = ['val', 'count', 'weight', 'size', 'left', 'right']
    def __init__(self, val):
        self.val = val
        self.count = 1
        self.weight = random.random()
        self.size = 1
        self.left = self.right = None

def size(root):
    if root is None:
        return 0
    return root.size

def touch(root):
    if root is not None:
        root.size = root.count + size(root.left) + size(root.right)

def rotate_right(p):
    q = p.left
    p.left = q.right
    q.right = p
    touch(p)
    touch(q)
    return q

def rotate_left(p):
    q = p.right
    p.right = q.left
    q.left = p
    touch(p)
    touch(q)
    return q

def insert(root, val):
    if root is None:
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
    if root is None:
        return None
    if val < root.val:
        root.left = remove(root.left, val)
    elif val > root.val:
        root.right = remove(root.right, val)
    else:
        if root.count > 1:
            root.count -= 1
        elif root.left is None:
            return root.right
        elif root.right is None:
            return root.left
        else:
            if root.left.weight < root.right.weight:
                root = rotate_right(root)
                root.right = remove(root.right, val)
            else:
                root = rotate_left(root)
                root.left = remove(root.left, val)
    touch(root)
    return root

def get(root, k):
    left_size = size(root.left)
    if k <= left_size:
        return get(root.left, k)
    if k <= left_size + root.count:
        return root.val
    return get(root.right, k - left_size - root.count)

class Solution:
    def medianSlidingWindow(self, nums: List[int], k: int) -> List[float]:
        tree = None
        ans = []
        for i, x in enumerate(nums):
            tree = insert(tree, x)
            if size(tree) > k:
                tree = remove(tree, nums[i - k])
            if size(tree) == k:
                if k % 2:
                    ans.append(float(get(tree, k // 2 + 1)))
                else:
                    ans.append((get(tree, k // 2) + get(tree, k // 2 + 1)) / 2.0)
        return ans