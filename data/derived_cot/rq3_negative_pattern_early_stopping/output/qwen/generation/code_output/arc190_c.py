import sys
sys.setrecursionlimit(300000)

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    it = iter(data)
    H = int(next(it)); W = int(next(it))
    A = []
    for _ in range(H):
        row = []
        for _ in range(W):
            row.append(int(next(it)) % MOD)
        A.append(row)
    
    # We are going to store the grid and the dp for each cell, but note: the grid has HW <= 200000, so we can store the entire grid.
    # But we need to update and recalc the dp for the entire grid after each update? That would be too slow.

    # However, note: the grid has at most 200000 cells, so we can store the grid as a 2D list, but the dp table is also 200000 cells.

    # But the problem requires Q up to 200000 updates. We cannot recalc the entire dp table (which is 200000 cells) for each update because 200000 * 200000 = 40e9 operations.

    # Alternative approach: use a Fenwick tree or segment tree for 2D range queries? But the operation is multiplicative and the recurrence is not additive.

    # Another idea: use the fact that the grid is a DAG and use dynamic programming with memoization, but updating one cell and then updating the entire grid from that cell is O(n) per update.

    # But note: the grid has 200000 cells, so the worst-case update is 200000 cells. And 200000 updates would be 40e9, which is acceptable in C++ but not in Python.

    # However, the problem constraints say HW <= 200000, and Q <= 200000. But the grid has 200000 cells, so the worst-case update is 200000 cells. 200000 * 200000 = 40e9, which is 40 billion operations. In Python, each operation is a multiplication and addition modulo MOD, which is a few cycles. But 40 billion operations might take minutes or hours in Python.

    # We need to optimize.

    # Let's try to find a better way.

    # Consider: the total sum for (H,W) is the product of the values along the path. We can use the idea of "generating function" for the entire grid.

    # Alternatively, we can use the concept of "path-independent" contributions. Each cell (i,j) has a fixed number of paths from (1,1) to (i,j) and from (i,j) to (H,W). But the product is multiplicative, so the contribution of a cell (i,j) is not linear.

    # But note: the total sum is the sum over all paths. We can break the path into two parts: from (1,1) to (i,j) and from (i,j) to (H,W). However, the product is the product of all cells, so the entire path is the product of the two parts.

    # Let F(i,j) = sum_{paths from (1,1) to (i,j)} (product of cells from (1,1) to (i,j))
    # Let G(i,j) = sum_{paths from (i,j) to (H,W)} (product of cells from (i,j) to (H,W))

    # Then the total sum for (H,W) is sum_{i,j} F(i,j) * G(i,j) / (A[i][j])? No, because the cell (i,j) is counted in both F and G, but in the entire path product, (i,j) is only once.

    # Actually, the entire path product is F(i,j) * (product of cells from (i,j) to (H,W) without the cell (i,j)) but wait, F(i,j) already includes A[i][j] if we define F(i,j) as the product up to (i,j). 

    # Let me redefine:

    # Let F(i,j) = sum_{paths from (1,1) to (i,j)} (product of cells from (1,1) to (i,j))
    # Then F(i,j) = (F(i-1,j) + F(i,j-1)) * A[i][j]   [if we define F(1,1)=A[1][1]]

    # Similarly,