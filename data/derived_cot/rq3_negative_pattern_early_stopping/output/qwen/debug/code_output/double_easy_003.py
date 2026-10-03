class Solution:
    def minimumDifference(self, nums: List[int], k: int) -> int:
        n = len(nums)
        if k > n:
            return 0
        
        res = float('inf')
        l, r = 0, k
        while r < len(nums):
            window = nums[l:r]
            window.sort()
            min_diff = float('inf')
            for i in range(1, len(window)):
                diff = window[i] - window[i-1]
                if diff < min_diff:
                    min_diff = diff
            if min_diff < res:
                res = min_diff
            l += 1
            r += 1
        
        return res