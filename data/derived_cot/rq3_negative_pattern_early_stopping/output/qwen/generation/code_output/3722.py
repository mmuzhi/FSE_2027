class Solution:
    def maxSum(self, nums: List[int], k: int, m: int) -> int:
        n = len(nums)
        pre = [0]*(n+1)
        for i in range(n):
            pre[i+1] = pre[i] + nums[i]
        
        # dp[j][i] = maximum sum for j segments with the j-th segment ending at i
        # We'll use dp[j] as a list of length n, and best[j] as the maximum dp[j] from 0 to i
        # But we can use two arrays: dp_prev and dp_curr for j-1 and j
        # We'll do for j from 1 to k
        
        # Initialize dp0: for 0 segments, the maximum sum is 0, but we don't use it for j=0.
        # Instead, we'll use best_prev[i] = 0 for all i (for j=0)
        # Then for j=1, we compute dp_curr[i] for each i
        
        # We'll use two arrays: best_prev and best_curr for the previous and current j
        # But we need to store dp_prev for each index to compute best_prev
        
        # Alternatively, we can use a 2D DP array, but that might be too memory heavy (k * n, k up to 666, n=2000 -> 1.332e6 states, which is acceptable in Python if we do it carefully)
        
        # Let dp[j][i] be the maximum sum for j segments with the j-th segment ending at i
        # We'll create a 2D array of size (k+1) x n, initialize with -10**18 (or a very small number)
        # dp[0][i] = 0 for all i? Actually, we don't use j=0 in the recurrence, but we need best_prev for j=0: best_prev[i] = 0 for all i (since 0 segments, sum 0)
        
        # But note: we are allowed to have 0 segments, but we need k segments. So we'll compute from j=1 to j=k.
        
        # We'll use dp[j][i] = maximum sum for j segments with the j-th segment ending at i
        # Then, for each j from 1 to k, and for each i from 0 to n-1:
        #   dp[j][i] = max_{s from 0 to i-m+1} [ (pre[i+1]-pre[s]) + (best_prev[s-1] if s-1>=0 else 0) ]
        #   where best_prev[s-1] is the maximum value of dp[j-1][x] for x from 0 to s-1 (if j-1==0, then best_prev[s-1] is 0)
        
        # But we need to compute best_prev for j-1 as we go.
        
        # We can do:
        #   dp = [[-10**18]*n for _ in range(k+1)]
        #   best_prev = [0]*(n)  # for j=0, best_prev[i] = 0 for all i (but we don't use j=0 in the recurrence for j>=1, so we can set best_prev as the best for j-1)
        #   Actually, we'll do for j from 1 to k:
        #       best_prev = [0]*(n)  # for j-1=0, best_prev[i] = 0 for all i (since 0 segments, sum 0)
        #       Then for i from 0 to n-1:
        #           dp[j][i] = -10**18
        #           for s in range(0, i-m+2):  # s from 0 to i-m+1 (inclusive)
        #               # the segment is from s to i, length = i-s+1 >= m
        #               current_segment_sum = pre[i+1]-pre[s]
        #               prev_best = best_prev[s-1] if s-1>=0 else 0
        #               total = current_segment_sum + prev_best
        #               if total > dp[j][i]:
        #                   dp[j][i] = total
        #           # Then update best_prev[i] for j-1 (but wait, we are in j, so we need to update best_prev for j-1? Actually, we are using best_prev for j-1, so we need to compute best_prev for j-1 from dp[j-1]
        #       Then, after computing dp[j], we compute best_curr for j: best_curr[i] = max(best_prev[i