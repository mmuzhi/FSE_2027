class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        if len(nums) < 2:
            return len(nums)
        j = 1
        count = {}
        for i in range(len(nums)):
            count[nums[i]] = count.get(nums[i], 0) + 1
            if count[nums[i]] <= 2:
                j += 1
                nums[j] = nums[i]
        return j+1