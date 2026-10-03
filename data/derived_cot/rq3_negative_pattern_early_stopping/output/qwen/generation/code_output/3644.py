class Solution:
    def minimumSumSubarray(self, nums: List[int], l: int, r: int) -> int:
        n = len(nums)
        prefix = [0] * (n + 1)
        for i in range(n):
            prefix[i+1] = prefix[i] + nums[i]
        
        min_sum = float('inf')
        for i in range(n):
            start = i + l - 1
            end = min(i + r, n - 1)
            if start > end:
                continue
            for j in range(start, end + 1):
                s = prefix[j+1] - prefix[i]
                if s > 0 and s < min_sum:
                    min_sum = s
        
        return min_sum if min_sum != float('inf') else -1