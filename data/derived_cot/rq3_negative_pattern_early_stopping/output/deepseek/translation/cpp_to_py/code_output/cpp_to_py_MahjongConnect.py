import random

class MahjongConnect:
    def __init__(self, board_size, icons):
        """
        board_size: tuple (rows, cols)
        icons: list of single-character strings
        """
        self.BOARD_SIZE = board_size
        self.ICONS = icons
        self.board = self.create_board()

    def create_board(self):
        rows, cols = self.BOARD_SIZE
        board = [[random.choice(self.ICONS) for _ in range(cols)] for _ in range(rows)]
        return board

    def is_valid_move(self, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2

        rows, cols = self.BOARD_SIZE
        if not (0 <= x1 < rows and 0 <= y1 < cols and
                0 <= x2 < rows and 0 <= y2 < cols):
            return False

        if pos1 == pos2:
            return False

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
            rows, cols = self.BOARD_SIZE
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < rows and 0 <= ny < cols:
                    if (nx, ny) not in visited and self.board[nx][ny] == self.board[x][y]:
                        stack.append((nx, ny))

        return False

    def remove_icons(self, pos1, pos2):
        self.board[pos1[0]][pos1[1]] = ' '
        self.board[pos2[0]][pos2[1]] = ' '

    def is_game_over(self):
        for row in self.board:
            for cell in row:
                if cell != ' ':
                    return False
        return True