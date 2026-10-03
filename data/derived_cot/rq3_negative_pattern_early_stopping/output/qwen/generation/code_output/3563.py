class Solution:
    def maxScore(self, grid: List[List[int]]) -> int:
        rows = len(grid)
        cols = len(grid[0])
        # We'll collect for each row the minimum value that is unique? Or we can use a different approach.
        # Since grid is small, we can try to use DP with bitmask for rows and track the numbers chosen? But numbers can be up to 100, so that's too big.

        # Alternatively, we can consider that the maximum distinct numbers we can pick is at most the number of rows (or less). We can try to pick the largest numbers first.

        # Another idea: for each row, we can record the maximum value that hasn't been used. But we need to ensure distinctness.

        # We can use a greedy approach: sort the numbers in descending order and assign them to rows if they are available (i.e., the row has that number and we haven't used that number before). But we have to consider that a row can only contribute one number.

        # But note: we can choose any cell from a row, so for a row, we can choose the largest number that hasn't been chosen and is present in that row.

        # Steps:
        # 1. For each row, find the set of numbers present and their maximum value (or we can just note the maximum value in the row, but then we have to consider that the same maximum might be in multiple rows and we can only use it once).
        # 2. We want to assign distinct numbers to rows (each row gets one number, and the number must be present in that row) and maximize the sum.

        # But note: we don't have to use all rows. We can skip a row if we don't find a number that hasn't been used.

        # We can use a state-space search with rows and a set of used numbers. But the state space is 2^10 (for rows) and 2^100 for numbers — too big.

        # Alternatively, we can use a different approach: consider that the distinct numbers we choose must be a subset of the numbers in the grid. The maximum number of distinct numbers is at most 10 (since there are 10 rows). We can consider all numbers from 1 to 100, but only those that appear in the grid.

        # But 100 is too many to iterate over.

        # Another idea: since the grid is small (10x10), we can try to use recursion with memoization, but the state would be (row_index, used_numbers_set) — but the set can be up to 10 elements, and the numbers are from 1 to 100, so the state space is 10! * (number of distinct numbers) — which is too big.

        # Let me think simpler: we are allowed to choose at most one cell per row, and the numbers must be distinct. We want the maximum sum.

        # We can consider: for each row, we can choose a number (or skip). We want to maximize the sum with distinct numbers.

        # This is similar to a matching problem between rows and numbers (each row can be matched to a number that appears in that row, and each number can be matched only once). We want the maximum weight matching.

        # But the numbers are not fixed; we can choose any number from the row, but the same number cannot be chosen twice.

        # We can transform the problem: create a bipartite graph with rows on one side and numbers on the other. But the numbers are not fixed — we don't know which numbers to consider. But we can consider that the numbers are from 1 to 100, but only those that appear in the grid.

        # Steps for bipartite matching:
        # 1. Collect all distinct numbers that appear in the grid. But then, we have to consider that a row can only use a number if it appears in that row.
        # 2. Then, we want to assign each row to a number (each row can be assigned at most one number, and each number can be assigned at most once) and maximize the sum.

        # But the problem is that the same number might appear multiple times in the same row or different rows, but we can only use it once.

        # Actually, we can set up a bipartite graph where left nodes are rows (0 to rows-1) and right nodes are the distinct numbers (from 1 to 100, but only those that appear). Then, for each row i and each number x, if x is in grid[i], then we add an edge from row i to x with weight x.

        # Then, we want the maximum weight matching in this bipartite graph. But note: we are allowed to skip rows, so