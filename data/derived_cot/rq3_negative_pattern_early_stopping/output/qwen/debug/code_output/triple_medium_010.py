class Solution:
    def minFlips(self, a: int, b: int, c: int) -> int:
        # Convert to 32-bit binary strings
        a_str = ('0' * 32 + bin(a)[2:])[-32:]
        b_str = ('0' * 32 + bin(b)[2:])[-32:]
        c_str = ('0' * 32 + bin(c)[2:])[-32:]
        
        cnt = 0
        for i in range(32):
            a_bit = a_str[i]
            b_bit = b_str[i]
            c_bit = c_str[i]
            if c_bit == '1':
                if a_bit == '1' or b_bit == '1':
                    continue
                else:
                    cnt += 1
            else:
                # For '0', we need both to be 0, so we flip every 1
                if a_bit == '1':
                    cnt += 1
                if b_bit == '1':
                    cnt += 1
        return cnt