from collections import deque
from typing import List, Optional

class Solution:
    def levelOrderBottom(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []
        queue = deque()
        queue.append(root)
        lst = []
        while queue:
            levels = []
            for _ in range(len(queue)):
                tmp = queue.popleft()
                levels.append(tmp.val)
                if tmp.left:
                    queue.append(tmp.left)
                if tmp.right:
                    queue.append(tmp.right)
            if levels:
                lst.append(levels)
        return lst[::-1]