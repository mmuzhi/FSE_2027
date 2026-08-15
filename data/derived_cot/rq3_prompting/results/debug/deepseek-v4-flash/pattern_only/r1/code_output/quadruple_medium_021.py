I need output only fixed code. The final answer should be code. Let's ensure no extra text. I'll output code block? The instruction says output only fixed code. I'll output raw code. Need maybe include `from typing import List`. Good.

Let's produce final.</think>```python
from typing import List

class Solution:
    def construct(self, grid: List[List[int]]) -> 'Node':
        n = len(grid)
        if n == 0:
            return None
        return self.buildTree(grid, 0, n, 0, n, n)

    def buildTree(self, grid, rs, re, cs, ce, level):
        if level == 1:
            return Node(grid[rs][cs] == 1, True, None, None, None, None)

        mid = level // 2
        topLeft = self.buildTree(grid, rs, re - mid, cs, ce - mid, mid)
        topRight = self.buildTree(grid, rs, re - mid, ce - mid, ce, mid)
        bottomLeft = self.buildTree(grid, re - mid, re, cs, ce - mid, mid)
        bottomRight = self.buildTree(grid, re - mid, re, ce - mid, ce, mid)

        if (topLeft.isLeaf and topRight.isLeaf and bottomLeft.isLeaf and bottomRight.isLeaf and
                topLeft.val == topRight.val == bottomLeft.val == bottomRight.val):
            return Node(topLeft.val, True, None, None, None, None)

        return Node(topLeft.val, False, topLeft, topRight, bottomLeft, bottomRight)