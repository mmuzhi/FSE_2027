class Solution:
    def findPeakElement(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 1:
            return 0
        
        low, high = 0, n - 1
        
        while low <= high:
            mid = (low + high) // 2
            if (mid == 0 or nums[mid] >= nums[mid - 1]) and (mid == n - 1 or nums[mid] >= nums[mid + 1]):
                return mid
            elif mid < n - 1 and nums[mid] < nums[mid + 1]:
                low = mid + 1
            else:
                high = mid - 1
        
        return -1