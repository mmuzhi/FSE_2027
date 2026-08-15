from typing import List

class Solution:
    def findMaxK(self, nums: List[int]) -> int:
        nums = sorted(nums, reverse=True)
        s = set(nums)
        for x in nums:
            if x > 0 and -x in s:
                return x
        return -1