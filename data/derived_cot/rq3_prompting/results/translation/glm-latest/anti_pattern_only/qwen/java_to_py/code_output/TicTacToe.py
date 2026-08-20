from typing import Optional


class TicTacToe:
    def __init__(self) -> None:
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.currentPlayer = 'X'

    def makeMove(self, row: int, col: int) -> bool:
        # Java raises ArrayIndexOutOfBoundsException for out-of-range indices;
        # guard explicitly since Python would silently wrap negative indices.
        if not (0 <= row < 3 and 0 <= col < 3):
            raise IndexError("Index out of bounds for length 3")
        if self.board[row][col] == ' ':
            self.board[row][col] = self.currentPlayer
            self.currentPlayer = 'O' if self.currentPlayer == 'X' else 'X'
            return True
        return False

    def checkWinner(self) -> Optional[str]:
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] and self.board[i][0] != ' ':
                return self.board[i][0]
        for j in range(3):
            if self.board[0][j] == self.board[1][j] == self.board[2][j] and self.board[0][j] != ' ':
                return self.board[0][j]
        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] != ' ':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] != ' ':
            return self.board[0][2]
        return None

    def isBoardFull(self) -> bool:
        return all(cell != ' ' for row in self.board for cell in row)

    def getCurrentPlayer(self) -> str:
        return self.currentPlayer