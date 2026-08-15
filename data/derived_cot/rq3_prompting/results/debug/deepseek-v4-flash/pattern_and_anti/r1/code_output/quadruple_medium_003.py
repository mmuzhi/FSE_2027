from typing import Optional, List

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def levelOrderBottom(self, root: Optional[TreeNode]) -> List[List[int]]:
        def checkReverse(ans):
            left, right = 0, len(ans) - 1
            while left < right:
                ans[left], ans[right] = ans[right], ans[left]
                left += 1
                right -= 1
            return ans

        if not root:
            return []

        q, ans = [root], []
        while q:
            n = len(q)
            level = []
            for _ in range(n):
                node = q.pop(0)
                level.append(node.val)
                if node.left is not None:
                    q.append(node.left)
                if node.right is not None:
                    q.append(node.right)
            ans.append(level)

        return checkReverse(ans)