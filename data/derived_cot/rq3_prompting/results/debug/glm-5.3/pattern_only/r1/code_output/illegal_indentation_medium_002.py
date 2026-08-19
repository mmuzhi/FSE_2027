from typing import List


class Solution:
    '''
        Test cases walk through 
        Given 7, 4, 9 prove 1, 2                                                            6, 5, 4, 3, 10, prove 2, 3 

        Sort stones -> 4, 7, 9                                                              3, 4, 5, 6, 10 
        Stone length -> 3                                                                   5
        Move penultimate = 7 - 4 - 3 + 2 = 2                                                6-3-5+2 = 0 
        Move final = 9 - 7 - 3 + 2 = 1                                                      10-4-5+2 = 3 
        Neither is 0, so we cannot return for sure                                          Move penultimate is 0, so move final is assured 
                                                                                            This means we can return [min(2, 3), 3] -> [2, 3]

        Max legal moves is 0                                                                For completeness, max legal moves is 0, max moves is 3  
        starting index is 0                                                                 starting index is 0 

        Enumeration                                                                         Enumeration
            index is 0, stone is 4                                                             index is 0, stone is 3 
            stones[0] lte 4 - 3 ? No, skip while loop                                          stones[0] lte 3 - 5 ? No, skip while 
            max legal moves is max of self and 0 - 0 + 1                                       max legal moves is max of self and 0 - 0 + 1
                 -> max legal moves is 1                                                      -> max legal moves is 1 

            index is 1, stone is 7                                                             index is 1, stone is 4 
            stones[0] <= 7 - 3 ? Yes, enter while                                              stones[0] lte 4 - 5 ? No, skip while 
                starting index is now 1                                                        max legal moves is max of self and 1 - 0 + 1 -> max legal moves is 2
            stones[1] <= 7 - 3 ? No, skip while                                                 
            max legal moves -> max(max of self and 1 - 1 + 1)                                  
                -> max legal moves is 1                                                        index is 2, stone is 5 
                                                                                               stones[0] lte 5 - 5 ? No skip while 
            index is 2, stone is 9                                                             max legal moves is max of self and 2 - 0 + 1 -> max legal moves is 3 
            stones[1] <= 9 - 3 ? No, skip while                                                 
            max legal moves is max(max of self and 2-1 + 1)                                     
                 -> max legal moves is 2                                                       index is 3, stone is 6 
        End enumeration                                                                        stones[0] lte 6 - 5 ? No skip while 
                                                                                               max legal moves is max of self and 3 - 0 + 1 -> max legal moves is 4 
                                                                                              
                                                                                               index is 4, stones is 10 
                                                                                               stones[0] lte 10 - 5 ? Yes, enter while 
                                                                                                    starting index is 1 
                                                                                               stones[1] lte 10 - 5 ? Yes, enter while 
                                                                                                    starting index is 2 
                                                                                               stones[2] lte 10 - 5 ? Yes, enter while 
                                                                                                    starting index is 3 
                                                                                               max legal moves is max of self and 4 - 3 + 1 
                                                                                            End enumeration

                                                                                            Return [2, 3]
    '''
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
        # if n-1 stones are already tightly consecutive, we cannot finish in a single move
        # (the hole sits at the boundary and is unreachable by the lone stone in one move),
        # so the minimum is 2 unless the configuration can be finished in exactly 1 (most_moves == 1)
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