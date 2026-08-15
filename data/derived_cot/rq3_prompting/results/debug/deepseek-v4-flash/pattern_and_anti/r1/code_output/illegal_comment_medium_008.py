class Solution:
    def addBinary(self, A, B):
        i, j = len(A) - 1, len(B) - 1
        carry = 0
        res = []
        while i >= 0 or j >= 0 or carry:
            if i >= 0:
                carry += A[i]
                i -= 1
            if j >= 0:
                carry += B[j]
                j -= 1
            res.append(carry & 1)
            carry >>= 1
        while len(res) > 1 and res[-1] == 0:
            res.pop()
        return res[::-1]

    def addNegabinary(self, A, B):
        i, j = len(A) - 1, len(B) - 1
        carry = 0
        res = []
        while i >= 0 or j >= 0 or carry:
            if i >= 0:
                carry += A[i]
                i -= 1
            if j >= 0:
                carry += B[j]
                j -= 1
            res.append(carry & 1)
            carry = -(carry >> 1)
        while len(res) > 1 and res[-1] == 0:
            res.pop()
        return res[::-1]