from functools import lru_cache
from math import inf
from typing import List

class Solution:
    def maxMoves(self, kx: int, ky: int, positions: List[List[int]]) -> int:
        # If there are no pawns, return 0
        if not positions:
            return 0
        
        # Precompute minimal moves from any point to any other point (only between pawns and start)
        # We'll create a list of all points: start and pawns
        points = [(kx, ky)] + positions
        n = len(points)
        # Map index: 0 is start, 1 to n-1 are pawns
        # We'll compute a distance matrix between these points
        # But note: the minimal moves from a point to another is independent of other pawns (since pawns can be jumped over)
        # We can use BFS for each point because the grid is 50x50 and points are only 16 (start + up to 15 pawns)
        # But actually, we can use a BFS from each point to all other points. However, 16 points, each BFS on 50x50 grid is 2500 nodes, which is acceptable.

        # Directions for knight moves
        directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        
        # Function to compute minimal moves from a given point to all other points
        def bfs(start):
            dist = {}
            for i in range(n):
                dist[i] = -1  # -1 means not visited
            q = [(start[0], start[1], 0)]
            dist[start[0]*50 + start[1] + 5000] = 0  # Use a unique key for the starting position
            while q:
                x, y, moves = q.pop(0)
                if (x, y) == (points[0][0], points[0][1]):
                    # We found the start point? Actually, we are computing from start to all, but we need to map to point indices.
                    # Actually, we are computing from a given point to all points. We need to record the minimal moves to each point index.
                    # But we don't know the index of the point (x, y) in the points list. So we can store the minimal moves for each point index.
                    # Instead, we can run BFS from a point and then for each point index, we look up the minimal moves from the BFS result.
                    pass  # This approach is not efficient for our purpose.

            # Alternatively, we can precompute the minimal moves between every pair of points (0 to n-1) by running BFS from each point.
            # But that would be 16 BFS runs, each on a 50x50 grid, which is 16 * 2500 = 40000 nodes, which is acceptable.

        # Actually, we can do: for each point, run BFS to all other points and record the minimal moves to each point index.
        # But we have 16 points, so 16 BFS runs. Each BFS runs on a grid of 50x50, so 2500 nodes per BFS. 16*2500=40000, which is acceptable in Python if done carefully.

        # Let's create a distance matrix: dist[i][j] = minimal moves from point i to point j
        dist = [[-1] * n for _ in range(n)]
        
        # We'll run BFS from each point i
        for i in range(n):
            # BFS starting from points[i]
            start_x, start_y = points[i]
            q = [(start_x, start_y, 0)]
            visited = [[False] * 50 for _ in range(50)]
            visited[start_x][start_y] = True
            while q:
                x, y, moves = q.pop(0)
                # Check if this (x, y) is one of the points
                for j in range(n):
                    tx, ty = points[j]
                    if x == tx and y == ty:
                        # We found point j from point i
                        dist[i][j] = moves
                # Explore neighbors
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < 50 and 0 <= ny < 50 and not visited[nx][ny]:
                        visited[nx][ny] = True