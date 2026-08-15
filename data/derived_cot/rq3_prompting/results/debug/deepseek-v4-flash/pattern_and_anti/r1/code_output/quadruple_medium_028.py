class Solution:
    def maximumGap(self, nums: list) -> int:
        if len(nums) < 2:
            return 0

        nums = sorted(nums)
        max_gap = 0

        for i in range(len(nums) - 1):
            gap = abs(nums[i] - nums[i + 1])
            if gap > max_gap:
                max_gap = gap

        return max_gap