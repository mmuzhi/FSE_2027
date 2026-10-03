from collections import deque
import copy

class EightPuzzle:
    def __init__(self, initialState):
        self.initial_state = copy.deepcopy(initialState)
        self.goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    def find_blank(self, state):
        for i in range(3):
            for j in range(3):
                if state[i][j] == 0:
                    return [i, j]
        return None

    def move(self, state, direction):
        blank = self.find_blank(state)
        if blank is None:
            return None
        i, j = blank
        new_state = [row[:] for row in state]
        
        if direction == "up" and i > 0:
            new_state[i][j] = new_state[i-1][j]
            new_state[i-1][j] = 0
        elif direction == "down" and i < 2:
            new_state[i][j] = new_state[i+1][j]
            new_state[i+1][j] = 0
        elif direction == "left" and j > 0:
            new_state[i][j] = new_state[i][j-1]
            new_state[i][j-1] = 0
        elif direction == "right" and j < 2:
            new_state[i][j] = new_state[i][j+1]
            new_state[i][j+1] = 0
        else:
            return None
        
        return new_state

    def get_possible_moves(self, state):
        blank = self.find_blank(state)
        if blank is None:
            return []
        i, j = blank
        moves = []
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
        start_node = Node(self.initial_state, [])
        open_list = deque([start_node])
        closed_set = set()
        
        while open_list:
            current_node = open_list.popleft()
            current_state = current_node.state
            path = current_node.path
            
            state_str = self.state_to_string(current_state)
            if state_str in closed_set:
                continue
            closed_set.add(state_str)
            
            if self.state_to_string(current_state) == self.state_to_string(self.goal_state):
                return path
            
            for move in self.get_possible_moves(current_state):
                next_state = self.move(current_state, move)
                if next_state is None:
                    continue
                next_state_str = self.state_to_string(next_state)
                if next_state_str not in closed_set:
                    new_path = path + [move]
                    open_list.append(Node(next_state, new_path))
        
        return None

    @staticmethod
    def state_to_string(state):
        return ''.join(str(num) for row in state for num in row)

class Node:
    def __init__(self, state, path):
        self.state = state
        self.path = path
        
    def __eq__(self, other):
        return self.state == other.state
    
    def __hash__(self):
        return hash(str(self.state))