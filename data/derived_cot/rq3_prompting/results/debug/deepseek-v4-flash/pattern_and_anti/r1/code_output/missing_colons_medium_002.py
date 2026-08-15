class Solution:
    def addBinary(self, A, B):
        if not A and not B:
            return "0"
        i, j = len(A) - 1, len(B) - 1
        carry = 0
        res = []
        while i >= 0 or j >= 0 or carry:
            total = carry
            if i >= 0:
                total += int(A[i])
                i -= 1
            if j >= 0:
                total += int(B[j])
                j -= 1
            res.append(str(total & 1))
            carry = total >> 1
        while len(res) > 1 and res[-1] == '0':
            res.pop()
        return ''.join(reversed(res))

    def addNegabinary(self, A, B):
        if not A and not B:
            return [0]
        i, j = len(A) - 1, len(B) - 1
        carry = 0
        res = []
        while i >= 0 or j >= 0 or carry:
            total = carry
            if i >= 0:
                total += int(A[i])
                i -= 1
            if j >= 0:
                total += int(B[j])
                j -= 1
            res.append(total & 1)
            carry = -(total >> 1)
        while len(res) > 1 and res[-1] == 0:
            res.pop()
        return res[::-1]