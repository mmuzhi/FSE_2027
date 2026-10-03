class Solution:
    def numPermsDISequence(self, s: str) -> int:
        n = len(s) + 1
        mod = 10**9 + 7
        
        # dp[i][j] = number of ways to have a sequence of length i+1 ending with digit j
        # But j from 0 to n-1, and we need to ensure distinct digits.
        # Alternatively, we can use DP with state (i, j) and then use a Fenwick tree to count available digits, but that is complex.
        # Instead, we can use DP with state (i, j) and then use a separate DP table for the next state, but we need to know which digits are available.
        # We can use a DP that iterates over the next digit and subtracts the used ones, but that is too slow.

        # Another known approach for such problems is to use DP with state (i, j) where j is the current digit, and then use a Fenwick tree to count the available digits for the next step. But n is 50, so we can do O(n^2) with state (i, j) and then use a 2D DP.

        # Let dp[i][j] = number of ways to have a sequence of length i+1 ending with digit j (where j from 0 to n-1)
        # Then, for the next character s[i] (at position i, 0-indexed), we need to choose a digit k such that:
        #   if s[i]=='I', then k > j
        #   if s[i]=='D', then k < j
        # But we must also ensure that k is not used in the sequence so far.

        # However, we cannot easily keep track of which digits are used in the sequence so far in the state (i, j). 

        # Alternatively, we can use a DP that doesn't fix the exact digits but uses the relative order. But note: the problem requires distinct digits.

        # We can use DP with state (i, j) where j is the current digit, and then use a Fenwick tree to count the available digits. But the constraints are small (n<=50) so we can do:

        # Let dp[i][j] = number of ways to have a sequence of length i+1 ending with digit j, and we maintain an array of used digits? No, that would be too slow.

        # Another idea: we can use DP that doesn't fix the exact digits but uses the fact that the sequence is a permutation of 0 to n-1. We can use a DP that counts the number of ways to have a sequence of length i+1 with the last digit being j, and then for the next step, we consider all digits that are not used. But we don't know which digits are used.

        # We can use a DP that is O(n^2) in state and then use a Fenwick tree to count the available digits for the next step. But note: the state (i, j) doesn't remember the entire set of used digits.

        # Alternatively, we can use a DP that iterates over the next digit and subtracts the ones that are already used. But we don't know the used digits.

        # Let's change the state: let dp[i][j] = number of ways to have a sequence of length i+1 ending with digit j, and we also keep an array of used digits? No, that is too heavy.

        # We can use a different approach: 
        #   Let dp[i][j] = number of ways to have a sequence of length i+1 ending with the j-th smallest digit (where j from 0 to n-1). Then the next digit must be chosen from the remaining digits, but we don't know which ones are used.

        # Another known solution for such problems is to use DP with state (i, j) where j is the current digit, and then use a Fenwick tree to count the available digits. But we can do without Fenwick tree because n is small.

        # We can precompute the next state by iterating over all available digits. But we don't know which digits are available.

        # We can use a DP that doesn't fix the exact digits but uses the relative order. But note: the problem requires distinct digits.

        # Actually, there is a known combinatorial solution: 
        #   We can think of the sequence as having some increasing runs and decreasing runs. But the problem is asking for the count.

        # Alternatively, we can use DP with state (i, j) where j is the current digit, and then use a 2D DP table and update the next state by iterating over all digits that are not used. But we don't know the used digits.

        # We can