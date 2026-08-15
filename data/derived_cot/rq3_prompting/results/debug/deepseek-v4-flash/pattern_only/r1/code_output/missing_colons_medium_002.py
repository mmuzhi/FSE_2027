class Solution:
    def addBinary(self, A, B):
        A = list(map(int, A))
        B = list(map(int, B))
        res = []
        carry = 0
        while A or B or carry:
            carry += (A or [0]).pop() + (B or [0]).pop()
            res.append(str(carry & 1))
            carry >>= 1
        ans = ''.join(res[::-1]).lstrip('0')
        return ans if ans else '0'

    def addNegabinary(self, A, B):
        A = list(map(int, A))
        B = list(map(int, B))
        res = []
        carry = 0
        while A or B or carry:
            carry += (A or [0]).pop() + (B or [0]).pop()
            res.append(carry & 1)
            carry = -(carry >> 1)
        while len(res) > 1 and res[-1] == 0:
            res.pop()
        if not res:
            return [0]
        return res[::-1]