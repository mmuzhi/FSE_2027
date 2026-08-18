# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def findBottomLeftValue(self, root: Optional[TreeNode]) -> int:
        stack = collections.deque([root])
        lvl = []
        while stack:
            lvl = []
            for i in range(len(stack)):
                n = stack.popleft()
                lvl.append(n.val)
                if n.left: stack.append(n.left)
                if n.right: stack.append(n.right)
        return lvl[0]