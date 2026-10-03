from typing import List
from functools import reduce

class Solution:
    def numberOfGoodSubarraySplits(self, nums: List[int]) -> int:
        if 1 not in nums:
            return 0
        parts = ''.join(map(str, nums)).strip('0').split('1')
        ways = [len(part) + 1 for part in parts]
        return reduce(lambda x, y: (x * y) % 1000000007, ways)