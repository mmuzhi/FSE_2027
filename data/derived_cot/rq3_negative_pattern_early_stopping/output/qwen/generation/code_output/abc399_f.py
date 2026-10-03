def main():
    import sys
    data = sys.stdin.read().split()
    n = int(data[0])
    k = int(data[1])
    A = list(map(int, data[2:2+n]))
    
    # If k == 0, then the sum is the number of subarrays, but k>=1 per constraints.
    # We are going to iterate over all exponent vectors (k1, k2, ..., kn) with sum k.
    # But note: n can be up to 200000, and k up to 10, but the number of exponent vectors is C(k+n-1, n-1) which is too many.

    # Alternative approach: use generating functions and dynamic programming.

    # Since k is small (<=10), we can use a DP that iterates over the array and keeps track of the last k+1 moments (or power sums) of the subarray sums.

    # But note: we need to compute the sum_{l<=r} (S_{l,r})^K.

    # We can use the idea of "contribution" of each element and use the binomial expansion, but the multinomial expansion is too heavy.

    # Another idea: use the linearity and the fact that (a+b)^K can be expanded, but then we need to combine the contributions.

    # Alternatively, we can use the method of iterating over the starting index and then using a DP that accumulates the sum and its powers.

    # But note: the total number of subarrays is O(n^2), which is too many.

    # We need a linear or near-linear method.

    # Insight: use the idea of "adding one element at a time" and update the moments.

    # Let dp[i][j] be the number of subarrays ending at i with sum^j. But j can be up to 10, and i up to 200000, so that's 200000*11 states, which is acceptable.

    # But then, we need to compute the sum_{j=0}^{k} dp[i][j] * (some value) but wait, we need the sum of (S_{l,r})^K for all subarrays.

    # Alternatively, we can use a DP that for each ending index i, and for each power j from 0 to k, we store the sum of (subarray sum)^j for all subarrays ending at i.

    # Then, the recurrence is:
    # Let S_i be the prefix sum up to i.
    # Then, the subarray ending at i is from j to i, and the sum is S_i - S_{j-1} (if we define S_0=0).
    # Then, the subarray sum for ending at i and starting at j is (S_i - S_{j-1}).
    # Then, we want to compute for each j from 0 to i, the value (S_i - S_{j-1})^K.

    # But then, we need to sum over j from 0 to i.

    # We can use the binomial expansion for (S_i - S_{j-1})^K, but then we need to sum over j.

    # Alternatively, we can use a DP that for each i and for each power p (from 0 to k), we store the sum of (subarray sum)^p for all subarrays ending at i.

    # Let dp[i][p] = sum_{j=0}^{i} ( (S_i - S_{j-1})^p )

    # Then, the answer is the sum_{i=0}^{n-1} dp[i][k].

    # But how to compute dp[i][p] from dp[i-1][p]? 

    # We can use the recurrence for the power sums. Let T_j = S_{j-1} (the prefix sum up to j-1). Then, the subarray ending at i is from j to i, and the sum is S_i - T_j.

    # Then, dp[i][p] = sum_{j=0}^{i} (S_i - T_j)^p.

    # We can expand (S_i - T_j)^p using binomial theorem:

    # dp[i][p] = sum_{m=0}^{p} binom(p, m) * S_i^m * (-1)^(p-m) * (sum_{j=0}^{i} T_j^(p-m))

    # But note: the binomial expansion is (x+y)^p = sum_{m=0}^{p} binom(p, m) x^m y^{p-m