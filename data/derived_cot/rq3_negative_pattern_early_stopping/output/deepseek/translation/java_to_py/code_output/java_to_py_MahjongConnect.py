import random

class MahjongConnect:
    def __init__(self, BOARD_SIZE, ICONS):
        self.BOARD_SIZE = BOARD_SIZE
        self.ICONS = ICONS
        self.board = self.createBoard()

    def createBoard(self):
        board = [[random.choice(self.ICONS) for _ in range(self.BOARD_SIZE[1])] for _ in range(self.BOARD_SIZE[0])]
        return board

    def isValidMove(self, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        if not self.isValidPosition(x1, y1) or not self.isValidPosition(x2, y2):
            return False
        if x1 == x2 and y1 == y2:
            return False
        if self.board[x1][y1] != self.board[x2][y2]:
            return False
        return self.hasPath(pos1, pos2)

    def isValidPosition(self, x, y):
        return 0 <= x < self.BOARD_SIZE[0] and 0 <= y < self.BOARD_SIZE[1]

    def hasPath(self, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        if not self.isValidPosition(x1, y1) or not self.isValidPosition(x2, y2):
            return False
        visited = [[False] * self.BOARD_SIZE[1] for _ in range(self.BOARD_SIZE[0])]
        return self.dfs(x1, y1, pos2, visited)

    def dfs(self, x, y, target, visited):
        if x == target[0] and y == target[1]:
            return True
        if visited[x][y]:
            return False
        visited[x][y] = True
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dx, dy in directions:
            newX, newY = x + dx, y + dy
            if self.isValidPosition(newX, newY) and not visited[newX][newY] and self.board[newX][newY] == self.board[x][y]:
                if self.dfs(newX, newY, target, visited):
                    return True
        return False

    def removeIcons(self, pos1, pos2):
        self.board[pos1[0]][pos1[1]] = " "
        self.board[pos2[0]][pos2[1]] = " "

    def isGameOver(self):
        for row in self.board:
            for cell in row:
                if cell != " ":
                    return False
        return True

if __name__ == "__main__":
    boardSize = [4, 4]
    icons = ["a", "b", "c"]
    mc = MahjongConnect(boardSize, icons)
    print(mc.isValidMove([0, 0], [1, 0]))
    mc.removeIcons([0, 0], [1, 0])
    print(mc.isGameOver())