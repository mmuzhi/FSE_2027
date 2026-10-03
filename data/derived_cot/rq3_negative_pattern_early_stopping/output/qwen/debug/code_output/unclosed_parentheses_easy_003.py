class Solution:
    def smallerNumbersThanCurrent(self, nums: List[int]) -> List[int]:
        # Shift the numbers by 100 to handle negative numbers
        shifted_nums = [x + 100 for x in nums]
        max_index = 200  # because 100+100=200
        count = [0] * (max_index+1)  # indices 0 to 200
        for num in shifted_nums:
            if num <= max_index:  # num is at most 200, so this is safe
                count[num] += 1
        res = []
        for num in shifted_nums:
            # Sum the frequencies of numbers with indices from 0 to num-1
            res.append(sum(count[:num]))
        return res