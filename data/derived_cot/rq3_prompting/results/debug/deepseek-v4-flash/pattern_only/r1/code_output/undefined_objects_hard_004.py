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

            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                new_r, new_c = r + dr, c + dc
                if 0 <= new_r < 2 and 0 <= new_c < 3:
                    new_board = [row[:] for row in board]
                    new_board[r][c] = new_board[new_r][new_c]
                    new_board[new_r][new_c] = 0
                    neighbors.append(new_board)

            return neighbors

        queue = deque([(board, 0)])
        seen = {tuple(tuple(row) for row in board)}

        while queue:
            cur, moves = queue.popleft()

            if cur == [[1, 2, 3], [4, 5, 0]]:
                return moves

            for neighbor in get_neighbors(cur):
                key = tuple(tuple(row) for row in neighbor)
                if key not in seen:
                    seen.add(key)
                    queue.append((neighbor, moves + 1))

        return -1