class Solution:
    def findKthNumber(self, n: int, k: int) -> int:
        def fn(x):
            d = len(str(x))
            base = 10**(d-1)
            block_end = x + base - 1
            return min(block_end, n) - x + 1
        
        x = 1
        while k > 1:
            cnt = fn(x)
            if k > cnt:
                k -= cnt
                x += 1
            else:
                k -= 1
                x *= 10
        return x
