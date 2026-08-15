from typing import List
import sys

class Solution:
    def componentValue(self, nums: List[int], edges: List[List[int]]) -> int:
        sys.setrecursionlimit(10**6)
        tree = [[] for _ in nums]
        for u, v in edges:
            tree[u].append(v)
            tree[v].append(u)

        total = sum(nums)

        def fn(u, p):
            ans = nums[u]
            for v in tree[u]:
                if v != p:
                    ans += fn(v, u)
            return 0 if ans == cand else ans

        divisors = []
        d = 1
        while d * d <= total:
            if total % d == 0:
                divisors.append(d)
                if d != total // d:
                    divisors.append(total // d)
            d += 1
        divisors.sort()

        for cand in divisors:
            if cand == total:
                continue
            if fn(0, -1) == 0:
                return total // cand - 1
        return 0