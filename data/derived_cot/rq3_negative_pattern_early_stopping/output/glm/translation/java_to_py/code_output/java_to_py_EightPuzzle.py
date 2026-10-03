from collections import deque
from typing import List, Optional

class EightPuzzle:
    def __init__(self, initial_state: List[List[int]]):
        self.initial_state = self._deep_copy(initial_state)
        self.goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    def find_blank(self, state: List[List[int]]) -> Optional[List[int]]:
        for i in range(3):
            for j in range(3):
                if state[i][j] == 0:
                    return [i, j]
        return None

    def move(self, state: List[List[int]], direction: str) -> List[List[int]]:
        blank = self.find_blank(state)
        i, j = blank[0], blank[1]
        new_state = self._deep_copy(state)

        if direction == "up":
            if i > 0:
                new_state[i][j] = new_state[i - 1][j]
                new_state[i - 1][j] = 0
        elif direction == "down":
            if i < 2:
                new_state[i][j] = new_state[i + 1][j]
                new_state[i + 1][j] = 0
        elif direction == "left":
            if j > 0:
                new_state[i][j] = new_state[i][j - 1]
                new_state[i][j - 1] = 0
        elif direction == "right":
            if j < 2:
                new_state[i][j] = new_state[i][j + 1]
                new_state[i][j + 1] = 0

        return new_state

    def get_possible_moves(self, state: List[List[int]]) -> List[str]:
        moves = []
        blank = self.find_blank(state)
        i, j = blank[0], blank[1]

        if i > 0: moves.append("up")
        if i < 2: moves.append("down")
        if j > 0: moves.append("left")
        if j < 2: moves.append("right")

        return moves

    def solve(self) -> Optional[List[str]]:
        open_list = deque()
        closed_list = set()
        open_list.append(self.Node(self.initial_state, []))

        while open_list:
            current_node = open_list.popleft()
            current_state = current_node.state
            path = current_node.path
            closed_list.add(self._state_to_string(current_state))

            if current_state == self.goal_state:
                return path

            for move_dir in self.get_possible_moves(current_state):
                new_state = self.move(current_state, move_dir)
                if self._state_to_string(new_state) not in closed_list:
                    new_path = list(path)
                    new_path.append(move_dir)
                    open_list.append(self.Node(new_state, new_path))

        return None

    def _state_to_string(self, state: List[List[int]]) -> str:
        return "".join(str(val) for row in state for val in row)

    def _deep_copy(self, original: List[List[int]]) -> List[List[int]]:
        return [row[:] for row in original]

    class Node:
        def __init__(self, state: List[List[int]], path: List[str]):
            self.state = state
            self.path = path