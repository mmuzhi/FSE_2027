from typing import List
from functools import reduce
from operator import mul

class Solution:
    def numberOfGoodSubarraySplits(self, nums: List[int]) -> int:
        if 1 not in nums:
            return 0

        parts = ''.join(map(str, nums)).strip('0').split('1')
        return reduce(mul, (len(part) + 1 for part in parts), 1) % 1000000007