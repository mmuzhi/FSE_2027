class GomokuGame:
    def __init__(self, board_size):
        self.board_size = board_size
        self.board = [[' ' for _ in range(board_size)] for _ in range(board_size)]
        self.current_player = 'X'

    def make_move(self, row, col):
        if 0 <= row < self.board_size and 0 <= col < self.board_size and self.board[row][col] == ' ':
            self.board[row][col] = self.current_player
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        return False

    def check_winner(self):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board[row][col] != ' ':
                    for dx, dy in directions:
                        if self._check_five_in_a_row(row, col, dx, dy):
                            return self.board[row][col]
        return None

    def _check_five_in_a_row(self, row, col, dx, dy):
        count = 1
        symbol = self.board[row][col]
        # Positive direction
        for i in range(1, 5):
            r, c = row + dx * i, col + dy * i
            if not (0 <= r < self.board_size and 0 <= c < self.board_size):
                break
            if self.board[r][c] != symbol:
                break
            count += 1
        # Negative direction
        for i in range(1, 5):
            r, c = row - dx * i, col - dy * i
            if not (0 <= r < self.board_size and 0 <= c < self.board_size):
                break
            if self.board[r][c] != symbol:
                break
            count += 1
        return count >= 5

if __name__ == '__main__':
    gomoku_game = GomokuGame(10)
    moves = [
        (5, 5), (0, 0), (5, 4), (0, 1), (5, 3), (0, 2), (5, 2), (0, 3), (5, 1)
    ]
    for move in moves:
        gomoku_game.make_move(*move)
    print(gomoku_game.check_winner())