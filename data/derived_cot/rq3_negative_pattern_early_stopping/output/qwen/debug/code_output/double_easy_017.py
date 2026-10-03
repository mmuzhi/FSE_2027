class Solution:
    def smallerNumbersThanCurrent(self, nums: List[int]) -> List[int]:
        sorted_nums = sorted(nums)
        prefix = [0] * len(sorted_nums)
        if len(sorted_nums) > 0:
            prefix[0] = 0
            for i in range(1, len(sorted_nums)):
                prefix[i] = prefix[i-1] + (1 if sorted_nums[i] == sorted_nums[i-1] else 0)
            prefix[-1] = len(sorted_nums)
        result = []
        for num in nums:
            index = 0
            left, right = 0, len(sorted_nums) - 1
            while left <= right:
                mid = (left + right) // 2
                if sorted_nums[mid] < num:
                    index = mid + 1
                    left = mid + 1
                elif sorted_nums[mid] > num:
                    right = mid - 1
                else:
                    left = mid + 1
            count_less = index
            result.append(count_less)
        return result