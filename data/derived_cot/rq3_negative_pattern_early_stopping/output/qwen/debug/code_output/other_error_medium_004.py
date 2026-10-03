# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
from collections import deque

class Solution:
    def kthLargestLevelSum(self, root: Optional[TreeNode], k: int) -> int:
        dq = deque([root])
        level_sums = []
        while dq:
            current_sum = 0
            for _ in range(len(dq)):
                node = dq.popleft()
                current_sum += node.val
                if node.left:
                    dq.append(node.left)
                if node.right:
                    dq.append(node.right)
            level_sums.append(current_sum)
        level_sums.sort(reverse=True)
        return level_sums[k-1] if len(level_sums) >= k else -1