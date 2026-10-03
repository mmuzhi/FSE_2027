class GomokuGame:
    def __init__(self, board_size):
        self.board_size = board_size
        self.board = [[' ' for _ in range(board_size)] for _ in range(board_size)]
        self.current_player = 'X'

    def make_move(self, row, col):
        if not (0 <= row < self.board_size and 0 <= col < self.board_size):
            return False
        if self.board[row][col] == ' ':
            self.board[row][col] = self.current_player
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        return False

    def check_winner(self):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for r in range(self.board_size):
            for c in range(self.board_size):
                if self.board[r][c] != ' ':
                    for dr, dc in directions:
                        if self._check_five_in_a_row(r, c, dr, dc):
                            return self.board[r][c]
        return None

    def get_board(self):
        return self.board

    def _check_five_in_a_row(self, row, col, dx, dy):
        count = 1
        symbol = self.board[row][col]
        for i in range(1, 5):
            r = row + dx * i
            c = col + dy * i
            if not (0 <= r < self.board_size and 0 <= c < self.board_size):
                return False
            if self.board[r][c] != symbol:
                return False
            count += 1
        return count == 5