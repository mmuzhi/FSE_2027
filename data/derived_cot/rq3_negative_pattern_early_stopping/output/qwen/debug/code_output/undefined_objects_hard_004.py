from collections import deque
from typing import List

class Solution:
    def slidingPuzzle(self, board: List[List[int]]) -> int:
        def get_neighbors(board):
            r, c = None, None
            for i in range(2):
                for j in range(3):
                    if board[i][j] == 0:
                        r, c = i, j
                        break
                if r is not None:
                    break
            
            neighbors = []
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < 2 and 0 <= nc < 3:
                    new_board = [row[:] for row in board]
                    new_board[r][c], new_board[nr][nc] = new_board[nr][nc], new_board[r][c]
                    neighbors.append(new_board)
            return neighbors
        
        queue = deque()
        queue.append((board, 0))
        seen = set()
        seen.add(tuple(tuple(row) for row in board))
        
        while queue:
            board, moves = queue.popleft()
            if board == [[1, 2, 3], [4, 5, 0]]:
                return moves
            for neighbor in get_neighbors(board):
                state = tuple(tuple(row) for row in neighbor)
                if state not in seen:
                    seen.add(state)
                    queue.append((neighbor, moves + 1))
        return -1