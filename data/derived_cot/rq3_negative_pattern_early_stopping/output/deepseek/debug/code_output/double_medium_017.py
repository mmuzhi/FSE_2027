from typing import List
import collections
import itertools
import functools

class Solution:
    def countMaxOrSubsets(self, nums: List[int]) -> int:
        mapping = collections.defaultdict(int)
        for count in range(1, len(nums) + 1):
            subsets = itertools.combinations(nums, count)
            for ele in subsets:
                or_val = functools.reduce(lambda a, b: a | b, ele, 0)
                mapping[or_val] += 1
        return mapping[max(mapping.keys())]