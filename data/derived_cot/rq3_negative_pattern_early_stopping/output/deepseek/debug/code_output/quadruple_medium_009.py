from typing import List

class Solution:
    def restoreIpAddresses(self, s: str) -> List[str]:
        res = []
        cur = []
        
        def backtrack(i: int):
            if len(cur) > 4:
                return
            if i == len(s):
                if len(cur) == 4:
                    res.append(".".join(cur))
                return
            if s[i] == '0':
                cur.append(s[i])
                backtrack(i + 1)
                cur.pop()
                return
            for j in range(3):
                if i + j + 1 > len(s):
                    break
                segment = s[i:i + j + 1]
                if int(segment) <= 255:
                    cur.append(segment)
                    backtrack(i + j + 1)
                    cur.pop()
                    
        backtrack(0)
        return res