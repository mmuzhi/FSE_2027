class Solution:
    def restoreIpAddresses(self, s: str) -> List[str]:
        res = []
        cur = []
        
        def backtrack(i):
            if len(cur) > 4:
                return
            if i == len(s) and len(cur) == 4:
                res.append(".".join(cur))
                return
            if s[i] == '0':
                cur.append(s[i])
                backtrack(i+1)
                cur.pop()
                return
            j = 0
            while j < 3 and i+j+1 <= len(s):
                num = s[i:i+j+1]
                if int(num) < 256:
                    cur.append(num)
                    backtrack(i+j+1)
                    cur.pop()
                j += 1
        
        backtrack(0)
        return res
