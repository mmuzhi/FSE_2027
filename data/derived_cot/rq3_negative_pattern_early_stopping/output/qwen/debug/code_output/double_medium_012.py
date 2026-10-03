from collections import deque

class Solution:
    def isPossibleToCutPath(self, grid: List[List[int]]) -> bool:
        m, n = len(grid), len(grid[0])
        if grid[0][0] == 1 or grid[m-1][n-1] == 1:
            return False
        
        # If the grid is 1x1, then we have only one cell, so we cannot have two paths (since two paths would require two cells)
        if m == 1 and n == 1:
            return True
        
        # We'll use BFS from (0,0) and mark visited nodes with a special marker (like 2) to avoid revisiting.
        # But note: we are allowed to cut obstacles, so we can remove obstacles (turn 1 to 0) if needed? Actually, the grid is fixed and we can only traverse 0s and 1s? 
        # The problem says: "You are given a grid of size m x n, where each cell can be either 0 (empty) or 1 (obstacle)."
        # And we can cut the path, meaning we can remove obstacles? Actually, the problem statement is ambiguous, but the example code marks cells as 2 and then uses them as traversable.
        # Let me re-read: "You are given a grid of size m x n, where each cell can be either 0 (empty) or 1 (obstacle)." and we are to check if we can cut the path (i.e., remove some obstacles) so that there are two distinct paths.

        # However, note: the example code marks cells as 2 and then uses them as traversable. But the grid initially has only 0 and 1.

        # Actually, the problem is: we can remove obstacles (turn 1 to 0) arbitrarily, but we cannot remove the start and end? And we want to know if there are two distinct paths (vertex-disjoint) from (0,0) to (m-1, n-1).

        # We can use a standard method: 
        # 1. Use BFS to mark the shortest path from (0,0) to every cell (ignoring obstacles? Actually, we can remove obstacles arbitrarily, so we can traverse any cell if we remove the obstacle).
        # 2. Then, we can use a second BFS (or DFS) to see if there is a second path that does not use the same cells as the first.

        # But note: we are allowed to remove obstacles arbitrarily, so the grid becomes all 0s except the obstacles we don't remove. However, we are not forced to remove all obstacles. We just need two disjoint paths.

        # Actually, the problem is equivalent to: is there a way to assign two vertex-disjoint paths from (0,0) to (m-1, n-1) in the grid where we can ignore obstacles (by cutting them) but we cannot change the start and end?

        # We can use the following: 
        #   Let's mark the grid with two different markers for two different paths. But note, we are allowed to cut obstacles arbitrarily, so we can use any cell (by cutting the obstacle) but we cannot use the same cell twice.

        # We can do:
        #   Step 1: BFS from (0,0) to (m-1, n-1) without considering obstacles (since we can cut them). But then we mark the first path.
        #   Step 2: BFS from (0,0) to (m-1, n-1) again, but this time we cannot use the cells that were used in the first path.

        # However, note: the grid is fixed and we can cut obstacles arbitrarily, so we can use any cell (by cutting the obstacle) but we cannot use a cell twice.

        # But wait, the problem does not require the entire grid to be cut, just the path. So we can use a cell only once.

        # We can do:
        #   Let's create a new grid where we mark the cells that are used in the first path as blocked (so we cannot use them in the second path).
        #   Then, check if there is a path from (0,0) to (m-1, n-1) in the original grid with the first path blocked.

        # However, note: we are allowed to cut obstacles arbitrarily, so the first path might have cut some obstacles, but the second path can also cut obstacles independently. But the condition is that the two paths must be vertex-disjoint.

        # So, we can do:
        #   Step 1: Find one path from (0,0) to (m-1, n-1) (using BFS or DFS, ignoring obstacles because we can cut them).
        #   Step