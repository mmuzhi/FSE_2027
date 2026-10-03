from typing import List
import random

class Node:
    __slots__ = ['val', 'count', 'weight', 'size', 'left', 'right']
    def __init__(self, val: int):
        self.val = val
        self.count = 1
        self.weight = random.random()
        self.size = 1
        self.left = None
        self.right = None

def size(root: Node) -> int:
    return root.size if root else 0

def touch(root: Node) -> None:
    if root:
        root.size = root.count + size(root.left) + size(root.right)

def split(root: Node, key: int):
    """Split by value: left tree contains nodes with val < key, right tree with val >= key"""
    if not root:
        return (None, None)
    if root.val < key:
        left, right = split(root.right, key)
        root.right = left
        touch(root)
        return (root, right)
    else:
        left, right = split(root.left, key)
        root.left = right
        touch(root)
        return (left, root)

def merge(left: Node, right: Node) -> Node:
    if not left or not right:
        return left or right
    if left.weight > right.weight:
        left.right = merge(left.right, right)
        touch(left)
        return left
    else:
        right.left = merge(left, right.left)
        touch(right)
        return right

def insert(root: Node, val: int) -> Node:
    """Insert val into treap, handling duplicates by incrementing count"""
    if not root:
        return Node(val)
    if val == root.val:
        root.count += 1
        root.size += 1
        return root
    left, right = split(root, val)
    new_node = Node(val)
    return merge(merge(left, new_node), right)

def remove(root: Node, val: int) -> Node:
    """Remove one occurrence of val. If count > 1, decrement; else remove node."""
    if not root:
        return None
    if val == root.val:
        if root.count > 1:
            root.count -= 1
            root.size -= 1
            return root
        else:
            return merge(root.left, root.right)
    elif val < root.val:
        root.left = remove(root.left, val)
        touch(root)
        return root
    else:
        root.right = remove(root.right, val)
        touch(root)
        return root

def get(root: Node, k: int) -> float:
    """Return the k-th smallest element (1-indexed)."""
    left_size = size(root.left)
    if k <= left_size:
        return get(root.left, k)
    elif k <= left_size + root.count:
        return root.val
    else:
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
                if k % 2 == 1:
                    ans.append(float(get(tree, k // 2 + 1)))
                else:
                    left = get(tree, k // 2)
                    right = get(tree, k // 2 + 1)
                    ans.append((left + right) / 2.0)
        return ans