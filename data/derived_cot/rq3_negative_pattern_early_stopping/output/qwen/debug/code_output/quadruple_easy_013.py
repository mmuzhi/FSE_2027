class Solution:
    def findComplement(self, num: int) -> int:
        if num == 0:
            return 1
        bin_str = bin(num)[2:]
        flipped_str = ''.join('1' if bit == '0' else '0' for bit in bin_str)
        return int(flipped_str, 2)