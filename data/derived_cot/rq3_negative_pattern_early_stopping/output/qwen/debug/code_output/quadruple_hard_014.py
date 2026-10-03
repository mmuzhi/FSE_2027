class Solution:
    def numPermsDISequence(self, s: str) -> int:
        n = len(s) + 1  # because we are forming a permutation of length n (digits 0..n-1) but wait, the problem says digits 0 to n (so n+1 digits) and length n+1? Actually, the problem says: "permutations of digits from 0 to n", so the permutation has length n+1 (digits 0..n). But note: the string s has length n (which is the number of conditions, so the permutation has length n+1). So n = len(s) + 1.

        # We'll use DP with state (i, j) where i is the index (0 to n) and j is the last digit (0 to n)
        # But note: the permutation is of digits 0..n, so the digits are from 0 to n (inclusive) and there are n+1 digits.

        # However, the problem says: "permutations of digits from 0 to n", so the set is {0,1,...,n}. The length is n+1.

        # Let dp[i][j] = number of ways to have a permutation of length i (so we have chosen i digits) ending with digit j.

        # But note: the condition is given by s, which has length n-1 (because the permutation has length n, so there are n-1 conditions). Actually, the problem says: "sequence" of length n (digits 0..n-1) but wait, the problem statement says: "permutations of digits from 0 to n", so the set is {0,1,...,n} and the length is n+1. And the string s has length n (the number of conditions) because there are n+1 digits, so n conditions.

        # So n = len(s) + 1? Actually, the problem says: "s: str" and the example: s = "IDID", then n+1 = 5, so n=4, and the permutation is of digits 0..4.

        # Let's re-read: "permutations of digits from 0 to n" — but note the example: s = "IDID", then the permutation is of length 5 (digits 0..4). So the set is {0,1,2,3,4} and the length is 5.

        # Therefore, the length of the permutation is len(s)+1, and the digits are from 0 to len(s) (inclusive).

        # We'll let n = len(s) + 1.

        # But note: the problem does not specify the length of the permutation, but the condition string s has length (n-1) because the permutation has length n (digits 0..n-1) but wait, the problem says "digits from 0 to n", so the permutation has length n+1.

        # Actually, the problem statement: "permutations of digits from 0 to n" — so the set has n+1 elements (0 to n). The permutation has length n+1.

        # And the string s has length (n) because there are n conditions (between n+1 digits). So n = len(s) + 1.

        # We'll set:
        n_val = len(s) + 1
        mod = 10**9+7

        # dp[i][j] = number of ways to have a permutation of length i (i from 0 to n_val) ending with digit j (j from 0 to n_val-1)
        # But note: the digits are from 0 to n_val-1 (which is 0 to len(s)).

        # We'll use a 2D DP array of size (n_val+1) x (n_val) but we can use a 1D DP and update.

        # Alternatively, we can use a 1D DP for the current row and update for the next.

        # But note: the condition at step i (0-indexed) is s[i] (which is the i-th character of s) and it applies to the transition from the i-th digit to the (i+1)-th digit.

        # We start with the first digit. The first digit can be any digit from 0 to n_val-1.

        # Then, for the next digit, we choose a digit that is either greater (if s[i]=='I') or less (if s[i]=='D') than the last digit.

        # However, we must not reuse digits.

        # We can use DP with state (i, j) and then for each state, we iterate over all available digits (not used) and check the condition.

        # But the state space is (