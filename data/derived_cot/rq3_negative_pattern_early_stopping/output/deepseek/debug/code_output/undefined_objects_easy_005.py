from collections import defaultdict
from typing import List, Optional


class Solution:
    def findMode(self, root: Optional[TreeNode]) -> List[int]:
        def traverse(node, freq):
            if not node:
                return
            freq[node.val] += 1
            traverse(node.left, freq)
            traverse(node.right, freq)

        freq = defaultdict(int)
        traverse(root, freq)
        max_count = max(freq.values())
        return [num for num, cnt in freq.items() if cnt == max_count]