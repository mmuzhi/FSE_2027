class Solution:
    def maximumValueSum(self, board: List[List[int]]) -> int:
        m, n = len(board), len(board[0])
        ans = -10**18
        
        # We'll iterate over all possible placements of three rooks
        # But that is too slow, so we need a better approach
        
        # Alternative approach: use DP with state (row, col1, col2, col3) is too big.
        
        # Another idea: since we need three rooks, we can consider that the three rooks must be in three distinct rows and three distinct columns.
        # We can precompute for each row the top three values and their columns, but then we have to ensure columns are distinct.
        
        # But then, we can use a two-step: first, choose three rows, then choose three columns and assign the best values without conflict.
        # But the number of ways to choose three rows is C(m,3) and three columns is C(n,3), which is too many.
        
        # We need to use a different idea.
        
        # Let's consider: we need to choose three cells (i, j) such that all i are distinct and all j are distinct.
        # We can iterate over the columns and then for each column, we can record the best value from each row, but then we have to combine three columns.
        
        # Alternatively, we can use a DP that goes column by column and for each column, we choose one row (if not used) and update the state of used rows and the count of rooks placed.
        # But the state would be (col, mask) where mask is the set of rows used so far. The mask has m bits, which is 100, so 2^100 states, which is too big.
        
        # But note: we only need to place three rooks, so we can use a state that records the number of rooks placed and the rows used (but rows used are three at most). We can represent the state as (col, r1, r2, r3) but that is too big.
        
        # Another idea: use recursion with backtracking, but with pruning. Start by selecting a row and a column, then another, then another. But worst-case is still too big.
        
        # Let me think of a mathematical approach.
        # We need to maximize the sum of three values, each from a different row and different column.
        # This is similar to the assignment problem for a 3x3 submatrix, but we can choose any three rows and columns.
        
        # We can use the following: for each cell, we consider it as a candidate. Then, we need to pick two more cells from different rows and columns.
        # But then, we can use a two-pointer or something? Not really.
        
        # Alternatively, we can use a greedy approach: select the three largest values in the entire board, but then check if they are in distinct rows and columns. If not, then try to replace one of them with a value that is in a different row and column and gives a higher sum.
        # But that might not work because the three largest might be in the same row or column.
        
        # Another idea: use a priority queue to get the top k values (say k=100) and then try to form a set of three that are in distinct rows and columns. But the top k values might not form a valid set, and we have to consider all possibilities.
        
        # Given the complexity, perhaps the intended solution is to iterate over all possible triplets of cells that are in distinct rows and columns. But that is O(m^2 * n^2 * m^2) which is too slow.
        
        # Wait, actually, we can do the following: for each row, we can record the best value and its column. Then, for each pair of rows, we can consider the best two columns that are not used by the third row. But then we have to choose three rows and three columns.
        
        # Actually, we can use a three-level nested loop for rows and then for columns, but that is O(m^3 * n^3) which is 100^6 = 1e12, which is too slow in Python.
        
        # We need to optimize. Let's try to fix the columns first. For each column, we can record the best three values from different rows. Then, we need to choose three columns and three rows (each row from a different column) such that the sum is maximized.
        
        # But then, we have to ensure that the three rows are distinct. So, for three columns, we have three rows, and we need to check that the rows are distinct.
        
        # We can precompute for each column j, an array of