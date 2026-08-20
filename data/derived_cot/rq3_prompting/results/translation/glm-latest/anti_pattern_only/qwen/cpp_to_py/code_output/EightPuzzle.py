from collections import deque
from typing import List, Optional, Tuple

# NOTE: The C++ `EightPuzzle::operator=` (assignment from a state matrix) has no
# Python counterpart, since assignment cannot be overloaded in Python; it is
# therefore omitted (the C++ version did not even mutate `this`, it merely
# returned a new EightPuzzle by value).


class EightPuzzle:
    def __init__(self, initial_state: Optional[List[List[int]]] = None) -> None:
        # Mirrors the two C++ constructors:
        #   EightPuzzle()              -> empty initial state
        #   EightPuzzle(initial_state) -> stores a copy of initial_state
        if initial_state is None:
            self.initialState: List[List[int]] = []
        else:
            self.initialState = [list(row) for row in initial_state]
        self.goalState: List[List[int]] = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    def find_blank(self, state: List[List[int]]) -> Tuple[int, int]:
        for i in range(3):
            for j in range(3):
                if state[i][j] == 0:
                    return (i, j)
        return (-1, -1)

    def move(self, state: List[List[int]], direction: str) -> List[List[int]]:
        i, j = self.find_blank(state)
        new_state = [list(row) for row in state]

        if direction == "up" and i > 0:
            new_state[i][j], new_state[i - 1][j] = new_state[i - 1][j], new_state[i][j]
        elif direction == "down" and i < 2:
            new_state[i][j], new_state[i + 1][j] = new_state[i + 1][j], new_state[i][j]
        elif direction == "left" and j > 0:
            new_state[i][j], new_state[i][j - 1] = new_state[i][j - 1], new_state[i][j]
        elif direction == "right" and j < 2:
            new_state[i][j], new_state[i][j + 1] = new_state[i][j + 1], new_state[i][j]

        return new_state

    def get_possible_moves(self, state: List[List[int]]) -> List[str]:
        moves: List[str] = []
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
        open_list = deque()  # FIFO queue of (state, path) pairs
        closed_list: List[List[List[int]]] = []

        open_list.append((self.initialState, []))

        while open_list:
            current_state, path = open_list.popleft()
            closed_list.append(current_state)

            if current_state == self.goalState:
                return path

            for move in self.get_possible_moves(current_state):
                new_state = self.move(current_state, move)
                if new_state not in closed_list:
                    open_list.append((new_state, path + [move]))

        return []