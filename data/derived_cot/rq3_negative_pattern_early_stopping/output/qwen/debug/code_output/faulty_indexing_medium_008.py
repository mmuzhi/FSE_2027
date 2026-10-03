class Solution:
    def findPeakElement(self, nums: List[int]) -> int:
        n = len(nums)
        low = 0
        high = n - 1
        if n == 1:
            return 0
        
        while low <= high:
            mid = (low + high) // 2
            # Check if mid is a peak
            is_peak = True
            if mid > 0 and nums[mid] < nums[mid-1]:
                is_peak = False
            if mid < n-1 and nums[mid] < nums[mid+1]:
                is_peak = False
            if is_peak:
                return mid
            
            # If not a peak, then we need to decide the direction
            if mid < n-1 and nums[mid] < nums[mid+1]:
                low = mid + 1
            else:
                high = mid - 1
        return -1