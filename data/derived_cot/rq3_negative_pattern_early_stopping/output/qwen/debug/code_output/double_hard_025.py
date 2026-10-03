class Solution:
    def minCost(self, A, K):
        n = len(A)
        dp = [float('inf')] * (n+1)
        dp[0] = 0
        
        for i in range(1, n+1):
            freq = {}
            distinct = 0
            for j in range(i-1, -1, -1):
                # Update frequency for A[j]
                if A[j] in freq:
                    freq[A[j]] += 1
                else:
                    freq[A[j]] = 1
                    distinct += 1
                # The cost for the segment from j to i-1 is distinct
                dp[i] = min(dp[i], dp[j] + distinct)
        return dp[n]
