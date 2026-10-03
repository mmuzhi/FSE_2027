class Solution:
    def longestWPI(self, A):
        curr, ans, D = 0, 0, {0: -1}
        for e, i in enumerate([1 if x > 8 else -1 for x in A]):
            curr += i
            D[curr] = D.get(curr, e)
            ans = e + 1 if curr > 0 else max(ans, e - D.get(curr - 1, e))
        return ans