import random


class MahjongConnect:
    def __init__(self, board_size, icons):
        self.BOARD_SIZE = board_size
        self.ICONS = icons
        self.board = self.create_board()

    def create_board(self):
        new_board = [[random.choice(self.ICONS) for _ in range(self.BOARD_SIZE[1])]
                     for _ in range(self.BOARD_SIZE[0])]
        return new_board

    def is_valid_move(self, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2

        # Bounds check for both positions
        if not (0 <= x1 < self.BOARD_SIZE[0] and 0 <= y1 < self.BOARD_SIZE[1] and
                0 <= x2 < self.BOARD_SIZE[0] and 0 <= y2 < self.BOARD_SIZE[1]):
            return False

        # Same position is not a valid move
        if pos1 == pos2:
            return False

        # Icons must match
        if self.board[x1][y1] != self.board[x2][y2]:
            return False

        return self.has_path(pos1, pos2)

    def has_path(self, pos1, pos2):
        visited = set()
        stack = [pos1]

        while stack:
            current_pos = stack.pop()

            if current_pos == pos2:
                return True

            if current_pos in visited:
                continue

            visited.add(current_pos)
            x, y = current_pos

            for direction in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                new_x = x + direction[0]
                new_y = y + direction[1]
                if 0 <= new_x < self.BOARD_SIZE[0] and 0 <= new_y < self.BOARD_SIZE[1]:
                    if (new_x, new_y) not in visited and self.board[new_x][new_y] == self.board[x][y]:
                        stack.append((new_x, new_y))

        return False

    def remove_icons(self, pos1, pos2):
        self.board[pos1[0]][pos1[1]] = ' '
        self.board[pos2[0]][pos2[1]] = ' '

    def is_game_over(self):
        for row in self.board:
            if any(icon != ' ' for icon in row):
                return False
        return True