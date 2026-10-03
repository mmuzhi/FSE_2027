class Solution:
    def canAliceWin(self, n: int) -> bool:
        if n < 10:
            return False
        moves = [10,9,8,7,6,5,4,3,2,1]
        current = n
        turn = 0  # 0 for Alice, 1 for Bob
        for move in moves:
            if current < move:
                return turn == 1
            else:
                current -= move
                turn = 1 - turn
        return turn == 1