from collections import defaultdict


class Solution:
    def numPermsDISequence(self, s: str) -> int:
        mem = defaultdict(int)
        mod = 10 ** 9 + 7

        def dfs(i, val):
            # val = rank (0-indexed from smallest) of the value placed at
            # position i among the remaining values {0..len(s)-i}
            if i == len(s):
                return 1
            if (i, val) in mem:
                return mem[i, val]
            p = 0
            if s[i] == "D":
                # next value must be smaller -> new relative ranks 0..val-1
                for ind in range(0, val):
                    p = (p + dfs(i + 1, ind)) % mod
            else:
                # next value must be larger -> ranks shift down by 1 -> val..len(s)-i-1
                for ind in range(val, len(s) - i):
                    p = (p + dfs(i + 1, ind)) % mod
            mem[i, val] = p
            return p

        # sum over all possible ranks for the first position
        return sum(dfs(0, v) for v in range(len(s) + 1)) % mod