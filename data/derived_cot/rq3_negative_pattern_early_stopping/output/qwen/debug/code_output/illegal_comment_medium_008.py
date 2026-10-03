class Solution:
    def addBinary(self, A, B):
        res = []
        carry = 0
        # We'll process from least significant bit to most
        # Convert A and B to lists of bits in reverse order (least significant first)
        A = A[::-1]
        B = B[::-1]
        while A or B or carry:
            a = A.pop() if A else 0
            b = B.pop() if B else 0
            total = a + b + carry
            carry = total // 2
            res.append(total % 2)
        # Convert the result to normal order (most significant first)
        return ''.join(str(x) for x in res[::-1])
    
    def addNegabinary(self, A, B):
        res = []
        carry = 0
        # We'll process from least significant bit to most
        # Convert A and B to lists of bits in reverse order (least significant first)
        A = A[::-1]
        B = B[::-1]
        while A or B or carry:
            a = A.pop() if A else 0
            b = B.pop() if B else 0
            total = a + b + carry
            carry = 0
            if total % 2 == 0:
                carry = total // 2
                res.append(0)
            else:
                carry = (total + 1) // -2
                res.append(1)
        # Convert the result to normal order (most significant first)
        # Remove any trailing zeros
        while len(res) > 1 and res[-1] == 0:
            res.pop()
        return ''.join(str(x) for x in res[::-1])
