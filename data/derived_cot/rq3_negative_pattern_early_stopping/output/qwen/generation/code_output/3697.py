import math
from functools import reduce
from math import gcd
from typing import List

class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        # Precompute the LCM for all subsets of target
        n = len(target)
        # There are 2^n subsets, but we need to consider each subset's LCM
        # But note: the LCM of a subset is the LCM of all elements in that subset.
        # We'll generate all subsets (as bit masks) and compute the LCM for each subset.
        subsets = []
        # We'll store for each subset (represented by bitmask) the LCM and the minimal multiple (the next multiple above a given x) but we don't know x yet.
        # Actually, for each subset, we need the LCM. Then, for each x, we can compute the minimal operations to cover that subset by setting x to the next multiple of the LCM (if the subset is non-empty). For the empty subset, LCM is 0? But we don't need to cover empty subset. We need to cover the full set? Actually, we need to cover each target individually, but we can combine them.

        # But note: the condition is that for each target, there is at least one element in nums that is a multiple of that target. This is equivalent to: for each target t, there is an element x in nums such that x is divisible by t. 

        # However, if we set an element x to be a multiple of the LCM of a subset S, then x will be divisible by every t in S. So we can cover S by x.

        # Now, the problem is: we need to cover the entire set of targets (which is the union of all subsets) by a collection of elements (each element can cover a subset). The total operations is the sum of the operations for each element (each element is used for one subset). But note: we can use the same element for multiple subsets? Actually, no: each element is one number. But we can assign multiple subsets to the same element? Actually, no: each element can be set to one final value. That final value must be a multiple of the LCM of the union of all subsets assigned to it. But then, the minimal operations for an element to cover a set S is the minimal increments needed to make it a multiple of the LCM(S). 

        # But the problem is: we need to cover all targets (each target must be covered by at least one element). We can assign multiple targets to the same element (then that element must be a multiple of the LCM of those targets). 

        # This is a set cover problem: universe is the set of targets (size 4). Each element x in nums can cover a subset S (the set of targets t for which x (after operations) is a multiple of t). But note: the subset S that x can cover is not fixed: we can choose to set x to a multiple of any subset's LCM (by increasing x). But the minimal operation for x to cover a subset S is determined by the LCM of S.

        # However, the set cover problem is NP-hard, but with 4 elements, we can use dynamic programming or iterate over all 16 subsets and then use a greedy approach? But note: we have 50,000 elements. We can precompute for each element x and for each subset S (of targets) the minimal operations needed to set x to a multiple of the LCM(S). Then, we need to cover the full set (all targets) by selecting a collection of elements (each element can be used only once) and the total operations is the sum of the operations for each element. But wait, we can use the same element multiple times? No, because each element is one number. Actually, we can use each element only once (each element is one number, and we can only set it to one final value). But we can use multiple elements. 

        # Actually, the problem does not require that we use each element only once. We can use each element independently. But we are allowed to use the same element to cover multiple targets (by setting it to a multiple of the LCM of the targets we want to cover). 

        # So the problem is: we have 50,000 elements, each can be set to a value (by increments) and we want to cover all targets (each target must be divided by at least one element). We can set each element to any value (by incrementing). The cost is the total increments. We want the minimal total increments.

        # We can think of it as: for each target, we need to "hit" it. We can hit a target t by increasing an element x to the next multiple of t (if