class Solution:
    def palindromePartition(self, s: str, k: int) -> int:
        def Cost(sub):
            i, j, c = 0, len(sub)-1, 0
            while i < j:
                if sub[i] != sub[j]:
                    c += 1
                i += 1
                j -= 1
            return c

        dp = {}

        def A(s, k):
            if (s, k) in dp:
                return dp[(s, k)]
            if k == 1:
                return Cost(s)

            f = float('inf')
            for x in range(1, len(s)):
                if len(s[:x]) and len(s[x:]):
                    f = min(f, Cost(s[:x]) + A(s[x:], k-1))

            dp[(s, k)] = f
            return dp[(s, k)]

        return A(s, k)