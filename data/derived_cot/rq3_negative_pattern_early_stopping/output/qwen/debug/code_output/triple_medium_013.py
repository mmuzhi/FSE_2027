# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def maxAncestorDiff(self, root: Optional[TreeNode]) -> int:
        ans = [0]
        if root is None:
            return 0
        self.fun(root, root.val, root.val, ans)
        return ans[0]
    
    def fun(self, root, mx, mn, ans):
        if root is None:
            return
        d1 = abs(root.val - mx)
        d2 = abs(root.val - mn)
        current_max = max(d1, d2)
        if current_max > ans[0]:
            ans[0] = current_max
        new_mx = max(mx, root.val)
        new_mn = min(mn, root.val)
        self.fun(root.left, new_mx, new_mn, ans)
        self.fun(root.right, new_mx, new_mn, ans)