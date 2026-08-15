from typing import Optional
import sys

sys.setrecursionlimit(10**6)

def tsum(root):
    if root is None:
        return 0
    return root.val + tsum(root.left) + tsum(root.right)

def fun(root, sm, mx):
    if root is None:
        return 0
    a = fun(root.left, sm, mx)
    b = fun(root.right, sm, mx)

    if root.left:
        mx[0] = max(mx[0], a * (sm - a))
    if root.right:
        mx[0] = max(mx[0], b * (sm - b))

    return a + b + root.val

class Solution:
    def maxProduct(self, root: Optional[TreeNode]) -> int:
        mx = [-10**30]
        sm = tsum(root)
        fun(root, sm, mx)
        return mx[0] % (10**9 + 7)