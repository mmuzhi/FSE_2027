from collections import deque

class EightPuzzle:
    def __init__(self, initial_state=None):
        if initial_state is None:
            self.initialState = [[0] * 3 for _ in range(3)]
        else:
            self.initialState = initial_state

    goal_state = ((1, 2, 3), (4, 5, 6), (7, 8, 0))
    
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
            new_state[i][j], new_state[i-1][j] = new_state[i-1][j], new_state[i][j]
        elif direction == "down" and i < 2:
            new_state[i][j], new_state[i+1][j] = new_state[i+1][j], new_state[i][j]
        elif direction == "left" and j > 0:
            new_state[i][j], new_state[i][j-1] = new_state[i][j-1], new_state[i][j]
        elif direction == "right" and j < 2:
            new_state[i][j], new_state[i][j+1] = new_state[i][j+1], new_state[i][j]
        
        return new_state

    def get_possible_moves(self, state):
        i, j = self.find_blank(state)
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
        if self.initialState == EightPuzzle.goal_state:
            return []
        
        openList = deque()
        openList.append((self.initialState, []))
        closedSet = set()
        
        while openList:
            state, path = openList.popleft()
            state_tuple = tuple(tuple(row) for row in state)
            
            if state_tuple == EightPuzzle.goal_state:
                return path
                
            if state_tuple not in closedSet:
                closedSet.add(state_tuple)
                
                for move_str in self.get_possible_moves(state):
                    new_state = self.move(state, move_str)
                    openList.append((new_state, path + [move_str]))
                    
        return []
    
    @classmethod
    def from_state(cls, initial_state):
        return cls(initial_state)