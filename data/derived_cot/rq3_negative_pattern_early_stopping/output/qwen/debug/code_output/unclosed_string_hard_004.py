class Solution:
    def totalNQueens(self, n: int) -> int:
        def addans(board, ans):
            temp = []
            for row in board:
                for j in range(len(row)):
                    if row[j] == 'Q':
                        temp.append(j+1)
            ans.append(temp)
        
        def solve(col, board, low, upper, lower, ans):
            if col == n:
                addans(board, ans)
                return
            for row in range(n):
                if low[col] == 0 and upper[row - col + n - 1] == 0 and lower[row + col] == 0:
                    board[row][col] = 'Q'
                    low[col] = 1
                    upper[row - col + n - 1] = 1
                    lower[row + col] = 1
                    solve(col+1, board, low, upper, lower, ans)
                    board[row][col] = 0
                    low[col] = 0
                    upper[row - col + n - 1] = 0
                    lower[row + col] = 0
        
        ans = []
        board = [[0] * n for _ in range(n)]
        low = [0] * n
        upper = [0] * (2 * n - 1)
        lower = [0] * (2 * n - 1)
        solve(0, board, low, upper, lower, ans)
        return len(ans)
