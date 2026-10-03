import bisect

class Solution:
    def getSumAbsoluteDifferences(self, nums: List[int]) -> List[int]:
        n = len(nums)
        if n == 0:
            return []
        total = sum(nums)
        sorted_nums = sorted(nums)
        prefix_sorted = [0] * n
        prefix_sorted[0] = sorted_nums[0]
        for i in range(1, n):
            prefix_sorted[i] = prefix_sorted[i-1] + sorted_nums[i]
        
        res = []
        for num in nums:
            idx = bisect.bisect_right(sorted_nums, num)
            count = idx
            if count == 0:
                left_sum = 0
            else:
                left_sum = prefix_sorted[count-1]
            left_abs = num * count - left_sum
            right_abs = (total - left_sum) - num * (n - count)
            res.append(left_abs + right_abs)
        return res