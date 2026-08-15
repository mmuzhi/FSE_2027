from typing import List

class Solution:
    def construct(self, grid: List[List[int]]) -> 'Node':
        n = len(grid)
        if n == 0:
            return None
        return self.buildTree(grid, 0, n, 0, n, n)

    def buildTree(self, grid, rs, re, cs, ce, level):
        if level == 1:
            return Node(grid[rs][cs], True, None, None, None, None)

        half = level // 2
        mid_r = rs + half
        mid_c = cs + half

        tl = self.buildTree(grid, rs, mid_r, cs, mid_c, half)
        tr = self.buildTree(grid, rs, mid_r, mid_c, ce, half)
        bl = self.buildTree(grid, mid_r, re, cs, mid_c, half)
        br = self.buildTree(grid, mid_r, re, mid_c, ce, half)

        if (tl.isLeaf and tr.isLeaf and bl.isLeaf and br.isLeaf and
                tl.val == tr.val == bl.val == br.val):
            return Node(tl.val, True, None, None, None, None)

        return Node(tl.val, False, tl, tr, bl, br)