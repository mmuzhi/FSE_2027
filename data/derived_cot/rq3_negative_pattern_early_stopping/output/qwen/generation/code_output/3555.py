class Solution:
    def getFinalState(self, nums: List[int], k: int, multiplier: int) -> List[int]:
        for _ in range(k):
            current_min = min(nums)
            idx = nums.index(current_min)
            nums[idx] = current_min * multiplier
        return nums