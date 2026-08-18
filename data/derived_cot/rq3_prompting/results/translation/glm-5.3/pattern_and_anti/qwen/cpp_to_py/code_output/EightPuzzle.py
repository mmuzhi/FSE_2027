from collections import deque


class EightPuzzle:
    GOAL_STATE = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    def __init__(self, initial_state=None):
        if initial_state is None:
            self._initial_state = []
        else:
            # C++ copies the nested vector by value; mirror that with row copies
            self._initial_state = [row[:] for row in initial_state]

    def find_blank(self, state):
        for i in range(3):
            for j in range(3):
                if state[i][j] == 0:
                    return (i, j)
        return (-1, -1)

    def move(self, state, direction):
        i, j = self.find_blank(state)
        new_state = [row[:] for row in state]

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

        open_list.append((self._initial_state, []))

        while open_list:
            current_state, path = open_list.popleft()
            closed_list.append(current_state)

            if current_state == self.GOAL_STATE:
                return path

            for mv in self.get_possible_moves(current_state):
                new_state = self.move(current_state, mv)
                if new_state not in closed_list:
                    new_path = list(path)
                    new_path.append(mv)
                    open_list.append((new_state, new_path))

        return []

    def assign(self, initial_state):
        # Maps C++ operator=: returns a new EightPuzzle; does not modify self
        return EightPuzzle(initial_state)