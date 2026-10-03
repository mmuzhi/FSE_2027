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
            level_size = len(queue)
            for _ in range(level_size):
                tmp = queue.popleft()
                if tmp:
                    levels.append(tmp.val)
                    queue.append(tmp.left)
                    queue.append(tmp.right)
            if levels:
                lst.append(levels)
        
        return lst[::-1]