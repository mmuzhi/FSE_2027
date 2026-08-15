from typing import List
from collections import deque

class Solution:
    def slidingPuzzle(self, board: List[List[int]]) -> int:
        def get_neighbors(board):
            neighbors = []
            r, c = 0, 0
            for i in range(2):
                for j in range(3):
                    if board[i][j] == 0:
                        r, c = i, j

            for dr, dc in ((0, 1), (1, 0), (0, -1), (-1, 0)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < 2 and 0 <= nc < 3:
                    new_board = [row[:] for row in board]
                    new_board[r][c] = new_board[nr][nc]
                    new_board[nr][nc] = 0
                    neighbors.append(new_board)

            return neighbors

        queue = deque([(board, 0)])
        seen = {tuple(tuple(row) for row in board)}

        while queue:
            cur, moves = queue.popleft()

            if cur == [[1, 2, 3], [4, 5, 0]]:
                return moves

            for neighbor in get_neighbors(cur):
                state = tuple(tuple(row) for row in neighbor)
                if state not in seen:
                    seen.add(state)
                    queue.append((neighbor, moves + 1))

        return -1