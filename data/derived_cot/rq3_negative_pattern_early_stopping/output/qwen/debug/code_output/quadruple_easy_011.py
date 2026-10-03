class Solution:
    def findMaxK(self, nums: List[int]) -> int:
        s = set(nums)
        candidate = None
        for num in nums:
            if num in s and -num in s:
                if candidate is None or num > candidate:
                    candidate = num
        return candidate if candidate is not None else -1