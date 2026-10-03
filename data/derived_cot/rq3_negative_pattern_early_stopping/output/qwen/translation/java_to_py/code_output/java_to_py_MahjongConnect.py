import random


class MahjongConnect:
    def __init__(self, BOARD_SIZE, ICONS):
        self.BOARD_SIZE = BOARD_SIZE
        self.ICONS = ICONS
        self.board = self.create_board()

    def create_board(self):
        rows, cols = self.BOARD_SIZE
        board = [[""] * cols for _ in range(rows)]
        icons_list = list(self.ICONS)
        for i in range(rows):
            for j in range(cols):
                board[i][j] = random.choice(icons_list)
        return board

    def is_valid_position(self, x, y):
        return 0 <= x < len(self.BOARD_SIZE) and 0 <= y < self.BOARD_SIZE[1]

    def is_valid_move(self, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        if not self.is_valid_position(x1, y1) or not self.is_valid_position(x2, y2):
            return False
        if x1 == x2 and y1 == y2:
            return False
        if self.board[x1][y1] != self.board[x2][y2]:
            return False
        visited = [[False] * self.BOARD_SIZE[1] for _ in range(self.BOARD_SIZE[0])]
        return self.dfs(x1, y1, x2, y2, visited)

    def dfs(self, x, y, target_x, target_y, visited):
        if x == target_x and y == target_y:
            return True
        if visited[x][y]:
            return False
        visited[x][y] = True
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if self.is_valid_position(nx, ny) and not visited[nx][ny] and self.board[nx][ny] == self.board[x][y]:
                if self.dfs(nx, ny, target_x, target_y, visited):
                    return True
        return False

    def remove_icons(self, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        self.board[x1][y1] = " "
        self.board[x2][y2] = " "

    def is_game_over(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] != " ":
                    return False
        return True


def main():
    board_size = [4, 4]
    icons = ["a", "b", "c"]
    mc = MahjongConnect(board_size, icons)
    print(mc.is_valid_move([0, 0], [1, 0]))
    mc.remove_icons([0, 0], [1, 0])
    print(mc.is_game_over())


if __name__ == "__main__":
    main()