class Solution:
    def findSafeWalk(self, grid: List[List[int]], health: int) -> bool:
        m = len(grid)
        n = len(grid[0])
        # If the start or end is unsafe, we need to check
        if grid[0][0] == 1 or grid[m-1][n-1] == 1:
            return False
        
        # dp[i][j] will store the maximum health remaining at (i, j)
        dp = [[-1] * n for _ in range(m)]
        dp[0][0] = health
        
        # Directions for moving up, down, left, right
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        
        # Use a queue for BFS, but we can use a stack for DFS as well, but BFS is more natural for this
        # We'll use a queue (BFS) to update the dp table
        from collections import deque
        q = deque()
        q.append((0, 0))
        
        while q:
            x, y = q.popleft()
            current_health = dp[x][y]
            # If current_health is -1, it means not visited, but we set initial to health, so skip if not visited
            if current_health == -1:
                continue
            # Check all four directions
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < m and 0 <= ny < n:
                    # Calculate the health after moving to (nx, ny)
                    new_health = current_health - 1 if grid[nx][ny] == 1 else current_health
                    # If new_health is negative, skip
                    if new_health < 0:
                        continue
                    # If we found a better way to reach (nx, ny) (i.e., with more health remaining), update
                    if new_health > dp[nx][ny]:
                        dp[nx][ny] = new_health
                        q.append((nx, ny))
        
        return dp[m-1][n-1] >= 1