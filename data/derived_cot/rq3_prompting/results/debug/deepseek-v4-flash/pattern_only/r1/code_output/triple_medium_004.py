from typing import Optional
import collections

class Solution:
    def kthLargestLevelSum(self, root: Optional[TreeNode], k: int) -> int:
        if not root or k <= 0:
            return -1

        q = collections.deque([root])
        sums = []

        while q:
            level_sum = 0
            for _ in range(len(q)):
                node = q.popleft()
                level_sum += node.val
                if node.left:
                    q.append(node.left)
                if node.right:
                    q.append(node.right)
            sums.append(level_sum)

        sums.sort(reverse=True)
        return sums[k - 1] if len(sums) >= k else -1