from math import gcd
from functools import reduce
from typing import List

class Solution:
    def maxScore(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 1:
            return nums[0] * nums[0]
        
        def lcm(a, b):
            return a // gcd(a, b) * b
        
        def calc_score(arr):
            if not arr:
                return 0
            g = reduce(gcd, arr)
            l = reduce(lcm, arr)
            return g * l
        
        best = calc_score(nums)
        for i in range(n):
            new_arr = nums[:i] + nums[i+1:]
            score = calc_score(new_arr)
            if score > best:
                best = score
        return best