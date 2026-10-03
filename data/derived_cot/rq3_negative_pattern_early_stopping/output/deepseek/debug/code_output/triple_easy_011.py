class Solution:
    def findComplement(self, num: int) -> int:
        if num == 0:
            return 1
        com = ''
        while num > 0:
            if num % 2 == 1:
                com = '0' + com
            else:
                com = '1' + com
            num = num // 2
        return int(com, 2)