import heapq

class Solution:
    def minTimeToReach(self, moveTime: List[List[int]]) -> int:
        n = len(moveTime)
        m = len(moveTime[0])
        # Directions for adjacent cells
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        # Initialize a 2D array with infinity for each cell's earliest arrival time
        dist = [[float('inf')] * m for _ in range(n)]
        # Priority queue: (time, row, col)
        heap = []
        dist[0][0] = 0
        heapq.heappush(heap, (0, 0, 0))
        
        while heap:
            time, i, j = heapq.heappop(heap)
            if time != dist[i][j]:
                continue
            for dx, dy in directions:
                ni, nj = i + dx, j + dy
                if 0 <= ni < n and 0 <= nj < m:
                    # Calculate the arrival time at (ni, nj)
                    new_time = max(time, moveTime[ni][nj]) + 1
                    if new_time < dist[ni][nj]:
                        dist[ni][nj] = new_time
                        heapq.heappush(heap, (new_time, ni, nj))
        return dist[n-1][m-1]