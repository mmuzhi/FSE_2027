class Solution:
    def minimumPossibleSum(self, n: int, target: int) -> int:
        mod = 10**9 + 7
        # If target is 1, then we can only use numbers >=1, but since distinct and no two sum to 1, actually only one number is allowed. But n=1, so [1] is the only option.
        # Let's break the numbers into two parts:
        # 1. Numbers from 1 to target-1: these form pairs (x, target-x). We can take at most half of them (rounded down) from the lower half (1 to (target-1)//2) and then the rest must be taken from numbers >= target.
        # 2. Numbers from target onwards: these are safe because if I take a number >= target, then the smallest number I can pair it with is 1, and 1 + (target) is already >= target+1, which is greater than target. But wait, if I take two numbers both >= target, then their sum is >= 2*target, which is definitely greater than target. So the only issue is with numbers from 1 to target-1.

        # So, the strategy is:
        #   - Use as many small numbers as possible, but avoid using both x and target-x.
        #   - The maximum numbers we can take from 1 to target-1 is (target-1)//2 (if target is odd) or target//2 (if target is even). Actually, the number of pairs is (target-1)//2, so we can take one from each pair, so the count is (target-1)//2.

        # Let's define:
        #   Let m = (target-1)//2  [the number of pairs we can form from 1 to target-1, and we can take one from each pair, so we can take m numbers from 1 to target-1 without violating the condition? Actually, no: the pairs are (1, target-1), (2, target-2), ... until (m, target-m). So the count is m, which is (target-1)//2.

        # But wait, if target is even, then the pairs are (1, target-1), (2, target-2), ... (target/2 - 1, target/2 + 1) and then target/2 is left alone. But since we can't have two same numbers, we can only take one of each pair. So the maximum numbers we can take from 1 to target-1 is (target-1)//2 (which is the same as floor((target-1)/2)).

        # So, if n <= (target-1)//2, then we can just take the first n numbers from 1 to (target-1)//2, and the sum is the sum of the first n natural numbers.

        # But wait, actually, the numbers we can take from 1 to target-1 are the numbers from 1 to (target-1)//2, because if we take a number from the upper half, say x > target/2, then target-x would be in the lower half and we cannot take both. But actually, we can choose either the lower or the upper. To minimize the sum, we should choose the smaller numbers. So the minimal way is to take all numbers from 1 to (target-1)//2, and then if we need more numbers, we take numbers from target onwards.

        # Actually, the minimal numbers we can use are:
        #   First, take all numbers from 1 to (target-1)//2. That gives us m = (target-1)//2 numbers.
        #   Then, if we need more numbers (n > m), we take the next numbers from target to target + (n - m) - 1.

        # But wait, is that correct? Let me test with example 2: n=3, target=3.
        #   m = (3-1)//2 = 1. So we can take 1 number from 1 to 1 (which is 1). Then we need 2 more numbers. The next numbers are from 3 onwards. So we take 3 and 4. Then the array is [1,3,4] which is correct. The sum is 1+3+4=8.

        # Example 1: n=2, target=3.
        #   m = (3-1)//2 = 1. So we take 1 number from 1 to 1 (which is 1). Then we need 1 more number, which is 3. So array [1,3] and sum 4.

        # Another example: n=4, target=4.
        #   m = (