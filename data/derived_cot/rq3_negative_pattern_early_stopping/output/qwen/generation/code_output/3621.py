class Solution:
    def minOperations(self, nums: List[int], k: int) -> int:
        # Count the distinct numbers in the array
        distinct_nums = set(nums)
        # If k is not in the array, then we need to set all numbers to k, but we can only set numbers above h to h.
        # However, note that we can set numbers to k only if k is valid. But k might not be present initially.
        # Actually, the operations can set numbers to k only if k is chosen as h and k is valid. But if k is not present, then we can still set numbers to k if we can form a valid h=k.

        # But note: the operation sets numbers greater than h to h. So, to set a number to k, we must have an operation with h=k, and for that, all numbers strictly greater than k must be identical (if they exist). 

        # However, we can perform operations in any order. We can first set numbers above k to some value, and then set them to k.

        # Actually, the problem is: we want to make all elements equal to k. We can only set numbers above h to h (and h must be valid). 

        # Let me reframe: We need to reduce all numbers to k. But we can only set numbers above h to h. So, the numbers that are already <= k can stay. 

        # But wait, if a number is less than k, we cannot set it to k because the operation only sets numbers above h to h. So, if we have a number less than k, we cannot increase it. Therefore, if there is any number in nums that is less than k, then we cannot set it to k (because we can only decrease numbers). 

        # So, first condition: if there is any number in nums that is less than k, then it's impossible to make all elements equal to k (because we can't increase them). But wait, in the example 1: nums = [5,2,5,4,5], k=2. Here, 2 is the target, and there are numbers (2,4,5) but 4 and 5 are above 2. However, note that 2 is present. 

        # Actually, the operation sets numbers above h to h. So, if we have a number less than k, we cannot change it (unless we set it to a lower value, but then we can't get it to k). Therefore, if there is any number in nums that is less than k, then it's impossible to make all elements equal to k. 

        # But wait, in example 1, the array has 2, which is equal to k. But there are numbers (5,5,4) that are above 2. The operation with h=2 would set all numbers above 2 to 2. But is h=2 valid? For h=2, all numbers strictly greater than 2 must be identical. In the initial array [5,2,5,4,5], the numbers greater than 2 are 5,5,4. They are not all identical (5 and 4 are different). So, h=2 is not valid initially.

        # So, we need to first set the numbers above 2 to something else. The example says they used h=4 first. Then the array becomes [4,2,4,4,4]. Then they use h=2. Now, for h=2, the numbers greater than 2 are all 4, which are identical. So, h=2 is valid.

        # Therefore, the steps are:
        # 1. We need to ensure that all numbers that are greater than k are set to a value that is the same (so that we can then set them to k). 

        # Actually, the goal is to have all numbers equal to k. The operations can be done in any order. 

        # Observation:
        # - We can only decrease numbers (set them to a lower value).
        # - To set a number to k, we must use an operation with h=k, and for h=k to be valid, all numbers strictly greater than k must be identical (and then they are set to k). 

        # But note: we can set numbers above k to a value that is not k, but then set them to k in a later operation. However, the operation with h=k requires that all numbers greater than k are identical. 

        # So, the plan is:
        # 1. We need to set all numbers greater than k to the same value (say, x) such that x is greater than k (or maybe not, but we can set them to x and then set x to k). But wait, we can set them to k directly if we can use