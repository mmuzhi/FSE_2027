from typing import List, Optional

class Solution:
    def findMode(self, root: Optional[TreeNode]) -> List[int]:
        if not root:
            return []

        def bfs(freq):
            queue = [root]
            while queue:
                curr = queue.pop()
                if curr.left is not None:
                    queue.append(curr.left)
                if curr.right is not None:
                    queue.append(curr.right)
                freq[curr.val] = freq.get(curr.val, 0) + 1

        freq = {}
        bfs(freq)

        items = list(freq.items())
        max_cnt = 0
        for _, cnt in items:
            if cnt > max_cnt:
                max_cnt = cnt

        return [num for num, cnt in items if cnt == max_cnt]