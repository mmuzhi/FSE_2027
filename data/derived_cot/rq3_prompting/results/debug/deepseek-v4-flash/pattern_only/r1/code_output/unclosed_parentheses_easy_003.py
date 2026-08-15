from typing import List

class Solution:
    def smallerNumbersThanCurrent(self, nums: List[int]) -> List[int]:
        count = [0] * 101
        for num in nums:
            count[num] += 1

        for i in range(1, 101):
            count[i] += count[i - 1]

        res = []
        for num in nums:
            if num == 0:
                res.append(0)
            else:
                res.append(count[num - 1])
        return res