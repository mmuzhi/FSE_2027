import sys
sys.setrecursionlimit(10000)

MOD = 998244353

def main():
    data = sys.stdin.read().splitlines()
    if not data: 
        print(0)
        return
    H, W = map(int, data[0].split())
    grid = []
    for i in range(1, 1+H):
        grid.append(list(data[i].strip()))
    
    # If there are no '?' then we can check the condition.
    # But we'll use DP with state as the current row and the previous row's digits (for adjacent rows) and also the current row's digits.

    # However, note that adjacent also includes left and right. So we need to consider the entire grid.

    # We can use a DP that goes cell by cell (in row-major order) and the state is the current row and the previous row's cell (for up) and the left cell (for left). But then the state space is 3 * 3 for the current cell and the left cell and the above cell? Actually, we need to remember the entire row above and the current row so far? 

    # Alternatively, we can use iterative DP that goes row by row and for each row, we store the entire row's configuration. But the state space is 3^W for each row, and W can be up to 200, which is too big.

    # We need a better way.

    # Observation: the grid is at most 200 cells, but the constraint is H*W<=200. So the grid is small (at most 200 cells). We can use DFS with memoization that traverses the grid in a fixed order (like row-major) and the state is the current cell and the previous cell's digit (for the left neighbor) and the cell above's digit (for the above neighbor). But then the state space is 3 * 3 for the two neighbors and the current cell, but we have to remember the entire grid? Actually, we don't need the entire grid, but we need to know the digits of the left and above neighbors.

    # However, the grid has fixed digits and we are replacing '?'. We can do:

    # Let dp[i][j][a][b] = number of ways to fill the grid up to cell (i, j) such that the cell (i, j) is filled with digit d (we can use d as a variable) and the left neighbor (if exists) is d_left and the above neighbor (if exists) is d_above. But then we have to remember the entire grid? 

    # Alternatively, we can use a state that is the entire grid? But 200 cells and 3^200 is too big.

    # Another idea: use iterative DP that goes row by row and for each row, we store the entire row's configuration. But the state space is 3^W and W can be up to 200, which is 3^200 states, which is too big.

    # We need to use a smarter way.

    # Since the grid is small (<=200 cells) but the state space is too big for the entire grid, we can use a recursive DFS with memoization that uses the entire grid as state? But 3^200 is too big.

    # Alternatively, we can use a DP that goes cell by cell and the state is the current cell and the digits of the left and above neighbors. But then we have to remember the entire grid? Actually, we don't need the entire grid, but we need to know the digits of the left and above neighbors. However, the grid has fixed digits and we are replacing '?'. 

    # We can do:

    # Let dp[i][j][d] be the number of ways to fill the grid up to cell (i, j) such that the cell (i, j) is d, and the left neighbor (if exists) is set, and the above neighbor (if exists) is set. But then we have to check the condition with the left and above. But the left neighbor is the cell (i, j-1) and above is (i-1, j). 

    # However, the condition also requires that the current cell is different from the left and above. But the left and above are already set in the DP state? 

    # We can do:

    # dp[i][j][d] = 
    #   if grid[i][j] is not '?', then d must equal grid[i][j] (if it's a digit) or if it's '?' then d can be 1,2,3.
    #   Then, if j>0, then the left cell (i, j-1) must have