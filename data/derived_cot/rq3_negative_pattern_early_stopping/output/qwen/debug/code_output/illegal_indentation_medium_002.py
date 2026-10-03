class Solution:
    def numMovesStonesII(self, stones: List[int]) -> List[int]:
        stones.sort()
        stone_length = len(stones)
        # Calculate the two potential minimal moves
        move_penultimate = stones[-2] - stones[0] - stone_length + 2
        move_final = stones[-1] - stones[1] - stone_length + 2
        most_moves = max(move_penultimate, move_final)
        
        if move_penultimate == 0 or move_final == 0:
            min_legal_moves = min(2, most_moves)
            return [min_legal_moves, most_moves]
        
        max_legal_moves = 0
        starting_index = 0
        for index, stone in enumerate(stones):
            while stones[starting_index] <= stone - stone_length:
                starting_index += 1
            current_moves = index - starting_index + 1
            if current_moves > max_legal_moves:
                max_legal_moves = current_moves
        
        min_legal_moves = stone_length - max_legal_moves
        return [min_legal_moves, most_moves]
