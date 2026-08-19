from collections import deque


class EightPuzzle:
    # const member in C++; class-level constant, never mutated
    goalState = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    def __init__(self, initial_state=None):
        # maps both ctors: EightPuzzle() -> initialState = {}
        if initial_state is None:
            initial_state = []
        self.initialState = initial_state

    def find_blank(self, state):
        for i in range(3):
            for j in range(3):
                if state[i][j] == 0:
                    return (i, j)
        return (-1, -1)

    def move(self, state, direction):
        i, j = self.find_blank(state)
        new_state = [row[:] for row in state]  # value-copy like C++ vector copy

        if direction == "up" and i > 0:
            new_state[i][j], new_state[i - 1][j] = new_state[i - 1][j], new_state[i][j]
        elif direction == "down" and i < 2:
            new_state[i][j], new_state[i + 1][j] = new_state[i + 1][j], new_state[i][j]
        elif direction == "left" and j > 0:
            new_state[i][j], new_state[i][j - 1] = new_state[i][j - 1], new_state[i][j]
        elif direction == "right" and j < 2:
            new_state[i][j], new_state[i][j + 1] = new_state[i][j + 1], new_state[i][j]

        return new_state

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
        open_list = deque()
        closed_list = []

        open_list.append((self.initialState, []))

        while open_list:
            current_state, path = open_list.popleft()
            closed_list.append(current_state)

            if current_state == self.goalState:
                return path

            for mv in self.get_possible_moves(current_state):
                new_state = self.move(current_state, mv)
                # note: membership checked only against closedList (popped states),
                # matching C++ semantics (no visited-check at enqueue time)
                if new_state not in closed_list:
                    new_path = list(path)
                    new_path.append(mv)
                    open_list.append((new_state, new_path))

        return []

    # C++ operator= cannot be overloaded in Python; `assign` mirrors it:
    # returns a new EightPuzzle built from initial_state (self is not mutated,
    # exactly like the C++ operator which returns by value)
    def assign(self, initial_state):
        return EightPuzzle(initial_state)