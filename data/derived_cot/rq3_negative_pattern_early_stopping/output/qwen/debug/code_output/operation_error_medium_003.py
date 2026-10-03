class Solution:
    def longestString(self, x: int, y: int, z: int) -> int:
        if x > y:
            x, y = y, x
        base = min(x + y, 2 * x + 1)
        return (base * 2) - (2 * z)
