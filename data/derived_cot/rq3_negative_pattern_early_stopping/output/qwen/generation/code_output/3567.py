class Solution:
    def convertDateToBinary(self, date: str) -> str:
        parts = date.split('-')
        y = int(parts[0])
        m = int(parts[1])
        d = int(parts[2])
        return bin(y)[2:] + '-' + bin(m)[2:] + '-' + bin(d)[2:]