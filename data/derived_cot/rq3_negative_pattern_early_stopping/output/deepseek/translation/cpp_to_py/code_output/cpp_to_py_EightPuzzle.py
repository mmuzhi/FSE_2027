from collections import deque

class EightPuzzle:
    _GOAL_STATE = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    def __init__(self, initial_state=None):
        """
        Constructor. If initial_state is None, sets an empty state (matching C++ default constructor).
        """
        if initial_state is None:
            self.initialState = []
        else:
            self.initialState = [row[:] for row in initial_state]

    def find_blank(self, state):
        """
        Return (row, col) of the blank tile (value 0) in the given state.
        If not found (e.g., empty state), returns (-1, -1).
        """
        for i in range(3):
            for j in range(3):
                if state[i][j] == 0:
                    return (i, j)
        return (-1, -1)

    def move(self, state, direction):
        """
        Return a new state after moving the blank tile in the given direction.
        If the move is illegal (boundary or direction not possible), returns a copy of the original state.
        (Behavior matches C++: it will still attempt the swap even if indices are out-of-range – 
         for an empty state this will cause an IndexError, exactly as C++ undefined behavior.)
        """
        i, j = self.find_blank(state)
        new_state = [row[:] for row in state]

        if direction == "up" and i > 0:
            new_state[i][j], new_state[i-1][j] = new_state[i-1][j], new_state[i][j]
        elif direction == "down" and i < 2:
            new_state[i][j], new_state[i+1][j] = new_state[i+1][j], new_state[i][j]
        elif direction == "left" and j > 0:
            new_state[i][j], new_state[i][j-1] = new_state[i][j-1], new_state[i][j]
        elif direction == "right" and j < 2:
            new_state[i][j], new_state[i][j+1] = new_state[i][j+1], new_state[i][j]

        return new_state

    def get_possible_moves(self, state):
        """
        Return list of possible moves for the blank tile in the current state.
        Order: up, down, left, right (when possible).
        """
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
        """
        BFS search from the initial state to the goal state.
        Returns a list of moves (strings) that lead to the goal, or an empty list if unsolvable.
        """
        open_list = deque()
        open_list.append((self.initialState, []))
        closed_list = []          # list of states (list of lists), linear lookup – matches C++

        while open_list:
            current_state, path = open_list.popleft()
            closed_list.append(current_state)

            if current_state == self._GOAL_STATE:
                return path

            for move_dir in self.get_possible_moves(current_state):
                new_state = self.move(current_state, move_dir)
                if new_state not in closed_list:
                    new_path = path + [move_dir]
                    open_list.append((new_state, new_path))

        return []   # no solution

    def assign(self, initial_state):
        """
        Emulates C++ operator= (which returns a new EightPuzzle object).
        Ignores the current instance and returns a new EightPuzzle built from initial_state.
        """
        return EightPuzzle(initial_state)