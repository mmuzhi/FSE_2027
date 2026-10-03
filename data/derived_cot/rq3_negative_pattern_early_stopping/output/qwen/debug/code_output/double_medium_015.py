import bisect

class Solution:
    def getSumAbsoluteDifferences(self, nums: List[int]) -> List[int]:
        n = len(nums)
        sorted_nums = sorted(nums)
        prefix = [0] * n
        if n > 0:
            prefix[0] = sorted_nums[0]
            for i in range(1, n):
                prefix[i] = prefix[i-1] + sorted_nums[i]
        
        res = []
        for x in nums:
            pos = bisect.bisect_right(sorted_nums, x)
            left_sum = x * pos - (prefix[pos-1] if pos > 0 else 0)
            right_sum = (prefix[n-1] - (prefix[pos-1] if pos > 0 else 0)) - x * (n - pos)
            res.append(left_sum + right_sum)
        
        return res