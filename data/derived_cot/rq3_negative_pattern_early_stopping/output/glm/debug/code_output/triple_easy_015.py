class Solution:
    def findMaxK(self, nums: List[int]) -> int:
        s = set(nums)
        max_k = -1
        for num in nums:
            if -num in s:
                max_k = max(max_k, abs(num))
        return max_k