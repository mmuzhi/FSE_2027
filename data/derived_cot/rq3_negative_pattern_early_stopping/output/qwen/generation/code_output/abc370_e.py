import sys
from collections import defaultdict

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    K = int(data[1])
    A = list(map(int, data[2:2+n]))
    
    # Precompute prefix sums
    P = [0]*(n+1)
    for i in range(1, n+1):
        P[i] = P[i-1] + A[i-1]
    
    # dp[i] = number of ways to split the first i elements without any segment summing to K
    dp = [0]*(n+1)
    dp[0] = 1  # base case: 0 elements, one way (empty)
    
    # We'll use a dictionary to store the prefix sums and their corresponding dp values
    # But note: we need to avoid j such that P[j] == P[i] - K
    # We'll maintain a dictionary that maps prefix sum to the sum of dp[j] for all j with that prefix sum
    prefix_dict = defaultdict(int)
    prefix_dict[0] = 1  # P[0] = 0
    
    # We'll iterate i from 1 to n (i is the number of elements considered)
    for i in range(1, n+1):
        # We want to compute dp[i] = (sum of dp[j] for j from 0 to i-1) - (sum of dp[j] for j from 0 to i-1 such that P[j] == P[i] - K)
        # But note: the total sum of dp[j] for j from 0 to i-1 is not stored, but we can use the fact that the total ways without condition is 2^(i-1) but that's not directly helpful.
        # Actually, we are building dp[i] from dp[j] for j < i.
        # We can use the prefix_dict to get the sum of dp[j] for j with prefix P[i]-K.
        target = P[i] - K
        # The forbidden j are those with P[j] == target. But note: j must be in [0, i-1].
        # We subtract the sum of dp[j] for all j (with j < i) that have P[j] == target.
        # However, note: we are building dp[i] from j from 0 to i-1. But we haven't stored dp[i] yet, so we can use the prefix_dict which contains all j from 0 to i-1.
        subtract = prefix_dict.get(target, 0)
        # But wait: the above subtract is the sum of dp[j] for all j (from 0 to i-1) with P[j] == target. However, note that the condition is that the segment from j to i-1 is K, which is exactly P[i]-P[j]==K, so P[j]==target. So, we subtract these.
        # But is that correct? Actually, we are summing dp[j] for j from 0 to i-1, and then subtracting the ones that would form a segment with sum K. However, note that the dp[j] already accounts for the splits up to j being valid. But if we subtract dp[j] for which P[j]==target, then we are excluding those j that, when extended to i, form an invalid segment. But note: the entire division is invalid if the last segment is K, regardless of the splits before. So, we must not count those j that would form a K segment at the end.
        # However, there is a catch: the condition is that the entire division must not have any segment with sum K. The segment from j to i-1 is the last segment. But what if there is a segment inside [0, j-1] that is K? Then dp[j] would not have counted that j because dp[j] only counts splits that are valid up to j. So, we are safe to subtract only the j with P[j]==target, because those j are valid splits (so no segment in [0, j-1] is K) but the last segment is K, making the entire division invalid.
        # Therefore, we subtract the dp[j] for j with P[j]==target.
        # But note: the total sum of dp[j] for j from 0 to i-1 is not stored. We can compute it by keeping a running total? Alternatively, we can use the fact that the total ways to split the first i elements without the condition is 2^(i-1) but that's not the same as the sum of dp[j] for j from 0 to i-1.

        # Actually, we are building dp[i] from the dp[j] for