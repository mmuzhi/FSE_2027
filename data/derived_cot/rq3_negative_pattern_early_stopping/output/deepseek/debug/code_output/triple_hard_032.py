class Solution:
    def findKthNumber(self, n: int, k: int) -> int:
        def fn(x):
            ans, diff = 0, 1
            while x <= n:
                ans += min(n - x + 1, diff)
                x *= 10
                diff *= 10
            return ans
        
        cur = 1
        while k > 1:
            cnt = fn(cur)
            if k > cnt:
                k -= cnt
                cur += 1
            else:
                k -= 1
                cur *= 10
        return cur