from typing import List

class Solution:
    def numMovesStonesII(self, stones: List[int]) -> List[int]:
        stones.sort()
        n = len(stones)
        max_moves = max(stones[-2] - stones[0] - n + 2, stones[-1] - stones[1] - n + 2)
        left = 0
        min_moves = n
        for right in range(n):
            while stones[right] - stones[left] + 1 > n:
                left += 1
            count = right - left + 1
            if count == n - 1 and stones[right] - stones[left] + 1 == n - 1:
                min_moves = min(min_moves, 2)
            else:
                min_moves = min(min_moves, n - count)
        return [min_moves, max_moves]