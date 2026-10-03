class Solution:
    def addBinary(self, A, B):
        carry = 0
        res = []
        while A or B or carry:
            a = A.pop(0) if A else 0
            b = B.pop(0) if B else 0
            total = a + b + carry
            carry = total // 2
            res.append(total % 2)
        return res[::-1]

    def addNegabinary(self, A, B):
        res = []
        carry = 0
        while A or B or carry:
            a = A.pop(0) if A else 0
            b = B.pop(0) if B else 0
            carry += a + b
            res.append(carry & 1)
            carry = -(carry >> 1)
        while len(res) > 1 and res[-1] == 0:
            res.pop()
        return res[::-1]