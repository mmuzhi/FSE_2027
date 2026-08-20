from typing import List

class Solution:
    def getMinDistance(self, nums: List[int], target: int, start: int) -> int:
        curVal = len(nums)
        for i in range(start, len(nums)):
            if nums[i] == target:
                curVal = min(curVal, abs(i - start))
                break
        j = start
        while j >= 0:
            if nums[j] == target:
                curVal = min(curVal, abs(j - start))
                break
            j -= 1
        return curVal