class Solution:
    def findComplement(self, num: int) -> int:
        if num == 0:
            return 0
        com = ''
        n = num
        while n > 0:
            if n % 2 == 1:
                com += '0'
            else:
                com += '1'
            n = n // 2
        com = com[::-1]
        return int(com, 2)