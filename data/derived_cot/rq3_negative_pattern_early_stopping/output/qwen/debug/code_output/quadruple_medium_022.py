class Solution:
    def smallestString(self, s: str) -> str:
        ct1 = 0
        for i in s:
            if i == 'a':
                ct1 += 1
            else:
                break
        
        ans = 'a' * ct1
        s_rest = s[ct1:]
        if not s_rest:
            return ans
        
        change = False
        contiguous = True
        new_s = []
        for cha in s_rest:
            if contiguous:
                if cha == 'a':
                    new_s.append('a')
                    contiguous = False
                else:
                    new_char = chr(ord(cha) - 1)
                    new_s.append(new_char)
                    change = True
            else:
                new_s.append(cha)
        
        return ans + ''.join(new_s)