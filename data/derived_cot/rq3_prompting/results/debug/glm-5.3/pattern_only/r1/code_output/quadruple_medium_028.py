class Solution:
    def maximumGap(self, nums: list) -> int:
        if len(nums) < 2:
            return 0
        nums = sorted(nums)
        max_gap = 0
        for i in range(len(nums) - 1):
            x = abs(nums[i + 1] - nums[i])
            if x > max_gap:
                max_gap = x
        return max_gap