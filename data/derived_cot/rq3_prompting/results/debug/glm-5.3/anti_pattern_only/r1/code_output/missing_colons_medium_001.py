class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        ans = min(2, len(nums))
        for i in range(2, len(nums)):
            if nums[i] != nums[ans - 2]:
                nums[ans] = nums[i]
                ans += 1
        return ans