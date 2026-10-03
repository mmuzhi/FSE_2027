from collections import defaultdict

class Solution:
    def numPermsDISequence(self, s: str) -> int:
        mem = defaultdict(int)
        def dfs(i, val=0):
            if i == len(s):
                return 1
            if (i, val) in mem:
                return mem[i, val]
            p = 0
            if s[i] == "D":
                for ind in range(0, val):
                    p = (p + dfs(i + 1, ind)) % (10**9 + 7)
            else:
                for ind in range(val, len(s) - i):
                    p = (p + dfs(i + 1, ind)) % (10**9 + 7)
            mem[i, val] = p
            return p
        return sum(dfs(0, val) for val in range(len(s) + 1)) % (10**9 + 7)