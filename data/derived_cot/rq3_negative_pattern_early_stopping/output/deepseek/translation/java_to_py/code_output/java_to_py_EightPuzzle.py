import collections

class EightPuzzle:
    def __init__(self, initialState):
        self.initialState = self.deepCopy(initialState)
        self.goalState = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    def findBlank(self, state):
        for i in range(3):
            for j in range(3):
                if state[i][j] == 0:
                    return [i, j]
        return None

    def move(self, state, direction):
        blank = self.findBlank(state)
        i, j = blank[0], blank[1]
        newState = self.deepCopy(state)

        if direction == "up":
            if i > 0:
                newState[i][j] = newState[i - 1][j]
                newState[i - 1][j] = 0
        elif direction == "down":
            if i < 2:
                newState[i][j] = newState[i + 1][j]
                newState[i + 1][j] = 0
        elif direction == "left":
            if j > 0:
                newState[i][j] = newState[i][j - 1]
                newState[i][j - 1] = 0
        elif direction == "right":
            if j < 2:
                newState[i][j] = newState[i][j + 1]
                newState[i][j + 1] = 0
        return newState

    def getPossibleMoves(self, state):
        moves = []
        blank = self.findBlank(state)
        i, j = blank[0], blank[1]

        if i > 0:
            moves.append("up")
        if i < 2:
            moves.append("down")
        if j > 0:
            moves.append("left")
        if j < 2:
            moves.append("right")

        return moves

    def solve(self):
        openList = collections.deque()
        closedList = set()
        openList.append(self.Node(self.initialState, []))

        while openList:
            currentNode = openList.popleft()
            currentState = currentNode.state
            path = currentNode.path
            closedList.add(self.stateToString(currentState))

            if currentState == self.goalState:
                return path

            for direction in self.getPossibleMoves(currentState):
                newState = self.move(currentState, direction)
                if self.stateToString(newState) not in closedList:
                    newPath = path + [direction]
                    openList.append(self.Node(newState, newPath))

        return None

    def stateToString(self, state):
        return ''.join(str(val) for row in state for val in row)

    def deepCopy(self, original):
        return [row[:] for row in original]

    class Node:
        def __init__(self, state, path):
            self.state = state
            self.path = path