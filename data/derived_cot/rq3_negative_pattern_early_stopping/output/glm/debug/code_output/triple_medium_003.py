from typing import List

class Solution:
    def numMovesStonesII(self, stones: List[int]) -> List[int]:
        stones.sort()
        n = len(stones)
        move_penultimate = stones[-2] - stones[0] - n + 2
        move_final = stones[-1] - stones[1] - n + 2
        max_moves = max(move_penultimate, move_final)
        
        if move_penultimate == 0 or move_final == 0:
            min_moves = min(1, max_moves)
            return [min_moves, max_moves]
            
        min_moves = n
        left = 0
        for right in range(n):
            while stones[right] - stones[left] + 1 > n:
                left += 1
            min_moves = min(min_moves, n - (right - left + 1))
            
        return [min_moves, max_moves]

solution = Solution()
print(solution.numMovesStonesII([7, 4, 9]))