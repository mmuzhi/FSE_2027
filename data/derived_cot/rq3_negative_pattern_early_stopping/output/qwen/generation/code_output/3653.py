class Solution:
    def maxSubarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)
        prefix = [0]*(n+1)
        for i in range(n):
            prefix[i+1] = prefix[i] + nums[i]
        max_sum = -10**18
        for i in range(k, n+1):
            if (i % k == 0):
                current_sum = prefix[i] - prefix[i-k]
                if current_sum > max_sum:
                    max_sum = current_sum
        return max_sum