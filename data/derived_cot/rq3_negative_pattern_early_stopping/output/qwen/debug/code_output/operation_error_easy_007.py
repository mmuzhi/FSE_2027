class Solution:
    def findComplement(self, num: int) -> int:
        com = ''
        while num > 0:
            if num % 2 == 1:
                com = '1' + com
            else:
                com = '0' + com
            num = num // 2
        if com == '':
            return 1
        else:
            flipped = ''.join('1' if bit=='0' else '0' for bit in com)
            return int(flipped, 2)