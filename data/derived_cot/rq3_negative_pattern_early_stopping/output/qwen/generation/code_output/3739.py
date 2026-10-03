class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        T = m * n
        mod = 10**9 + 7
        
        # Precompute factorials and inverse factorials up to T (which is <= 10^5)
        max_n = T
        fact = [1] * (max_n + 1)
        inv_fact = [1] * (max_n + 1)
        
        for i in range(1, max_n + 1):
            fact[i] = fact[i-1] * i % mod
        
        inv_fact[max_n] = pow(fact[max_n], mod-2, mod)
        for i in range(max_n, 0, -1):
            inv_fact[i-1] = inv_fact[i] * i % mod
        
        def nCr(n, r):
            if r < 0 or r > n:
                return 0
            return fact[n] * inv_fact[r] % mod * inv_fact[n - r] % mod
        
        # Function to compute the sum of absolute differences for a set of numbers (here, row indices) over all combinations of k elements from the set {0, 1, ..., m-1} (with repetition allowed? Actually, we are choosing k cells from T cells, but the row indices are from 0 to m-1, and each row index can be chosen multiple times (if there are multiple columns in that row). But wait, the grid has m rows and n columns. The row indices are from 0 to m-1, and each row index appears n times (once for each column). 

        # Actually, we need to consider the entire grid as T = m*n cells. But the row part: the row indices are from 0 to m-1, and each row index has n cells. Similarly for columns.

        # However, the problem is separable. We can compute the row part and column part independently.

        # For the row part: we have m rows, each row has n cells. We are choosing k cells from T = m*n cells. The row part of the Manhattan distance is the sum of |row_i - row_j| for all pairs in the chosen k cells.

        # We can think of the entire grid as having m rows, and each row has n copies (the columns). But actually, the row index of a cell is fixed (the row number). 

        # Alternatively, we can use linearity of expectation or combinatorial identities.

        # There's a known way to compute the sum of absolute differences for a set of numbers. But here, we are choosing k numbers from a multiset (each row index from 0 to m-1 appears n times). 

        # Actually, we can use the idea of "contribution technique": for each pair of row indices (i, j) (with i < j), count the number of arrangements in which both row i and row j are chosen, and then multiply by (j - i) (the absolute difference) and then sum over all pairs.

        # But note: the arrangement is a set of k distinct cells. The row indices can be repeated only if we choose two cells from the same row. But the Manhattan distance for two cells in the same row is 0. 

        # Actually, the Manhattan distance between two cells is |row_i - row_j| + |col_i - col_j|. For the row part, if two cells are in the same row, then |row_i - row_j| = 0. 

        # So, for the row part, we need to consider pairs of cells that are in different rows. 

        # Let me define:
        # Let R be the set of row indices (0 to m-1). Each row index i has n cells (columns). 

        # The total number of ways to choose k cells is C(T, k).

        # Now, for a fixed pair of rows (i, j) (i < j), the number of ways to choose two cells, one from row i and one from row j, and then choose the remaining k-2 cells from the other T - n - n cells (since we've used one cell from row i and one from row j). But wait, actually, we are choosing k cells, and we want to count the arrangements that include at least one cell from row i and one from row j. But actually, we want to count the arrangements that include at least one cell from row i and one from row j, and then the contribution of the pair (i, j) is (j - i) multiplied by the number of ways to choose the remaining k-2 cells from the rest, but also considering that we might have more than one cell from row i or j? 

        # Actually, the Manhattan distance is between every pair