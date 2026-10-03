class Solution:
    def minMaxSums(self, nums: List[int], k: int) -> int:
        nums.sort()
        n = len(nums)
        mod = 10**9 + 7
        
        # Precompute combinations up to n (which is 10^5) but k is at most 70, so we can compute binomial coefficients for numbers up to 10^5 and for k up to 70.
        # But note: for each i, we need to compute C(i, j) for j from 0 to min(i, k-1) and C(n-i-1, j) for j from 0 to min(n-i-1, k-1). 
        # Since k is at most 70, we can precompute a Pascal triangle for rows up to n (which is 10^5) but that's too big. Alternatively, we can use a loop for each i and compute the binomial coefficients using a formula, but that might be O(n*k) which is 10^5 * 70 = 7e6, which is acceptable in Python.

        # Alternatively, we can precompute a list of binomial coefficients for each row up to n, but that would require a 2D array of size n x (k+1) which is 10^5 * 71 ~ 7.1e6 integers, which is acceptable in C++ but in Python might be heavy in memory? But we can compute on the fly.

        # But note: we need to compute for each i, the sum of binomial coefficients for row i (for maximum) and row n-i-1 (for minimum) from j=0 to min(i, k-1) and j=0 to min(n-i-1, k-1) respectively.

        # We can precompute a 2D DP for binomial coefficients for rows from 0 to n, but only for columns 0 to k (since k is small). 

        # Let's create a 2D list dp where dp[i][j] = C(i, j) for j from 0 to min(i, k) (we only need j up to k-1, so k). But note: i can be up to 10^5, but k is 70, so we can compute for each row i, the binomial coefficients for j from 0 to k.

        # We can use dynamic programming for binomial coefficients with a 1D array and update for each row. But since k is small, we can compute each row using a simple loop and the formula: C(i, j) = C(i-1, j-1) + C(i-1, j). But we need to compute for i from 0 to n (10^5) and j from 0 to k.

        # Alternatively, we can use a 1D array and update for each i from 0 to n, but that would be O(n*k) which is 7e6, acceptable.

        # Steps:
        # 1. Precompute a 2D list of binomial coefficients for n+1 rows (0 to n) and k+1 columns (0 to k). But n is 10^5, so we need a list of 10^5+1 rows, each with k+1 elements. That's about 7.1e6 integers, which is acceptable in C++ but in Python might use a lot of memory (about 50 MB? 7.1e6 * 4 bytes = 28.4 MB, which is acceptable).

        # But we can also compute on the fly for each i without storing the entire table. But then we have to compute for each i the binomial coefficients for j from 0 to min(i, k). 

        # Alternatively, we can use a different approach: for each i, we can compute the binomial coefficients for row i (for j from 0 to min(i, k)) using a loop and the multiplicative formula. But that would be O(k) per i, so total O(n*k) = 7e6, which is acceptable.

        # However, we need two sets: for each i, we need the sum of binomial coefficients for row i (for maximum) and for row n-i-1 (for minimum). 

        # Let me define a function to compute the binomial coefficient C(n, k) for n up to 10^5 and k up to 70. We can use iterative computation for each row.

        # But note: we need to compute for each i from 0 to n, the binomial coefficients for j from 0 to min(i, k). 

        # Actually, we can precompute a 2D array for binom