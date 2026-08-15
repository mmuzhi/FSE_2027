from typing import List

class Solution:
    def numMovesStonesII(self, stones: List[int]) -> List[int]:
        stones.sort()
        n = len(stones)

        move_penultimate = stones[-2] - stones[0] - n + 2
        move_final = stones[-1] - stones[1] - n + 2
        most_moves = max(move_penultimate, move_final)

        if move_penultimate == 0 or move_final == 0:
            return [min(2, most_moves), most_moves]

        max_legal_moves = 0
        starting_index = 0

        for index, stone in enumerate(stones):
            while stones[starting_index] <= stone - n:
                starting_index += 1
            max_legal_moves = max(max_legal_moves, index - starting_index + 1)

        return [n - max_legal_moves, most_moves]