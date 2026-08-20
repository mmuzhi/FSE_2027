class GomokuGame:
    def __init__(self, board_size):
        self.board_size = board_size
        self.board = [[' ' for _ in range(board_size)] for _ in range(board_size)]
        self.current_player = 'X'

    def make_move(self, row, col):
        # Match Java's ArrayIndexOutOfBoundsException for out-of-bounds indices
        # (Python would silently wrap around on negative indices otherwise).
        if row < 0 or row >= self.board_size or col < 0 or col >= self.board_size:
            raise IndexError(
                f"Index [{row}][{col}] out of bounds for board size {self.board_size}"
            )
        if self.board[row][col] == ' ':
            self.board[row][col] = self.current_player
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        return False

    def check_winner(self):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board[row][col] != ' ':
                    for direction in directions:
                        if self.check_five_in_a_row(row, col, direction):
                            return self.board[row][col]
        return None

    def check_five_in_a_row(self, row, col, direction):
        dx, dy = direction
        count = 1
        symbol = self.board[row][col]
        for i in range(1, 5):
            new_row = row + dx * i
            new_col = col + dy * i
            if (new_row < 0 or new_row >= self.board_size
                    or new_col < 0 or new_col >= self.board_size):
                break
            if self.board[new_row][new_col] != symbol:
                break
            count += 1
        for i in range(1, 5):
            new_row = row - dx * i
            new_col = col - dy * i
            if (new_row < 0 or new_row >= self.board_size
                    or new_col < 0 or new_col >= self.board_size):
                break
            if self.board[new_row][new_col] != symbol:
                break
            count += 1
        return count >= 5


if __name__ == "__main__":
    gomoku_game = GomokuGame(10)
    moves = [(5, 5), (0, 0), (5, 4), (0, 1), (5, 3), (0, 2), (5, 2), (0, 3), (5, 1)]
    for move in moves:
        gomoku_game.make_move(move[0], move[1])
    print(gomoku_game.check_winner())