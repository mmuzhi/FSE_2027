class PushBoxGame:
    def __init__(self, map):
        self.map = [row[:] for row in map]
        self.playerRow = 0
        self.playerCol = 0
        self.targets = []
        self.boxes = []
        self.targetCount = 0
        self._isGameOver = False
        self._initGame()

    def _initGame(self):
        for row in range(len(self.map)):
            for col in range(len(self.map[row])):
                if self.map[row][col] == 'O':
                    self.playerRow = row
                    self.playerCol = col
                elif self.map[row][col] == 'G':
                    self.targets.append([row, col])
                    self.targetCount += 1
                elif self.map[row][col] == 'X':
                    self.boxes.append([row, col])

    def checkWin(self):
        boxOnTargetCount = 0
        for box in self.boxes:
            for target in self.targets:
                if box == target:
                    boxOnTargetCount += 1
        self._isGameOver = (boxOnTargetCount == self.targetCount)
        return self._isGameOver

    def move(self, direction):
        newPlayerRow = self.playerRow
        newPlayerCol = self.playerCol

        if direction == 'w':
            newPlayerRow -= 1
        elif direction == 's':
            newPlayerRow += 1
        elif direction == 'a':
            newPlayerCol -= 1
        elif direction == 'd':
            newPlayerCol += 1

        if self._isValidMove(newPlayerRow, newPlayerCol):
            if self._isBoxAt(newPlayerRow, newPlayerCol):
                boxPosition = self._getBoxPosition(newPlayerRow, newPlayerCol)
                newBoxRow = newPlayerRow + (newPlayerRow - self.playerRow)
                newBoxCol = newPlayerCol + (newPlayerCol - self.playerCol)

                if self._isValidMove(newBoxRow, newBoxCol) and not self._isBoxAt(newBoxRow, newBoxCol):
                    self._moveBox(boxPosition, newBoxRow, newBoxCol)
                    self.playerRow = newPlayerRow
                    self.playerCol = newPlayerCol
            else:
                self.playerRow = newPlayerRow
                self.playerCol = newPlayerCol

        return self.checkWin()

    def _isValidMove(self, row, col):
        return 0 <= row < len(self.map) and 0 <= col < len(self.map[row]) and self.map[row][col] != '#'

    def _isBoxAt(self, row, col):
        for box in self.boxes:
            if box == [row, col]:
                return True
        return False

    def _getBoxPosition(self, row, col):
        for box in self.boxes:
            if box == [row, col]:
                return box
        return None

    def _moveBox(self, boxPosition, newRow, newCol):
        for i in range(len(self.boxes)):
            if self.boxes[i] == boxPosition:
                self.boxes[i] = [newRow, newCol]
                break

    def isGameOver(self):
        return self._isGameOver

    def getPlayerCol(self):
        return self.playerCol

    def getPlayerRow(self):
        return self.playerRow

    def getTargets(self):
        return list(self.targets)

    def getTargetCount(self):
        return self.targetCount

    def getMap(self):
        return self.map

    def getBoxes(self):
        return list(self.boxes)