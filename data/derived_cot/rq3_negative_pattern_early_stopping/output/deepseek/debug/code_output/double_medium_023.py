from typing import List

class Solution:
    def construct(self, grid: List[List[int]]) -> 'Node':
        level = len(grid)
        root = None
        if level >= 1:
            root = self.buildTree(grid, 0, level, 0, level, level)
        return root
        
    def buildTree(self, grid, rs, re, cs, ce, level):
        if level == 1:
            return Node(grid[rs][cs], True, None, None, None, None)
        
        next_level = level // 2
        mid_r = rs + next_level
        mid_c = cs + next_level
        tl = self.buildTree(grid, rs, mid_r, cs, mid_c, next_level)
        tr = self.buildTree(grid, rs, mid_r, mid_c, ce, next_level)
        bl = self.buildTree(grid, mid_r, re, cs, mid_c, next_level)
        br = self.buildTree(grid, mid_r, re, mid_c, ce, next_level)
        
        if tl.isLeaf and tr.isLeaf and bl.isLeaf and br.isLeaf:
            if tl.val == tr.val == bl.val == br.val:
                new_node = Node(tl.val, True, None, None, None, None)
            else:
                new_node = Node(tl.val, False, tl, tr, bl, br)
        else:
            new_node = Node(tl.val, False, tl, tr, bl, br)
            
        return new_node