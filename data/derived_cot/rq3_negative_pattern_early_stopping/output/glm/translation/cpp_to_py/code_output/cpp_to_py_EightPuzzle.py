from collections import deque
from typing import List, Tuple, Optional

class EightPuzzle:
    goalState = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    def __init__(self, initial_state: Optional[List[List[int]]] = None):
        if initial_state is None:
            self.initialState = []
        else:
            self.initialState = [row[:] for row in initial_state]

    def find_blank(self, state: List[List[int]]) -> Tuple[int, int]:
        for i in range(3):
            for j in range(3):
                if state[i][j] == 0:
                    return (i, j)
        return (-1, -1)

    def move(self, state: List[List[int]], direction: str) -> List[List[int]]:
        i, j = self.find_blank(state)
        newState = [row[:] for row in state]

        if direction == "up" and i > 0:
            newState[i][j], newState[i - 1][j] = newState[i - 1][j], newState[i][j]
        elif direction == "down" and i < 2:
            newState[i][j], newState[i + 1][j] = newState[i + 1][j], newState[i][j]
        elif direction == "left" and j > 0:
            newState[i][j], newState[i][j - 1] = newState[i][j - 1], newState[i][j]
        elif direction == "right" and j < 2:
            newState[i][j], newState[i][j + 1] = newState[i][j + 1], newState[i][j]

        return newState

    def get_possible_moves(self, state: List[List[int]]) -> List[str]:
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

    def solve(self) -> List[str]:
        openList = deque()
        closedList = []

        openList.append((self.initialState, []))

        while openList:
            currentState, path = openList.popleft()
            closedList.append(currentState)

            if currentState == self.goalState:
                return path

            for move_dir in self.get_possible_moves(currentState):
                newState = self.move(currentState, move_dir)
                if newState not in closedList:
                    newPath = path + [move_dir]
                    openList.append((newState, newPath))

        return []

    def operator_assign(self, initial_state: List[List[int]]) -> 'EightPuzzle':
        return EightPuzzle(initial_state)