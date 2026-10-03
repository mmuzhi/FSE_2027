from typing import Optional, List
from collections import deque

class Solution:
    def findMode(self, root: Optional[TreeNode]) -> List[int]:
        if not root:
            return []

        freq = {}

        def bfs(freq):
            queue = deque([root])
            while queue:
                curr = queue.popleft()
                if curr.left:
                    queue.append(curr.left)
                if curr.right:
                    queue.append(curr.right)
                freq.setdefault(curr.val, 0)
                freq[curr.val] += 1

        bfs(freq)
        items = list(freq.items())
        max_cnt = 0
        for num, cnt in items:
            if cnt > max_cnt:
                max_cnt = cnt
        ans = []
        for num, cnt in items:
            if cnt == max_cnt:
                ans.append(num)
        return ans