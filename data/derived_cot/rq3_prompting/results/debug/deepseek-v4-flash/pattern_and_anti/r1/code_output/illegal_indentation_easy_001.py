class Solution:
    def minBitFlips(self, start: int, goal: int) -> int:
        s = bin(start)[2:]
        g = bin(goal)[2:]
        max_len = max(len(s), len(g))
        s = s.zfill(max_len)
        g = g.zfill(max_len)

        count = 0
        for i in range(max_len):
            if s[i] != g[i]:
                count += 1
        return count