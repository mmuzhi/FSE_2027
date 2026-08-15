from typing import List

class Solution:
    def construct(self, grid: List[List[int]]) -> 'Node':
        if not grid:
            return None
        n = len(grid)
        return self.buildTree(grid, 0, n, 0, n, n)

    def buildTree(self, grid, rs, re, cs, ce, level):
        if level == 1:
            return Node(grid[rs][cs], True, None, None, None, None)

        half = level // 2
        mr = rs + half
        mc = cs + half

        tl = self.buildTree(grid, rs, mr, cs, mc, half)
        tr = self.buildTree(grid, rs, mr, mc, ce, half)
        bl = self.buildTree(grid, mr, re, cs, mc, half)
        br = self.buildTree(grid, mr, re, mc, ce, half)

        if tl.isLeaf and tr.isLeaf and bl.isLeaf and br.isLeaf and tl.val == tr.val == bl.val == br.val:
            return Node(tl.val, True, None, None, None, None)

        return Node(tl.val, False, tl, tr, bl, br)