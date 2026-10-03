class Solution:
    def f(self, n, r, count):
        if count == 32:
            return r
        return self.f(n << 1, (r << 1) | (n & 1), count + 1)
    
    def reverseBits(self, n: int) -> int:
        # Mask n to 32 bits to ensure we only process the least significant 32 bits
        n = n & 0xFFFFFFFF
        return self.f(n, 0, 0)