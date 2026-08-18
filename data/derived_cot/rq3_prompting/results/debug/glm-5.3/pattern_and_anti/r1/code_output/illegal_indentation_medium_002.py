from typing import List

class Solution:
    def numMovesStonesII(self, stones: List[int]) -> List[int]:
        # order does not need to be maintained, so sorting is optimal
        stones.sort()
        # want to work within stone physical space since 10^9 >> 10^4 (stone weight vs length)
        stone_length = len(stones)
        # what is the cost of moving the second to last stone and the 0th stone?
        move_penultimate = stones[-2] - stones[0] - stone_length + 2
        # what is the cost of moving the last stone and the 1st stone?
        move_final = stones[-1] - stones[1] - stone_length + 2
        # our most moves possible are the max of these two
        most_moves = max(move_penultimate, move_final)
        # if either is 0, the stones form n-1 consecutive stones at one end,
        # which is the special case where the last stone cannot join in one move,
        # so the minimum is locked at min(2, most_moves)
        if move_penultimate == 0 or move_final == 0:
            min_legal_moves = min(2, most_moves)
            return [min_legal_moves, most_moves]
        # how many legal moves are there in sorted order?
        max_legal_moves = 0
        # starting from 0th index
        starting_index = 0
        # enumerate each stone and index
        for index, stone in enumerate(stones):
            # while the stone at starting index is lte this stone minus stone length (cost of a move)
            while stones[starting_index] <= stone - stone_length:
                starting_index += 1
            # max legal moves is then set to maxima of self and indexed difference with 1 for 0 based indexing
            max_legal_moves = max(max_legal_moves, index - starting_index + 1)
        # return length - max legal moves when in sorted order (your minimal move state) and most moves in sorted order
        return [stone_length - max_legal_moves, most_moves]