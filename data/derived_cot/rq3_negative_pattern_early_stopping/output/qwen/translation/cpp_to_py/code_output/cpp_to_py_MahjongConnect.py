import random


class MahjongConnect:
    def __init__(self, board_size, icons):
        self.BOARD_SIZE = board_size  # (rows, columns)
        self.ICONS = icons  # list of characters
        self.board = self.create_board()

    def create_board(self):
        rows, cols = self.BOARD_SIZE
        board = [['' for _ in range(cols)] for _ in range(rows)]
        for i in range(rows):
            for j in range(cols):
                if self.ICONS:
                    board[i][j] = random.choice(self.ICONS)
                else:
                    board[i][j] = ' '
        return board

    def is_valid_move(self, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        
        if not (0 <= x1 < self.BOARD_SIZE[0] and 0 <= y1 < self.BOARD_SIZE[1] and
                0 <= x2 < self.BOARD_SIZE[0] and 0 <= y2 < self.BOARD_SIZE[1]):
            return False
        
        if pos1 == pos2:
            return False
        
        if self.board[x1][y1] != self.board[x2][y2]:
            return False
        
        return self.has_path(pos1, pos2)

    def has_path(self, pos1, pos2):
        start = pos1
        target = pos2
        
        visited = set()
        stack = [start]
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        while stack:
            current = stack.pop()
            if current == target:
                return True
            if current in visited:
                continue
            visited.add(current)
            x, y = current
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if (0 <= nx < self.BOARD_SIZE[0] and 0 <= ny < self.BOARD_SIZE[1] and
                        (nx, ny) not in visited and self.board[nx][ny] == self.board[x][y]):
                    stack.append((nx, ny))
        return False

    def remove_icons(self, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        self.board[x1][y1] = ' '
        self.board[x2][y2] = ' '

    def is_game_over(self):
        for row in self.board:
            if any(cell != ' ' for cell in row):
                return False
        return True