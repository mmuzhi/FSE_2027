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
            l, r = 0, len(ans) - 1
            while l < r:
                ans[l], ans[r] = ans[r], ans[l]
                l += 1
                r -= 1
            return ans

        if root is None:
            return []

        q, ans = [root], []
        while q:
            n = len(q)
            level = []
            for _ in range(n):
                curr = q.pop(0)
                level.append(curr.val)
                if curr.left is not None:
                    q.append(curr.left)
                if curr.right is not None:
                    q.append(curr.right)
            ans.append(level)

        return checkReverse(ans)