class Solution:
    def maximumGap(self, nums: list) -> int:
        if len(nums) < 2:
            return 0
        nums = sorted(nums)
        min_gap = float("-inf")
        for i in range(len(nums) - 1):
            x = abs(nums[i] - nums[i + 1])
            if min_gap < x:
                min_gap = x
        return min_gap