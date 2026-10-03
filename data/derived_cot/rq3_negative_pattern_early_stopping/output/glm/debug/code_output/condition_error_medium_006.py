import collections

class Solution:
    def findBottomLeftValue(self, root: Optional[TreeNode]) -> int:
        stack = collections.deque([root])
        ans = 0
        while stack:
            lvl = []
            for i in range(len(stack)):
                n = stack.popleft()
                lvl.append(n.val)
                if n.left: stack.append(n.left)
                if n.right: stack.append(n.right)
            ans = lvl[0]
        return ans