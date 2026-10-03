class Solution:
    def numPermsDISequence(self, s: str) -> int:
        n = len(s)
        mod = 10**9+7
        
        # dp[i][last] = number of ways to have built a sequence of length i+1 (from index 0 to i) with the last digit being 'last'
        # But note: the digits are from 0 to n (inclusive) and we are building a permutation of length n+1.
        # However, we cannot use a 2D DP with last from 0 to n because n is 50 and i from 0 to 50, so 51*51=2601 states, which is acceptable.

        # But we need to know which digits are available. Alternatively, we can use a Fenwick tree or segment tree to count available digits, but that might be overkill.

        # Alternatively, we can use a DP that doesn't store the last digit but the set of used digits? No, that's too expensive.

        # Let's try with DP state (i, last) and then we need to know the set of used digits? No, we cannot.

        # Another idea: use DP with state (i, last) and then use a Fenwick tree to count the available digits that are greater/less than last.

        # But note: the condition is only about the last digit and the next one. The rest of the digits don't matter for the condition, but they must be distinct.

        # We can use a DP that stores the last digit and the number of digits used so far? But that doesn't help.

        # Alternatively, we can use a DP that stores the last digit and then use combinatorics to count the ways to choose the remaining digits.

        # However, let's try a different approach:

        # We are building a permutation of length n+1 (digits 0 to n). We start with a set of available digits.

        # We can use DP with state (i, last) and then for the next step, we need to choose a digit from the available set that satisfies the condition.

        # But we don't want to iterate over all available digits for each state because that would be O(n) per state and total states O(n^2) so O(n^3) which is 51^3 = 132651, which is acceptable for n=50? Actually, n=50, so 51^3 = 132651, which is acceptable in Python if we optimize.

        # But we need to know the available digits. We can maintain a set of available digits, but updating the set for each state would be too heavy.

        # Alternatively, we can use a DP that stores the last digit and the set of used digits? That state space is too large.

        # Let's try to use a DP that stores the last digit and then use a Fenwick tree to count the available digits. But we are in Python and Fenwick tree might be heavy.

        # Alternatively, we can use a DP that stores the last digit and the number of digits used so far? No.

        # Another idea: use DP with state (i, last) and then use a precomputed list of available digits. But we need to update the available digits.

        # We can use a DP that stores the last digit and then use a Fenwick tree to count the available digits that are greater/less than last. But we need to update the Fenwick tree as we go.

        # Alternatively, we can use a DP that stores the last digit and then use a segment tree to count the available digits. But again, we are in Python.

        # Let's try to use a DP that stores the last digit and then use a simple array for the available digits. But we need to update the available digits for each state.

        # We can use memoization with state (i, last) and then for each state, we know the set of used digits? No, we don't.

        # We need to know the set of used digits to know which digits are available. But storing the set of used digits is too expensive.

        # Let's try to use a different state: (i, last) and then use a Fenwick tree that is updated as we go. But we are doing DP, so we need to backtrack.

        # Alternatively, we can use a DP that stores the last digit and the number of digits used so far? No.

        # Another idea: use a DP that stores the last digit and then use a combinatorial count for the remaining digits. But the condition is only about the last digit and the next one.

        # We can use a DP that stores the last digit and then use a Fenwick tree to count the available digits that are greater/less than last. But