class Solution:
    def longestWPI(self, A):
        curr, ans, D = 0, 0, {}
        for e, i in enumerate(self.transform(A)):
            curr += i
            D[curr] = D.get(curr, e)
            ans = e + 1 if curr > 0 else max(ans, e - D.get(curr - 1, e))
        return ans

    def transform(self, A):
        return [1 if h > 8 else -1 for h in A]