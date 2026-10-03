class Solution:
    def maxFrequency(self, nums: List[int], k: int) -> int:
        nums.sort()
        n = len(nums)
        left = 0
        max_count = 0
        total = 0