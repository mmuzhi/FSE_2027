class Solution:
    def subarraySum(self, nums: List[int]) -> int:
        total_sum = 0
        n = len(nums)
        for i in range(n):
            start = max(0, i - nums[i])
            current_sum = 0
            for j in range(start, i + 1):
                current_sum += nums[j]
            total_sum += current_sum
        return total_sum