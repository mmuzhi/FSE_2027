import heapq
from typing import List

class Solution:
    def maxSum(self, grid: List[List[int]], limits: List[int], k: int) -> int:
        n = len(grid)
        # Precompute sorted rows in descending order
        rows = []
        for i in range(n):
            rows.append(sorted(grid[i], reverse=True))
        
        next_index = [0] * n
        heap = []
        # Initialize the heap with the first element of each row that has a positive limit
        for i in range(n):
            if limits[i] > 0:
                heapq.heappush(heap, (-rows[i][0], i))
        
        ans = 0
        count = 0
        while heap and count < k:
            neg_val, i = heapq.heappop(heap)
            value = -neg_val
            ans += value
            count += 1
            next_index[i] += 1
            # If we haven't reached the row's limit, push the next element from that row
            if next_index[i] < limits[i]:
                heapq.heappush(heap, (-rows[i][next_index[i]], i))
        return ans