class Solution:
    def totalNQueens(self, n: int) -> int:
        def addans(board, ans):
            temp = []
            for row in board:
                for j in range(len(row)):
                    if row[j] == "Q":
                        temp.append(j + 1)
            ans.append(temp)
        
        def solve(col, board, col_used, upper_used, lower_used, ans, n):
            if col == n:
                addans(board, ans)
                return
            for row in range(n):
                if col_used[col] == 0 and upper_used[n - 1 + col - row] == 0 and lower_used[row + col] == 0:
                    board[row][col] = "Q"
                    col_used[col] = 1
                    upper_used[n - 1 + col - row] = 1
                    lower_used[row + col] = 1
                    solve(col + 1, board, col_used, upper_used, lower_used, ans, n)
                    col_used[col] = 0
                    upper_used[n - 1 + col - row] = 0
                    lower_used[row + col] = 0
        
        ans = []
        board = [[0] * n for _ in range(n)]
        col_used = [0] * n
        upper_used = [0] * (2 * n - 1)
        lower_used = [0] * (2 * n - 1)
        solve(0, board, col_used, upper_used, lower_used, ans, n)
        return len(ans)