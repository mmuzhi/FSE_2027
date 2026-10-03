import random

class Node:
    __slots__ = ['val', 'count', 'priority', 'size', 'left', 'right']
    def __init__(self, val):
        self.val = val
        self.count = 1
        self.priority = random.random()
        self.size = 1
        self.left = None
        self.right = None

def touch(root):
    if not root:
        return
    root.size = root.count + size(root.left) + size(root.right)

def size(root):
    if not root:
        return 0
    return root.size

def left_rotate(node):
    right = node.right
    node.right = right.left
    right.left = node
    touch(node)
    touch(right)
    return right

def right_rotate(node):
    left = node.left
    node.left = left.right
    left.right = node
    touch(node)
    touch(left)
    return left

def merge(left, right):
    if not left:
        return right
    if not right:
        return left
    if left.priority < right.priority:
        left.right = merge(left.right, right)
        touch(left)
        return left
    else:
        right.left = merge(left, right.left)
        touch(right)
        return right

def insert(node, val):
    if not node:
        return Node(val)
    if val == node.val:
        node.count += 1
        touch(node)
        return node
    if val < node.val:
        node.left = insert(node.left, val)
    else:
        node.right = insert(node.right, val)
    if node.left and node.left.priority < node.priority:
        node = right_rotate(node)
    if node.right and node.right.priority < node.priority:
        node = left_rotate(node)
    return node

def remove(node, val):
    if not node:
        return None
    if val == node.val:
        node.count -= 1
        if node.count == 0:
            return merge(node.left, node.right)
        touch(node)
        return node
    if val < node.val:
        node.left = remove(node.left, val)
    else:
        node.right = remove(node.right, val)
    touch(node)
    if node.left and node.left.priority < node.priority:
        node = right_rotate(node)
    if node.right and node.right.priority < node.priority:
        node = left_rotate(node)
    return node

def get_order(node, k):
    if not node:
        return None
    left_size = size(node.left)
    if k <= left_size:
        return get_order(node.left, k)
    elif k <= left_size + node.count:
        return node.val
    else:
        return get_order(node.right, k - left_size - node.count)

class Solution:
    def medianSlidingWindow(self, nums: List[int], k: int) -> List[float]:
        root = None
        ans = []
        for i, x in enumerate(nums):
            root = insert(root, x)
            if i >= k:
                root = remove(root, nums[i - k])
            if i >= k - 1:
                if k % 2 == 1:
                    median = get_order(root, k // 2 + 1)
                    ans.append(median)
                else:
                    mid1 = get_order(root, k // 2)
                    mid2 = get_order(root, k // 2 + 1)
                    ans.append((mid1 + mid2) / 2.0)
        return ans