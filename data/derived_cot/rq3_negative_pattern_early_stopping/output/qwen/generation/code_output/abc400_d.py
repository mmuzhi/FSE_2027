import sys
from collections import deque

def main():
    data = sys.stdin.read().splitlines()
    if not data: 
        return
    
    H, W = map(int, data[0].split())
    grid = []
    for i in range(1, 1+H):
        grid.append(data[i].strip())
    
    A, B, C, D = map(int, data[1+H].split())
    # Convert to 0-indexed
    start = (A-1, B-1)
    goal = (C-1, D-1)
    
    # We'll use a BFS with state (i, j) and we'll keep a 2D array for the minimum kicks to reach (i, j)
    # But note: the grid changes when we kick, so we need to consider that we can break walls and then use them.
    # However, we can precompute the effect of kicks: a kick from a cell (x, y) in a direction d will break walls at distance 1 and 2 in that direction.
    # But note: the problem allows to break walls that are at most 2 steps away. So from (x, y), in direction (dx,dy), the cells are (x+dx, y+dy) and (x+2*dx, y+2*dy) (if within bounds).

    # But note: the grid changes, so we cannot precompute the entire grid. However, we can consider that breaking a wall is permanent and we can use that information to traverse.

    # We can use a Dijkstra where the state is (i, j) and the cost is the number of kicks. But we need to know which walls are broken to allow movement.

    # Alternatively, we can use a multi-layered graph: the grid has two types of cells: original roads and broken walls (which are treated as roads). But the breaking is done by kicks and we pay for each kick.

    # However, note that breaking a wall might be done from multiple directions and we don't want to break the same wall multiple times.

    # We can use a BFS that considers two types of moves:
    # 1. Move to adjacent road (original or broken) with 0 cost.
    # 2. Kick in one of the four directions (cost 1) and then from the current cell, we break the walls (if any) in the two steps in that direction. But note: breaking walls might enable new moves.

    # But the state must include the entire grid? That is too expensive.

    # Another idea: we can precompute the minimum number of kicks required to break a wall at a particular cell, but note that one kick can break multiple walls.

    # Insight: We are allowed to break walls only by front kicks from adjacent cells (within 2 steps). So to break a wall at (i, j), we must have a kick from a cell (x, y) such that (i, j) is at distance 1 or 2 from (x, y) in the same direction.

    # However, we are not required to break every wall. We only need to break the walls that are in the way.

    # We can use a Dijkstra where the state is (i, j) and we keep a 2D array "dist" for the minimum kicks to reach (i, j). But we need to know the grid configuration to know which cells are roads. But the grid configuration depends on the kicks we have done.

    # We can consider that a cell is a road if:
    #   - It was originally a road, OR
    #   - It was broken by at least one kick (and we know that breaking a wall requires a kick from a cell within 2 steps in the same direction).

    # But note: the grid changes only by kicks, and we are allowed to perform kicks from any road cell (original or broken). 

    # We can use a two-dimensional Dijkstra where the state is (i, j) and we store the minimum kicks to reach (i, j). However, the grid configuration is not stored, but we can update the grid as we go? But the grid is shared and we break walls permanently.

    # But note: if we break a wall, then that wall becomes a road and we can use it for free (without additional kick) in the future. However, the same wall might be broken by multiple paths, but we only need to break it once.

    # We can precompute the minimum kicks required to break a wall at each cell. Then, the total cost to reach a cell (i, j) is the minimum kicks to break all walls that are in the path? Not exactly, because we can break walls from different directions and the path might use broken walls.

    # Alternatively, we can use a BFS that considers two types of