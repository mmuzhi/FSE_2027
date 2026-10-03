class Solution:
    def construct(self, grid: List[List[int]]) -> 'Node':
        level = len(grid)
        if level == 0:
            return None
        return self.buildTree(grid, 0, level-1, 0, level-1, level)
        
    def buildTree(self, grid, rs, re, cs, ce, level):
        if level == 1:
            return Node(grid[rs][cs], True, None, None, None, None)
        
        next_level = level // 2
        tl = self.buildTree(grid, rs, rs + next_level - 1, cs, cs + next_level - 1, next_level)
        tr = self.buildTree(grid, rs, rs + next_level - 1, cs + next_level, ce, next_level)
        bl = self.buildTree(grid, rs + next_level, re, cs, cs + next_level - 1, next_level)
        br = self.buildTree(grid, rs + next_level, re, cs + next_level, ce, next_level)
        
        if tl.isLeaf and tr.isLeaf and bl.isLeaf and br.isLeaf:
            if tl.val == tr.val == bl.val == br.val:
                return Node(tl.val, True, None, None, None, None)
            else:
                return Node(tl.val, False, tl, tr, bl, br)
        else:
            return Node(tl.val, False, tl, tr, bl, br)