class Solution:
    def minFlips(self, a: int, b: int, c: int) -> int:
        if a | b == c:
            return 0
        
        # We'll consider up to the maximum bit length of a, b, c
        n = max(a.bit_length(), b.bit_length(), c.bit_length(), 1)
        cnt = 0
        for i in range(n):
            bit_a = (a >> i) & 1
            bit_b = (b >> i) & 1
            bit_c = (c >> i) & 1
            
            if bit_c == 1:
                if bit_a == 0 and bit_b == 0:
                    cnt += 1
            else:  # bit_c == 0
                if bit_a == 1 or bit_b == 1:
                    cnt += (1 if bit_a else 0) + (1 if bit_b else 0)
                    
        return cnt