class Solution:
    def levelOrderBottom(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root: 
            return []
        q, ans = [root], []
        while q:
            n, l = len(q), []
            for i in range(n):
                curr = q.pop(0)
                l.append(curr.val)
                if curr.left:
                    q.append(curr.left)
                if curr.right:
                    q.append(curr.right)
            ans.append(l)
        def checkReverse(ans):
            ans.reverse()
            return ans
        return checkReverse(ans)
