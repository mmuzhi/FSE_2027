class Solution:
    def minFlips(self, a: int, b: int, c: int) -> int:
        if (a | b) == c: return 0
        c = ('0' * 32 + bin(c)[2:])[-32:]
        a = ('0' * 32 + bin(a)[2:])[-32:]
        b = ('0' * 32 + bin(b)[2:])[-32:]
        
        cnt = 0
        for i in range(len(c)):
            if c[i] == '0':
                cnt += int(a[i]) + int(b[i])
            else:
                if a[i] == '0' and b[i] == '0':
                    cnt += 1
        return cnt