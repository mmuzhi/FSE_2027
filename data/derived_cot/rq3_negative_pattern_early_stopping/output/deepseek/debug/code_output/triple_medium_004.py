from collections import deque
from typing import Optional

class Solution:
    def kthLargestLevelSum(self, root: Optional[TreeNode], k: int) -> int:
        if not root:
            return -1
        dq = deque([root])
        a = []
        while dq:
            lvlsum = 0
            for _ in range(len(dq)):
                n = dq.popleft()
                lvlsum += n.val
                if n.left:
                    dq.append(n.left)
                if n.right:
                    dq.append(n.right)
            a.append(lvlsum)
        a.sort(reverse=True)
        if k > len(a):
            return -1
        return a[k-1]