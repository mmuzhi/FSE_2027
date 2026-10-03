class Solution:
    def numberOfGoodSubarraySplits(self, nums: List[int]) -> int:
        n = len(nums)
        # If the array is empty, return 0
        if n == 0:
            return 0
        
        # If there's no positive segment at all, return 0
        total = sum(nums)
        if total <= 0:
            return 0
        
        # dp[i] will be the number of ways to split the subarray starting at index i
        dp = [0] * (n+1)
        dp[n] = 1  # base case: empty array has 1 way
        
        # Precompute next[i] for each i: the smallest j>=i such that the sum from i to j is >=1
        next_index = [n] * (n+1)  # next_index[i] = smallest j>=i such that the sum from i to j>=1, or n if not found
        cur = 0
        # We'll use a two-pointer to compute next_index
        j = 0
        for i in range(n):
            # Reset for each i
            cur = 0
            for k in range(i, n):
                cur += nums[k]
                if cur >= 1:
                    next_index[i] = k
                    break
            # If we didn't find any k, then next_index[i] remains n (meaning no valid split starting at i)
        
        # Now, compute dp[i] from the end
        for i in range(n-1, -1, -1):
            if next_index[i] == n:
                dp[i] = 0
            else:
                # We can split at any k from next_index[i] to n-1, but only if the segment from i to k is positive.
                # However, note: the segment from i to k is positive for k>=next_index[i] only if next_index[i] is the smallest index.
                # But we must ensure that the segment from i to k is positive. We can use the next_index[i] to know the first positive segment, but for k>next_index[i], the segment might become negative and then positive again.
                # We need to find all k>=next_index[i] such that the segment from i to k is positive.
                # But note: the condition for the first segment is that it is positive, and then the rest is split.
                # However, the problem is that the segment from i to k might not be positive for every k>=next_index[i].
                # We need to know the next_index for each i, but also the next_index for the rest of the array.
                # Alternatively, we can use a different approach: 
                #   dp[i] = sum_{k=next_index[i]}^{n-1} dp[k+1]   but only if the segment from i to k is positive.
                # But we already know that the segment from i to next_index[i] is positive, but for k>next_index[i], it might not be.
                # We can precompute an array `valid` that for each i and k>=next_index[i], whether the segment from i to k is positive.
                # But that is O(n^2).
                #
                # Given the complexity, we might need to use a different method.
                #
                # Let's try to use a two-pointer to maintain the current segment sum and then use a Fenwick tree or segment tree to query the dp values.
                #
                # But note: the problem might be intended to be solved by a simpler method.
                #
                # After rethinking, there is a known solution for the problem "Number of Ways to Split the Array" (LeetCode 2168) but for product. For sum, we can use:
                #   We can split the array if the product of the segments is positive, but for sum it's different.
                #
                # Given the time, I decide to use the following:
                #   We'll use a two-pointer to find the next split position and then use a prefix sum array to quickly compute the sum of dp from next_index[i]+1 to n.
                #
                # But note: the condition for the first segment is that it is positive, and then the rest is split. The rest must be split into positive segments.
                #
                # We can do:
                #   dp[i] = 0
                #   Let j = next_index[i]
                #   Let cur = 0
                #   For k from j to n-1:
                #       cur += nums[k]
                #       if cur >= 1:
                #           dp[i] = (dp[i] + dp[k+1]) % 1000000007
                #       else:
                #           #