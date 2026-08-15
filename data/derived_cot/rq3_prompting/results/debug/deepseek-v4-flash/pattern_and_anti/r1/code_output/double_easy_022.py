from typing import List

class Solution:
    def findMaxK(self, nums: List[int]) -> int:
        s = set(nums)
        nums = sorted(nums, reverse=True)

        for x in nums:
            if x <= 0:
                break
            if -x in s:
                return x

        return -1