from typing import List

class Solution:
    def findPeakElement(self, nums: List[int]) -> int:
        n = len(nums)
        low = 0
        high = n - 1
        if n == 1:
            return 0
        
        while low <= high:
            mid = (low + high) // 2
            left_ok = (mid == 0 or nums[mid] >= nums[mid - 1])
            right_ok = (mid == n - 1 or nums[mid] >= nums[mid + 1])
            if left_ok and right_ok:
                return mid
            elif nums[mid] <= nums[mid + 1]:
                low = mid + 1
            else:
                high = mid - 1
        return -1