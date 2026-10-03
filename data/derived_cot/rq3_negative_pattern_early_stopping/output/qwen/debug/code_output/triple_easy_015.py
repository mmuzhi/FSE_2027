class Solution:
    def findMaxK(self, nums: List[int]) -> int:
        s = set(nums)
        max_val = -10**9  # Start with a very small number
        for num in s:
            if num > 0 and -num in s:
                if num > max_val:
                    max_val = num
        return max_val