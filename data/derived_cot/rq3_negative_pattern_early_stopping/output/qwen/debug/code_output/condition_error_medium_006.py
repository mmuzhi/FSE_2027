from collections import deque
from typing import Optional

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def findBottomLeftValue(self, root: Optional[TreeNode]) -> int:
        if not root:
            return None
        queue = deque()
        queue.append((root, 0))
        max_depth = -1
        result = None
        
        while queue:
            node, depth = queue.popleft()
            if depth > max_depth:
                max_depth = depth
                result = node.val
            if node.left:
                queue.append((node.left, depth + 1))
            if node.right:
                queue.append((node.right, depth + 1))
                
        return result