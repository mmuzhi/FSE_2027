from typing import List

class Solution:
    def findMaxK(self, nums: List[int]) -> int:
        nums_sorted = sorted(nums, reverse=True)
        s = set(nums)
        for num in nums_sorted:
            if -num in s:
                return num
        return -1