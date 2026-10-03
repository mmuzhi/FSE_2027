class Solution:
    def addBinary(self, A, B):
        if isinstance(A, str):
            A = list(map(int, A))[::-1]
        if isinstance(B, str):
            B = list(map(int, B))[:: -1]
        n = max(len(A), len(B))
        A = A + [0] * (n - len(A))
        B = B + [0] * (n - len(B))
        carry = 0
        res = []
        for i in range(n):
            bitA = A[i]
            bitB = B[i]
            total = bitA + bitB + carry
            carry = total // 2
            res.append(total % 2)
        while carry:
            res.append(carry % 2)
            carry //= 2
        # Convert to big-endian
        res.reverse()
        # Remove leading zeros
        i = 0
        while i < len(res) and res[i] == 0:
            i += 1
        if i == len(res):
            return "0"
        return ''.join(str(x) for x in res[:i])
    
    def addNegabinary(self, A, B):
        if isinstance(A, str):
            A = list(map(int, A))[::-1]
        if isinstance(B, str):
            B = list(map(int, B))[::-1]
        n = max(len(A), len(B))
        A = A + [0] * (n - len(A))
        B = B + [0] * (n - len(B))
        carry = 0
        res = []
        for i in range(n):
            bitA = A[i]
            bitB = B[i]
            total = bitA + bitB + carry
            carry = total // -2
            digit = total % -2
            if digit < 0:
                digit += 2
                carry += 1
            res.append(digit)
        while carry:
            digit = carry % -2
            carry //= -2
            if digit < 0:
                digit += 2
                carry += 1
            res.append(digit)
        # Convert to big-endian
        res.reverse()
        # Remove leading zeros
        i = 0
        while i < len(res) and res[i] == 0:
            i += 1
        if i == len(res):
            return "0"
        return ''.join(str(x) for x in res[:i])