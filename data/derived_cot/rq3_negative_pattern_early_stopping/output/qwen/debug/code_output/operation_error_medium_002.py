import functools
import collections
import itertools

class Solution:
    def countMaxOrSubsets(self, nums: List[int]) -> int:
        mapping = collections.defaultdict(int)
        n = len(nums)
        # We'll generate all non-empty subsets using bit masks
        # There are 2^n subsets, including the empty set. We skip the empty set.
        for bitmask in range(1, 1 << n):
            # Build the subset by checking each bit
            subset = []
            for i in range(n):
                if bitmask & (1 << i):
                    subset.append(nums[i])
            # Compute the OR of the subset
            or_val = functools.reduce(lambda a, b: a | b, subset)
            mapping[or_val] += 1
        # If there are no subsets, then mapping is empty. But the problem states non-empty subsets, so we assume at least one element.
        if not mapping:
            return 0
        max_or_val = max(mapping.keys())
        return mapping[max_or_val]