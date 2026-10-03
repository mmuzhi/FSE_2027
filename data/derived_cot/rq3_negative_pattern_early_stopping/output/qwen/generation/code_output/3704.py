class Solution:
    def countPartitions(self, nums: List[int]) -> int:
        total = sum(nums)
        left_sum = 0
        count = 0
        for i in range(len(nums) - 1):
            left_sum += nums[i]
            right_sum = total - left_sum
            # The difference is left_sum - right_sum, but we care about parity.
            # The parity of left_sum - right_sum is the same as the parity of left_sum + right_sum (because (a-b) mod 2 = (a+b) mod 2? Actually, no: 
            # But note: (left_sum - right_sum) % 2 = (left_sum + (-right_sum)) % 2 = (left_sum + (2 - (right_sum % 2))) % 2? 
            # Actually, we can use: 
            # (left_sum - right_sum) % 2 = (left_sum % 2 - right_sum % 2) % 2, but subtraction modulo 2 is the same as addition modulo 2 because 1-1=0, 1-0=1, 0-1= (0+1) mod 2? Actually, in modulo 2, subtraction is the same as addition because the additive inverse of 1 is 1 (since 1+1=0) and of 0 is 0. So (a-b) mod 2 = (a + (2 - b)) mod 2, but note that (2-b) mod 2 is the same as (-b) mod 2, and then adding a and then mod 2. But actually, we can also think: 
            # The condition for the difference to be even is that left_sum and right_sum have the same parity (both even or both odd). Because:
            # (left_sum - right_sum) is even if and only if left_sum and right_sum have the same parity (because even-even=even, odd-odd=even, even-odd=odd, odd-even=odd).
            if (left_sum % 2) == (right_sum % 2):
                count += 1
        return count