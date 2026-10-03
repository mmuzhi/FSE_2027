import sys
from collections import deque

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    
    it = iter(data)
    h = int(next(it)); w = int(next(it)); q = int(next(it))
    queries = []
    for _ in range(q):
        r = int(next(it)); c = int(next(it))
        queries.append((r, c))
    
    # We'll maintain a grid (2D list) to mark if a wall is present.
    # Initially, all walls are present. We'll use a 2D list of booleans, but that's 400000 elements, which is acceptable.
    # But we also need to quickly find the next wall in four directions. We can use a 2D array for the grid, and then for each row and column, we can precompute the next wall positions.

    # Alternatively, we can use a set for walls that are still present. But then how to find the next wall in a row? We can't.

    # Let's use a 2D grid (list of lists) for walls, initially all True (wall present).
    grid = [[True] * (w+1) for _ in range(h+1)]
    # We'll also maintain two 2D arrays: next_up, next_down, next_left, next_right, but that's too heavy.

    # Instead, we can use four 2D arrays (or lists) for each row and column to store the next wall in each direction. But updating them is complex.

    # Another idea: use a union-find to group consecutive empty cells, but then how to find the next wall?

    # Alternatively, we can use a "sweep line" and process the queries in a way that we update the grid and then use a pointer for each cell to the next wall. But that's too vague.

    # Let me think of the sample: 
    # 2 4 3
    # 1 2
    # 1 2
    # 1 3

    # Initially, grid[1][2] is True, then after first query, set to False. Then second query: 
    #   Check up: row 0 doesn't exist, so nothing.
    #   Down: row 2, column 2: True -> remove (2,2)
    #   Left: column 1 in row 1: True -> remove (1,1)
    #   Right: column 3 in row 1: True -> remove (1,3)

    # Then third query: (1,3) is now False, so check directions:
    #   Down: (2,3) is True -> remove (2,3)
    #   Right: (1,4) is True -> remove (1,4)

    # So after all, walls at (2,1) and (2,4) remain.

    # We can simulate by having a grid and then for each query, if the cell is wall, remove it. Else, for each direction, find the next wall by scanning until we hit a wall. But worst-case, each query could scan the entire row or column.

    # But note: the grid has H*W <= 400000, so worst-case, a row has 400000 columns. Then, scanning a row for a wall could be 400000 steps. And with 200000 queries, worst-case 200000 * 400000 * 4 = 320e9 operations, which is too slow in Python.

    # We need a smarter way.

    # Idea: Precompute for each row and column the next wall in each direction. But then update when a wall is removed.

    # We can maintain for each row i:
    #   left_wall[i][j]: the next wall to the left of (i, j) (or None if none)
    #   right_wall[i][j]: the next wall to the right of (i, j) (or None if none)
    # Similarly for columns.

    # But then, when a wall at (i, j) is removed, we need to update all cells in row i and column j that had (i, j) as their next wall. That's too heavy.

    # Alternatively, we can use a pointer array that points to the next wall in each direction. For example, for each cell, we store the next wall in the four directions. But then updating is still heavy.

    # Another idea: use a segment tree or a Fenwick tree to store the minimum row or column index with a wall in a given direction? Not sure.

    # Let me consider a different approach: offline queries. But the queries