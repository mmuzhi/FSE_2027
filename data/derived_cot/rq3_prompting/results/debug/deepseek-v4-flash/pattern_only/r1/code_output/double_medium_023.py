from typing import List

class Solution:
    def construct(self, grid: List[List[int]]) -> 'Node':
        n = len(grid)
        if n == 0:
            return None
        return self.buildTree(grid, 0, n, 0, n, n)

    def buildTree(self, grid: List[List[int]], rs: int, re: int, cs: int, ce: int, level: int) -> 'Node':
        if level == 1:
            return Node(grid[rs][cs] == 1, True, None, None, None, None)

        half = level // 2
        tl = self.buildTree(grid, rs, rs + half, cs, cs + half, half)
        tr = self.buildTree(grid, rs, rs + half, cs + half, ce, half)
        bl = self.buildTree(grid, rs + half, re, cs, cs + half, half)
        br = self.buildTree(grid, rs + half, re, cs + half, ce, half)

        if tl.isLeaf and tr.isLeaf and bl.isLeaf and br.isLeaf:
            if tl.val == tr.val == bl.val == br.val:
                return Node(tl.val, True, None, None, None, None)

        return Node(True, False, tl, tr, bl, br)