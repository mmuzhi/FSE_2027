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
        
        next_level = level // 2
        tl = self.buildTree(grid, rs, rs + next_level, cs, cs + next_level, next_level)
        tr = self.buildTree(grid, rs, rs + next_level, cs + next_level, ce, next_level)
        bl = self.buildTree(grid, rs + next_level, re, cs, cs + next_level, next_level)
        br = self.buildTree(grid, rs + next_level, re, cs + next_level, ce, next_level)

        if tl.isLeaf and tr.isLeaf and bl.isLeaf and br.isLeaf and tl.val == tr.val == bl.val == br.val:
            return Node(tl.val, True, None, None, None, None)
        else:
            return Node(True, False, tl, tr, bl, br)