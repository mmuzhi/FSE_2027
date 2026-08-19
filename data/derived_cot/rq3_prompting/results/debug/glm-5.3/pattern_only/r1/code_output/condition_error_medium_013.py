class Solution:
    def minPairSum(self, nums: List[int]) -> int:
        nums.sort()
        result = 0
        left, right = 0, len(nums) - 1
        while left < right:
            result = max(result, nums[left] + nums[right])
            left += 1
            right -= 1
        return result