class Solution:
    def countBalancedPermutations(self, num: str) -> int:
        n = len(num)
        total = sum(int(d) for d in num)
        if total % 2 != 0:
            return 0
        
        target = total // 2
        cnt = Counter(num)
        E_size = (n + 1) // 2
        O_size = n // 2
        
        # Precompute factorials up to 80
        max_fact = 80
        fact = [1] * (max_fact + 1)
        for i in range(1, max_fact + 1):
            fact[i] = fact[i - 1] * i
        
        # DP: dp[i][j] = number of ways to achieve a difference j (sum_E - sum_O) after processing some digits
        # But we need to consider the counts of each digit. Alternatively, we can use a dictionary for the state.
        # But the state space is too large. Instead, we can use a different approach: iterate over digits and use a dictionary for the state (difference, and the counts used for each digit) but that is too heavy.

        # Alternatively, we can use a DP that iterates over the digits and for each digit, we iterate over the number of times we use it in E (from 0 to cnt[digit]).
        # But the state is (digit_index, current_difference) and we need to keep track of the counts used for each digit? Actually, we can use a dictionary for the state (difference) and then for each digit, update the state by adding the digit to E or O.

        # But the problem is that the counts for each digit are limited, and we have to use all digits.

        # We can use a DP that goes digit by digit (from '0' to '9') and for each digit, we decide how many to put in E and how many in O, but the state is the current difference (sum_E - sum_O) and the total digits used (or the counts for each digit). But the counts for each digit are independent.

        # Actually, we can use a DP that iterates over digits from 0 to 9, and for each digit d, we iterate over the number of times we use it in E (from 0 to cnt[d]), and update the state (difference) accordingly.

        # The state: (d, diff) where d is the current digit (from 0 to 9) and diff is the current difference (sum_E - sum_O). But we need to know how many digits we have used so far? Actually, we can compute the total digits used from the counts, but we need to ensure that the counts for E and O do not exceed the available digits.

        # Alternatively, we can use a DP that iterates over the digits and for each digit, we consider all possible ways to split the available count of that digit between E and O.

        # Let dp[d][diff] = number of ways to assign digits from '0' to d (inclusive) such that the difference (sum_E - sum_O) is diff, and we have used some counts for each digit.

        # But the state space: d from 0 to 9, diff from -720 to 720, which is 1441 * 10 = 14410 states. Then for each state, we iterate over the number of times we use the digit (from 0 to cnt[d]), and update the difference.

        # Steps:
        # 1. Precompute the total counts for each digit.
        # 2. Let dp be a dictionary or array for the current digit index and difference.
        # 3. Start with dp0: {0: 1} (difference 0, no digits used).
        # 4. For each digit from 0 to 9:
        #    - For each current difference in dp, and for each k from 0 to cnt[digit]:
        #        - Let k1 = k (number of times we put the digit in E)
        #        - Then the number of times in O is cnt[digit] - k1, but wait, we are iterating by digit, so we must use all occurrences of the digit at once? Actually, we are iterating by digit, so we must use all occurrences of the digit at once. But then, we can only use the entire count of the digit in one go? Actually, no: we can use a digit multiple times (each occurrence