class Solution:
    def maxProduct(self, root: Optional[TreeNode]) -> int:
        mx=[0]
        sm=tsum(root)
        fun(root,sm,mx)
        return mx[0]%(10**9+7)