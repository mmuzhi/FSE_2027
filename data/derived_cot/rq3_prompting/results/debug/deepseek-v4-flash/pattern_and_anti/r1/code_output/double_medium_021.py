from collections import deque
from typing import Optional, List

class Solution:
    def levelOrderBottom(self, root: Optional[TreeNode]) -> List[List[int]]:
        queue = deque()
        queue.append(root)
        lst = []

        while queue:
            levels = []
            for _ in range(len(queue)):
                node = queue.popleft()
                if node:
                    levels.append(node.val)
                    queue.append(node.left)
                    queue.append(node.right)

            if levels:
                lst.append(levels)

        return lst[::-1]