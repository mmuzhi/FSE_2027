class Solution:
    def numPermsDISequence(self, s: str) -> int:
        n = len(s) + 1
        mod = 10**9 + 7
        
        # dp[i][j] = number of ways to have a sequence of i+1 digits ending with digit j (where j is from 0 to 9)
        # But we need to track which digits have been used? Alternatively, we can use a DP that iterates over the positions and the last digit, and use a set of used digits? 
        # However, the state space would be too big if we use a set. Instead, we can use a DP that uses the last digit and the count of digits used so far? But that doesn't help.

        # Alternatively, we can use DP with state (i, last) and then use a set of used digits? But that is too slow.

        # Another idea: since the length is at most 10, we can use a DP that iterates over the positions and the last digit, and then use a bitmask of used digits (10 bits). The state would be (i, last, mask) but mask has 2^10 states and i up to 10, so 10 * 10 * 1024 = 102400 states, which is acceptable.

        # But note: the problem does not require the entire set of 10 digits, just a permutation of length n (which is <=10). We are allowed to choose any n distinct digits from 0-9.

        # Let's define:
        # dp[i][j][mask] = number of ways to have a sequence of i+1 digits, with the last digit being j (0<=j<=9) and mask representing the set of digits used so far (bitmask of 10 bits)

        # However, we can optimize by noting that the mask is just a set of digits, and we are only using digits from 0 to 9.

        # But the state space is 10 (positions) * 10 (last digit) * 1024 (mask) = 102400, which is acceptable.

        # Alternatively, we can use a different approach: since the sequence must be strictly increasing or decreasing, we can also think of it as a sequence of digits that are distinct and the pattern is given.

        # However, the original code did not track the set of used digits, so it was incorrect.

        # Let's use DP with state (i, last, mask) but we can also use a dictionary for memoization.

        # But note: the problem says the permutation is of distinct digits, so we must avoid repeating digits.

        # We'll do:
        # dp(i, last, mask) = number of ways to complete the sequence from position i to the end, given that the last digit is `last` (if i==0, then no last) and the set of used digits is represented by `mask`.

        # However, we can also use iterative DP.

        # Steps:
        #   n = len(s)+1
        #   We'll have dp[i][mask] but then we need to know the last digit? Actually, we need the last digit to decide the next step.

        # Alternatively, we can use state (i, mask) and then the last digit is the last digit in the sequence? But we don't store the last digit in the state, so we cannot.

        # We need to know the last digit to decide the next digit (whether it should be greater or smaller).

        # So we must store the last digit.

        # Let's define:
        #   dp[i][last][mask] = number of ways, but we can combine: we can have a 2D DP for each i: a dictionary with keys (last, mask) or we can use a 3D array.

        # Since n is at most 10, and mask has 1024 states, and last can be 10, we can do:

        # dp[i][last][mask] for i in range(n), last in range(10), mask in range(1024)

        # But we can optimize by iterating over the next digit and updating the mask.

        # Alternatively, we can use a DP that iterates over the positions and the mask, and then for each mask, we know the set of digits used, and then we can choose the next digit from the available digits (0-9) that are not used and satisfy the condition (if s[i] is 'I' then next digit > last, else < last).

        # But note: the condition is given by the string s, and the condition applies at each step.

        # Steps for DP:

        #