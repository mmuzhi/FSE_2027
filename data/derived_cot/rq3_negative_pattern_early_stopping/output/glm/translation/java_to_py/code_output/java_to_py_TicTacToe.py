class TicTacToe:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'

    def make_move(self, row, col):
        if row < 0 or row >= 3 or col < 0 or col >= 3:
            raise IndexError("Index out of bounds")
        if self.board[row][col] == ' ':
            self.board[row][col] = self.current_player
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        else:
            return False

    def check_winner(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != ' ':
                return self.board[i][0]
        for j in range(3):
            if self.board[0][j] == self.board[1][j] == self.board[2][j] != ' ':
                return self.board[0][j]
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return self.board[0][2]
        return None

    def is_board_full(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    return False
        return True

    def get_current_player(self):
        return self.current_player