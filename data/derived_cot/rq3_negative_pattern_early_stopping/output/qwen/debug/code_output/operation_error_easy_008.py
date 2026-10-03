class Solution:
    def findMaxK(self, nums: List[int]) -> int:
        nums_set = set(nums)
        nums_sorted = sorted(nums, reverse=True)
        for num in nums_sorted:
            if num > 0 and -num in nums_set:
                return num
        return -1