class Solution:
    def beautifulNumbers(self, l: int, r: int) -> int:
        def f(n):
            s = str(n)
            m = len(s)
            # dp[i][tight][started][sum][product] -> but product can be large, so we need to use memoization with state (i, tight, started, sum, product) but product can be up to 9^m, which is too big for m=10 (9^10 is 3.4e9, which is too big for state)

            # Alternatively, we can use a different approach: count numbers with at least one 0 separately and then count numbers without 0 that satisfy the condition.

            # But wait, the problem constraints are up to 10^9, so we need an efficient way.

            # Actually, note that the condition for numbers with 0 is always true. So we can count:
            #   total0 = count of numbers in [l, r] that have at least one 0
            #   total_non0 = count of numbers in [l, r] that have no 0 and for which product of digits is divisible by the sum of digits.

            # Then answer = total0 + total_non0

            # How to count numbers with at least one 0 in [l, r]? We can use digit DP to count numbers without 0 and subtract from the total numbers? But wait, we can use inclusion-exclusion or complementary counting.

            # Alternatively, we can use a digit DP that counts numbers with at least one 0. But that might be complex.

            # Another idea: use digit DP to count numbers without 0 and then subtract from the total numbers to get numbers with at least one 0? Actually, no: we need to count numbers with at least one 0, which is total numbers minus numbers without 0.

            # But wait, we can compute:
            #   total = r - l + 1
            #   numbers_without_0 = count of numbers in [l, r] that don't have any 0
            #   Then numbers_with_0 = total - numbers_without_0

            # But then we also need to count the beautiful numbers without 0 separately.

            # So we need two things:
            #   1. Count numbers without 0 in [l, r] (to get numbers_with_0 by subtracting from total)
            #   2. Count numbers without 0 in [l, r] that are beautiful (i.e., product divisible by sum)

            # But wait, the beautiful numbers without 0 are a subset of numbers without 0. So we can use a digit DP that counts numbers without 0 and also tracks the product and sum, but the product and sum are too big.

            # Alternatively, we can use a digit DP that counts numbers without 0 and then for each number, we check the condition? But that would be too slow.

            # We need a digit DP that can handle the condition for numbers without 0.

            # But note: the condition is product divisible by sum. The sum is at most 81 (for 9 nines) and the product is the product of digits (each 1-9). We can use state (pos, tight, sum, product) but the product can be up to 9^10 which is 3.4e9, which is too big for memoization.

            # We need to find a smarter way.

            # Observation: The condition is product % sum == 0. The sum is the sum of digits, which is small (at most 81). So we can iterate over possible sums (from 1 to 81) and for each sum, we can count the numbers without 0 that have digit sum = s and product divisible by s. But then we need to count numbers with digit sum s and product divisible by s, and then sum over s from 1 to 81.

            # But how to count numbers with a given digit sum and product divisible by s? We can use DP that tracks the position, tight, sum, and product. But product is still too big.

            # Alternatively, we can use a different approach: since the numbers are up to 10^9, but the beautiful condition is rare, we can iterate over numbers that are beautiful. But how?

            # Another idea: use BFS to generate all beautiful numbers (without 0) up to 10^9? But 10^9 is too big.

            # Let me think differently. The product of digits must be divisible by the sum. The product is the product of digits (each 1-9). The sum is the sum of digits. The product is a number that is the product of digits, and the sum is the sum of digits. The condition