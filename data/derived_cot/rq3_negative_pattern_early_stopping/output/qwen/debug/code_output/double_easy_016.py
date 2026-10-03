class Solution:
    def findMaxK(self, nums: List[int]) => int:
        nums_sorted = sorted(nums, reverse=True)
        s = set(nums_sorted)
        for num in nums_sorted:
            if num > 0 and -num in s:
                return num
        return -1