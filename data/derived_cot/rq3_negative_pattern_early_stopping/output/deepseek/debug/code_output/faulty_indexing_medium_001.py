from typing import Optional, List

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
        q, ans = [root], []
        while q:
            n, level = len(q), []
            for _ in range(n):
                curr = q.pop(0)
                level.append(curr.val)
                if curr.left:
                    q.append(curr.left)
                if curr.right:
                    q.append(curr.right)
            ans.append(level)
        return checkReverse(ans)