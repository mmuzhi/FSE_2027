from collections import deque

class EightPuzzle:
    def __init__(self, initial_state=None):
        self.goalState = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        if initial_state is None:
            self.initialState = []
        else:
            self.initialState = [row[:] for row in initial_state]

    def find_blank(self, state):
        for i in range(3):
            for j in range(3):
                if state[i][j] == 0:
                    return (i, j)
        return (-1, -1)

    def move(self, state, direction):
        i, j = self.find_blank(state)
        newState = [row[:] for row in state]

        if i == -1 or j == -1:
            return newState

        if direction == "up" and i > 0:
            newState[i][j], newState[i - 1][j] = newState[i - 1][j], newState[i][j]
        elif direction == "down" and i < 2:
            newState[i][j], newState[i + 1][j] = newState[i + 1][j], newState[i][j]
        elif direction == "left" and j > 0:
            newState[i][j], newState[i][j - 1] = newState[i][j - 1], newState[i][j]
        elif direction == "right" and j < 2:
            newState[i][j], newState[i][j + 1] = newState[i][j + 1], newState[i][j]

        return newState

    def get_possible_moves(self, state):
        moves = []
        i, j = self.find_blank(state)

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
        openList = deque()
        openList.append((self.initialState, []))
        closedList = []

        while openList:
            currentState, path = openList.popleft()
            closedList.append(currentState)

            if currentState == self.goalState:
                return path

            for move in self.get_possible_moves(currentState):
                newState = self.move(currentState, move)
                if newState not in closedList:
                    newPath = path + [move]
                    openList.append((newState, newPath))

        return []

    def assign(self, initial_state):
        return EightPuzzle(initial_state)