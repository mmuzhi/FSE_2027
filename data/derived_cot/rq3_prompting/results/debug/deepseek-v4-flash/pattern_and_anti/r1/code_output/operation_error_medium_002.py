import functools
import itertools
import collections
from typing import List

class Solution:
    def countMaxOrSubsets(self, nums: List[int]) -> int:
        mapping = collections.defaultdict(int)
        for count in range(1, len(nums) + 1):
            for ele in itertools.combinations(nums, count):
                mapping[functools.reduce(lambda a, b: a | b, ele)] += 1
        return mapping[max(mapping.keys())]