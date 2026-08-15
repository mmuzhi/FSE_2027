from typing import List, Optional
from collections import deque

class Solution:
    def levelOrderBottom(self, root: Optional[TreeNode]) -> List[List[int]]:
        def checkReverse(ans):
            l, r = 0, len(ans) - 1
            while l < r:
                ans[l], ans[r] = ans[r], ans[l]
                l += 1
                r -= 1
            return ans

        if not root:
            return []

        q = deque([root])
        ans = []

        while q:
            level = []
            for _ in range(len(q)):
                node = q.popleft()
                level.append(node.val)
                if node.left:
                    q.append(node.left)
                if node.right:
                    q.append(node.right)
            ans.append(level)

        return checkReverse(ans)