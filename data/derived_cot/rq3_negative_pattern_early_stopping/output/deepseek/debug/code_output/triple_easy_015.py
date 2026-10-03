from typing import List

class Solution:
    def findMaxK(self, nums: List[int]) -> int:
        s = set(nums)
        ans = -1
        for x in s:
            if x > 0 and -x in s:
                ans = max(ans, x)
        return ans