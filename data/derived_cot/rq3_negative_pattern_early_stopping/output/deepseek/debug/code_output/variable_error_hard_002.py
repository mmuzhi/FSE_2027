from typing import List

class Solution:
    def secondGreaterElement(self, nums: List[int]) -> List[int]:
        n = len(nums)
        ans = [-1] * n
        s = []   # waiting for first greater
        ss = []  # waiting for second greater (already got first greater)
        for i, x in enumerate(nums):
            while ss and nums[ss[-1]] < x:
                ans[ss.pop()] = x
            buff = []
            while s and nums[s[-1]] < x:
                buff.append(s.pop())
            while buff:
                ss.append(buff.pop())
            s.append(i)
        return ans