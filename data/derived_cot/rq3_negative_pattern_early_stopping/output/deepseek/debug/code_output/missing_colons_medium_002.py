class Solution:
    def addBinary(self, A, B):
        res = []
        carry = 0
        i, j = len(A) - 1, len(B) - 1
        while i >= 0 or j >= 0 or carry:
            a = A[i] if i >= 0 else 0
            b = B[j] if j >= 0 else 0
            carry += a + b
            res.append(carry & 1)
            carry >>= 1
            i -= 1
            j -= 1
        return res[::-1]

    def addNegabinary(self, A, B):
        res = []
        carry = 0
        i, j = len(A) - 1, len(B) - 1
        while i >= 0 or j >= 0 or carry:
            a = A[i] if i >= 0 else 0
            b = B[j] if j >= 0 else 0
            carry += a + b
            res.append(carry & 1)
            carry = -(carry >> 1)
            i -= 1
            j -= 1
        while len(res) > 1 and res[-1] == 0:
            res.pop()
        return res[::-1]