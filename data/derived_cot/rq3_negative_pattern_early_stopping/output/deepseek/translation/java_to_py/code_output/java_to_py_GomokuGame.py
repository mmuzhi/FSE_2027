class GomokuGame:
    def __init__(self, boardSize):
        self.boardSize = boardSize
        self.board = [[' ' for _ in range(boardSize)] for _ in range(boardSize)]
        self.currentPlayer = 'X'

    def makeMove(self, row, col):
        if self.board[row][col] == ' ':
            self.board[row][col] = self.currentPlayer
            self.currentPlayer = 'O' if self.currentPlayer == 'X' else 'X'
            return True
        return False

    def checkWinner(self):
        directions = [[0, 1], [1, 0], [1, 1], [1, -1]]
        for row in range(self.boardSize):
            for col in range(self.boardSize):
                if self.board[row][col] != ' ':
                    for direction in directions:
                        if self.checkFiveInARow(row, col, direction):
                            return self.board[row][col]
        return None

    def checkFiveInARow(self, row, col, direction):
        dx, dy = direction
        count = 1
        symbol = self.board[row][col]
        for i in range(1, 5):
            newRow = row + dx * i
            newCol = col + dy * i
            if newRow < 0 or newRow >= self.boardSize or newCol < 0 or newCol >= self.boardSize:
                break
            if self.board[newRow][newCol] != symbol:
                break
            count += 1
        for i in range(1, 5):
            newRow = row - dx * i
            newCol = col - dy * i
            if newRow < 0 or newRow >= self.boardSize or newCol < 0 or newCol >= self.boardSize:
                break
            if self.board[newRow][newCol] != symbol:
                break
            count += 1
        return count >= 5

if __name__ == '__main__':
    gomokuGame = GomokuGame(10)
    moves = [[5, 5], [0, 0], [5, 4], [0, 1], [5, 3], [0, 2], [5, 2], [0, 3], [5, 1]]
    for move in moves:
        gomokuGame.makeMove(move[0], move[1])
    print(gomokuGame.checkWinner())