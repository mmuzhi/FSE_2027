class Solution:
    def levelOrderBottom(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []

        q = [root]
        ans = []

        while q:
            level = []
            for _ in range(len(q)):
                curr = q.pop(0)
                level.append(curr.val)

                if curr.left:
                    q.append(curr.left)
                if curr.right:
                    q.append(curr.right)

            ans.append(level)

        ans.reverse()
        return ans