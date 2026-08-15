class Solution:
    def minFlips(self, a: int, b: int, c: int) -> int:
        flips = 0
        for i in range(max(a, b, c).bit_length()):
            abit = (a >> i) & 1
            bbit = (b >> i) & 1
            cbit = (c >> i) & 1

            if cbit == 0:
                flips += abit + bbit
            elif abit == 0 and bbit == 0:
                flips += 1

        return flips