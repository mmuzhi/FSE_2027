class TicTacToe:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.currentPlayer = 'X'

    def makeMove(self, row, col):
        # Java throws ArrayIndexOutOfBoundsException on out-of-range indices;
        # explicit check prevents Python's silent negative indexing.
        if not (0 <= row < 3 and 0 <= col < 3):
            raise IndexError(f"Index {row}, {col} out of bounds for 3x3 board")
        if self.board[row][col] == ' ':
            self.board[row][col] = self.currentPlayer
            self.currentPlayer = 'O' if self.currentPlayer == 'X' else 'X'
            return True
        else:
            return False

    def checkWinner(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] and self.board[i][1] == self.board[i][2] and self.board[i][0] != ' ':
                return self.board[i][0]
        for j in range(3):
            if self.board[0][j] == self.board[1][j] and self.board[1][j] == self.board[2][j] and self.board[0][j] != ' ':
                return self.board[0][j]
        if self.board[0][0] == self.board[1][1] and self.board[1][1] == self.board[2][2] and self.board[0][0] != ' ':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] and self.board[1][1] == self.board[2][0] and self.board[0][2] != ' ':
            return self.board[0][2]
        return None

    def isBoardFull(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    return False
        return True

    def getCurrentPlayer(self):
        return self.currentPlayer