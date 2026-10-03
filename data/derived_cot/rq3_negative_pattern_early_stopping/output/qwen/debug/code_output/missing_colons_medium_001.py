class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        n = len(nums)
        if n <= 2:
            return n
        ans = 2
        for i in range(2, n):
            if nums[i] != nums[ans-2]:
                nums[ans] = nums[i]
                ans += 1
        return ans