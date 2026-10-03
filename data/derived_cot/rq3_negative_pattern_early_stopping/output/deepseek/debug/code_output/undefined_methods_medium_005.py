class Solution:
    def longestWPI(self, A):
        curr, ans, D = 0, 0, {}
        for i, hour in enumerate(A):
            curr += 1 if hour > 8 else -1
            if curr > 0:
                ans = i + 1
            else:
                if curr - 1 in D:
                    ans = max(ans, i - D[curr - 1])
            if curr not in D:
                D[curr] = i
        return ans