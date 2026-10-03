class Solution:
    def smallestNumber(self, n: int) -> int:
        k = n.bit_length()
        candidate = (1 << k) - 1
        if candidate < n:
            candidate = (1 << (k + 1)) - 1
        return candidate