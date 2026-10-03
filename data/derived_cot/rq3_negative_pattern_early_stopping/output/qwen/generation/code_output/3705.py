class Solution:
    def largestInteger(self, nums: List[int], k: int) -> int:
        n = len(nums)
        # If k is larger than n, then no subarray exists, but k is at least 1 and <= n per constraints, so skip.
        subarrays = []
        for i in range(n - k + 1):
            subarrays.append(nums[i:i+k])
        
        distinct_nums = set(nums)
        almost_missing = []
        for x in distinct_nums:
            count = 0
            for arr in subarrays:
                if x in arr:
                    count += 1
            if count == 1:
                almost_missing.append(x)
        if not almost_missing:
            return -1
        return max(almost_missing)