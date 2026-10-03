import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    m = int(data[1])
    A = list(map(int, data[2:2+n]))
    B = list(map(int, data[2+n:2+n+m]))
    
    # If M is 0, then we have an empty subsequence. There are multiple ways (if n>=0) but note: two subsequences? 
    # But the problem states: two subsequences that match B. If B is empty, then we need at least two ways to choose an empty subsequence? 
    # However, the constraints say M>=1, so we don't have to handle M=0.

    # We'll use a DP array for the number of ways to match B, but we don't need the full count if it's too big.
    # Instead, we can use a greedy method to find two distinct subsequences.

    # First, we need to check if B is a subsequence at all.
    # We can do a two-pointer to find one occurrence.

    # But we need two distinct ones.

    # We can use the following idea:
    # Let's record the indices of the first occurrence of B.
    # Then, we try to find a second occurrence by modifying the matching.

    # Alternatively, we can use a DP array that stores the last index for each state, but that is too heavy.

    # Another idea: 
    # We can use a DP array that stores the count of ways to match the first j elements of B, but we can use a sliding window and update in O(1) per element.

    # Standard method for counting distinct subsequences (for a pattern) is to use:
    # Let dp[j] = number of ways to match B[0:j] (the first j elements of B)
    # Then, for each a in A:
    #   for j from M-1 down to 0:
    #       if a == B[j], then dp[j+1] += dp[j]

    # But that is O(N*M). We need to optimize.

    # We can use a dictionary to store the last occurrence of elements in B and update the dp in a smarter way.

    # Actually, there is a known efficient way to count the number of distinct subsequences for a pattern B in A in O(N) time.

    # However, note that we don't need the exact count, only to check if there are at least two.

    # We can do:

    # Let dp[j] = the number of ways to match B[0:j] (for j from 0 to M)
    # We can update dp[j] by:
    #   dp[0] = 1 (empty subsequence)
    #   Then, for each a in A, we update from j = M-1 down to 0:
    #       if a == B[j], then dp[j+1] += dp[j]

    # But that is O(N*M) and M can be 200000, so worst-case 40e9 operations.

    # We need a better way.

    # We can use a dictionary to store the last occurrence of each element in B and then use a pointer for the current matching position.

    # Alternatively, we can use a two-pointer method to find the first occurrence and then try to find a second occurrence by "bypassing" one element.

    # Steps for two distinct subsequences:

    # 1. Find the first occurrence of B in A (by indices).
    # 2. Then, from the same starting point, try to find a second occurrence by allowing one "detour".

    # Actually, we can use the following method:

    # Let's define a function that, given a starting index, returns the next occurrence of B from that index.

    # But we need two distinct subsequences.

    # We can do:

    #   Let i = 0 (index in A), j = 0 (index in B)
    #   We traverse A to find the first occurrence of B, recording the indices.

    #   Then, we try to find a second occurrence by starting from the same initial part until a divergence.

    #   Specifically, we can try to match B again, but at one point, we can skip an element that is not necessary for the first occurrence.

    #   Actually, we can use the following:

    #   Let's record the positions of the first occurrence: p0, p1, ..., p_{m-1}

    #   Then, we try to find a second occurrence that uses a different index for at least one element.

    #   We can do this by:

    #       Let j = 0 (current position in B)
    #       Let i = 0 (current position in A)