class Solution:
    def maxAncestorDiff(self, root: Optional[TreeNode]) -> int:
        ans = [0]
        if root is None:
            return 0
        fun(root, root.val, root.val, ans)
        return ans[0]