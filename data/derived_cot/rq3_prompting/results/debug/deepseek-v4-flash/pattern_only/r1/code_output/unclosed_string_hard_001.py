class Solution:
    def palindromePartition(self, s: str, k: int) -> int:
        def cost(t):
            i, j = 0, len(t) - 1
            c = 0
            while i < j:
                if t[i] != t[j]:
                    c += 1
                i += 1
                j -= 1
            return c

        dp = {}

        def dfs(t, parts):
            if (t, parts) in dp:
                return dp[(t, parts)]

            if parts == 1:
                dp[(t, parts)] = cost(t)
                return dp[(t, parts)]

            if parts > len(t):
                dp[(t, parts)] = float('inf')
                return dp[(t, parts)]

            best = float('inf')

            for x in range(1, len(t)):
                best = min(best, cost(t[:x]) + dfs(t[x:], parts - 1))

            dp[(t, parts)] = best
            return best

        return dfs(s, k)