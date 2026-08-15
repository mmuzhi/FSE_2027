class Solution:
    def addBinary(self, A, B):
        as_str = isinstance(A, str)
        A = list(map(int, A))
        B = list(map(int, B))

        res = []
        carry = 0
        while A or B or carry:
            carry += (A or [0]).pop() + (B or [0]).pop()
            res.append(carry & 1)
            carry = carry >> 1

        if not res:
            res = [0]
        while len(res) > 1 and res[-1] == 0:
            res.pop()

        if as_str:
            return ''.join(map(str, res[::-1]))
        return res[::-1]

    def addNegabinary(self, A, B):
        A = list(map(int, A))
        B = list(map(int, B))

        res = []
        carry = 0
        while A or B or carry:
            carry += (A or [0]).pop() + (B or [0]).pop()
            res.append(carry & 1)
            carry = -(carry >> 1)

        if not res:
            res = [0]
        while len(res) > 1 and res[-1] == 0:
            res.pop()
        return res[::-1]