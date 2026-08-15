from typing import Optional, List

class Solution:
    def findMode(self, root: Optional[TreeNode]) -> List[int]:
        if not root:
            return []

        freq = {}
        stack = [root]

        while stack:
            node = stack.pop()
            freq[node.val] = freq.get(node.val, 0) + 1

            if node.left:
                stack.append(node.left)
            if node.right:
                stack.append(node.right)

        max_cnt = max(freq.values())
        return [num for num, cnt in freq.items() if cnt == max_cnt]