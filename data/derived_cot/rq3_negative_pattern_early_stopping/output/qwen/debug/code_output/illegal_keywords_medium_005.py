class Solution:
    def findValueOfPartition(self, nums: List[int]) -> int:
        if len(nums) < 2:
            return 0
        nums.sort()
        min_diff = float('inf')
        for i in range(1, len(nums)):
            min_diff = min(min_diff, abs(nums[i] - nums[i-1]))
        return min_diff