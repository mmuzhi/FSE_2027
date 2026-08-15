from typing import List

class Solution:
    def construct(self, grid: List[List[int]]) -> 'Node':
        n = len(grid)
        if n == 0:
            return None
        return self.buildTree(grid, 0, n, 0, n, n)

    def buildTree(self, grid: List[List[int]], rs: int, re: int, cs: int, ce: int, level: int) -> 'Node':
        if level == 1:
            return Node(grid[rs][cs], True, None, None, None, None)

        half = level // 2
        mid_r = rs + half
        mid_c = cs + half

        topLeft = self.buildTree(grid, rs, mid_r, cs, mid_c, half)
        topRight = self.buildTree(grid, rs, mid_r, mid_c, ce, half)
        bottomLeft = self.buildTree(grid, mid_r, re, cs, mid_c, half)
        bottomRight = self.buildTree(grid, mid_r, re, mid_c, ce, half)

        if (topLeft.isLeaf and topRight.isLeaf and bottomLeft.isLeaf and bottomRight.isLeaf and
                topLeft.val == topRight.val == bottomLeft.val == bottomRight.val):
            return Node(topLeft.val, True, None, None, None, None)

        return Node(topLeft.val, False, topLeft, topRight, bottomLeft, bottomRight)