# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def maxProduct(self, root: Optional[TreeNode]) -> int:
        sm = self.tsum(root)
        mx = [0]
        self.fun(root, sm, mx)
        return mx[0] % (10**9 + 7)
    
    def tsum(self, root):
        if root is None:
            return 0
        return root.val + self.tsum(root.left) + self.tsum(root.right)
    
    def fun(self, root, sm, mx):
        if root is None:
            return 0
        a = self.fun(root.left, sm, mx)
        b = self.fun(root.right, sm, mx)
        current_sum = a + b + root.val
        product_left = a * (sm - a)
        product_right = b * (sm - b)
        if product_left > mx[0]:
            mx[0] = product_left
        if product_right > mx[0]:
            mx[0] = product_right
        return current_sum