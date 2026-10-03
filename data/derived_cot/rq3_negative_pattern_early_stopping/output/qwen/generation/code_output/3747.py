class Solution:
    def maxAdjacentDistance(self, nums: List[int]) -> int:
        n = len(nums)
        max_diff = 0
        for i in range(n):
            j = (i + 1) % n
            current_diff = abs(nums[i] - nums[j])
            if current_diff > max_diff:
                max_diff = current_diff
        return max_diff