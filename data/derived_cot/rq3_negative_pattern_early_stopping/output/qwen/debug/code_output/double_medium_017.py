import functools
import collections
import itertools

class Solution:
    def countMaxOrSubsets(self, nums: List[int]) -> int:
        mapping = collections.defaultdict(int)
        for count in range(1, len(nums)+1):
            subsets = list(itertools.combinations(nums, count))
            for ele in subsets:
                # Use OR instead of XOR
                or_value = functools.reduce(lambda a, b: a | b, ele, 0)
                mapping[or_value] += 1
        # If there are no subsets, then return 0. But the problem says non-empty subsets, so there should be at least one.
        if not mapping:
            return 0
        return mapping[max(mapping.keys())]